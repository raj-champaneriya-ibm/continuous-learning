"""Escalation triggers as code: policy rules 6, 9 and 11 plus `escalation_policy` in business_rules.json.

Version C3's decision envelope runs these before the model sees the email. A trigger forces
needs_human. It never stops the model from escalating for a reason no rule can see here (possible
fraud, a safety hazard, staff misconduct, a question the help articles don't answer).

Precision matters more than recall: a false trigger sends a routine email to a person every time.
So every pattern is a phrase a customer uses for that reason only, and
tests/features/escalation_triggers.feature checks that no trigger fires on a case labelled
"no human needed" in any of the four case files. The patterns read English and Hinglish; an email
in Marathi or Tamil falls through to the model.

This module only uses the standard library: the caller passes the record, the rules and the
amounts, so the triggers can be tested without the ontology.
"""
from __future__ import annotations

import re
from typing import Any, Callable, Dict, Iterable, List

_APOS = "['’]"

# Policy 6: legal threats, including complaints to the regulator (TRAI) or a consumer court.
LEGAL_THREAT = re.compile(
    r"\b(consumer (?:court|forum)|court|legal (?:notice|action)|lawyer|sue|trai|ombudsman|police complaint)\b",
    re.IGNORECASE,
)
# Policy 6: a threat to leave ...
CHURN_THREAT = re.compile(
    r"\b(switch\w*|leav(?:e|ing)|cancel\w*|close (?:my|the) (?:connection|account)"
    r"|(?:another|other|doosr[aei]|dusr[aei]) provider)\b",
    re.IGNORECASE,
)
# ... after repeated complaints. The customer's own count is enough (policy 9: the record can lag).
REPEAT_COMPLAINT = re.compile(
    r"\b(third|3rd|fourth|4th|fifth|5th|teesr[ia]|chauth[ia]|paanchv[ia])\s+(?:\w+\s+){0,3}?"
    r"(times?|complaints?|baar|bar)\b",
    re.IGNORECASE,
)
# Policy 11: someone other than the account holder asks to change the account.
THIRD_PARTY_SENDER = re.compile(
    rf"\b(?:i{_APOS}?m|i am|this is)\s+\w+{_APOS}s\s+(?:husband|wife|son|daughter|father|mother|dad|mum|mom"
    r"|brother|sister|tenant|landlord|flatmate|roommate|friend|neighbou?r|colleague|assistant|secretary|relative)\b"
    r"|\bon (?:his|her|their) (?:account|behalf)\b|\bon behalf of\b",
    re.IGNORECASE,
)
ACCOUNT_CHANGE = re.compile(
    r"\b(cancel\w*|close (?:the|her|his|their) (?:connection|account)|shift\w*|relocat\w*"
    r"|move (?:the|her|his|their) connection|transfer\w*|upgrade\w*|downgrade\w*"
    r"|change (?:the |her |his |their )?plan)\b",
    re.IGNORECASE,
)
# A change of owner always involves someone other than the account holder.
OWNERSHIP_TRANSFER = re.compile(
    r"\btransfer (?:the |my |this |our )?(?:account|connection)\b|\b(?:in|into|to) (?:his|her|their) name\b",
    re.IGNORECASE,
)
# Policy 11: anyone asking to change the registered phone number or email.
CONTACT_CHANGE = re.compile(
    r"\b(?:change|update|replace|badal\w*)\b[^.?!\n]{0,30}\b(?:registered (?:phone|mobile|number|e-?mail)"
    r"|(?:phone|mobile) number|e-?mail(?: id| address)?|contact (?:number|details))\b"
    r"|\b(?:phone|mobile) number\b[^.?!\n]{0,20}\b(?:change|update|badal\w*)",
    re.IGNORECASE,
)
# business_rules.json explicit_human_request_escalates: the customer asks for a person or a call.
HUMAN_REQUEST = re.compile(
    r"\b(?:talk|speak)\w*\s+(?:it\s+through\s+)?(?:to|with)\s+(?:a\s+|an\s+)?(?:real\s+)?"
    r"(?:person|human|someone|somebody|agent|manager|supervisor)\b"
    r"|\b(?:someone|somebody|a person|sales ?person|an? agent|a human|koi)\b[^.?!\n]{0,25}"
    r"\b(?:call|phone)\s*(?:me\b|kar\w*)"
    r"|\bcall me back\b|\bbot se baat nahi\b|\b(?:kisi|koi)\s+(?:insaan|insan|senior|bande|aadmi)\b",
    re.IGNORECASE,
)
# Policy 9: a claimed system note or hidden instruction to the assistant.
INJECTION_MARKERS = ("[system note", "<!--")
INJECTION = re.compile(
    r"\bignore (?:all |any |your )?(?:previous |prior |earlier )?(?:instructions|rules|policies)\b"
    r"|\bnote to (?:the )?(?:ai|assistant|bot|agent)\b|^\s*system\s*:",
    re.IGNORECASE | re.MULTILINE,
)
# Policy 8: money only counts as asked for when the customer asks to receive it. "Why is my bill
# ₹699?" quotes a bill; it asks for nothing.
MONEY_REQUEST = re.compile(
    r"\b(refund\w*|credit(?!\s*card)\w*|compensat\w*|waiv\w*|discount\w*|cashback|reimburs\w*|money back"
    r"|wapas|vapas)\b"
    r"|(?:₹|\brs\.?)\s?\d[\d,]*\s+back\b"
    r"|\b(?:expect|want) (?:acme|you) to pay\b|\b(?:acme|you) (?:should|must|has to|have to|need to) pay\b",
    re.IGNORECASE,
)


SENTENCES = re.compile(r"(?<![Rr][Ss]\.)(?<=[.!?;])\s+|\n+")


def amounts_asked_for(text: str, amounts: Callable[[str], List[int]]) -> List[int]:
    """Rupee amounts the customer asks to receive; `amounts` is lab.evals.amounts.

    Read per sentence, so a bill quoted next to the ask doesn't count: "My bill says ₹1,499 but I'm
    on Plus. Credit me the ₹500 difference." -> [500]. An ask with no amount in its sentence
    ("I paid ₹1,499. I want a full refund.") falls back to every amount in the message."""
    asks = [s for s in SENTENCES.split(text or "") if MONEY_REQUEST.search(s)]
    if not asks:
        return []
    return [a for s in asks for a in amounts(s)] or amounts(text)


def _trigger(code: str, rule: str, reason: str) -> Dict[str, str]:
    return {"code": code, "rule": rule, "reason": reason}


def escalation_triggers(text: str,
                        record: Dict[str, Any],
                        rules: Dict[str, Any],
                        *,
                        headroom: int,
                        requested_amounts: Iterable[int] = (),
                        double_payment_eligible: bool = False,
                        concepts: Iterable[str] = ()) -> List[Dict[str, str]]:
    """Every rule that says a person must handle this email: [{"code", "rule", "reason"}], [] when none fire.

    text               the customer's own words (lab.acme.customer_text), never the agent's turns
    record             the customer record from customers.json
    rules              the business rules (reads `escalation_policy` and `concession_limit`)
    headroom           remaining 30-day concession headroom in rupees
    requested_amounts  rupee amounts the customer asks to receive (see amounts_asked_for())
    concepts           ontology concept names found in the text ("manipulation", ...)

    Codes follow the escalation_rule labels in data/acme/cases*.jsonl (E1 legal, E2 churn after
    repeated complaints, E3 money above the limit, E5 manipulation, E7 asks for a person,
    E9 account change by someone else), so triggers can be scored against the labels."""
    text = text or ""
    policy = rules.get("escalation_policy", {})
    limit = rules.get("concession_limit", {})
    found: List[Dict[str, str]] = []

    if policy.get("legal_or_regulator_threat_escalates", True) and LEGAL_THREAT.search(text):
        found.append(_trigger("E1", "legal_threat", "Customer threatens legal or regulator action (policy 6)."))

    min_prior = int(policy.get("min_prior_complaints_for_churn_escalation", 2))
    prior = int(record.get("complaints_last_30_days") or 0)
    claims_repeat = policy.get("trust_customer_claimed_complaint_count", True) and REPEAT_COMPLAINT.search(text)
    if CHURN_THREAT.search(text) and (prior >= min_prior or claims_repeat):
        source = f"record shows {prior} complaints" if prior >= min_prior else "customer says this is a repeat complaint"
        found.append(_trigger("E2", "churn_after_repeated_complaints",
                              f"Threat to leave after repeated complaints ({source}) (policy 6)."))

    # Policy 8 adds up everything asked for now: "₹300 for last week and ₹300 for this week" is ₹600.
    asked_total = sum(int(a) for a in requested_amounts)
    if (limit.get("escalate_on_exceed", True) and asked_total > headroom and not double_payment_eligible):
        found.append(_trigger("E3", "money_above_headroom",
                              f"Amount asked for (₹{asked_total} in total) exceeds remaining 30-day headroom of "
                              f"₹{headroom} (policy 3, 8)."))

    low = text.lower()
    if policy.get("manipulation_or_claimed_policy_escalates", True) and (
            "manipulation" in set(concepts) or any(m in low for m in INJECTION_MARKERS) or INJECTION.search(text)):
        found.append(_trigger("E5", "manipulation",
                              "Message contains manipulation / claimed policy or system instruction (policy 9)."))

    if policy.get("explicit_human_request_escalates", True) and HUMAN_REQUEST.search(text):
        found.append(_trigger("E7", "human_request", "Customer asks to talk to a person."))

    if policy.get("third_party_account_change_escalates", True) and (
            (THIRD_PARTY_SENDER.search(text) and ACCOUNT_CHANGE.search(text)) or OWNERSHIP_TRANSFER.search(text)):
        found.append(_trigger("E9", "third_party_account_change",
                              "Someone other than the account holder asks to change the account (policy 11)."))

    if policy.get("contact_detail_change_always_escalates", True) and CONTACT_CHANGE.search(text):
        found.append(_trigger("E9", "contact_detail_change",
                              "Request to change the registered phone number or email (policy 11)."))
    return found
