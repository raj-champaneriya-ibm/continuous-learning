# Day 9 · Run all three: success, cost, latency

<!-- learn:status -->
**Status:** ✅ shipped · dropped 2026-10-29 · ship by Sat 31 Oct, 05:00 · shipped 2026-10-31 04:33 · project 1, step 9
<!-- /learn:status -->

> **First-principles question:** Is the extra intelligence worth its price and its wait?

**Why it matters for an FDE:** Every architecture choice trades quality, cost and speed. Customers decide with a table, not a demo.

**Time:** about 120 minutes, over 2 mornings

### Set up
- Move your code into lab/: version B (day 6) into lab/version_b.py and the agent loop (day 8) into lab/agent.py. Keep the signatures written at the top of each file.

### 1 · Learn (about 25 minutes)
- [Your AI Product Needs Evals: 'Logging Traces' and 'Looking At Your Traces'](https://hamel.dev/blog/posts/evals/) · 10 min. Why you keep every input, output, token count and time.
- [Building effective agents: 'When (and when not) to use agents'](https://www.anthropic.com/engineering/building-effective-agents) · 5 min. Re-read it with your numbers in mind.

**Maths you need today: Mean, median and 95th percentile.** The mean is pulled up by a few slow calls. The median is the middle call. p95 is the time that 95% of calls beat: the number users feel on a bad day.

### 2 · Build (about 70 minutes)
1. Run version C on every case (cached). Collect tokens and seconds for A, B and C (A uses 0 tokens).
2. Write percentile(values, q) by sorting, and check it against numpy.
3. Look up one paid model's price per million input and output tokens and fill in the prices.
4. One table: pass rate ± 2 se, median and p95 seconds, tokens per email, cost per 1,000 emails, cost per correct reply. Two charts: pass rate vs cost, pass rate vs p95.

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Done when
- [ ] One table with 3 rows (A, B, C) and all the columns.
- [ ] Two charts.
- [ ] One paragraph: which version would you ship today, and what would change your mind?

### 3 · Record (5 minutes or less)
- Walk through the table row by row.
- Say which version you would ship and why.
- Say what the cheapest version is missing.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Run the same table on a paid API with a hard monthly spending cap._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

## In my words
<!-- Fill these in before you ship (plain, simple English is perfect). Claude can help you turn what you said
     in your video into text, but keep your own words. -->
**For a beginner:** Every new feature adds cost and latency. Choosing which ones you are fine to live with — balancing time, cost and reply quality — is more of an art than a science.

**For an engineer:** My job is to recommend with evidence, not to hand the client a table. Today the evidence says none of the three ships: A and B miss almost every escalation, and C escalates but is slow and still fails most replies. All three ran on one small local model, so the next step is to fix routing and repeat the run on other local models with tool-call support before choosing.

**For a customer:** Highest priority is to work with someone with judgement to find a balance and accept an output appropriate to the brand's reputation.

## What surprised me
How widely the data points can contradict each other — and that giving clarity without hiding facts is what helps a client make an informed decision.

## How I used AI
…

## Video
<!-- learn:video -->
[![Watch the video](video/thumbnail.png)](https://youtu.be/dsue_wyekpY)
<!-- /learn:video -->
