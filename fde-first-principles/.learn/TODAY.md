# Today · Day 8 of 66: Version C: an agent loop from scratch

**Ship by Fri 30 Oct, 05:00** · **morning 1 of 2** · folder: [1-measure-before-you-believe/08-agent-loop-from-scratch](../1-measure-before-you-believe/08-agent-loop-from-scratch/README.md)

> **First-principles question:** What is an 'agent', really, once you remove the framework?

**Why it matters for an FDE:** An agent is a loop: the model asks for a tool, your code runs it, the result goes back. Knowing this lets you debug any framework a customer uses.

**Time:** about 115 minutes, over 2 mornings

### Set up
- lab/acme_tools.py is given: four tools and their JSON schemas. Today is about the loop.

### 1 · Learn (about 30 minutes)
- [Ollama: tool calling](https://docs.ollama.com/capabilities/tool-calling) · 10 min. Read a single tool call, then the agent-loop example.
- [Building effective agents: 'Agents' and 'Appendix 2: Prompt engineering your tools'](https://www.anthropic.com/engineering/building-effective-agents) · 10 min. Notice: the loop has a stop condition and a step limit.

### 2 · Build (about 60 minutes)
1. Write run_agent(case): send the email and the tools; while the reply has tool_calls, run each tool, add a 'tool' message, and call the model again. Stop after 6 steps.
2. At the end, ask for the same JSON as version B.
3. Print the full trace (each tool call and its result) for 2 cases.
4. Run on the first 10 cases. Count the steps per case.

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Done when
- [ ] run_agent() always stops, never more than 6 steps.
- [ ] Two full traces are shown.
- [ ] Version C ran on at least 10 cases and the step counts are printed.

### 3 · Record (5 minutes or less)
- Show a trace and narrate each step.
- Point to the line that makes it an 'agent'.
- Say one risk you saw: a wrong tool, an extra step or a loop.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Add a tool that changes data (issue_refund), but only in project 6, with a human check._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

### Ship it
```
fde-coach learn done --video https://youtu.be/…
```
or tell Claude Code: *ship today's topic*. Partial work can ship too (`--partial`).

Upload the video as Unlisted with any title: when you ship, the coach sets its title, description and blue title-card thumbnail on YouTube. Want them while you upload? `fde-coach learn video`.
