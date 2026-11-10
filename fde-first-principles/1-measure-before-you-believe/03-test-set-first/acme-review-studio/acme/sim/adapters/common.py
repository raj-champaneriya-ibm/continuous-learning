"""Shared normalization and guardrails for standalone adapters."""
from __future__ import annotations

import json
from typing import Any

from acme.checks import claim_checks, guard_hits
from acme.lab import INTENTS, Lab
from acme.workflow import PORTALS

from ..trace import RunInput


def validate_draft(draft: Any) -> dict[str, Any]:
    if not isinstance(draft, dict):
        raise ValueError("Adapter returned no draft object")
    if draft.get("intent") not in INTENTS:
        raise ValueError("Draft has an invalid intent")
    if not isinstance(draft.get("reply"), str) or not isinstance(draft.get("needs_human"), bool):
        raise ValueError("Draft needs a string reply and a boolean needs_human")
    if not isinstance(draft.get("escalation_reason"), str):
        raise ValueError("Draft needs a string escalation_reason")
    cited = draft.get("cited_sources")
    if not isinstance(cited, list) or not all(isinstance(item, str) for item in cited):
        raise ValueError("Draft cited_sources must be a list of strings")
    return draft


def no_draft(reason: str) -> dict[str, Any]:
    return {"intent": "other", "reply": "", "needs_human": True, "escalation_reason": reason,
            "cited_sources": []}


def direct_output(lab: Lab, config: dict[str, Any], run_input: RunInput,
                  draft: dict[str, Any] | None, *, provider: str, model: str) -> dict[str, Any]:
    customer = lab.customers.get(run_input.customer_id)
    if not customer:
        reason = "account not verified: unknown customer id"
        return {**no_draft(reason), "has_draft": False, "model_called": False, "provider": provider,
                "model": model, "decision": "escalate", "reasons": [reason], "flags": [], "guard_hits": [],
                "outcome": "held", "final_reply": None}
    draft = validate_draft(draft)
    outage = lab.outage_for(customer)
    sources = " ".join([json.dumps(customer, ensure_ascii=False), json.dumps(outage or {}, ensure_ascii=False)]
                       + [a["text"] for a in lab.kb.values()]
                       + [t["text"] for t in run_input.history])
    style = PORTALS.get(run_input.portal)
    issues = [] if style else [f"unknown portal '{run_input.portal}'"]
    flags = claim_checks(
        draft["reply"], customer=customer, outage=outage,
        others=[c for c in lab.customers.values() if c["id"] != customer["id"]],
        sources_text=sources, message=run_input.message, cited=draft["cited_sources"],
        known_ids=set(lab.kb) | {"CRM", "OUTAGE"},
        max_words=(style or PORTALS["email"])["max_words"],
    )
    hits = guard_hits(run_input.message, config["guards"])
    reasons = issues
    if not draft["reply"].strip():
        reasons.append("empty draft")
    if draft["needs_human"]:
        reasons.append(f"model: {draft['escalation_reason'] or 'asked for a human'}")
    reasons.extend(f"guard: {hit}" for hit in hits)
    if config["block_on_high_flags"]:
        reasons.extend(f"check: {flag['check']}" for flag in flags if flag["severity"] == "high")
    decision = "escalate" if reasons else "send"
    return {**draft, "has_draft": True, "model_called": True, "provider": provider, "model": model,
            "decision": decision, "reasons": list(dict.fromkeys(reasons)), "flags": flags, "guard_hits": hits,
            "outcome": "held" if reasons else "sent", "final_reply": None if reasons else draft["reply"]}
