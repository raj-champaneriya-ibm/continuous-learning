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

    from lab.version_c3 import run_agent, version_c3, build_decision_envelope
    output, trace = run_agent(case, temperature=0.0, run=0)
    row = version_c3(case, temperature=0.0, run=0)
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple

from .acme import INTENTS, conversation, customer_text, kb_by_id, load_customers
from .acme_tools import (
    TOOLS as BASE_TOOLS,
    escalate,
    get_article,
    lookup_customer as _base_lookup_customer,
    search_kb as _base_search_kb,
)
from .business_rules import load_business_rules
from .escalation import amounts_asked_for, escalation_triggers
from .evals import amounts, policy_violations
from .llm import chat, extract_json
from .ontology import (
    compute_entitlements,
    define,
    extract_concepts,
    glossary,
    pune_service_areas,
)

MAX_STEPS = 6

SYSTEM_C3 = f"""You are a support agent for Acme Fibre, a broadband company in Pune.
Use the tools: look up the customer and their pre-computed entitlements, check help articles, and use define_term when policy wording or regional terms appear.
Follow every rule in the policy:
- Greet the customer by their first name.
- Never promise an exact time or date for fixing an outage; share the outage ticket ID instead.
- Never approve or promise a concession above the customer's remaining 30-day ₹500 headroom. Say it needs approval and set needs_human to true.
- Only offer the late-fee waiver (KB02) or 50% retention offer (KB11) when the entitlement check shows eligible=true.
- Never ask for OTPs, passwords or card numbers.
- Only the account holder can cancel, shift, change the plan, transfer the account, or change contact details.
- Call escalate and set needs_human to true when a human is needed: the envelope lists an escalation trigger,
  or the email reports possible fraud or a security incident, a safety hazard or staff misconduct, the
  customer disputes the record a second time, or the help articles and the record can't answer it.
- Answer these yourself without a human: anger, urgency or Hinglish on their own; a cancellation, shift or
  plan change asked by the account holder; a general question the help articles answer; a first
  disagreement with what the record shows.
When you are done, answer ONLY with JSON: {{"intent": one of {", ".join(INTENTS)}; "reply": the email to send; "needs_human": true or false}}."""


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
            }
    return report


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
    triggers = escalation_triggers(
        words,
        load_customers().get(cid.strip().upper(), {}),
        load_business_rules(overrides=rules) if rules else load_business_rules(),
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
        "pune_service_areas": pune_service_areas(),
        "escalation_triggers": triggers,
        "escalation_reasons": [t["reason"] for t in triggers],
        "pruned_glossary": glossary(only_terms=glossary_terms),
    }


def _envelope_brief(envelope: Dict[str, Any]) -> str:
    """Short deterministic summary attached to the user prompt so the LLM doesn't guess arithmetic."""
    offers = envelope["offers"]
    lines = [
        "--- Business Graph Decision Envelope ---",
        f"Remaining 30-day concession headroom: ₹{envelope['concession_headroom_rupees']}",
        f"- late-fee waiver (KB02): {'ELIGIBLE' if offers['late-fee waiver']['eligible'] else 'INELIGIBLE'} ({offers['late-fee waiver']['reason']})",
        f"- retention offer (KB11): {'ELIGIBLE' if offers['retention offer']['eligible'] else 'INELIGIBLE'} ({offers['retention offer']['reason']})",
        f"- double payment refund (KB04): {'ELIGIBLE' if offers['double payment refund']['eligible'] else 'INELIGIBLE'} ({offers['double payment refund']['reason']})",
        f"- outage credit (KB06): {'ELIGIBLE' if offers['outage credit']['eligible'] else 'INELIGIBLE'} ({offers['outage credit']['reason']})",
    ]
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
    # Who sent this case to a person: rule triggers, the escalate tool, the model's JSON, the policy guard.
    # Saved with the output, so a run shows why each case was escalated.
    sources: List[str] = [f"rule:{t['rule']}" for t in envelope["escalation_triggers"]]

    def _finish(output: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
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
            "tool_calls": [],
        }
        trace.append(entry)
        messages.append(r["message"])

        if not r["tool_calls"]:
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
            if name not in FUNCTIONS_C3:
                result = {"error": f"unknown tool {name}"}
            else:
                try:
                    result = FUNCTIONS_C3[name](**args)
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
        "tokens_in": sum(t["tokens_in"] for t in trace),
        "tokens_out": sum(t["tokens_out"] for t in trace),
        "seconds": round(sum(t["seconds"] for t in trace), 3),
    }
