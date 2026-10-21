# Today · Day 5 of 66: A grader you can trust

**Ship by Fri 23 Oct, 05:00** · folder: [1-measure-before-you-believe/05-a-grader-you-can-trust](../1-measure-before-you-believe/05-a-grader-you-can-trust/README.md)

> **First-principles question:** What exactly makes a reply 'correct' for this customer?

**Why it matters for an FDE:** If you cannot write the check, you cannot promise the behaviour. This is where vague requirements become concrete.

**Time:** minimum scope, 1 morning (about 100 minutes for the full topic)

**Attempt 2: minimum scope.** Ship at least this: score() works and the tests pass.

### 1 · Learn (about 25 minutes)
- [Define success criteria and build evaluations (Claude docs)](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) · 15 min. Read the eval design principles and the code-based grading examples. Skip model-based grading for now.

### 2 · Build (about 50 minutes)
1. Open lab/evals.py. Implement policy_violations() and score() (TODOs 1 to 7).
2. Run the tests in the notebook until they all pass.
3. Score version A on every case and print the summary table.
4. Find one case where your grader itself is wrong (hint: 'Please do not share your OTP'). Fix it.

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Done when
- [ ] All tests in the notebook pass.
- [ ] Version A has a score table: intent, facts, policy, human, passed.
- [ ] You found and fixed at least one case where the grader was wrong.

### 3 · Record (5 minutes or less)
- Show score() and explain each check in one sentence.
- Show the case where your grader was wrong.
- Say why 'passed' needs every check to pass.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Add a model-based grader for tone later, and test the grader too._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

### Ship it
```
fde-coach learn done --video https://youtu.be/…
```
or tell Claude Code: *ship today's topic*. Partial work can ship too (`--partial`).

Upload the video as Unlisted with any title: when you ship, the coach sets its title, description and blue title-card thumbnail on YouTube. Want them while you upload? `fde-coach learn video`.
