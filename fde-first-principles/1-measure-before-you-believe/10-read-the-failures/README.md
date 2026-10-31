# Day 10 · Read the failures, not the averages

<!-- learn:status -->
**Status:** ⏳ open · morning 1 of 2 · dropped 2026-10-30 · ship by Sun 1 Nov, 05:00 · project 1, step 10
<!-- /learn:status -->

> **First-principles question:** Why does it fail, and which fix matters most?

**Why it matters for an FDE:** Averages tell you that something is wrong. Only failures tell you what to change. You already read failures on day 3 (one system) and day 4 (rules only). Two things are new today: you compare how A, B and C fail differently, and you close the loop by shipping one fix and measuring it.

**Time:** about 105 minutes, over 2 mornings

### The idea: error analysis is an OODA loop
John Boyd's OODA loop (observe, orient, decide, act) is a decision cycle. Error analysis follows the same cycle:

| Step    | What you do today                                                                               | What you have at the end                     |
|---------|-------------------------------------------------------------------------------------------------|----------------------------------------------|
| Observe | Read failures from A, B and C. Write one line on what went wrong.                               | Notes                                        |
| Orient  | Fit each note to a failure mode you already know from day 3. Add a new mode only when none fits. | A category × version table                   |
| Decide  | Pick the one fix that should remove the most failures in the version you would ship.            | A prediction: "this fix removes about N"     |
| Act     | Apply the fix, re-run that version on all 84 cases, score again.                                | Before and after numbers                     |

Then the loop starts again. The re-run is your next Observe.

Your hunch is that the more you observe and orient, the better the replies get. Test it today, with three limits in mind:

- Observing alone changes nothing. A list of failures is a report. Reply quality moves only when you act and then observe again.
- Orientation cuts both ways. The day 3 modes help you see faster, but they can also make every failure look like one you already know. Add a new category when the evidence says so.
- Speed matters. One small fix tested today teaches more than a perfect analysis that never ships.

### 1 · Learn (about 15 minutes)
- [OODA loop (Wikipedia)](https://en.wikipedia.org/wiki/OODA_loop) · 5 min. Read the introduction and 'Criticism'. Note the claim that the loop allows late commitment, unlike plan-do-check-act.
- [Your day 3 failure modes](../03-test-set-first/acme-review-studio/reports/round1-principal-engineer-review.md) · 10 min. Re-read section 2. These are your starting categories.

### 2 · Build (about 70 minutes)
1. Observe: the notebook writes every failed case (A, B, C) into failures.csv. Read at least 20, spread across all three versions, and write a one-line note for each before you pick a category.
2. Orient: give each note a category. Start from the day 3 modes and add new ones (wrong tool, gave up, bad JSON…) only when nothing fits. Find the categories that show up in only one version.
3. Decide: choose one fix for B or C, whichever you would ship. Write down which category it targets and how many failures you expect it to remove.
4. Act: apply the fix (one prompt line or one code change), re-run that version on all 84 cases and compare before and after. Check the cases that used to pass, too.

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Done when
- [ ] At least 20 failures have a note and a category, from all three versions.
- [ ] A category × version table, with at least one category that appears in only one version and an example case id.
- [ ] A written prediction for one fix.
- [ ] Before and after pass counts for that fix, plus every case it broke.

### 3 · Record (5 minutes or less)
- Show the category × version table. Say where the agent fails differently from the single call.
- Read one failure aloud and explain its category.
- Say what you predicted, what happened, and what you will observe on the next loop.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Run a second loop on the next-largest category, or build a tiny HTML page to browse traces._

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
