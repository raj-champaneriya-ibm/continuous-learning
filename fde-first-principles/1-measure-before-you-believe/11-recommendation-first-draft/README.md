# Day 11 · The recommendation, first draft (an ADR)

<!-- learn:status -->
**Status:** not dropped yet · project 1, step 11
<!-- /learn:status -->

> **First-principles question:** What would you tell the customer to build, and what would change your mind?

**Why it matters for an FDE:** FDEs are trusted when advice is backed by evidence and honest about uncertainty. An architecture decision record (ADR) makes both visible.

**Time:** about 85 minutes, over 1 morning

### Before you start: what your evidence already says
- Ship day 10 first. The ADR's "top failure category" column and your fix's before and after numbers come from it.
- The day 9 pass rates overlap: A 19% ± 9%, B 29% ± 10%, C 20% ± 9%. The pass rate alone cannot pick a winner.
- Safety can. Of the 40 cases that need a human, A escalates 0, B escalates 2 and C escalates 23. Add `safe` and `missed escalations` columns to the evidence table: they are the ship blockers.
- B's numbers use oracle context (the help articles for the *expected* intent). A production B has to search for them, which project 2 measures. Say this under Consequences.
- Every run so far used one small local model (`qwen3:4b`, temperature 0). That is the scope of your evidence, and project 6 re-runs it on a stronger model.
- A decision with conditions is still a decision. Say what you would build and which numbers must hold before it goes live.

### 1 · Learn (about 15 minutes)
- [Documenting Architecture Decisions (Michael Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · 10 min. Short. Use its parts: Context, Decision, Status, Consequences.

### 2 · Build (about 45 minutes)
1. Run `notebook.ipynb` in this folder. It rebuilds the evidence table from the saved runs in `data/results/` (A, B, C, plus B2 or C2 from day 10) and prints it as a markdown table.
2. Fill in decision.md (one page): context, options A/B/C, the evidence table with error bars, decision, consequences, risks, 'what would change my mind'.
3. Draw the chosen design in draw.io or Excalidraw: email in → steps → model calls → human check → reply out. Save it in this folder as `diagram.drawio.svg` (or any `.svg` or `.png`).
4. List the open questions projects 2 to 6 will answer.

Your starter is `decision.md` in this folder. `notebook.ipynb` gathers the numbers; run its ✅ self-check at the end.

### Done when
- [ ] decision.md fits on one page and every section is filled.
- [ ] The evidence has error bars.
- [ ] A diagram of the chosen design.
- [ ] At least 3 open questions.

### 3 · Record (5 minutes or less)
- Give a 5-minute readout to an imaginary CTO, using the diagram, not the notebook.
- End with what you will test next.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Turn the readout into a one-slide summary._

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
