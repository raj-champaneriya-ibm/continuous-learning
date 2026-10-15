# Day 2 · Workflow or agent? Map the decisions first

<!-- learn:status -->
**Status:** ✅ shipped · dropped 2026-10-15 · ship by Fri 16 Oct, 05:00 · shipped 2026-10-16 04:25 · project 1, step 2
<!-- /learn:status -->

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

## In my words
<!-- Fill these in before you ship (plain, simple English is perfect). Claude can help you turn what you said
     in your video into text, but keep your own words. -->
**For a beginner:** Not every task needs AI. We should first understand the problem, identify which steps require judgment, and use AI only where traditional software is not sufficient.

**For an engineer:** I would start with a deterministic workflow and introduce LLM calls only for tasks involving language ambiguity or contextual generation. I would evaluate their accuracy, cost, and failure modes before considering more autonomous execution.

**For a customer:** My goal is not to introduce AI everywhere. I want to understand your existing process, identify the most valuable improvement opportunities, and work with your team to choose a reliable and measurable solution.

## What surprised me
A customer-support process may involve many steps, but only a few might benefit significantly from an LLM. The difficult part is identifying where model intelligence adds enough value to justify its risks.

## How I used AI
I used AI to challenge my initial assumptions, discuss architectural alternatives, and practice explaining my ideas to a CTO. I reviewed the recommendations and made the final design decisions myself.

## Video
<!-- learn:video -->
[![Watch the video](video/thumbnail.png)](https://youtu.be/i51y2NiYdDo)
<!-- /learn:video -->
