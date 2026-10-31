# Day 10 · Read the failures, not the averages

<!-- learn:status -->
**Status:** ⏳ open · morning 1 of 2 · dropped 2026-10-30 · ship by Sun 1 Nov, 05:00 · project 1, step 10
<!-- /learn:status -->

> **First-principles question:** Why does it fail, and which fix matters most?

**Why it matters for an FDE:** Averages tell you that something is wrong. Only failures tell you what to change. You already read failures on day 3 (one system) and day 4 (rules only). Two things are new today: you compare how A, B and C fail differently, and you close the loop by shipping one fix and measuring it.

**Time:** about 105 minutes, over 2 mornings

### The idea: error analysis is an OODA loop
John Boyd's OODA loop (observe, orient, decide, act) is a decision cycle. Error analysis follows the same cycle:

| Step    | What you do today                                                                                         | What you have at the end                     |
|---------|-----------------------------------------------------------------------------------------------------------|----------------------------------------------|
| Observe | Read the safety scoreboard, then failures from A, B and C. Write one line on what went wrong.             | Notes, and how often the grader was wrong    |
| Orient  | Fit each note to a failure mode you already know from day 3. Add a new mode only when none fits.          | A category × version table                   |
| Decide  | Pick the one fix that should remove the most failures in the version you would ship.                     | A prediction: "this fix removes about N"     |
| Act     | Apply the fix, re-run on the tuning cases, then confirm once on held-out cases you never read.            | Before and after numbers, with provenance    |

Then the loop starts again. The re-run is your next Observe.

Your hunch is that the more you observe and orient, the better the replies get. Test it today, with four limits in mind:

- Observing alone changes nothing. A list of failures is a report. Reply quality moves only when you act and then observe again.
- Orientation cuts both ways. The day 3 modes help you see faster, but they can also make every failure look like one you already know. Add a new category when the evidence says so.
- What you observe through can be wrong. The grader is an instrument: check it before you trust what it tells you to fix.
- Speed matters. One small fix tested today teaches more than a perfect analysis that never ships.

### Before you start: three things the day 9 numbers hide
- Safety, not the pass rate, decides what ships. Of the 40 cases that need a human, A escalates 0, B escalates 2 and C escalates 23. The grader now reports `safe` (no policy break and no missed escalation) and `human_rate` (the share of emails handed to a person) next to `passed`.
- The comparison favours B. B is handed the help articles for the *expected* intent (oracle context); C has to search for them. Part of B's lead is the answer key.
- The grader has known false alarms. The mutation tests in `tests/test_grader_mutations.py` show it fails a correct reply that writes "5-7 working days" or "Rs. 100". Some of your failures are the grader's, not the model's.

### 1 · Learn (about 15 minutes)
- [OODA loop (Wikipedia)](https://en.wikipedia.org/wiki/OODA_loop) · 5 min. Read the introduction and 'Criticism'. Note the claim that the loop allows late commitment, unlike plan-do-check-act.
- [Your day 3 failure modes](../03-test-set-first/acme-review-studio/reports/round1-principal-engineer-review.md) · 10 min. Re-read section 2. These are your starting categories.

### 2 · Build (about 70 minutes)
1. Split: the notebook puts 24 cases aside as a held-out set (same share of escalation cases as the rest). You never read their failures; they only answer "did the fix work on cases I did not tune on?"
2. Observe: read the safety scoreboard (safe, missed escalations, human intervention, passed) for A, B and C. Then read at least 20 failures from the tuning cases, spread across all three versions. For each, first decide whether the grader was right. Write a one-line note before you pick a category.
3. Orient: give each note a category. Start from the day 3 modes, use `grader wrong` when the reply was fine, and add new ones (wrong tool, gave up, bad JSON…) only when nothing fits. Find the categories that show up in only one version.
4. Decide: choose one fix for B or C. Day 9 points at routing: missed escalations block every version. Write down which category it targets and how many tuning failures you expect it to remove.
5. Act: apply the fix (one prompt line or one code change) and re-run that version. Compare before and after on the tuning cases, including the ones that used to pass. Then read the held-out result once. The run is saved with its model, prompt fingerprint and settings.

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Done when
- [ ] The safety scoreboard for A, B and C is shown.
- [ ] At least 20 tuning failures have a note and a category, from all three versions, and you know what share of them were `grader wrong`.
- [ ] A category × version table, with at least one category that appears in only one version and an example case id.
- [ ] A written prediction for one fix.
- [ ] Before and after numbers for that fix on the tuning cases (plus every case it broke) and on the held-out cases.
- [ ] The re-run has a `.meta.json` file in `data/results/` recording the model and prompt fingerprint.

### 3 · Record (5 minutes or less)
- Walk through one turn of the loop: what you observed, how you oriented, what you decided, what happened when you acted.
- Show the category × version table. Say where the agent fails differently from the single call, and why the comparison favours B.
- Say how often the grader was wrong, and read one failure aloud with its category.
- Say what you predicted, what the held-out cases showed, and what you will observe on the next loop.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Run a second loop on the next-largest category, repeat the run on another local model with tool-call support (`llm.use(...)`), or build a tiny HTML page to browse traces._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

## In my words
<!-- Fill these in before you ship (plain, simple English is perfect). Claude can help you turn what you said
     in your video into text, but keep your own words. -->
**For a beginner:** …

**For an engineer:** …

**For a customer:** …

## What surprised me
…

## How I used AI
…

## Video
<!-- learn:video -->
_Added when you ship._
<!-- /learn:video -->
