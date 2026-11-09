# View of 1-measure-before-you-believe/11-recommendation-first-draft/notebook.ipynb (markdown and code cells; outputs omitted)

---- cell 1 (markdown) ----
# Day 11 · The recommendation, first draft (an ADR)

**First-principles question:** What would you tell the customer to build, and what would change your mind?

This notebook only gathers evidence. It rebuilds one table from the saved runs in `data/results/`, so every number
in `decision.md` (and in day 12's article) traces back to a run with its model and prompt fingerprint.
The real work today is `decision.md` and the diagram. Run top to bottom with **Shift + Enter**, copy the table
into `decision.md`, and finish with the **✅ self-check** cell.

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

import math
import re
import pandas as pd
from lab.acme import RESULTS, load_cases, load_meta, load_results
from lab.evals import score, summary

cases = {c["id"]: c for c in load_cases()}
PROJECT = ROOT / "1-measure-before-you-believe"
HERE = PROJECT / "11-recommendation-first-draft"
FAILURES = PROJECT / "10-read-the-failures" / "failures.csv"
VERSIONS = [v for v in ["A", "B", "C", "B2", "C2"] if (RESULTS / f"{v}.jsonl").exists()]
print("saved runs:", VERSIONS)

---- cell 3 (markdown) ----
## 1 · The evidence table
Same formulas as day 9 (nearest-rank percentiles, the same prices), plus the day 10 safety columns.
`± 2 se` is the 95% range from day 7. `B2` or `C2` shows up once you have run day 10 step 6.
Remember while reading B: its context is the oracle, not a search.

---- cell 4 (code) ----
# Same prices as day 9, so the ₹ column matches that table
PRICE_IN_USD, PRICE_OUT_USD, INR_PER_USD = 0.02, 0.01, 82.0

def percentile(values, q):
    values = sorted(values)
    return values[max(1, math.ceil(q / 100 * len(values))) - 1]

def two_se(p, n):
    return 2 * math.sqrt(p * (1 - p) / n)

def evidence(version):
    rows = load_results(version)
    scores = [score(cases[r["id"]], r) for r in rows]
    s, n = summary(scores), len(scores)
    secs = [r.get("seconds", 0) for r in rows]
    inr = [(r.get("tokens_in", 0) * PRICE_IN_USD + r.get("tokens_out", 0) * PRICE_OUT_USD) / 1e6 * INR_PER_USD
           for r in rows]
    return {"version": version, "model": (load_meta(version) or {}).get("model"),
            "pass rate": s["passed"], "pass ± 2 se": two_se(s["passed"], n),
            "safe": s["safe"], "safe ± 2 se": two_se(s["safe"], n),
            "missed escalations": sum(x["human_expected"] and not x["human_flagged"] for x in scores),
            "human rate": s["human_rate"],
            "median s": percentile(secs, 50), "p95 s": percentile(secs, 95),
            "₹ per 1,000 emails": 1000 * sum(inr) / n}

evidence_table = pd.DataFrame([evidence(v) for v in VERSIONS]).set_index("version")
evidence_table.round(2)

---- cell 5 (markdown) ----
## 2 · Top failure category per version (from day 10)
The category you labelled most often in `failures.csv`. Re-run day 10 if this cell says the file is missing.

---- cell 6 (code) ----
if FAILURES.exists():
    labelled = pd.read_csv(FAILURES).fillna("")
    labelled = labelled[labelled.category != ""]
    evidence_table["top failure category"] = labelled.groupby("version").category.agg(
        lambda c: c.value_counts().idxmax())
else:
    print("No failures.csv yet: finish day 10 step 4 first")
evidence_table.round(2)

---- cell 7 (markdown) ----
## 3 · Copy it into decision.md
Paste the printed table over the empty one in `decision.md`. Keep the rows you will talk about.

---- cell 8 (code) ----
print("| | Pass rate (± 2 se) | Safe (± 2 se) | Missed escalations | Median s | p95 s | ₹ per 1,000 emails "
      "| Top failure category |")
print("|---|---|---|---|---|---|---|---|")
for v, r in evidence_table.iterrows():
    top = r.get("top failure category")
    print(f"| {v} | {r['pass rate']:.0%} ± {r['pass ± 2 se']:.0%} | {r['safe']:.0%} ± {r['safe ± 2 se']:.0%} "
          f"| {r['missed escalations']} of {sum(c['needs_human'] for c in cases.values())} "
          f"| {r['median s']:.1f} | {r['p95 s']:.1f} | {r['₹ per 1,000 emails']:.2f} "
          f"| {top if isinstance(top, str) else ''} |")

---- cell 9 (code) ----
# ✅ Self-check: run me last. A clear message tells you what to fix.
adr = (HERE / "decision.md").read_text(encoding="utf-8")
sections = ["## Context", "## Options", "## Evidence", "## Decision", "## Consequences",
            "## What would change my mind", "## Open questions"]
missing = [s for s in sections if s not in adr]
assert not missing, f"decision.md lost these sections: {missing}"
assert "…" not in adr, "decision.md: replace every … with your own words"
assert "±" in adr, "decision.md: the evidence table needs error bars (± 2 se)"
questions = re.findall(r"^\d+\.\s+\S", adr.split("## Open questions", 1)[1], re.M)
assert len(questions) >= 3, f"List at least 3 open questions ({len(questions)} so far)"
assert len(adr.split()) <= 700, f"decision.md should fit on one page: {len(adr.split())} words, aim for 700 or fewer"
assert [p for p in HERE.iterdir() if p.suffix in (".svg", ".png")], \
    "Save the design diagram in this folder as .svg or .png (for example diagram.drawio.svg)"
print("All checks passed ✅  Now write 'In my words' in README.md and record your readout.")
