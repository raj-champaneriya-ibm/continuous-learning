"""Version C4: C3 with the two fixes day 10's failure read picked.

C3's last 6 failures on the base 84 (C3-glm53flash-v4): c13/c15/c47/c73 missed a KB
fact in the reply ('restart', '30 days') and escalated instead of answering; c84 hit
max_steps, returned an empty reply and failed every check. Fixes:

1. `_envelope_brief_c4` puts short excerpts of the envelope's grounded KB articles
   (not just their ids) in front of the model, and asks it to quote the concrete
   steps or terms. The answer it needs is in the prompt, so it answers instead of
   handing the email to a person.
2. When the loop runs out of steps or the draft comes back empty, one final no-tools
   call drafts the reply from what the trace already knows. A clean draft is
   sendable; the post-draft policy guard still runs.

    from lab.version_c4 import run_agent, version_c4
    output, trace = run_agent(case, temperature=0.0, run=0)
    row = version_c4(case, temperature=0.0, run=0)
"""
from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional, Tuple

from .acme import conversation, customer_text, kb_by_id
from .business_rules import load_business_rules
from .evals import policy_violations
from .llm import chat, extract_json
from .version_c3 import (
    MAX_STEPS,
    TOOLS_C3,
    _envelope_brief,
    build_decision_envelope,
    offers_not_allowed,
    scoped_functions,
    system_prompt,
)

FINAL_DRAFT_INSTRUCTION = (
    "The tools are no longer available. Using only what you already know from the record, "
    "the decision envelope and the help articles above, write the reply now. "
    'Answer ONLY with JSON: {"intent": str, "reply": str, "needs_human": bool}.'
)


def _excerpt(kid: str, limit: int = 280) -> str:
    article = kb_by_id()[kid]
    return f"{kid} · {article['title']}: {article['text'][:limit].strip()}…"


def _envelope_brief_c4(envelope: Dict[str, Any]) -> str:
    """C3's brief plus grounded KB excerpts the reply should quote from."""
    brief = _envelope_brief(envelope)
    ids = envelope.get("grounded_kb_ids") or []
    if ids:
        brief += (
            "\nGrounded KB excerpts (quote the concrete steps or terms from these in your reply):\n- "
            + "\n- ".join(_excerpt(kid) for kid in ids[:4])
        )
    return brief


def run_agent(case: Dict[str, Any],
              temperature: float = 0.0,
              run: int = 0,
              *,
              rules: Optional[Dict[str, Any]] = None,
              model: Optional[str] = None,
              max_steps: int = MAX_STEPS,
              envelope: Optional[Dict[str, Any]] = None,
              timeout: Optional[float] = None,
              persist_cache: bool = True) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Version C4 agent loop: C3's grounding, KB excerpts up front, and a forced final draft
    so the loop never returns an empty reply."""
    envelope = envelope if envelope is not None else build_decision_envelope(case, rules=rules)
    user_content = (
        f"Customer id: {case['customer_id']}\n\n"
        f"{_envelope_brief_c4(envelope)}\n\n"
        f"Email:\n{conversation(case)}"
    )
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": system_prompt()},
        {"role": "user", "content": user_content},
    ]
    trace: List[Dict[str, Any]] = []
    functions = scoped_functions(envelope)
    sources: List[str] = [f"rule:{t['rule']}" for t in envelope["escalation_triggers"]]
    active_rules = load_business_rules(overrides=rules) if rules else load_business_rules()

    def _finish(output: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        if not str(output.get("reply") or "").strip():
            sources.append("guard:empty_reply")
        output["escalation_sources"] = list(dict.fromkeys(sources))
        output["needs_human"] = bool(sources)
        return output, trace

    def _guard(output: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        violations = policy_violations(
            output.get("reply") or "",
            customer_id=case.get("customer_id"),
            rules=rules,
            asked=customer_text(case),
        )
        if violations:
            output["policy_guard_triggered"] = violations
            sources.extend(f"guard:{v}" for v in violations)
        sources.extend(offers_not_allowed(output.get("reply") or "", envelope["offer_decisions"],
                                          active_rules))
        return _finish(output)

    def _final_no_tools_draft() -> Dict[str, Any]:
        """One forced draft when the loop gave up or produced nothing."""
        r = chat(messages + [{"role": "user", "content": FINAL_DRAFT_INSTRUCTION}],
                 temperature=temperature, run=run, model=model, timeout=None,
                 **({} if persist_cache else {"use_cache": False, "write_cache": False}))
        trace.append({"step": max_steps, "tokens_in": r["tokens_in"], "tokens_out": r["tokens_out"],
                      "seconds": r["seconds"], "stop_reason": r.get("stop_reason"),
                      "tool_calls": [], "forced_final_draft": True})
        try:
            return extract_json(r["content"])
        except ValueError:
            return {"intent": "other", "reply": r["content"], "needs_human": True,
                    "parse_error": True}

    deadline = time.monotonic() + timeout if timeout is not None else None
    for step in range(max_steps):
        remaining = deadline - time.monotonic() if deadline is not None else None
        if remaining is not None and remaining <= 0:
            raise TimeoutError("C4 agent exceeded its run timeout")
        options = {} if persist_cache else {"use_cache": False, "write_cache": False}
        r = chat(messages, tools=TOOLS_C3, temperature=temperature, run=run, model=model,
                 timeout=remaining, **options)
        entry: Dict[str, Any] = {
            "step": step,
            "tokens_in": r["tokens_in"],
            "tokens_out": r["tokens_out"],
            "seconds": r["seconds"],
            "stop_reason": r.get("stop_reason"),
            "tool_calls": [],
            "system_prompt": messages[0]["content"] if step == 0 else None,
            "user_prompt": messages[1]["content"] if step == 0 else None,
        }
        trace.append(entry)
        messages.append(r["message"])

        if not r["tool_calls"]:
            if r.get("stop_reason") == "max_tokens":
                sources.append("guard:cut_off")
            try:
                output = extract_json(r["content"])
            except ValueError:
                output = {"intent": "other", "reply": r["content"], "needs_human": True,
                          "parse_error": True}
            if output.get("parse_error"):
                sources.append("fallback:parse_error")
            elif output.get("needs_human"):
                sources.append("model")
            if not str(output.get("reply") or "").strip():
                # Fix 2: never ship an empty reply when the model was still willing to talk.
                sources.append("fallback:empty_draft")
                retry = _final_no_tools_draft()
                if str(retry.get("reply") or "").strip() and not retry.get("parse_error"):
                    sources.remove("fallback:empty_draft")
                    if retry.get("needs_human"):
                        sources.append("model")
                    return _guard(retry)
            return _guard(output)

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

    # Fix 2: max_steps exhausted — draft from what the trace knows instead of giving up.
    sources.append("fallback:steps_exhausted")
    output = _final_no_tools_draft()
    if str(output.get("reply") or "").strip() and not output.get("parse_error"):
        sources.remove("fallback:steps_exhausted")
        if output.get("needs_human"):
            sources.append("model")
    return _guard(output)


def version_c4(case: Dict[str, Any],
               temperature: float = 0.0,
               run: int = 0,
               *,
               rules: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run Version C4 on one case and return a single result row with token and latency totals."""
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
