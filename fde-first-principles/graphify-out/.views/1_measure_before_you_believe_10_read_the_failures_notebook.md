# View of 1-measure-before-you-believe/10-read-the-failures/notebook.ipynb (markdown and code cells; outputs omitted)

---- cell 1 (markdown) ----
# Day 10 · Read the failures, not the averages

**First-principles question:** Why does it fail, and which fix matters most?

Today is one turn of an OODA loop: **Observe** the safety scoreboard and the failures, **Orient** them against the
day 3 failure modes, **Decide** on one fix, **Act** by re-running and scoring again. You tune on 60 cases and keep
24 held-out cases you never read, so the last step can tell you whether the fix works beyond the cases you studied.

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

import csv
import random
import pandas as pd
import matplotlib.pyplot as plt
from lab.acme import load_cases, load_meta, load_results
from lab.evals import CHECKS, score, summary

cases = {c["id"]: c for c in load_cases()}
FAILURES = ROOT / "1-measure-before-you-believe" / "10-read-the-failures" / "failures.csv"    # in this folder

# Hold out 24 cases with the same share of escalation cases as the whole set. Fixed seed: same split every run.
rng = random.Random(10)
HELD_OUT = set()
for needs_human in (True, False):
    ids = sorted(c for c, case in cases.items() if case["needs_human"] == needs_human)
    HELD_OUT |= set(rng.sample(ids, round(len(ids) * 24 / len(cases))))
TUNING = [c for c in cases if c not in HELD_OUT]
print(f"{len(TUNING)} tuning cases, {len(HELD_OUT)} held-out cases")

---- cell 3 (markdown) ----
## 1 · Observe: the safety scoreboard first
`passed` treats a missing first name and a missed escalation the same. Ship decisions do not:
- **safe**: no policy break and no missed escalation (the ship blockers)
- **human intervention**: share of emails handed to a person, the work automation does not remove
- **passed**: every check, quality included

The `model` column comes from each run's `.meta.json`. Runs saved before day 10 were backfilled, so read their notes.

---- cell 4 (code) ----
def scoreboard(version, ids):
    out = {r["id"]: r for r in load_results(version)}
    scores = [score(cases[i], out[i]) for i in ids]
    s = summary(scores)
    return {"safe": s["safe"],
            "missed escalations": sum(x["human_expected"] and not x["human_flagged"] for x in scores),
            "policy breaks": sum(not x["policy_ok"] for x in scores),
            "human intervention": s["human_rate"],
            "escalation recall": s["escalation_recall"],
            "passed": s["passed"]}

board = pd.DataFrame({v: scoreboard(v, cases) for v in "ABC"}).T.astype({"missed escalations": int, "policy breaks": int})
board["model"] = [(load_meta(v) or {}).get("model") for v in board.index]
board.round(2)

---- cell 5 (markdown) ----
### 1b · Observe one email at a time, not one version at a time
Every chart so far had one dot per version. This one has one dot per email: version C's steps against its
seconds, coloured by pass or fail (tuning cases only). Steps are whole numbers, so the dots are nudged sideways
to stop them hiding each other.

**TODO:** one sentence: do the failures cluster somewhere, or are they spread evenly? What would you look at next?

---- cell 6 (code) ----
c_points = pd.DataFrame([{"steps": r["steps"], "seconds": r["seconds"],
                          "passed": score(cases[r["id"]], r)["passed"]}
                         for r in load_results("C") if r["id"] not in HELD_OUT])
jitter = random.Random(0)
c_points["x"] = c_points.steps + [jitter.uniform(-0.2, 0.2) for _ in range(len(c_points))]

fig, ax = plt.subplots(figsize=(7, 4))
for passed, colour, label in [(True, "#2563EB", "pass"), (False, "#F97316", "fail")]:
    group = c_points[c_points.passed == passed]
    ax.scatter(group.x, group.seconds, c=colour, alpha=0.7, label=f"{label} ({len(group)})")
ax.set(xlabel="agent steps", ylabel="seconds", title="Version C, one dot per email (tuning cases)")
ax.legend(); plt.show()

---- cell 7 (markdown) ----
## 2 · Observe: collect the tuning failures into a spreadsheet
Only the 60 tuning cases go into `failures.csv`. The held-out failures stay unread until step 6.

---- cell 8 (code) ----
rows = []
for version in ["A", "B", "C"]:
    for r in load_results(version):
        if r["id"] in HELD_OUT:
            continue
        s = score(cases[r["id"]], r)
        if not s["passed"]:
            failed = [k for k in CHECKS if not s[k]]
            rows.append({"key": f"{r['id']}:{version}", "case": r["id"], "version": version,
                         "safe": s["safe"], "failed_checks": " ".join(failed),
                         "violations": " ".join(s["violations"]), "note": "", "category": ""})

if FAILURES.exists():   # keep the notes you already wrote
    old = {r["key"]: r for r in csv.DictReader(FAILURES.open(encoding="utf-8"))}
    for r in rows:
        r["note"], r["category"] = old.get(r["key"], {}).get("note", ""), old.get(r["key"], {}).get("category", "")
with FAILURES.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)
print(len(rows), "tuning failures written to", FAILURES.resolve())

---- cell 9 (markdown) ----
## 3 · Observe: read one failure at a time
**TODO:** read at least 20 failures, spread across A, B and C. For each one, ask first: *was the grader right?*
The mutation tests show it fails correct replies that write "5-7" or "Rs." instead of "5 to 7" or "₹".
Then write a one-line **note** in `failures.csv` (VS Code or Numbers) saying what went wrong in your own words.
Leave **category** empty for now. Re-run step 2 any time: your notes are kept.

Remember while reading B: it was handed the help articles for the *expected* intent, which C had to search for.

---- cell 10 (code) ----
def show(key):
    case_id, version = key.split(":")
    case = cases[case_id]
    out = next(r for r in load_results(version) if r["id"] == case_id)
    print(f"── {key} · expected {case['expected_intent']} · must include {case['must_include']} · "
          f"needs_human {case['needs_human']}")
    print("EMAIL:", case["message"])
    print(f"OUTPUT: intent={out.get('intent')} needs_human={out.get('needs_human')}\n{out.get('reply')}")
    print("CHECKS:", score(case, out))

show(rows[0]["key"])

---- cell 11 (markdown) ----
## 4 · Orient: fit each note to a failure mode
**TODO:** fill in the **category** column. Start from your day 3 modes (unsupported-amount false positive,
over-escalation on an answerable case, unapproved offer), plus **missed escalation**. Use **grader wrong** when the
reply was fine. Add a new category (wrong tool, gave up, bad JSON…) only when no existing one fits the note.

---- cell 12 (code) ----
notes = pd.read_csv(FAILURES).fillna("")
labelled = notes[(notes.note != "") & (notes.category != "")]

# Where the architectures differ: categories seen in exactly one version
by_version = pd.crosstab(labelled.category, labelled.version)
only_one = by_version[(by_version > 0).sum(axis=1) == 1]

if len(labelled):
    pivot = pd.crosstab(labelled.category, labelled.version, margins=True)
    pivot.drop(index="All", errors="ignore").drop(columns="All", errors="ignore").plot.barh(
        stacked=True, figsize=(7, 3), title="Failures by category")
    plt.show()
    grader_wrong = (labelled.category == "grader wrong").mean()
    print(f"The grader was wrong on {grader_wrong:.0%} of the {len(labelled)} failures you read")
    for category in only_one.index:
        example = labelled[labelled.category == category].iloc[0]
        print(f"only in {example.version}: {category} (e.g. {example.case})")
    pivot
else:
    print("No labelled failures yet: fill in note and category in failures.csv, then re-run")

---- cell 13 (markdown) ----
## 5 · Decide: one fix, with a prediction
**TODO:** pick B or C and the single fix that should remove the most tuning failures. Day 9 points at routing:
missed escalations block every version. Write the prediction in the next cell **before** you change anything,
so the result can prove you wrong.

---- cell 14 (code) ----
# My decision: swap the small local model for a stronger one behind C's agent loop (a code-change fix, so FIX stays empty)
FIX_VERSION = "C"        # "B" or "C"
FIX_CATEGORY = "gave up"  # the category from step 4 that the fix targets
PREDICTED_REMOVED = 13   # 13 of C's 49 tuning failures are empty "gave up" replies; a stronger model should answer them
FIX = ""                 # the one instruction line you will add to that version's system prompt

---- cell 15 (markdown) ----
## 6 · Act: apply the fix, re-run, score again
The next cell adds `FIX` to the version's prompt, re-runs all 84 cases with the same model setup as day 9,
and saves the outputs as `B2` or `C2` together with `B2.meta.json` or `C2.meta.json`: model, prompt fingerprint,
settings, the fix and the held-out ids. If your fix is a code change in `lab/` instead, leave `FIX` empty:
the cell reloads `lab/` first.

Judge the fix on the **tuning** cases, including the ones that used to pass: a fix that breaks them is a regression.
Then read the **held-out** row once. With only 24 cases its error bars are about ± 20%, so it is a sanity check:
a fix that helps on tuning but not on held-out was probably tuned to the cases you read.
Afterwards, `show("c12:B2")` opens a re-run case in the viewer. That is your next Observe.

---- cell 16 (code) ----
import importlib
import lab.agent, lab.version_b
from lab import llm
from lab.acme import fingerprint, save_results
from lab.llm import current_model

assert FIX_VERSION in ("B", "C"), "Fill in your decision in step 5 first"

# Reload so re-running this cell never stacks the fix twice (llm first: agent imports chat from it)
importlib.reload(lab.llm)
vb = importlib.reload(lab.version_b)
ag = importlib.reload(lab.agent)

# The fix: a stronger model behind the same agent loop (LLM_ANTHROPIC_BASE + key live in .env)
llm.use("anthropic:glm-5.3-flash")

if FIX and FIX_VERSION == "B":
    vb.SYSTEM += "\n" + FIX
elif FIX:
    ag.SYSTEM_C += "\n" + FIX

def run(case):
    if FIX_VERSION == "B":
        return vb.version_b(case)
    output, trace = ag.run_agent(case)
    return {**output, "steps": len(trace)}

new_rows = [{**run(case), "id": cid} for cid, case in cases.items()]
NEW = f"{FIX_VERSION}2"
save_results(NEW, new_rows, meta={
    "model": current_model(), "temperature": 0.0,
    "prompt_sha": fingerprint(vb.SYSTEM if FIX_VERSION == "B" else ag.SYSTEM_C),
    "context": "oracle" if FIX_VERSION == "B" else "retrieved",
    "base": FIX_VERSION, "fix": FIX, "fix_category": FIX_CATEGORY, "held_out": sorted(HELD_OUT)})

def passed(version):
    return {r["id"]: score(cases[r["id"]], r)["passed"] for r in load_results(version)}

before, after = passed(FIX_VERSION), passed(NEW)
fixed = [c for c in TUNING if after[c] and not before[c]]
broke = [c for c in TUNING if before[c] and not after[c]]
print(f"Tuning: fixed {len(fixed)} (you predicted {PREDICTED_REMOVED}):", fixed)
print(f"Tuning: broke {len(broke)}:", broke)

pd.DataFrame({("tuning", FIX_VERSION): scoreboard(FIX_VERSION, TUNING), ("tuning", NEW): scoreboard(NEW, TUNING),
              ("held-out", FIX_VERSION): scoreboard(FIX_VERSION, HELD_OUT),
              ("held-out", NEW): scoreboard(NEW, HELD_OUT)}).round(2)

---- cell 17 (code) ----
# ✅ Self-check: run me last. A clear message tells you what to fix.
assert len(board) == 3 and "safe" in board, "Step 1: show the safety scoreboard for A, B and C"
assert len(labelled) >= 20, f"Label at least 20 failures (note + category): {len(labelled)} so far"
assert not set(labelled.case) & HELD_OUT, "Held-out cases must stay unread: re-run step 2"
missing = {"A", "B", "C"} - set(labelled.version)
assert not missing, f"Label failures from every version (none yet from {', '.join(sorted(missing))})"
assert len(only_one) >= 1, "Find at least one category that appears in only one version"
assert FIX_CATEGORY in set(labelled.category), "FIX_CATEGORY must be one of your categories from step 4"
assert PREDICTED_REMOVED > 0, "Write your prediction in step 5 before acting"
meta = load_meta(f"{FIX_VERSION}2") or {}
assert meta.get("model") and meta.get("prompt_sha"), "Step 6: re-run and save with its model and prompt fingerprint"
print("All checks passed ✅  Now write 'In my words' in README.md and record your video.")
