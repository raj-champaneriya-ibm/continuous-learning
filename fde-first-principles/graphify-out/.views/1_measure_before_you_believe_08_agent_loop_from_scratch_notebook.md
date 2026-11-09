# View of 1-measure-before-you-believe/08-agent-loop-from-scratch/notebook.ipynb (markdown and code cells; outputs omitted)

---- cell 1 (markdown) ----
# Day 8 · Version C: an agent loop from scratch

**First-principles question:** What is an 'agent', really, once you remove the framework?

The full task (learn → build → record) is in this folder's `README.md`. This notebook is your workbench:
run cells top to bottom with **Shift + Enter**, fill in every cell marked **TODO**, and finish with the
**✅ self-check** cell at the end.

```
email ─► model ─► tool call? ─yes─► your code runs the tool ─► result goes back to the model ─┐
                     │ no                                                                     │
                     ▼                                                                        │
               final answer ◄────────────────────────── loop (at most MAX_STEPS) ◄─────────────┘
```

---- cell 2 (code) ----
import sys
from pathlib import Path

def find_root():
    """The fde-first-principles folder (it has progress.json)."""
    for p in [Path.cwd(), *Path.cwd().parents]:
        if (p / ".learn" / "progress.json").exists() or (p / "progress.json").exists():
            return p
    raise RuntimeError("Open this notebook from inside your fde-first-principles folder.")

ROOT = find_root()
sys.path.insert(0, str(ROOT))  # so `import lab.…` works

import json
from lab.acme import load_cases
from lab.acme_tools import FUNCTIONS, TOOLS
from lab.llm import chat, extract_json

cases = load_cases()
print([t["function"]["name"] for t in TOOLS])

---- cell 3 (markdown) ----
## 1 · The agent's instructions

---- cell 4 (code) ----
SYSTEM_C = """You are a support agent for Acme Fibre, a broadband company in Pune.
Use the tools: always look up the customer first, then search the help articles you need.
Follow every rule in the policy (exact times are never promised; refunds above ₹500 need a human;
never ask for OTPs or passwords). Call escalate when a human is needed.
When you are done, answer ONLY with JSON: {"intent": one of billing, outage, speed, cancel, upgrade,
relocation, other; "reply": the email to send; "needs_human": true or false}."""

---- cell 5 (markdown) ----
## 2 · The loop

---- cell 6 (code) ----
MAX_STEPS = 6

def run_agent(case, temperature=0.0, run=0):
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

---- cell 7 (markdown) ----
## 3 · Read two traces

---- cell 8 (code) ----
def show(case):
    answer, trace = run_agent(case)
    print(f"── {case['id']}: {case['message']}")
    for e in trace:
        for name, args, result in e["tool_calls"]:
            print(f"   step {e['step']}: {name}({args}) → {json.dumps(result, ensure_ascii=False)[:120]}…")
    print(f"   answer: {answer}\n")
    return answer, trace

show(cases[0]); show(cases[7]);

---- cell 9 (markdown) ----
## 4 · The first 10 cases

---- cell 10 (code) ----
steps = {}
for case in cases[:10]:
    answer, trace = run_agent(case)
    steps[case["id"]] = len(trace)
print("model calls per case:", steps)

---- cell 11 (code) ----
# ✅ Self-check: run me last. A clear message tells you what to fix.
answer, trace = run_agent(cases[0])
assert isinstance(answer, dict) and "intent" in answer and "reply" in answer, "run_agent must return (answer dict, trace)"
assert 1 <= len(trace) <= MAX_STEPS, "The loop must stop within MAX_STEPS"
assert any(e["tool_calls"] for e in trace), "The agent should have called at least one tool (TODO 3)"
assert len(steps) == 10 and max(steps.values()) <= MAX_STEPS
print("All checks passed ✅  Now write 'In my words' in README.md and record your video.")
