# Today · Day 9 of 66: Run all three: success, cost, latency

**Ship by Sat 31 Oct, 05:00** · **morning 1 of 2** · folder: [1-measure-before-you-believe/09-success-cost-latency](../1-measure-before-you-believe/09-success-cost-latency/README.md)

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

### Ship it
```
fde-coach learn done --video https://youtu.be/…
```
or tell Claude Code: *ship today's topic*. Partial work can ship too (`--partial`).

Upload the video as Unlisted with any title: when you ship, the coach sets its title, description and blue title-card thumbnail on YouTube. Want them while you upload? `fde-coach learn video`.
