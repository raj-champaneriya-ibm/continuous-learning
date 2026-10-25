"""Write demo runs so the reports can be previewed with no model and no expert review.

Drafts come from the offline stand-in (rule-based and wrong on purpose). Verdicts are derived from
the automatic checks and marked verdict_source="demo-auto", so every page shows a demo banner.
This file is never evidence of quality.

    python reports/scripts/make_demo_runs.py          # writes reports/demo/reviews.json
    ACME_RUNS=reports/demo/reviews.json quarto render reports
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # acme-review-studio/
sys.path.insert(0, str(ROOT))

from langgraph.checkpoint.memory import InMemorySaver  # noqa: E402

from acme.checks import eval_checks  # noqa: E402
from acme.lab import load_lab  # noqa: E402
from acme.providers import OfflineProvider  # noqa: E402
from acme.store import ReviewStore  # noqa: E402
from acme.workflow import Deps, Workflow, to_record  # noqa: E402

OUT = ROOT / "reports" / "demo" / "reviews.json"


def demo_verdict(case: dict, rec: dict) -> tuple[str, str, str]:
    ev = eval_checks(case, rec)
    high = [f["check"] for f in rec.get("flags", []) if f["severity"] == "high"]
    if ev["routing_ok"] is False and case["needs_human"]:
        return "Fail", "Missed escalation", "Demo: should have gone to a human but was sent."
    if "time promise" in high:
        return "Fail", "Promised fix time", "Demo: the draft promises a fix time."
    if ev["banned"]:
        return "Fail", "Unsupported claim", f"Demo: says {', '.join(ev['banned'])}."
    if ev["missing"]:
        return "Fail", "Missing required fact", f"Demo: missing {', '.join(ev['missing'])}."
    if ev["routing_ok"] is False:
        return "Fail", "Unneeded escalation", "Demo: escalated a case the KB covers."
    return "Pass", "", "Demo: no automatic problems found."


def main():
    lab = load_lab(ROOT / "data" / "Acme_Fibre_Grounded_Draft_Eval.xlsx")
    wf = Workflow(Deps(lab=lab, provider=OfflineProvider()), InMemorySaver())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.unlink(missing_ok=True)
    store = ReviewStore(OUT)
    for i, case in enumerate(lab.cases):
        rec = to_record(wf.start(customer_id=case["customer_id"], message=case["message"], case_id=case["id"],
                                 history=case.get("history")))
        store.save_run(1, case["id"], rec)
        if i % 8 == 7:                       # leave some cases unreviewed, like a real review in progress
            continue
        verdict, mode, critique = demo_verdict(case, rec)
        store.save_review(1, case["id"], verdict=verdict, failure_mode=mode, critique=critique,
                          verdict_source="demo-auto")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(lab.cases)} cases)")


if __name__ == "__main__":
    main()
