# View of 1-measure-before-you-believe/07-error-bars/notebook.ipynb (markdown and code cells; outputs omitted)

---- cell 1 (markdown) ----
# Day 7 · Why 30 test cases can lie: error bars

**First-principles question:** How big must a difference be before you believe it?

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

import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng(7)

---- cell 3 (markdown) ----
## 1 · Simulate 10,000 test runs
A system that is truly right 80% of the time, tested on 30 cases. Each case is a biased coin flip.

---- cell 4 (code) ----
TRUE_P, N, RUNS = 0.80, 30, 10_000

# `measured` = an array of RUNS accuracies. Each one is the mean of N flips that are
#       'right' with probability TRUE_P.
measured = (rng.random((RUNS, N)) < TRUE_P).mean(axis=1)

plt.hist(measured, bins=np.arange(0.4, 1.02, 1 / N), color="#2153c4", edgecolor="white")
plt.axvline(TRUE_P, color="#c4362c", label="the truth: 80%")
plt.title("The same system, 10,000 different 30-case test sets"); plt.legend(); plt.show()

---- cell 5 (code) ----
# the share of runs that measured 70% or less
share_low = (measured <= 0.70).mean()
print(f"A truly-80% system scores 70% or less on {share_low:.0%} of 30-case test sets")

---- cell 6 (markdown) ----
## 2 · The formula
The spread you just simulated has a formula: the **standard error**.

---- cell 7 (code) ----
def se(p, n):
    """Standard error of an accuracy p measured on n cases."""
    return np.sqrt(p * (1 - p) / n)

print(f"formula: {se(TRUE_P, N):.3f} · simulation: {measured.std():.3f}")

---- cell 8 (markdown) ----
## 3 · Error bars on versions A and B
From your real results (± 2 standard errors ≈ a 95% range).

---- cell 9 (code) ----
from lab.acme import load_cases, load_results
from lab.evals import score
by_id = {c["id"]: c for c in load_cases()}

names, rates, bars = [], [], []
for version in ["A", "B"]:
    rows = load_results(version)
    passed = [score(by_id[r["id"]], r)["passed"] for r in rows]
    p, n = float(np.mean(passed)), len(passed)
    names.append(version); rates.append(p); bars.append(2 * se(p, n))
    print(f"{version}: {p:.0%} ± {2 * se(p, n):.0%} (n = {n})")

plt.bar(names, rates, yerr=bars, capsize=12, color=["#8a9aa1", "#2153c4"])
plt.ylim(0, 1); plt.ylabel("pass rate"); plt.title("Pass rate ± 2 standard errors"); plt.show()

---- cell 10 (markdown) ----
## 4 · How many cases would you need?
Solve 2 × se(p, n) = 0.05 for n.

---- cell 11 (code) ----
# n_needed for ± 5% when p = 0.8
n_needed = 4 * 0.8 * (1 - 0.8) / 0.05 ** 2
print(f"About {n_needed:.0f} cases for ± 5%")

---- cell 12 (markdown) ----
## 5 · What does your own test set buy you?
The same formula for the sizes you might choose. Each extra case helps less than the one before: the range shrinks
with the **square root** of n.

---- cell 13 (code) ----
from lab.acme import load_cases
MY_N = len(load_cases())

# ranges = a dict {n: ± range} for n in [30, 50, 100, MY_N], where ± range = 2 * se(0.8, n)
ranges = {n: 2 * se(0.8, n) for n in [30, 50, 100, MY_N]}

for n, r in ranges.items():
    print(f"{n:>4} cases: a measured 80% means somewhere between {0.8 - r:.0%} and {0.8 + r:.0%}")

---- cell 14 (markdown) ----
**Is B really better than A?** Not proven yet: A scored 18% ± 8% and B 26% ± 10% on the same 84 cases, so the ranges overlap; a paired check on the cases where they disagree (B alone passes 12, A alone passes 4, exact McNemar p ≈ 0.08) points towards B but stays short of the usual 0.05 bar, and part of B's lead comes from being handed the right help articles (oracle context) that A never gets.

---- cell 15 (code) ----
# ✅ Self-check: run me last. A clear message tells you what to fix.
assert measured is not None and len(measured) == RUNS, "Step 1: one accuracy per run"
assert abs(measured.mean() - TRUE_P) < 0.01, "Step 1: the average should be close to 80%"
assert share_low is not None and 0.08 < share_low < 0.2, "Step 1: about 1 in 8 test sets should show 70% or less"
assert abs(se(TRUE_P, N) - measured.std()) < 0.01, "Step 2: se() should match the simulated spread"
assert n_needed is not None and 230 < n_needed < 280, "Step 4: about 256 cases"
assert ranges is not None and abs(ranges[50] - 0.113) < 0.002, "Step 5: ± range for 50 cases is about 11%"
assert ranges[100] < ranges[50] < ranges[30], "Step 5: more cases, smaller range"
print("All checks passed ✅  Now write 'In my words' in README.md and record your video.")
