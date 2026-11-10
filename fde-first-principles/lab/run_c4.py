"""Run Version C4 against every Acme test set (base, abuse, multiturn, regional: 256 cases).

Usage, from fde-first-principles/:

    uv run python -m lab.run_c4                # full run, saved as C4-glm53flash
    uv run python -m lab.run_c4 --limit 3      # smoke test
    uv run python -m lab.run_c4 --only c01     # single case, any file

Every case is scored with lab.evals.score and the run is saved with provenance
(model, files, counts) via lab.acme.save_results. The chat cache makes a re-run free.
"""
from __future__ import annotations

import argparse
import json
import time

from .acme import DATA, load_cases, save_results
from .evals import score, summary
from .llm import api_usage, use
from .version_c4 import version_c4

MODEL = "anthropic:glm-5.3-flash"
CASE_FILES = ["cases.jsonl", "cases_abuse.jsonl", "cases_multiturn.jsonl", "cases_regional.jsonl"]
VERSION = "C4-glm53flash"


def all_cases() -> list[dict]:
    out = []
    for name in CASE_FILES:
        for case in load_cases(DATA / name):
            out.append({**case, "source_file": name})
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="run only the first N cases")
    ap.add_argument("--only", type=str, default=None, help="run one case id and print the reply")
    ap.add_argument("--version", type=str, default=VERSION, help="results file name")
    args = ap.parse_args()

    cases = all_cases()
    if args.only:
        cases = [c for c in cases if c["id"] == args.only]
    elif args.limit:
        cases = cases[: args.limit]

    use(MODEL)
    rows: list[dict] = []
    started = time.time()
    for i, case in enumerate(cases, 1):
        t0 = time.time()
        row = version_c4(case, temperature=0.0, run=0)
        s = score(case, row)
        rows.append({"case": case["id"], "source_file": case["source_file"],
                     "customer_id": case["customer_id"], **row})
        print(f"[{i}/{len(cases)}] {case['id']} ({case['source_file']}) "
              f"{'PASS' if s['passed'] else 'FAIL ' + ','.join(k for k in ('intent_ok','facts_ok','policy_ok','human_ok') if not s[k])}"
              f" {row['seconds']:.0f}s", flush=True)
        if args.only:
            print(json.dumps({k: row.get(k) for k in ("intent", "reply", "needs_human",
                                                      "escalation_sources")}, indent=2,
                             ensure_ascii=False))

    scores = [score(next(c for c in cases if c["id"] == r["case"]), r) for r in rows]
    print("\n== overall ==", flush=True)
    print(json.dumps(summary(scores), indent=1, default=str))
    for name in CASE_FILES:
        part = [s for s, r in zip(scores, rows) if r["source_file"] == name]
        if part:
            print(f"\n== {name} (n={len(part)}) ==")
            print(json.dumps(summary(part), indent=1, default=str))

    path = save_results(args.version, rows, meta={
        "model": MODEL, "temperature": 0.0, "files": CASE_FILES,
        "n_total": len(rows), "wall_seconds": round(time.time() - started, 1),
        "api_usage": api_usage(),
    })
    print(f"\nsaved {len(rows)} rows -> {path}")


if __name__ == "__main__":
    main()
