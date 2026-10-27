# Day 7 · Why 30 test cases can lie: error bars

<!-- learn:status -->
**Status:** ⏳ open · attempt 3 · dropped 2026-10-28 · ship by Thu 29 Oct, 05:00 · project 1, step 7
<!-- /learn:status -->

> **First-principles question:** How big must a difference be before you believe it?

**Why it matters for an FDE:** Customers will ask 'is the new version better?'. With small test sets the honest answer is often 'we can't tell yet'.

**Time:** about 140 minutes, over 2 mornings

### 1 · Learn (about 30 minutes)
- [A statistical approach to model evaluations (Anthropic)](https://www.anthropic.com/research/statistical-approach-to-model-evals) · 10 min. Read the introduction and Recommendation #1 only. Don't worry about the formulas: today's notebook builds them by simulation.
- [Seeing Theory: Basic probability (Brown University)](https://seeing-theory.brown.edu/basic-probability/) · 10 min. Play with the coin flips. How often do 10 fair flips give 7 or more heads?
- [Seeing Theory: Frequentist inference (Brown University)](https://seeing-theory.brown.edu/frequentist-inference/) · 10 min. The error-bar chapter: each sample gives a different estimate (the dartboard), and a confidence interval is the honest range around your guess. Local visual notes: `seeing-theory/04-frequentist-inference.drawio` — see "Point Estimation" (dartboard: bias vs scatter, scatter shrinks like 1/√n) and "Confidence Intervals" (estimate ± margin, the ring that catches the truth 19 times in 20).

**Maths you need today: Standard error and a 95% range.** If a system is right with probability p, a test of n cases wobbles by about √(p × (1 − p) ÷ n). About 95% of the time the truth is within 2 wobbles of what you measured.

### 2 · Build (about 85 minutes)
1. Simulate a system that is truly 80% right, tested on 30 cases, 10,000 times. Plot the measured accuracies.
2. From the simulation: how often does a 30-case test show 70% or less?
3. Write se(p, n). Check that it matches the spread you simulated.
4. Draw A and B with ± 2 × se error bars. Do they overlap?
5. Work out the ± range for 30, 50 and 100 cases and for your own test set. How much does each extra case buy?
6. How many cases would you need for ± 5%?

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Done when
- [ ] Histogram of 10,000 simulated test results.
- [ ] se() matches the simulation.
- [ ] Bar chart of A and B with error bars.
- [ ] The ± range for 30, 50, 100 and your own test set.
- [ ] One sentence: is B really better than A?

### 3 · Record (5 minutes or less)
- Explain the histogram like a weather forecast.
- Show A and B with error bars.
- Say how many test cases you would ask the customer for, and why.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Read Recommendation #4 (paired differences) and try it on A and B._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

## In my words
We tested the assistant on 30 real customer cases and it got 80% right. With only 30 cases, that number is like a restaurant rating from five reviews. The real performance could be anywhere from about 65% to 95%.

To narrow it to 75–85%, we need about 250 test cases. That lets us make go/no-go and 'is the new version better?' decisions with confidence.

Until then, if version B scores a few points higher than version A, treat it as a hint, not proof. 

**For a beginner:** Testing an AI on a few cases is like flipping a coin 10 times: a fair coin can still land heads 7 times. A score from a small test set is a rough guess, and more cases make the guess sharper.

**For an engineer:** Accuracy measured on n cases has a standard error of √(p(1−p)/n), and the 95% range is ±2 SE: ±15% at 30 cases, ±9% for our 84 cases, and about 256 cases for ±5%. Only call B better than A when the gap is bigger than the error bars, and remember that halving the range costs 4× the cases.

**For a customer:** Our 80% score on 30 cases is like a restaurant rating from five reviews: the real figure could be anywhere from 65% to 95%. With around 250 real cases we can tell you, within ±5%, whether the new version is actually better before you pay to roll it out.

## What surprised me
…

## How I used AI
…

## Video
<!-- learn:video -->
_Added when you ship._
<!-- /learn:video -->
