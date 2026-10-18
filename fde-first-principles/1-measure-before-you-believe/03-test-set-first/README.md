# Day 3 · Write the test set before the system

<!-- learn:status -->
**Status:** 🕒 late · dropped 2026-10-16 · ship by Sun 18 Oct, 05:00 · shipped 2026-10-18 05:35 · project 1, step 3
<!-- /learn:status -->

> **First-principles question:** How will you know the system works, before you build it?

**Why it matters for an FDE:** Evals are the contract between you and the customer. Writing them first turns 'it feels good' into numbers. Size matters too: on 30 cases a measured 80% could really be anything from 65% to 95%; on 50 cases the range shrinks to about ± 11 points (day 7 shows why).

**Time:** about 145 minutes, over 2 mornings

### 1 · Learn (about 30 minutes)
- [Your AI Product Needs Evals (Hamel Husain)](https://hamel.dev/blog/posts/evals/) · 15 min. Read 'Motivation' and 'Level 1: Unit Tests' (steps 1 to 3). Skim the rest.
- [Rules of Machine Learning (Google): rules 1 to 3](https://developers.google.com/machine-learning/guides/rules-of-ml#before_machine_learning) · 5 min. Three short rules. Notice rule 2: metrics first.

**Maths you need today: Counting and proportions.** A proportion is a count divided by the total. 6 billing cases out of 30 is 6 ÷ 30 = 0.2 = 20%.

### 2 · Build (about 90 minutes)
1. Open data/acme/cases.jsonl. Read the 10 example cases and their fields.
2. Write 10 cases yourself, the hard ones: angry customers, Hinglish, two problems in one email, missing details, a prompt-injection attempt, one that only a human should handle.
3. Let your local model draft 40 more with the notebook's draft cell. Review every draft by hand: fix the facts, delete the unrealistic ones, then set "reviewed" to true.
4. Load and validate every case, then draw a bar chart of cases per intent. Fix every case that fails validation.

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Tool · Acme Review Studio

`acme-review-studio/` is a Shiny app that shows what "capture data and prepare the set" looks like past the notebook: review one case at a time, fix its label (intent, must-include, must-not-say, should-go-to-human), run drafts, judge them, and read the scoreboard — with the Excel workbook as the system of record. It starts on an offline stand-in drafter, so no model calls are needed to click through it.

```bash
cd acme-review-studio && pip install -r requirements.txt && shiny run app.py --launch-browser
```

Shiny serves the app on **http://localhost:8000** (it opens in your browser with
`--launch-browser`). Port busy or want a fixed one? `shiny run app.py --port 8123`,
then open **http://localhost:8123**. Ground truth and SME notes are on the
**Cases** tab: the `ground truth` column in the grid, and the category dropdown plus
Expert note in the editor under it (pick a row first).

See its `README.md` for the expert's loop and `REVIEW.md` for known limits.

### Done when
- [x] data/acme/cases.jsonl has at least 50 cases (100 is better). — 84 cases
- [x] Every drafted case was reviewed by hand: no "reviewed": false is left.
- [x] Every intent has at least 5 cases. — 12 per intent
- [x] Validation passes and the bar chart is shown.
- [x] At least 5 Hinglish cases and 2 prompt-injection cases are tagged. — 14 Hinglish, 6 injection

### Ground truth · 20 SME-reviewed scenarios

For the grader work (task 2), 20 of the 84 cases are pinned as ground truth, marked in the
workbook's Dataset sheet (`Ground truth` column) and reviewed line by line with the domain
expert (`Expert check` = Agree + an `Expert note` each). The other 64 stay unlabeled until
they go through the same review.

| Category | Meaning | Cases |
|---|---|---|
| straightforward | One clear intent, complete facts, KB-covered, no escalation signal | c02, c05, c06, c31, c78 |
| ambiguous | Boundary case: policy gap, CRM contradiction, or a plausible wrong answer | c13, c19, c33, c68, c77 |
| escalation | Auto-acknowledgement fine, but the final action needs a human (E1–E3, E7) | c16, c26, c29, c36, c48 |
| unsafe-to-automate | Any automated reply is itself risky: injection, fraud, safety, third-party | c07, c20, c49, c74, c81 |

All 7 intents, Hinglish and Easy→Hard are covered. In the studio, the Cases grid shows the
`ground truth` column and the case editor has the category dropdown plus the SME note.
Next: the three graders (factual grounding, escalation correctness, response quality) judged
against these 20 before any automated score counts as evidence.

### 3 · Record (5 minutes or less)
- Show 3 tricky cases and say why each one is in the set.
- Show the bar chart. Which intent is tested least?
- Say why you wrote the tests before the system.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Grow the set to 100 cases, then check which intents are still thin._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

## In my words
<!-- Fill these in before you ship (plain, simple English is perfect). Claude can help you turn what you said
     in your video into text, but keep your own words. -->
**For a beginner:** A test set (or eval) is the scenario plus the expected output. But be aware: checking the output needs more than just a plain text comparison.

**For an engineer:** Writing the tests first gives you a crucial input to validate assumptions, system expectations and expected behavior — and it exposes how complex the business rules really are.

**For a customer:** The tests help stakeholders get familiar with the system, set expectations from the system for end users, and define the success criteria.

## What surprised me
…

## How I used AI
- I built the 84 test cases in the Excel workbook (`acme-review-studio/data/Acme_Fibre_Grounded_Draft_Eval.xlsx`) using a Claude Code iterative-critique workflow, then reviewed every case by hand in the workbook's Review_Log (round 1) and fixed labels there.
- Claude Code converted that workbook's Dataset sheet into `data/acme/cases.jsonl` (the format the notebook validates), filled the notebook's two TODO cells (case loader and `problems()` validation), and executed the notebook for me — the self-check now passes.
- Claude Code also patched the notebook's `find_root()` because `progress.json` moved into `.learn/`.
- Claude Code picked the 20 ground-truth cases, tagged them by category (straightforward / ambiguous / escalation / unsafe-to-automate) in the workbook, wrote the SME review notes, and added the `Ground truth` column to the studio's Cases grid and editor. I checked the choices and the notes before accepting them.

## Video
<!-- learn:video -->
[![Watch the video](video/thumbnail.png)](https://youtu.be/9N7xmktXyYg)
<!-- /learn:video -->
