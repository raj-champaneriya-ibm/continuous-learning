# View of 1-measure-before-you-believe/04-rules-baseline/notebook.ipynb (markdown and code cells; outputs omitted)

---- cell 1 (markdown) ----
# Day 4 · Version A: rules and templates (the honest baseline)

**First-principles question:** How far can plain code go before you need a model?

The full task (learn → build → record) is in this folder's `README.md`. This notebook is your workbench:
run cells top to bottom with **Shift + Enter**, fill in every cell marked **TODO**, and finish with the
**✅ self-check** cell at the end.

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

import pandas as pd
from lab.acme import INTENTS, first_name, load_cases, load_customers, outage_for, save_results

cases = load_cases()
customers = load_customers()
print(len(cases), "cases")

---- cell 3 (markdown) ----
## 1 · A keyword classifier
No model. Just words you choose.

---- cell 4 (code) ----
KEYWORDS = {
    "billing": ["bill", "charge", "refund", "payment", "paid", "fee"],
    "outage": ["down", "not working", "no internet", "band hai"],
    "speed": ["slow", "fast", "internet speed", "connection speed"],
    "cancel": ["cancel", "unsubscribe", "discontinue", "terminate"],
    "upgrade": ["upgrade", "improve", "enhance", "better"],
    "relocation": ["move", "relocate", "transfer", "shift"]
}

def classify(message):
    """The intent whose keywords appear most often in the message, or "other"."""
    text = message.lower()
    # TODO: count, for each intent, how many of its keywords appear in `text`;
    #       return the intent with the highest count, or "other" if every count is 0

    counts = {intent: 0 for intent in KEYWORDS}
    for intent, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                counts[intent] += 1
    max_intent = max(counts, key=lambda intent: counts[intent])
    if counts[max_intent] > 0:
        return max_intent
    return "other"

classify("My internet is not working since morning")

---- cell 5 (code) ----


---- cell 6 (markdown) ----
## 2 · Templates
One reply per intent. `{first_name}`, `{area}` and `{ticket}` are filled in for you.

---- cell 7 (code) ----
TEMPLATES = {
    "billing": (
        "Hi {first_name}, thanks for writing. Bills are due by the 10th, "
        "and a ₹100 late fee is added after that. "
        "You can see every bill in the Acme app under Billing."
    ),

    "outage": (
        "Hi {first_name}, there is an outage in {area} (ticket {ticket}). "
        "Our engineers are working on it and will update you by email "
        "and in the Acme app."
    ),

    "speed": (
        "Hi {first_name}, thanks for reporting your speed issue. "
        "Please turn off your router for 30 seconds, restart it, and test "
        "your speed at fast.com using a wired connection; if the speed is "
        "below half your plan speed, a technician can visit within "
        "2 working days."
    ),

    "cancel": (
        "Hi {first_name}, we understand your request to cancel your service. "
        "Cancellation requires 30 days' notice, router collection is free, "
        "and your final bill covers service until the end of the notice period."
    ),

    "upgrade": (
        "Hi {first_name}, thanks for your interest in upgrading your plan. "
        "Our plans are 100 Mbps at ₹699, 300 Mbps at ₹999, and 1 Gbps at "
        "₹1,499; upgrades activate within 1 hour, with pro-rata charges "
        "on your next bill."
    ),

    "relocation": (
        "Hi {first_name}, we can help you relocate your connection. "
        "Relocation is free in supported Pune areas, with re-installation "
        "within 48 hours of your requested date; outside supported areas, "
        "cancellation requires 30 days' notice."
    ),

    "other": (
        "Hi {first_name}, thanks for contacting Acme Fiber. "
        "Please share more details about your request so our support "
        "team can guide you."
    ),
}

def version_a(case):
    customer = customers[case["customer_id"]]
    outage = outage_for(customer)
    intent = classify(case["message"])
    fields = {"first_name": first_name(customer), "area": customer["area"],
              "ticket": outage["ticket"] if outage else "not available"}
    template = TEMPLATES.get(intent, TEMPLATES.get("other", "Hi {first_name}, thanks for writing to us."))
    return {"intent": intent, "reply": template.format(**fields), "needs_human": False}

version_a(cases[0])

---- cell 8 (markdown) ----
## 3 · Run version A on every case

---- cell 9 (code) ----
rows = []
for case in cases:
    out = version_a(case)
    rows.append(dict(out, id=case["id"], tokens_in=0, tokens_out=0, seconds=0.0))
save_results("A", rows)

df = pd.DataFrame({"id": [c["id"] for c in cases], "expected": [c["expected_intent"] for c in cases],
                   "predicted": [r["intent"] for r in rows]})
accuracy = (df.expected == df.predicted).mean()
print(f"Intent accuracy: {accuracy:.0%} on {len(df)} cases")
pd.crosstab(df.expected, df.predicted, margins=True)

---- cell 10 (markdown) ----
## 4 · Five failures
Read them. Then write one line per failure in the markdown cell below.

---- cell 11 (code) ----
wrong = df[df.expected != df.predicted]
for _, row in wrong.head(5).iterrows():
    case = next(c for c in cases if c["id"] == row.id)
    print(f"{row.id}: expected {row.expected}, got {row.predicted}\n   {case['message']}\n")

---- cell 12 (markdown) ----
Why the rules failed:

1. c05 — Keyword ambiguity: The word “move” was interpreted as relocation, although the customer wants to upgrade to the 1 Gbps plan.

2. c13 — Limited phrase recognition: The rules failed to recognize “internet stopped working” as an outage-related expression.

3. c15 — Language variation: The rules could not interpret Hinglish expressions such as “Internet dead” and “service zero” as an outage complaint.

4. c17 — Multiple intents: The customer reports an outage and requests compensation; the rules failed to identify the underlying outage intent.

5. c19 — Multilingual and multiple intents: The rules missed “net band” (internet down) and could not distinguish the primary outage complaint from the secondary escalation request.

Key learning: Simple keyword-based classification struggles with synonyms, multilingual expressions, ambiguous words, and multiple intents. It needs contextual understanding and explicit rules for intent prioritization.

---- cell 13 (code) ----
# ✅ Self-check: run me last. A clear message tells you what to fix.
assert classify("My bill has an extra charge") == "billing"
assert classify("internet is down since morning") == "outage"
assert classify("hello there") == "other", 'No keyword at all should give "other"'
missing = [i for i in INTENTS if i not in TEMPLATES]
assert not missing, f"Write templates for: {missing}"
assert len(rows) == len(cases) and 0 <= accuracy <= 1
assert (ROOT / "data" / "results" / "A.jsonl").exists()
print("All checks passed ✅  Now write 'In my words' in README.md and record your video.")
