# Day 1 · An LLM call is just an HTTP request

<!-- learn:status -->
**Status:** ⏳ open · attempt 2 · dropped 2026-10-14 · ship by Thu 15 Oct, 05:50 · project 1, step 1
<!-- /learn:status -->

> **First-principles question:** What exactly travels over the wire when you 'call an LLM'?

**Why it matters for an FDE:** Every agent framework hides this one request. When a customer's agent misbehaves, this is the level you debug at.

### Set up
- Ollama is already on your Mac. Pull a small model: `ollama pull qwen3:4b` (8 GB Mac: `ollama pull llama3.2:3b` and change MODEL in the notebook).
- In your fde-first-principles folder run `uv sync` once. In VS Code, open the notebook and pick the `.venv` kernel.

### 1 · Learn (about 20 minutes)
- [Ollama API: generate a chat message](https://docs.ollama.com/api/chat) · 10 min. Read the request body and the response fields. Note which numbers are tokens and which are nanoseconds.
- [Deep Dive into LLMs like ChatGPT (Andrej Karpathy): chapter 'inference'](https://www.youtube.com/watch?v=7xTGNNLPyMI&t=1561s) · 5 min. Watch 26:01 to 31:09: why the same prompt gives different answers.

### 2 · Build (about 40 minutes)
1. Send one POST request to http://localhost:11434/api/chat with the `requests` library (no SDK) and `stream: false`.
2. Print the whole JSON response. Find the reply text, prompt_eval_count, eval_count and total_duration.
3. Turn total_duration (nanoseconds) into seconds. Compute tokens per second.
4. Send the same request 5 times with temperature 0.8, then 5 times with temperature 0 and a seed. Compare the answers.

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Done when
- [ ] The notebook runs top to bottom without errors.
- [ ] It prints tokens in, tokens out and seconds for one call.
- [ ] It shows the 5 answers at temperature 0.8 and the 5 at temperature 0.
- [ ] README.md explains, in your words, why the answers differ.

### 3 · Record (5 minutes or less)
- Show the raw JSON. Point to the reply, the token counts and the time.
- Show the 5 different answers and say why they differ.
- Say what this means for a customer who wants 'the same answer every time'.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Make the same call to a paid API later and compare the JSON shape._

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
