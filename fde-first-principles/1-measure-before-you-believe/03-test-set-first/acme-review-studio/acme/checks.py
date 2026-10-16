"""Deterministic checks.

* claim_checks  — step 6 of the workflow: is every claim in the draft backed by the data we fetched?
* guard_hits    — step 7 backstop: rules in code that escalate whatever the model said.
* eval_checks   — not part of the workflow: compares a run with the case's expected answer (for the SME).
"""
from __future__ import annotations

import re

MONEY = re.compile(r"(?:₹|\brs\.?\s?|\binr\s?)(\d[\d,]*)", re.I)
TICKET = re.compile(r"\bOUT-[A-Z]+-\d+\b")
HINGLISH = {"hai", "nahi", "kya", "karo", "karu", "aap", "mein", "bhai", "kar", "gaya", "raha", "chal", "hoon", "jayega"}
NEGATION = re.compile(r"(never|n't|\bnot\b|no one|nobody|cannot|unable|no exact|don't have)", re.I)

TIME_PROMISE = re.compile(
    r"\b(fix(?:ed)?|restor(?:ed|e)|resolv(?:ed|e)|back (?:up|online)|working again|up and running)\b"
    r"[^.!?\n]{0,40}?\b(by|before|within|in the next)\s+"
    r"(\d{1,2}(?::\d{2})?\s*(?:am|pm)?|noon|tonight|this (?:morning|afternoon|evening)|today|tomorrow"
    r"|an? (?:hour|few hours)|\d+\s*(?:hours?|hrs?|minutes?|mins?))", re.I)
SECRET_ASK = re.compile(
    r"\b(share|send|tell|give|provide|confirm|enter)\b\s+(?:us\s+|me\s+)?(?:your\s+|the\s+)?"
    r"(otp|one[- ]time password|password|pin|cvv|card (?:number|details))", re.I)
MONEY_WORDS = re.compile(r"refund|credit|compensat|waiv", re.I)
COMMITMENT = re.compile(
    r"\b(has been|have been|i have|i've|we have|we've|is being|will be|i'll|we'll)\s+"
    r"(approved|processed|credited|refunded|added|issued|waived|reversed)", re.I)
HEDGE = re.compile(r"approval|request|review|eligible|automatic|if |once approved|team will", re.I)


def amounts(text: str) -> set[int]:
    return {int(m.replace(",", "")) for m in MONEY.findall(text or "") if m.replace(",", "").isdigit()}


def _flag(check, severity, detail):
    return {"check": check, "severity": severity, "detail": detail}


def claim_checks(reply: str, *, customer: dict, outage: dict | None, others: list[dict],
                 sources_text: str, message: str, cited: list[str], known_ids: set[str],
                 max_words: int = 200) -> list[dict]:
    flags: list[dict] = []
    text = reply or ""

    first = customer["name"].split()[0]
    if first.lower() not in text.lower():
        flags.append(_flag("greeting", "low", f"Doesn't greet {first} by first name (P1)."))

    expected_ticket = outage["ticket"] if outage else None
    for ticket in sorted(set(TICKET.findall(text))):
        if ticket != expected_ticket:
            flags.append(_flag("unsupported ticket", "high",
                               f"{ticket} isn't the outage on record for {customer['area']}"
                               f" ({expected_ticket or 'none'})."))

    for m in TIME_PROMISE.finditer(text):
        if not NEGATION.search(text[max(0, m.start() - 45):m.start()]):
            flags.append(_flag("time promise", "high", f"Promises a fix time: “{m.group(0)}” (P2)."))

    known = amounts(sources_text) | amounts(message)
    for value in sorted(amounts(text) - known):
        flags.append(_flag("unsupported amount", "high", f"₹{value:,} isn't in the CRM, outage record, KB or email."))

    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if MONEY_WORDS.search(sentence) and COMMITMENT.search(sentence) and not HEDGE.search(sentence):
            big = [a for a in amounts(sentence) if a > 500]
            if big or "full refund" in sentence.lower():
                flags.append(_flag("financial promise", "high", f"Commits money above ₹500: “{sentence.strip()}” (P3)."))

    for m in SECRET_ASK.finditer(text):
        if not NEGATION.search(text[max(0, m.start() - 30):m.start()]):
            flags.append(_flag("asks for a secret", "high", f"“{m.group(0)}” (P4)."))

    for other in others:
        if other["id"] in text or other["name"].lower() in text.lower():
            flags.append(_flag("other customer's data", "high", f"Mentions {other['id']} / {other['name']} (P5)."))

    words = re.findall(r"[A-Za-z]+", text.lower())
    if re.search(r"[ऀ-ॿ]", text) or sum(w in HINGLISH for w in words) >= 2:
        flags.append(_flag("not simple English", "low", "Reply isn't in simple English (P7)."))
    if len(words) > max_words:
        flags.append(_flag("too long", "low", f"{len(words)} words (limit {max_words})."))

    unknown = [c for c in cited or [] if c not in known_ids]
    if unknown:
        flags.append(_flag("unknown citation", "low", f"Cites sources that don't exist: {', '.join(unknown)}."))
    return flags


def guard_hits(message: str, guards: list[dict]) -> list[str]:
    hits = []
    for g in guards:
        if not g.get("enabled") or not g.get("pattern"):
            continue
        try:
            found = re.search(g["pattern"], message or "", re.I)
        except re.error:
            continue
        if not found:
            continue
        if g.get("kind") == "money" and not [a for a in amounts(message) if a > int(g.get("threshold", 500))]:
            continue
        hits.append(g["name"])
    return hits


def eval_checks(case: dict, run: dict) -> dict:
    """Compare one run with the case's expected answer."""
    reply = (run.get("reply") or "").lower()
    model_nh = run.get("model_needs_human")
    routed = run.get("decision")
    return {
        "intent_ok": None if not run.get("model_intent") else run["model_intent"] == case["expected_intent"],
        "model_escalation_ok": None if model_nh is None else bool(model_nh) == case["needs_human"],
        "routing_ok": None if not routed else (routed == "escalate") == case["needs_human"],
        "missing": [t for t in case["must_include"] if t.lower() not in reply] if reply else [],
        "banned": [t for t in case["must_not"] if t.lower() in reply] if reply else [],
    }
