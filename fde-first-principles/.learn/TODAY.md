# Today · Day 3 of 66: Write the test set before the system

**Ship by Sun 18 Oct, 05:00** · **morning 1 of 2** · folder: [1-measure-before-you-believe/03-test-set-first](../1-measure-before-you-believe/03-test-set-first/README.md)

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

### Done when
- [ ] data/acme/cases.jsonl has at least 50 cases (100 is better).
- [ ] Every drafted case was reviewed by hand: no "reviewed": false is left.
- [ ] Every intent has at least 5 cases.
- [ ] Validation passes and the bar chart is shown.
- [ ] At least 5 Hinglish cases and 2 prompt-injection cases are tagged.

### 3 · Record (5 minutes or less)
- Show 3 tricky cases and say why each one is in the set.
- Show the bar chart. Which intent is tested least?
- Say why you wrote the tests before the system.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Grow the set to 100 cases, then check which intents are still thin._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

### Ship it
```
fde-coach learn done --video https://youtu.be/…
```
or tell Claude Code: *ship today's topic*. Partial work can ship too (`--partial`).

Upload the video as Unlisted with any title: when you ship, the coach sets its title, description and blue title-card thumbnail on YouTube. Want them while you upload? `fde-coach learn video`.
