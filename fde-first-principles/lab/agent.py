"""Version C: the agent loop.

Moved here from day 8: SYSTEM_C, MAX_STEPS and run_agent(case).

    from lab.agent import run_agent
    output, trace = run_agent(case, temperature=0.0, run=0)
    # output -> {"intent": ..., "reply": ..., "needs_human": ...}
    # trace  -> one dict per model call: {"step": i, "tokens_in": ..., "tokens_out": ...,
    #                                     "seconds": ..., "tool_calls": [(name, args, result), ...]}
"""
from __future__ import annotations

import json
from typing import Dict, List, Tuple

from lab.acme_tools import FUNCTIONS, TOOLS
from lab.llm import chat, extract_json

SYSTEM_C = """You are a support agent for Acme Fibre, a broadband company in Pune.
Use the tools: always look up the customer first, then search the help articles you need.
Follow every rule in the policy (exact times are never promised; refunds above ₹500 need a human;
never ask for OTPs or passwords). Call escalate when a human is needed.
When you are done, answer ONLY with JSON: {"intent": one of billing, outage, speed, cancel, upgrade,
relocation, other; "reply": the email to send; "needs_human": true or false}."""

MAX_STEPS = 6


def run_agent(case: Dict, temperature: float = 0.0, run: int = 0) -> Tuple[Dict, List[Dict]]:
    messages = [{"role": "system", "content": SYSTEM_C},
                {"role": "user", "content": f"Customer id: {case['customer_id']}\n\nEmail:\n{case['message']}"}]
    trace = []
    for step in range(MAX_STEPS):
        r = chat(messages, tools=TOOLS, temperature=temperature, run=run)
        entry = {"step": step, "tokens_in": r["tokens_in"], "tokens_out": r["tokens_out"],
                 "seconds": r["seconds"], "tool_calls": []}
        trace.append(entry)

        messages.append(r["message"])
        if not r["tool_calls"]:
            try:
                return extract_json(r["content"]), trace
            except ValueError:
                return {"intent": "other", "reply": r["content"], "needs_human": True, "parse_error": True}, trace
        for call in r["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            if name not in FUNCTIONS:
                result = {"error": f"unknown tool {name}"}
            else:
                try:
                    result = FUNCTIONS[name](**args)
                except TypeError as e:
                    result = {"error": f"bad arguments for {name}: {e}"}
            messages.append({"role": "tool", "tool_name": name, "content": json.dumps(result, ensure_ascii=False)})
            entry["tool_calls"].append((name, args, result))

    return {"intent": "other", "reply": "", "needs_human": True, "gave_up": True}, trace
