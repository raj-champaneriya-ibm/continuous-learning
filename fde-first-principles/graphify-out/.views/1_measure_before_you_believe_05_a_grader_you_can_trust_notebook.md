# View of 1-measure-before-you-believe/05-a-grader-you-can-trust/notebook.ipynb (markdown and code cells; outputs omitted)

---- cell 1 (markdown) ----
# Day 5 · A grader you can trust

**First-principles question:** What exactly makes a reply 'correct' for this customer?

The full task (learn → build → record) is in this folder's `README.md`. This notebook is your workbench:
run cells top to bottom with **Shift + Enter**, fill in every cell marked **TODO**, and finish with the
**✅ self-check** cell at the end.

Today you write code in **`lab/evals.py`**, not here. This notebook tests it. After each change to the file,
re-run the first code cell (it reloads the module).

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

import importlib
import pandas as pd
import lab.evals as evals
importlib.reload(evals)
from lab.acme import load_cases, load_results

cases = {c["id"]: c for c in load_cases()}
print(len(cases), "cases")


---- cell 3 (markdown) ----
## 1 · Tests for your grader
Each line is one rule. Make them all pass.

---- cell 4 (code) ----
case = {"expected_intent": "outage", "must_include": ["Priya", "OUT-KOTH-1021"], "must_not": ["by 2 pm"],
        "needs_human": False}
good = {"intent": "outage", "needs_human": False,
        "reply": "Hi Priya, there is an outage in Kothrud (ticket OUT-KOTH-1021). Engineers are on site."}

tests = {
    "a good reply passes": evals.score(case, good)["passed"],
    "wrong intent fails intent_ok": not evals.score(case, dict(good, intent="billing"))["intent_ok"],
    "missing ticket fails facts_ok": not evals.score(case, dict(good, reply="Hi Priya, we are on it."))["facts_ok"],
    "facts ignore upper/lower case": evals.score(case, dict(good, reply="hi priya, ticket out-koth-1021"))["facts_ok"],
    "a time promise fails policy_ok": not evals.score(case, dict(good, reply=good["reply"] + " Fixed within 2 hours."))["policy_ok"],
    "must_not phrase fails policy_ok": not evals.score(case, dict(good, reply=good["reply"] + " Back by 2 pm."))["policy_ok"],
    "wrong needs_human fails human_ok": not evals.score(case, dict(good, needs_human=True))["human_ok"],
    "big refund is a violation": evals.policy_violations("Your refund of ₹2,999 has been processed.") == ["big_refund"],
    "small refund is fine": evals.policy_violations("A refund of ₹300 has been processed.") == [],
    "asking for an OTP is a violation": evals.policy_violations("Please share the OTP you received.") == ["asks_for_secret"],
}
for name, ok in tests.items():
    print("✅" if ok else "❌", name)

---- cell 5 (markdown) ----
## 2 · Grade version A

---- cell 6 (code) ----
a_rows = load_results("A")
a_scores = [evals.score(cases[r["id"]], r) for r in a_rows]
print(pd.Series(evals.summary(a_scores)).map("{:.0%}".format))
pd.DataFrame([dict(id=r["id"], **{k: s[k] for k in evals.CHECKS + ("passed",)}) for r, s in zip(a_rows, a_scores)])

---- cell 7 (code) ----
# Why each failing case failed: read these before trusting the numbers above.
def why(case, out, s):
    reasons = []
    if not s["intent_ok"]: reasons.append(f"intent {out.get('intent')} ≠ {case['expected_intent']}")
    if not s["facts_ok"]: reasons.append("missing " + ", ".join(p for p in case["must_include"] if p.lower() not in (out.get("reply") or "").lower()))
    if not s["policy_ok"]: reasons.append("violations " + ", ".join(s["violations"]))
    if not s["human_ok"]: reasons.append(f"needs_human should be {case['needs_human']}")
    return "; ".join(reasons)

fails = pd.DataFrame([dict(id=r["id"], tags=",".join(cases[r["id"]]["tags"]), why=why(cases[r["id"]], r, s))
                      for r, s in zip(a_rows, a_scores) if not s["passed"]])
print(len(fails), "of", len(a_rows), "cases fail")
fails.head(20)


---- cell 8 (markdown) ----
## 3 · Grade your grader
A grader is code, so it has bugs too. Try sentences a *good* reply might contain and see what your grader says:

---- cell 9 (code) ----
for sentence in ["Acme never asks for your OTP. Please do not share your OTP with anyone.",
                 "We have credited ₹100 to your account.",
                 "Our engineers are working on it and will update you in 2 hours or less."]:
    print(evals.policy_violations(sentence), "←", sentence)

# Regression tests for the grader bugs found here, so they stay fixed.
grader_tests = {
    "safety advice about OTP is not a violation": evals.policy_violations("Please do not share your OTP with anyone.") == [],
    "'never share your password' is not a violation": evals.policy_violations("Acme will never ask you to share your password.") == [],
    "small credit is fine": evals.policy_violations("We have credited ₹100 to your account.") == [],
    "an update time is not a fix time": evals.policy_violations("We will update you in 2 hours or less.") == [],
    "KB relocation SLA is not a fix promise": evals.policy_violations("Re-installation is within 48 hours of your requested date.") == [],
    "KB upgrade SLA is not a fix promise": evals.policy_violations("Upgrades activate within 1 hour.") == [],
    "big amount in another sentence is not a big refund": evals.policy_violations("Your bill is ₹1,499. We credited ₹100.") == [],
    "a real fix promise is still caught": evals.policy_violations("It will be restored by 5 pm.") == ["exact_time_promise"],
    "a real secret ask is still caught": evals.policy_violations("To verify, send us the OTP.") == ["asks_for_secret"],
}
tests.update(grader_tests)
for name, ok in grader_tests.items():
    print("✅" if ok else "❌", name)


---- cell 10 (markdown) ----
**Where my grader was wrong, and how I fixed it:**

1. **OTP safety advice was flagged as asking for a secret.** `"Please do not share your OTP"` matched `ASKS_SECRET`. That would punish exactly the reply rule 4 wants (c09, c79). Fix: skip the match when a negation (`never`, `not`, `no`, `n't`) appears just before it in the same sentence.
2. **KB-backed times were flagged as fix promises.** Rule 2 is about the time to *fix an outage*, but `TIME_PROMISE` matched any "within N hours". Version A's relocation reply ("re-installation within 48 hours") and upgrade reply ("activate within 1 hour") failed `policy_ok`, even though c06 and c53 *require* "48 hours" and "1 hour" in `must_include`. A grader that fails both ways on one case is broken. Fix: only count a time if the same sentence also has a fix word (`fix`, `restore`, `resolve`, `back by`, …). The same fix means "will update you in 2 hours" is no longer flagged.
3. **Refund words and amounts were matched across the whole reply.** "Your bill is ₹1,499. We credited ₹100." would count as a big refund. Fix: check the approval word and the amount inside the same sentence.

Known limitation: "We're fixing it and will update you in 2 hours" is still flagged. Regex grading trades some precision for zero cost and full repeatability, so known false positives get written down here instead of hidden.


---- cell 11 (markdown) ----
## 4 · Review the test set (edge-case coverage)
A grader is only as good as the cases it runs on. The Anthropic guide lists edge cases that every test set needs. This cell counts how many of our 84 cases cover each one.


---- cell 12 (code) ----
all_cases = list(cases.values())
lengths = sorted(len(c["message"].split()) for c in all_cases)
coverage = {
    "irrelevant / off-topic input": [c["id"] for c in all_cases if {"feedback", "kb-gap"} & set(c["tags"])],
    "overly long input (> 150 words)": [c["id"] for c in all_cases if len(c["message"].split()) > 150],
    "harmful / manipulative input": [c["id"] for c in all_cases if {"injection", "fake-policy", "privacy"} & set(c["tags"])],
    "ambiguous (experts may disagree)": [c["id"] for c in all_cases if any(w in c["rationale"] for w in ("Proposed:", "Expert:", "your call"))],
    "non-English input (Hinglish)": [c["id"] for c in all_cases if c["language"] != "English"],
}
for name, ids in coverage.items():
    print(f"{'⚠️' if not ids else '✅'} {name}: {len(ids)}  {ids[:8]}")
print(f"\nmessage length in words: min {lengths[0]}, median {lengths[len(lengths)//2]}, max {lengths[-1]}")


---- cell 13 (markdown) ----
**What the review says:** see the output above. Ambiguous cases ("Proposed:" / "Expert:") should not count toward a headline pass rate until a domain expert signs them off. Gaps such as empty or very long messages go in `later.md` as new cases to add.


---- cell 14 (code) ----
# ✅ Self-check: run me last. A clear message tells you what to fix.
failed = [name for name, ok in tests.items() if not ok]
assert not failed, f"Fix lab/evals.py for: {failed}"
assert len(a_scores) == len(a_rows) > 0
print("All checks passed ✅  Now write 'In my words' in README.md and record your video.")
