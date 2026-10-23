# Today · Day 6 of 66: Version B: one model call with the right context

**Ship by Sun 25 Oct, 05:00** · **morning 2 of 2** · folder: [1-measure-before-you-believe/06-one-llm-call](../1-measure-before-you-believe/06-one-llm-call/README.md)

> **First-principles question:** What does the model need to see to answer like a trained support agent?

**Why it matters for an FDE:** Most real wins come from one well-fed call, not from agents. The context is the product.

**Time:** about 110 minutes, over 2 mornings

### Set up
- lab/llm.py is given: it is your day 1 call plus a cache (re-runs are free), timing and token counts. Read it once.

### 1 · Learn (about 25 minutes)
- [Ollama: structured outputs](https://docs.ollama.com/capabilities/structured-outputs) · 5 min. How to make the model answer in a JSON shape you choose.
- [Building effective agents: 'Building block: The augmented LLM' and 'Workflow: Routing'](https://www.anthropic.com/engineering/building-effective-agents) · 10 min. Re-read these two sections.

### 2 · Build (about 60 minutes)
1. Write a system prompt with Acme's rules (data/acme/policy.md) in your own words.
2. For each case, put the customer card and the right help articles into the user message. Today the articles are hand-picked by intent ('oracle' context): the best case. Project 2 replaces this with real search.
3. Ask for JSON {intent, reply, needs_human} using a JSON schema.
4. Run version B on every case (cached), score it, and compare with version A.

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Done when
- [ ] Version B runs on every case; answers are cached.
- [ ] Score table: A and B side by side.
- [ ] JSON parse failures are counted.
- [ ] 3 cases where B beat A and 3 where it lost, one line each.

### 3 · Record (5 minutes or less)
- Show your prompt and explain each part.
- Show A versus B.
- Show one case B got wrong and say why you think it failed.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Try a bigger model (qwen3:8b) on the failures only._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

### Ship it
```
fde-coach learn done --video https://youtu.be/…
```
or tell Claude Code: *ship today's topic*. Partial work can ship too (`--partial`).

Upload the video as Unlisted with any title: when you ship, the coach sets its title, description and blue title-card thumbnail on YouTube. Want them while you upload? `fde-coach learn video`.
