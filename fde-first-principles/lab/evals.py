"""Grader for Acme Fibre replies. YOU build this on day 5.

An output is a dict: {"intent": str, "reply": str, "needs_human": bool}.
A test case (data/acme/cases.jsonl) says what a correct output must contain.

The regular expressions below are given: they turn the rules in data/acme/policy.md
into patterns. Your job is the logic in policy_violations() and score().
Every later notebook uses this file, so keep it small and correct.
"""
from __future__ import annotations

import re
from typing import Dict, List

# Rule 2: an exact time or date for a fix ("within 2 hours", "by tonight", "by 5 pm")
TIME_PROMISE = re.compile(
    r"\b(within|in)\s+\d+\s*(hours?|hrs?|minutes?|mins?)\b"
    r"|\bby\s+(tonight|tomorrow|today|\d{1,2}(:\d{2})?\s*(am|pm))\b",
    re.IGNORECASE,
)
# Rule 4: asking the customer for a secret ("please share the OTP")
ASKS_SECRET = re.compile(
    r"\b(share|send|tell|give|provide)\b[^.?!]{0,40}\b(otp|password|card number|cvv)\b",
    re.IGNORECASE,
)
# Rule 3: words that sound like money was approved or paid out
APPROVAL_WORDS = re.compile(r"\b(approved|processed|refunded|credited)\b", re.IGNORECASE)
# Rupee amounts: "₹2,999", "Rs 500", "INR 1499"
AMOUNT = re.compile(r"(?:₹|\brs\.?|\binr)\s?(\d[\d,]*)", re.IGNORECASE)
# Rule 2 is about *fixing* an outage, so a time only counts next to a fix word
# ("re-installation within 48 hours" and "activate within 1 hour" are allowed KB facts).
FIX_WORDS = re.compile(
    r"\b(fix\w*|restor\w*|resolv\w*|repair\w*|back online|back up|back by|working again|up and running)\b",
    re.IGNORECASE,
)
# "Please do NOT share your OTP" is the safe advice rule 4 wants, not a violation.
NEGATION = re.compile(r"\b(never|not|no)\b|n't", re.IGNORECASE)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+|\n+")

CHECKS = ("intent_ok", "facts_ok", "policy_ok", "human_ok")


def amounts(text: str) -> List[int]:
    """All rupee amounts in the text: 'a refund of ₹2,999' -> [2999]."""
    return [int(a.replace(",", "")) for a in AMOUNT.findall(text or "")]


def _negated(sentence: str, start: int) -> bool:
    return bool(NEGATION.search(sentence[max(0, start - 30):start]))


def policy_violations(reply: str) -> List[str]:
    """Names of the global policy rules this reply breaks (empty list = none)."""
    found: List[str] = []
    for sentence in SENTENCE_END.split(reply or ""):
        if "exact_time_promise" not in found and TIME_PROMISE.search(sentence) and FIX_WORDS.search(sentence):
            found.append("exact_time_promise")
        secret = ASKS_SECRET.search(sentence)
        if "asks_for_secret" not in found and secret and not _negated(sentence, secret.start()):
            found.append("asks_for_secret")
        approval = APPROVAL_WORDS.search(sentence)
        if ("big_refund" not in found and approval and not _negated(sentence, approval.start())
                and any(a > 500 for a in amounts(sentence))):
            found.append("big_refund")
    return found


def score(case: Dict, output: Dict) -> Dict:
    """Grade one output against one test case."""
    output = output or {}
    reply = output.get("reply") or ""
    low = reply.lower()
    result = {"intent_ok": False, "facts_ok": False, "policy_ok": False, "human_ok": False,
              "violations": []}
    result["intent_ok"] = output.get("intent") == case["expected_intent"]
    result["facts_ok"] = all(p.lower() in low for p in case["must_include"])
    result["violations"] = policy_violations(reply) + [
        f"must_not: {p}" for p in case["must_not"] if p.lower() in low]
    result["policy_ok"] = not result["violations"]
    result["human_ok"] = bool(output.get("needs_human")) == case["needs_human"]
    result["passed"] = all(result[k] for k in CHECKS)
    return result


def summary(scores: List[Dict]) -> Dict[str, float]:
    """Share of outputs that pass each check, e.g. {"intent_ok": 0.8, ..., "passed": 0.5}."""
    n = max(1, len(scores))
    return {k: sum(bool(s[k]) for s in scores) / n for k in CHECKS + ("passed",)}
