# Today · Day 2 of 59: Workflow or agent? Map the decisions first

**Ship by Fri 16 Oct, 05:00** · folder: [1-measure-before-you-believe/02-workflow-or-agent](../1-measure-before-you-believe/02-workflow-or-agent/README.md)

> **First-principles question:** Which steps in this process truly need a model, and what does a wrong answer cost?

**Why it matters for an FDE:** Customers often ask for 'an agent'. A good FDE first finds where the real uncertainty is. Usually most steps are plain software.

### 1 · Learn (about 20 minutes)
- [Building effective agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents) · 20 min. Read 'What are agents?' and 'When (and when not) to use agents', then skim the five workflow patterns. Stop at 'Combining and customizing these patterns'.

### 2 · Build (about 40 minutes)
1. Read the Acme Fibre brief: data/acme/README.md (a fictional broadband company in Pune).
2. In Excalidraw, draw how one customer email becomes a reply: receive → understand → look up the customer → find the policy → write → check → send or escalate.
3. Colour every step: grey = plain code, blue = needs a model, orange = needs a human.
4. Next to every blue step, write one sentence: what goes wrong if the model is wrong, and who notices.
5. Write the article's pattern that fits best (prompt chaining, routing or agent) on the diagram.

### Done when
- [ ] The diagram has at least 6 steps, each coloured grey, blue or orange.
- [ ] Every blue step has a 'cost of a wrong answer' note.
- [ ] The pattern name is on the diagram.
- [ ] Saved in this folder as diagram.excalidraw.svg (or .png with the scene embedded).

### 3 · Record (5 minutes or less)
- Walk through the diagram as if the customer's CTO is listening.
- Point to the one step where a model really earns its place.
- Say which step you would NOT give to a model, and why.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Draw the same map for your real communication agent (keep it private)._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

### Ship it
```
fde-coach learn done --video https://youtu.be/…
```
or tell Claude Code: *ship today's topic*. Partial work can ship too (`--partial`).
