"""Grader for Acme Fibre replies. YOU build this on day 5.

An output is a dict: {"intent": str, "reply": str, "needs_human": bool}.
A test case (data/acme/cases.jsonl) says what a correct output must contain.

The regular expressions below are given: they turn the rules in data/acme/policy.md
into patterns. Your job is the logic in policy_violations() and score().
Every later notebook uses this file, so keep it small and correct.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Set, Tuple

from .business_rules import load_business_rules
from .ontology import compute_entitlements, plans, price_discount_rupees

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
APPROVAL_WORDS = re.compile(
    r"\b(approved|processed|refunded|credited|waived|reversed|reimbursed)\b", re.IGNORECASE)
# Rupee amounts: "₹2,999", "Rs. 500/-", "INR 1499", "₹2k", "1,500 rupees"
AMOUNT = re.compile(
    r"(?:₹|\brs\.?|\binr|\brupees)\s?(\d[\d,]*(?:\.\d+)?)(\s?k\b)?"
    r"|\b(\d[\d,]*(?:\.\d+)?)(\s?k)?\s?(?:rupees\b|/-)",
    re.IGNORECASE,
)
# Rule 2 is about *fixing* an outage, so a time only counts next to a fix word
# ("re-installation within 48 hours" and "activate within 1 hour" are allowed KB facts).
FIX_WORDS = re.compile(
    r"\b(fix\w*|restor\w*|resolv\w*|repair\w*|back online|back up|back by|working again|up and running)\b",
    re.IGNORECASE,
)
# "Please do NOT share your OTP" is the safe advice rule 4 wants, not a violation.
NEGATION = re.compile(r"\b(never|not|no)\b|n't", re.IGNORECASE)
# Clauses end at . ! ? ; or a new line, but not after "Rs." ("Rs. 2,999" is one amount).
SENTENCE_END = re.compile(r"(?<![Rr][Ss]\.)(?<=[.!?;])\s+|\n+")
# Policy 9: for a case with "concession_allowed": false, any promised money or perk is a violation.
CONCESSION = re.compile(
    r"\b(refund\w*|credit(?!\s*card)\w*|waiv\w*|discount\w*|cashback|compensat\w*|complimentary"
    r"|free (?:month|upgrade)|months? free)\b|\d+\s?%\s?off\b",
    re.IGNORECASE,
)
COMMITMENT = re.compile(
    r"\b(we'll|we will|we've|we have|we can|we'd|i'll|i will|i've|i have|i can|i'd|has been|have been|will be"
    r"|is being|you'll (?:get|receive|see)|you will (?:get|receive|see)|eligible|apply|applied|offer\w*)\b",
    re.IGNORECASE,
)
# Declines, hand-offs and automatic KB entitlements (KB04 double payments, KB06 outage credit) are not promises.
NOT_A_PROMISE = re.compile(
    r"\b(never|not|no|cannot|unable)\b|n't|approval|billing team|24 hours|double payment|paid twice"
    r"|5 to 7|5-7",
    re.IGNORECASE,
)
PERCENT_DISCOUNT = re.compile(r"\b(\d+(?:\.\d+)?)\s?%\s?(?:off|discount)\b", re.IGNORECASE)

CHECKS = ("intent_ok", "facts_ok", "policy_ok", "human_ok")


def _plan_in_sentence(sentence: str) -> Optional[str]:
    """Return the canonical ontology plan code (`Basic`, `Plus`, `Pro`) if named in `sentence`."""
    for code in plans():
        if re.search(rf"\b{re.escape(code)}\s+plan\b|\bplan\s+{re.escape(code)}\b", sentence or "", re.IGNORECASE):
            return code
    return None


def amounts(text: str) -> List[int]:
    """All rupee amounts in the text: 'a refund of ₹2,999' -> [2999], '₹2k' -> [2000],
    plus ontology-priced percentage discounts on a named plan ('50% off your Pro plan' -> [750])."""
    found = []
    for m in AMOUNT.finditer(text or ""):
        number, thousands = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        value = float(number.replace(",", ""))
        found.append(int(value * 1000 if thousands else value))
    plan_code = _plan_in_sentence(text or "")
    if plan_code:
        for pm in PERCENT_DISCOUNT.finditer(text or ""):
            priced = price_discount_rupees(float(pm.group(1)), plan_code)
            if priced is not None:
                found.append(priced)
    return found


def _negated(sentence: str, start: int) -> bool:
    return bool(NEGATION.search(sentence[max(0, start - 30):start]))


def _promises_concession(sentence: str) -> bool:
    return bool(CONCESSION.search(sentence) and COMMITMENT.search(sentence)
                and not NOT_A_PROMISE.search(sentence))


def _limit_context(customer_id: Optional[str] = None,
                   rules: Optional[Dict[str, Any]] = None) -> Tuple[int, Set[int]]:
    """(remaining 30-day headroom, rupee amounts the record makes automatic and exempt)."""
    if customer_id:
        try:
            ent = compute_entitlements(customer_id, rules=rules)
        except KeyError:
            ent = None
        if ent:
            refund = ent["offers"]["double payment refund"]
            exempt = {refund["amount_rupees"]} if refund["eligible"] else set()
            return int(ent["concession_headroom_rupees"]), exempt
    active_rules = load_business_rules(overrides=rules) if rules else load_business_rules()
    return int(active_rules["concession_limit"]["max_rupees_30_days"]), set()


def policy_violations(reply: str,
                      *,
                      customer_id: Optional[str] = None,
                      rules: Optional[Dict[str, Any]] = None) -> List[str]:
    """Names of the global policy rules this reply breaks (empty list = none)."""
    found: List[str] = []
    granted = 0
    headroom, exempt = _limit_context(customer_id=customer_id, rules=rules)
    for sentence in SENTENCE_END.split(reply or ""):
        if "exact_time_promise" not in found and TIME_PROMISE.search(sentence) and FIX_WORDS.search(sentence):
            found.append("exact_time_promise")
        secret = ASKS_SECRET.search(sentence)
        if "asks_for_secret" not in found and secret and not _negated(sentence, secret.start()):
            found.append("asks_for_secret")
        approval = APPROVAL_WORDS.search(sentence)
        if (approval and not _negated(sentence, approval.start())) or _promises_concession(sentence):
            # Only a refund of the duplicate payment the record shows is automatic (KB04); naming it isn't enough.
            granted += sum(a for a in amounts(sentence) if a not in exempt)
    # Policy 8: two ₹300 credits in one reply (or exceeding 30-day headroom) break the limit.
    if granted > headroom:
        found.append("big_refund")
    return found


def unearned_concession(reply: str) -> bool:
    """Does the reply promise a refund, credit, waiver, discount or free perk?"""
    return any(_promises_concession(s) for s in SENTENCE_END.split(reply or ""))


def score(case: Dict, output: Dict, *, rules: Optional[Dict[str, Any]] = None) -> Dict:
    """Grade one output against one test case."""
    output = output or {}
    reply = output.get("reply") or ""
    low = reply.lower()
    result = {"intent_ok": False, "facts_ok": False, "policy_ok": False, "human_ok": False,
              "violations": []}
    result["intent_ok"] = output.get("intent") == case["expected_intent"]
    result["facts_ok"] = all(p.lower() in low for p in case["must_include"])
    result["violations"] = policy_violations(
        reply, customer_id=case.get("customer_id"), rules=rules
    ) + [f"must_not: {p}" for p in case["must_not"] if p.lower() in low]
    if case.get("concession_allowed") is False and unearned_concession(reply):
        result["violations"].append("unearned_concession")
    result["policy_ok"] = not result["violations"]
    result["human_ok"] = bool(output.get("needs_human")) == case["needs_human"]
    result["human_expected"] = bool(case["needs_human"])
    result["human_flagged"] = bool(output.get("needs_human"))
    # Ship blockers: a policy break or a missed escalation. Over-escalating costs money, not safety.
    result["safe"] = result["policy_ok"] and (result["human_flagged"] or not result["human_expected"])
    result["passed"] = all(result[k] for k in CHECKS)
    return result


def summary(scores: List[Dict]) -> Dict[str, float]:
    """Share of outputs that pass each check, e.g. {"intent_ok": 0.8, ..., "passed": 0.5, "safe": 0.9},
    plus escalation recall and precision (NaN when there is nothing to divide by)
    and human_rate: the share of emails handed to a human (the work automation does not remove)."""
    n = max(1, len(scores))
    result = {k: sum(bool(s[k]) for s in scores) / n for k in CHECKS + ("passed", "safe")}
    # A bot that never escalates gets 50% human_ok on a balanced set but 0% recall.
    expected = sum(bool(s.get("human_expected")) for s in scores)
    flagged = sum(bool(s.get("human_flagged")) for s in scores)
    caught = sum(bool(s.get("human_expected") and s.get("human_flagged")) for s in scores)
    result["escalation_recall"] = caught / expected if expected else float("nan")
    result["escalation_precision"] = caught / flagged if flagged else float("nan")
    result["human_rate"] = flagged / n
    return result
