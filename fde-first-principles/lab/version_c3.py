"""Version C3: the agent loop grounded in the Business Graph Engine (ontology + business rules).

Mitigates the structural gaps between Version B, Version C/C2, and the ontology:
1. Wires `define_term` and `check_entitlement` into the agent's toolset (`TOOLS_C3`).
2. Upgrades `search_kb` to traverse `Concept -> acme:documentedIn -> KBArticle` edges first,
   so Hinglish and regional queries ('paisa wapas', 'late fee maaf', 'सूट') find the right KB.
3. Pre-computes a deterministic `DecisionEnvelope` per case (30-day ₹ headroom, offer eligibility,
   linked KB articles, and pruned glossary) so the LLM never does date or percentage math in its head.
4. Runs the ontology-backed policy check (`lab.evals.policy_violations`) after drafting so any
   policy break or over-limit concession is routed to a human.
5. Runs the escalation rules as code (`lab.escalation`, from `escalation_policy` in business_rules.json):
   legal threats, churn after repeated complaints, money above headroom, manipulation, a request for a
   person, and account changes by someone else force needs_human before the model drafts anything.
   Every forced or chosen escalation is recorded in `escalation_sources`.
6. Separates eligibility from authority (`offer_decisions`): each discretionary offer is OFFER,
   NEEDS APPROVAL (above the headroom), HOLD (a person is handling the case) or DO NOT OFFER. A draft
   that offers something the decision doesn't allow goes to a person.
7. Keeps the area outage out of scope unless the customer reported that their service is down
   (policy 12): the envelope and the lookup_customer / check_entitlement tools withhold it.

    from lab.version_c3 import run_agent, version_c3, build_decision_envelope
    output, trace = run_agent(case, temperature=0.0, run=0)
    row = version_c3(case, temperature=0.0, run=0)
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from .acme import DATA, INTENTS, conversation, customer_text, intent_guide, kb_by_id, load_customers
from .acme_tools import (
    TOOLS as BASE_TOOLS,
    escalate,
    get_article,
    lookup_customer as _base_lookup_customer,
    search_kb as _base_search_kb,
)
from .business_rules import load_business_rules
from .escalation import amounts_asked_for, escalation_triggers
from .evals import APPROVAL_WORDS, NEGATION, NOT_A_PROMISE, SENTENCE_END, amounts, policy_violations
from .llm import chat, extract_json
from .ontology import (
    compute_entitlements,
    customer_reported_outage,
    define,
    extract_concepts,
    glossary,
    pune_service_areas,
)

MAX_STEPS = 6

# The full policy goes in verbatim (as in version B), so no rule is lost in a paraphrase. The bullets before it say
# how to apply the policy with C3's decision envelope.
POLICY = (DATA / "policy.md").read_text(encoding="utf-8")

SYSTEM_C3 = f"""You are a support agent for Acme Fibre, a broadband company in Pune.
Use the tools: look up the customer and their pre-computed entitlements, check help articles, and use define_term when policy wording or regional terms appear.
Follow every rule in the reply policy below. With the decision envelope, that means:
- Write the reply in simple, polite English, even when the customer writes in Hinglish or another language (policy 7).
- Discuss only the account in the envelope. If the sender is not its account holder, don't reveal that account's id, plan,
  area, balance or outage, and don't address the sender by the account holder's name (policies 5 and 11). Never give
  details of any other customer.
- Never approve or promise a concession above the customer's remaining 30-day ₹500 headroom. Say it needs approval and set needs_human to true.
- Eligible is not approved. Offer the late-fee waiver (KB02) or the retention offer (KB11) only as the envelope's
  offer decisions say. OFFER: you may offer it once (the retention offer only to a customer who asks to cancel).
  NEEDS APPROVAL: say a colleague will review it, never present it as given, and set needs_human to true.
  HOLD or DO NOT OFFER: don't offer it.
- Call escalate and set needs_human to true when a human is needed: the envelope lists an escalation trigger,
  or the email reports possible fraud or a security incident, a safety hazard or staff misconduct, the
  customer disputes the record a second time, or the help articles and the record can't answer it.
- When a person will take over, still answer what the customer asked, from the record and help articles; only the
  decision waits. Don't bring up other things from the record that the customer didn't ask about.
- Answer these yourself without a human: anger, urgency or Hinglish on their own; a cancellation, shift or
  plan change asked by the account holder; a general question the help articles answer; a first
  disagreement with what the record shows.
- Pick the intent with the intent guide below.
When you are done, answer ONLY with JSON: {{"intent": one of {", ".join(INTENTS)}; "reply": the email to send; "needs_human": true or false}}.

{intent_guide()}

{POLICY}"""


ELIGIBLE_IS_NOT_APPROVED = "Eligible is not approved: the offer decisions in the decision envelope say what you may offer."


def define_term(word: str) -> Dict[str, Any]:
    """Look up a policy or regional term in the Acme ontology."""
    info = define(word)
    if info is None:
        matches = extract_concepts(word)
        info = matches[0] if matches else None
    if info is None:
        return {"error": f"No ontology definition for {word!r}"}
    return {
        "term": info["term"],
        "definition": info["definition"],
        "note": info.get("note"),
        "source": info.get("source"),
        "counts_toward_limit": info.get("counts_toward_limit"),
        "once_per_months": info.get("once_per_months"),
        "kb_articles": info.get("kb_articles", []),
        "policy_rules": info.get("policy_rules", []),
    }


def check_entitlement(customer_id: str, offer: str = "") -> Dict[str, Any]:
    """Compute deterministic concession headroom and offer eligibility for a customer."""
    try:
        report = compute_entitlements(customer_id)
    except KeyError:
        return {"error": f"No customer with id {customer_id!r}"}
    if offer:
        canonical = (define(offer) or {}).get("term") or offer.strip().lower()
        if canonical in report["offers"]:
            return {
                "customer_id": report["customer_id"],
                "concession_headroom_rupees": report["concession_headroom_rupees"],
                "offer": canonical,
                **report["offers"][canonical],
                "note": ELIGIBLE_IS_NOT_APPROVED,
            }
    return {**report, "note": ELIGIBLE_IS_NOT_APPROVED}


def search_kb_c3(query: str, k: int = 2) -> List[Dict[str, Any]]:
    """Ontology-grounded KB search: traverses Concept -> acme:documentedIn edges before word overlap."""
    kb = kb_by_id()
    linked_ids: List[str] = []
    direct = define(query)
    if direct:
        for kid in direct.get("kb_articles", []):
            if kid in kb and kid not in linked_ids:
                linked_ids.append(kid)
    for concept in extract_concepts(query):
        for kid in concept.get("kb_articles", []):
            if kid in kb and kid not in linked_ids:
                linked_ids.append(kid)

    results = [{"id": kid, "title": kb[kid]["title"], "text": kb[kid]["text"]} for kid in linked_ids]
    for item in _base_search_kb(query, k=max(2, int(k))):
        if all(r["id"] != item["id"] for r in results):
            results.append(item)
    return results[: max(1, int(k))]


def lookup_customer_c3(customer_id: str) -> Dict[str, Any]:
    """Customer record enriched with active outage and deterministic entitlement status."""
    base = _base_lookup_customer(customer_id)
    if "error" in base:
        return base
    ent = compute_entitlements(customer_id)
    return {
        **base,
        "concession_headroom_rupees": ent["concession_headroom_rupees"],
        "is_pune_service_area": ent["is_pune_service_area"],
        "offer_eligibility": {
            name: {
                "eligible": details["eligible"],
                "auto_approvable": details["auto_approvable"],
                "amount_rupees": details.get("amount_rupees"),
                "reason": details["reason"],
            }
            for name, details in ent["offers"].items()
        },
        "note": ELIGIBLE_IS_NOT_APPROVED,
    }


FUNCTIONS_C3 = {
    "lookup_customer": lookup_customer_c3,
    "search_kb": search_kb_c3,
    "get_article": get_article,
    "define_term": define_term,
    "check_entitlement": check_entitlement,
    "escalate": escalate,
}

TOOLS_C3 = BASE_TOOLS + [
    {
        "type": "function",
        "function": {
            "name": "define_term",
            "description": "Look up the official Acme Fibre policy definition, KB source, and ₹500 limit rules "
                           "for an English, Hinglish, or regional term (e.g. 'paisa wapas', 'late fee maaf', "
                           "'retention offer', 'account holder', 'concession limit').",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {"type": "string", "description": "The word or phrase to define"}
                },
                "required": ["word"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_entitlement",
            "description": "Check a customer's remaining ₹500 30-day concession headroom and deterministic "
                           "eligibility for late-fee waiver, retention offer, double payment refund, and outage credit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Customer id like AC1003"},
                    "offer": {
                        "type": "string",
                        "description": "Optional specific offer name (e.g. 'late-fee waiver', 'retention offer')",
                    },
                },
                "required": ["customer_id"],
            },
        },
    },
]


DISCRETIONARY_OFFERS = ("late-fee waiver", "retention offer")
OFFER_LABELS = {"offer": "OFFER", "needs_approval": "NEEDS APPROVAL", "hold": "HOLD", "do_not_offer": "DO NOT OFFER",
                "automatic": "AUTOMATIC", "not_on_record": "NOT ON RECORD"}


def offer_decisions(offers: Dict[str, Dict[str, Any]],
                    headroom: int,
                    triggers: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    """What the agent may do with each offer. Eligibility (tenure, cooldown) is not authority (the ₹ headroom).

    late-fee waiver, retention offer (discretionary, once a year):
      do_not_offer    the record makes the customer ineligible
      hold            an escalation rule fired: a person is handling the case and decides
      offer           eligible and the amount fits the remaining 30-day headroom
      needs_approval  eligible but above the headroom (50% off Pro is ₹750): a colleague must approve
    double payment refund, outage credit (automatic, KB04 / KB06): automatic or not_on_record."""
    decisions: Dict[str, Dict[str, str]] = {}
    for name, offer in offers.items():
        if name not in DISCRETIONARY_OFFERS:
            status = "automatic" if offer["eligible"] else "not_on_record"
            decisions[name] = {"status": status, "why": offer["reason"]}
            continue
        amount = offer.get("amount_rupees")
        if not offer["eligible"]:
            status, why = "do_not_offer", offer["reason"]
        elif triggers:
            status, why = "hold", "A person is handling this case (" + "; ".join(t["rule"] for t in triggers) + ")."
        elif offer.get("auto_approvable"):
            status, why = "offer", f"Eligible, and ₹{amount} fits the ₹{headroom} headroom."
        else:
            status, why = "needs_approval", f"Eligible, but ₹{amount} is above the ₹{headroom} headroom (policy 8)."
        decisions[name] = {"status": status, "why": why}
    return decisions


def _offer_mention(name: str, rules: Dict[str, Any]) -> "re.Pattern[str]":
    """Words that name an offer in a reply: '50% off' / 'retention offer', or 'waive' for the late fee."""
    if name == "retention offer":
        pct = rules["offers"]["retention offer"]["discount_percent"]
        return re.compile(rf"\b{pct}\s?%|\bretention offer\b|\bhalf[- ]price\b", re.IGNORECASE)
    return re.compile(r"\bwaiv\w*|\blate[- ]fee\s+(?:maaf|hata)", re.IGNORECASE)


# A grant made to this customer: "we can offer you", "you're eligible for", "I've waived". Explaining the rule
# ("waivers can only be offered to customers with 13 months") or declining is not a grant.
OFFER_TO_YOU = re.compile(
    r"\b(?:offer|give|extend)\w*\s+you\b|\byou(?:'re| are)\s+eligible\b|\byou can (?:have|get|enjoy)\b"
    r"|\b(?:we|i)(?:'ll| will| can| have|'ve)\s+waive\w*",
    re.IGNORECASE,
)


def _grants(sentence: str) -> bool:
    approval = APPROVAL_WORDS.search(sentence)
    if approval and not NEGATION.search(sentence[max(0, approval.start() - 30):approval.start()]):
        return True
    return bool(OFFER_TO_YOU.search(sentence)) and not NOT_A_PROMISE.search(sentence)


def offers_not_allowed(reply: str,
                       decisions: Dict[str, Dict[str, str]],
                       rules: Dict[str, Any]) -> List[str]:
    """Offers the reply makes that its decision doesn't allow, as 'offer:<name>:<status>'.

    needs_approval: any mention goes to a person (the customer was told a colleague will review it).
    hold, do_not_offer: a sentence that grants the offer to the customer goes to a person; explaining the
    rule or declining is fine."""
    sentences = SENTENCE_END.split(reply or "")
    found = []
    for name in DISCRETIONARY_OFFERS:
        status = decisions.get(name, {}).get("status")
        if status not in ("needs_approval", "hold", "do_not_offer"):
            continue
        pattern = _offer_mention(name, rules)
        hits = [s for s in sentences if pattern.search(s)]
        if (status == "needs_approval" and hits) or any(_grants(s) for s in hits):
            found.append(f"offer:{name}:{status}")
    return found


OUTAGE_WITHHELD = "Withheld: the customer didn't report that their service is down (policy 12)."


def _without_outage(result: Any) -> Any:
    """A tool result with the area outage removed, so the model can't bring it up unasked."""
    if not isinstance(result, dict):
        return result
    if result.get("offer") == "outage credit":
        return {"customer_id": result.get("customer_id"), "offer": "outage credit", "note": OUTAGE_WITHHELD}
    out = dict(result)
    if "current_outage" in out:
        out["current_outage"] = OUTAGE_WITHHELD
    for key in ("offer_eligibility", "offers"):
        if isinstance(out.get(key), dict) and "outage credit" in out[key]:
            out[key] = {k: v for k, v in out[key].items() if k != "outage credit"}
    return out


def scoped_functions(envelope: Dict[str, Any]) -> Dict[str, Any]:
    """The tools for this email: the customer-record tools drop the outage when it is out of scope."""
    if envelope.get("outage_in_scope"):
        return FUNCTIONS_C3
    return {
        **FUNCTIONS_C3,
        "lookup_customer": lambda customer_id: _without_outage(lookup_customer_c3(customer_id)),
        "check_entitlement": lambda customer_id, offer="": _without_outage(check_entitlement(customer_id, offer)),
    }


def build_decision_envelope(case: Dict[str, Any],
                            *,
                            rules: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Compile the ontology TBox, business rules, and single-customer ABox into a DecisionEnvelope."""
    cid = case["customer_id"]
    text = conversation(case)
    words = customer_text(case)  # escalation reads only what the customer wrote, never earlier agent turns
    ent = compute_entitlements(cid, rules=rules)
    concepts = extract_concepts(text)
    matched_names = [c["term"] for c in concepts]

    grounded_kbs: List[str] = []
    for c in concepts:
        for kid in c.get("kb_articles", []):
            if kid not in grounded_kbs:
                grounded_kbs.append(kid)

    # Always include core money/identity terms alongside matched concepts in the pruned glossary
    core_terms = ["account holder", "concession limit", "manipulation"]
    glossary_terms = list(dict.fromkeys(matched_names + core_terms))

    headroom = ent["concession_headroom_rupees"]
    active_rules = load_business_rules(overrides=rules) if rules else load_business_rules()
    triggers = escalation_triggers(
        words,
        load_customers().get(cid.strip().upper(), {}),
        active_rules,
        headroom=headroom,
        requested_amounts=amounts_asked_for(words, amounts),
        double_payment_eligible=ent["offers"]["double payment refund"]["eligible"],
        concepts=[c["term"] for c in extract_concepts(words)],
    )

    return {
        "customer_id": cid,
        "matched_concepts": matched_names,
        "grounded_kb_ids": grounded_kbs,
        "concession_headroom_rupees": headroom,
        "offers": ent["offers"],
        "offer_decisions": offer_decisions(ent["offers"], headroom, triggers),
        "outage_in_scope": customer_reported_outage(words),
        "pune_service_areas": pune_service_areas(),
        "escalation_triggers": triggers,
        "escalation_reasons": [t["reason"] for t in triggers],
        "pruned_glossary": glossary(only_terms=glossary_terms),
    }


def _envelope_brief(envelope: Dict[str, Any]) -> str:
    """Short deterministic summary attached to the user prompt so the LLM doesn't guess arithmetic."""
    decisions = envelope["offer_decisions"]
    lines = [
        "--- Business Graph Decision Envelope ---",
        f"Remaining 30-day concession headroom: ₹{envelope['concession_headroom_rupees']}",
        "Offer decisions (eligible is not approved; follow these):",
    ]
    for name, kb in (("late-fee waiver", "KB02"), ("retention offer", "KB11"),
                     ("double payment refund", "KB04"), ("outage credit", "KB06")):
        if name == "outage credit" and not envelope["outage_in_scope"]:
            continue  # policy 12: the customer didn't report that their service is down
        d = decisions[name]
        lines.append(f"- {name} ({kb}): {OFFER_LABELS[d['status']]}. {d['why']}")
    if envelope["grounded_kb_ids"]:
        lines.append("Ontology-linked KB articles: " + ", ".join(envelope["grounded_kb_ids"]))
    if envelope["escalation_reasons"]:
        lines.append(" Escalation triggers detected: " + "; ".join(envelope["escalation_reasons"]))
    if envelope["pruned_glossary"]:
        lines.append("Definitions:\n" + envelope["pruned_glossary"])
    return "\n".join(lines)


def run_agent(case: Dict[str, Any],
              temperature: float = 0.0,
              run: int = 0,
              *,
              rules: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Run the Version C3 ontology-powered agent loop and enforce post-draft policy guardrails."""
    envelope = build_decision_envelope(case, rules=rules)
    user_content = (
        f"Customer id: {case['customer_id']}\n\n"
        f"{_envelope_brief(envelope)}\n\n"
        f"Email:\n{conversation(case)}"
    )
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_C3},
        {"role": "user", "content": user_content},
    ]
    trace: List[Dict[str, Any]] = []
    functions = scoped_functions(envelope)
    # Who sent this case to a person: rule triggers, the escalate tool, the model's JSON, the policy guard.
    # Saved with the output, so a run shows why each case was escalated.
    sources: List[str] = [f"rule:{t['rule']}" for t in envelope["escalation_triggers"]]

    def _finish(output: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        # A blank or cut-off reply must never look sendable.
        if not str(output.get("reply") or "").strip():
            sources.append("guard:empty_reply")
        output["escalation_sources"] = list(dict.fromkeys(sources))
        output["needs_human"] = bool(sources)
        return output, trace

    for step in range(MAX_STEPS):
        r = chat(messages, tools=TOOLS_C3, temperature=temperature, run=run)
        entry: Dict[str, Any] = {
            "step": step,
            "tokens_in": r["tokens_in"],
            "tokens_out": r["tokens_out"],
            "seconds": r["seconds"],
            "stop_reason": r.get("stop_reason"),
            "tool_calls": [],
        }
        trace.append(entry)
        messages.append(r["message"])

        if not r["tool_calls"]:
            if r.get("stop_reason") == "max_tokens":
                sources.append("guard:cut_off")
            try:
                output = extract_json(r["content"])
            except ValueError:
                output = {
                    "intent": "other",
                    "reply": r["content"],
                    "needs_human": True,
                    "parse_error": True,
                }
            if output.get("parse_error"):
                sources.append("fallback:parse_error")
            elif output.get("needs_human"):
                sources.append("model")
            # Post-draft ontology policy guardrail (ADR-001 step 3)
            violations = policy_violations(
                output.get("reply") or "",
                customer_id=case.get("customer_id"),
                rules=rules,
                asked=customer_text(case),
            )
            if violations:
                output["policy_guard_triggered"] = violations
                sources.extend(f"guard:{v}" for v in violations)
            sources.extend(offers_not_allowed(
                output.get("reply") or "", envelope["offer_decisions"],
                load_business_rules(overrides=rules) if rules else load_business_rules(),
            ))
            return _finish(output)

        for call in r["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            if name == "escalate":
                sources.append("tool:escalate")
            if name not in functions:
                result = {"error": f"unknown tool {name}"}
            else:
                try:
                    result = functions[name](**args)
                except TypeError as e:
                    result = {"error": f"bad arguments for {name}: {e}"}
            messages.append(
                {"role": "tool", "tool_name": name, "content": json.dumps(result, ensure_ascii=False)}
            )
            entry["tool_calls"].append((name, args, result))

    sources.append("fallback:gave_up")
    return _finish({"intent": "other", "reply": "", "needs_human": True, "gave_up": True})


def version_c3(case: Dict[str, Any],
               temperature: float = 0.0,
               run: int = 0,
               *,
               rules: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run Version C3 on one case and return a single result row with token and latency totals."""
    output, trace = run_agent(case, temperature=temperature, run=run, rules=rules)
    return {
        **output,
        "steps": len(trace),
        "tool_calls": [
            {"step": t["step"], "name": c[0], "args": c[1], "result": c[2]}
            for t in trace for c in t["tool_calls"]
        ],
        "tokens_in": sum(t["tokens_in"] for t in trace),
        "tokens_out": sum(t["tokens_out"] for t in trace),
        "seconds": round(sum(t["seconds"] for t in trace), 3),
    }
