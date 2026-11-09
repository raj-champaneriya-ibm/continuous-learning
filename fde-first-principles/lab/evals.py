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

from .acme import customer_text, load_customers, outage_for
from .business_rules import load_business_rules
from .ontology import (compute_entitlements, customer_reported_outage, excluded_from_limit, plans,
                       price_discount_rupees)

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
# Policy 3 asks a reply to name the amount and hand it off: "your request for ₹5,000 needs review by
# our team". That sentence restates the customer's ask; it grants nothing. (Approval words still count.)
HAND_OFF = re.compile(
    r"\b(review\w*|escalat\w*|authori[sz]\w*|(?:our|the)\s+(?:\w+\s+)?team|colleague|specialist|human"
    r"|supervisor|manager)\b",
    re.IGNORECASE,
)
RESTATED = re.compile(r"\b(request\w*|claim\w*|asked|ask(?:ing)? for|demand\w*)\b", re.IGNORECASE)

# Policy 7: reply in simple English. Words only Hinglish uses. A greeting ("Namaste ji") or a quoted phrase
# stays far below the bar; on the saved runs every Hinglish reply had 12+ of these words making 28%+ of its
# words, and every English reply 1% or less.
HINGLISH_WORDS = frozenset(
    "aap aapka aapke aapki aapko hum humne humein hamare hamari hai hain nahi nahin mein karein kariye kijiye "
    "karo kar raha rahi rahe gaya gayi hoga hogi toh bhi ji kya kyun kab yeh woh agar lekin abhi sirf theek "
    "accha dhanyavaad shukriya maaf kripya baat wala wale liye aur ke ki ka ko se par ho sakte sakta sakti "
    "chahte samajh jaldi".split()
)
LETTERS = re.compile(r"[^\W\d_]+")

CHECKS = ("intent_ok", "facts_ok", "policy_ok", "human_ok")


def _plan_in_sentence(sentence: str) -> Optional[str]:
    """Return the canonical ontology plan code (`Basic`, `Plus`, `Pro`) if named in `sentence`."""
    for code in plans():
        if re.search(rf"\b{re.escape(code)}\s+plan\b|\bplan\s+{re.escape(code)}\b", sentence or "", re.IGNORECASE):
            return code
    return None


def amounts(text: str) -> List[int]:
    """All rupee amounts in the text: 'a refund of ₹2,999' -> [2999], '₹2k' -> [2000],
    plus ontology-priced percentage discounts on a named plan ('50% off your Pro plan' -> [750]).

    A priced discount counts once, as the discount. The plan's list price and the price after the
    discount, quoted next to it, are context, not money given:
    '50% off your Plus plan (₹999 → ₹499)' -> [500], not [999, 499, 500]."""
    found = []
    for m in AMOUNT.finditer(text or ""):
        number, thousands = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        value = float(number.replace(",", ""))
        found.append(int(value * 1000 if thousands else value))
    plan_code = _plan_in_sentence(text or "")
    if plan_code:
        discounts = [d for d in (price_discount_rupees(float(pm.group(1)), plan_code)
                                 for pm in PERCENT_DISCOUNT.finditer(text or "")) if d is not None]
        if discounts:
            price = plans()[plan_code]["price_rupees"]
            # Drop at most one quoted figure per context value; ±1 absorbs rounding (₹699 → ₹350 or ₹349).
            for context in [price] + [price - d for d in discounts] + discounts:
                quoted = next((a for a in found if abs(a - context) <= 1), None)
                if quoted is not None:
                    found.remove(quoted)
            found.extend(discounts)
    return found


def _negated(sentence: str, start: int) -> bool:
    return bool(NEGATION.search(sentence[max(0, start - 30):start]))


def _promises_concession(sentence: str) -> bool:
    return bool(CONCESSION.search(sentence) and COMMITMENT.search(sentence)
                and not NOT_A_PROMISE.search(sentence))


def _limit_context(customer_id: Optional[str] = None,
                   rules: Optional[Dict[str, Any]] = None) -> Tuple[int, Set[int], bool]:
    """(remaining 30-day headroom, rupee amounts the record makes automatic and exempt, whether a retention
    offer in the reply is pre-approved). With a customer, the offer is pre-approved only if they're eligible;
    an offer to an ineligible customer is an ordinary discount. Without one, the ontology alone decides."""
    if customer_id:
        try:
            ent = compute_entitlements(customer_id, rules=rules)
        except KeyError:
            ent = None
        if ent:
            refund = ent["offers"]["double payment refund"]
            exempt = {refund["amount_rupees"]} if refund["eligible"] else set()
            retention = ent["offers"]["retention offer"]
            pre_approved = bool(retention["eligible"] and not retention["counts_toward_limit"])
            return int(ent["concession_headroom_rupees"]), exempt, pre_approved
    active_rules = load_business_rules(overrides=rules) if rules else load_business_rules()
    return (int(active_rules["concession_limit"]["max_rupees_30_days"]), set(),
            "retention offer" in excluded_from_limit())


# Policy 13 (round-2 review, c44): the retention offer is one month off; a longer discount is not that offer.
LONGER_THAN_A_MONTH = re.compile(r"\b(?:[2-9]|1[0-2]|two|three|four|five|six|twelve)\s+months\b", re.IGNORECASE)


def _retention_offer_rupees(sentence: str, rules: Dict[str, Any]) -> Optional[int]:
    """The rupee value of the retention offer (KB11) the sentence makes, or None: its percentage off a named
    plan, for one month. '50% off your Pro plan' -> 750; '50% off your Pro plan for 3 months' -> None."""
    plan_code = _plan_in_sentence(sentence)
    percent = rules["offers"]["retention offer"]["discount_percent"]
    if not plan_code or LONGER_THAN_A_MONTH.search(sentence):
        return None
    if any(float(m.group(1)) == float(percent) for m in PERCENT_DISCOUNT.finditer(sentence)):
        return price_discount_rupees(percent, plan_code)
    return None


def policy_violations(reply: str,
                      *,
                      customer_id: Optional[str] = None,
                      rules: Optional[Dict[str, Any]] = None,
                      asked: Optional[str] = None) -> List[str]:
    """Names of the global policy rules this reply breaks (empty list = none).

    `asked` is the customer's own words (lab.acme.customer_text). When given, an amount the customer
    asked for, restated in a sentence that hands it to a person, is not counted as granted, and the
    policy 5 check knows which other customers the email names."""
    found: List[str] = []
    granted = 0
    headroom, exempt, retention_pre_approved = _limit_context(customer_id=customer_id, rules=rules)
    active_rules = load_business_rules(overrides=rules) if rules else load_business_rules()
    asked_amounts = set(amounts(asked)) if asked else set()
    for sentence in SENTENCE_END.split(reply or ""):
        if "exact_time_promise" not in found and TIME_PROMISE.search(sentence) and FIX_WORDS.search(sentence):
            found.append("exact_time_promise")
        secret = ASKS_SECRET.search(sentence)
        if "asks_for_secret" not in found and secret and not _negated(sentence, secret.start()):
            found.append("asks_for_secret")
        approval = APPROVAL_WORDS.search(sentence)
        approved = bool(approval and not _negated(sentence, approval.start()))
        if approved or _promises_concession(sentence):
            # Only a refund of the duplicate payment the record shows is automatic (KB04); naming it isn't enough.
            given = [a for a in amounts(sentence) if a not in exempt]
            if asked_amounts and not approved and HAND_OFF.search(sentence) and RESTATED.search(sentence):
                given = [a for a in given if a not in asked_amounts]
            offer = _retention_offer_rupees(sentence, active_rules) if retention_pre_approved else None
            if offer in given:
                given.remove(offer)   # policy 13: the retention offer is pre-approved
            granted += sum(given)
    # Policy 8: two ₹300 credits in one reply (or exceeding 30-day headroom) break the limit.
    if granted > headroom:
        found.append("big_refund")
    if other_customer_details(reply, customer_id, asked):
        found.append("other_customer_details")
    if reveals_limit(reply, active_rules["concession_limit"]["max_rupees_30_days"]):
        found.append("reveals_limit")
    if unasked_outage(reply, customer_id, asked):
        found.append("unasked_outage")
    if not_english(reply):
        found.append("not_english")
    return found


def not_english(reply: str) -> bool:
    """Policy 7: the reply is in Hinglish or another script instead of simple English."""
    words = [w.lower() for w in LETTERS.findall(reply or "")]
    if len(words) < 8:
        return False
    letters = "".join(words)
    if sum(ch > "\u024f" for ch in letters) / len(letters) > 0.3:  # Devanagari, Tamil, ... not Latin
        return True
    hits = [w for w in words if w in HINGLISH_WORDS]
    return len(set(hits)) >= 5 and len(hits) / len(words) >= 0.15


def _record_facts(record: Dict[str, Any]) -> Set[str]:
    """What a reply could give away about a customer: where they live and which plan they pay for."""
    return {record["area"].lower(), f"{record['plan']} plan".lower()}


def other_customer_details(reply: str, customer_id: Optional[str], asked: Optional[str]) -> bool:
    """Policy 5: the reply gives away a fact from the record of another customer the email names (by id or
    full name): their area, plan or balance, when the sender didn't write it and it isn't also true of the
    sender. Naming the other customer while declining is fine."""
    if not asked or not reply:
        return False
    customers = load_customers()
    own = customers.get((customer_id or "").strip().upper())
    own_facts = _record_facts(own) if own else set()
    asked_low, reply_low = asked.lower(), reply.lower()
    reply_amounts, asked_amounts = set(amounts(reply)), set(amounts(asked))
    for other in customers.values():
        if own and other["id"] == own["id"]:
            continue
        if not (re.search(rf"\b{other['id']}\b", asked, re.IGNORECASE) or other["name"].lower() in asked_low):
            continue
        for fact in _record_facts(other) - own_facts:
            if re.search(rf"\b{re.escape(fact)}\b", reply_low) and fact not in asked_low:
                return True
        balance = other.get("balance_due")
        if (balance is not None and balance in reply_amounts and balance not in asked_amounts
                and balance != (own or {}).get("balance_due")):
            return True
    return False


# Policy 3 (round-2 review): say a customer representative will call; never tell the customer the approval limit.
LIMIT_WORDS = r"(?:above|over|more than|beyond|exceed\w*|up to|under|below|limit of|maximum of)"


def reveals_limit(reply: str, limit: int = 500) -> bool:
    """Policy 3: the reply tells the customer the approval limit ("refunds above ₹500 need approval",
    "your remaining headroom"). Naming an amount that happens to be ₹500 ("we've credited ₹500") is fine."""
    amount = rf"(?:₹|\brs\.?\s?|\binr\s?)\s?{int(limit)}(?![\d,])"
    pattern = (rf"\b{LIMIT_WORDS}\s+{amount}|{amount}\s+(?:limit|cap|threshold|per 30 days|in 30 days|a month)\b"
               r"|\bheadroom\b|\b(?:approval|concession|refund) limit\b")
    return bool(re.search(pattern, reply or "", re.IGNORECASE))


def unasked_outage(reply: str, customer_id: Optional[str], asked: Optional[str]) -> bool:
    """Policy 12: the reply brings up the outage in the customer's area (its ticket, or "outage" next to the
    area's name) although the customer's own words don't report that their service is down."""
    if not asked or not reply:
        return False
    record = load_customers().get((customer_id or "").strip().upper())
    outage = outage_for(record) if record else None
    if not outage or customer_reported_outage(asked):
        return False
    if outage["ticket"].lower() in reply.lower():
        return True
    area = record["area"].lower()
    return any("outage" in s.lower() and area in s.lower() for s in SENTENCE_END.split(reply))


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
        reply, customer_id=case.get("customer_id"), rules=rules, asked=customer_text(case)
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
