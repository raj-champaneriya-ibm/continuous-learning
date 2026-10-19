# Today · Day 4 of 66: Version A: rules and templates (the honest baseline)

**Ship by Wed 21 Oct, 05:00** · folder: [1-measure-before-you-believe/04-rules-baseline](../1-measure-before-you-believe/04-rules-baseline/README.md)

> **First-principles question:** How far can plain code go before you need a model?

**Why it matters for an FDE:** A baseline tells you what the model has to beat. Many 'AI projects' never measure one.

**Time:** minimum scope, 1 morning (about 115 minutes for the full topic)

**Attempt 2: minimum scope.** Ship at least this: Intent accuracy printed for all cases.

### 1 · Learn (about 30 minutes)
- [Building effective agents: 'Appendix 1, A. Customer support'](https://www.anthropic.com/engineering/building-effective-agents) · 5 min. Short: why support is a good fit for AI, and how to measure it.
- [Accuracy, recall, precision (Google ML Crash Course)](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall) · 15 min. Read the accuracy part closely. Skim the rest; we come back to it.

**Maths you need today: Accuracy.** Accuracy = correct answers ÷ all answers. One number hides which mistakes you make, so also count the mistakes per intent.

### 2 · Build (about 60 minutes)
1. Write classify(message) with keywords (for example 'bill', 'refund' → billing). Add Hinglish words too.
2. Write one reply template per intent. Fill in the first name, area and outage ticket.
3. Run version A on every case and compute the intent accuracy.
4. Show the mistakes per intent. Read 5 wrong cases and write why the rules failed.

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Done when
- [ ] Version A runs on every case without crashing.
- [ ] Intent accuracy is printed.
- [ ] A table of mistakes per intent is shown.
- [ ] 5 failures have a one-line reason each.

### 3 · Record (5 minutes or less)
- Show the accuracy number.
- Show one case where keywords failed (Hinglish is a good one).
- Say what a model would need to do to beat this.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Try regular expressions for customer IDs and amounts._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

### Ship it
```
fde-coach learn done --video https://youtu.be/…
```
or tell Claude Code: *ship today's topic*. Partial work can ship too (`--partial`).

Upload the video as Unlisted with any title: when you ship, the coach sets its title, description and blue title-card thumbnail on YouTube. Want them while you upload? `fde-coach learn video`.
