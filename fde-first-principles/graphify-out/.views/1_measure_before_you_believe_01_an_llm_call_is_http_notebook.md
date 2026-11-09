# View of 1-measure-before-you-believe/01-an-llm-call-is-http/notebook.ipynb (markdown and code cells; outputs omitted)

---- cell 1 (markdown) ----
# Day 1 · An LLM call is just an HTTP request

**First-principles question:** What exactly travels over the wire when you 'call an LLM'?

The full task (learn → build → record) is in this folder's `README.md`. This notebook is your workbench:
run cells top to bottom with **Shift + Enter**, fill in every cell marked **TODO**, and finish with the
**✅ self-check** cell at the end.

---- cell 2 (code) ----
import json
import time
import requests

OLLAMA = "http://localhost:11434"
MODEL = "qwen3:4b"          # 8 GB Mac? use "llama3.2:3b" (and `ollama pull llama3.2:3b`)

# Is Ollama running, and which models do you have?
print([m["name"] for m in requests.get(f"{OLLAMA}/api/tags", timeout=5).json()["models"]])

---- cell 3 (markdown) ----
## 1 · One raw call
No SDK, no framework: one HTTP POST with a JSON body.

---- cell 4 (code) ----
body = {
    "model": MODEL,
    "messages": [{"role": "user", "content": "A customer says their internet is down. Reply in one sentence."}],
    "stream": False,
    "think": False,      # qwen3 can 'think' before answering; switch that off for now (remove this line for llama3.2)
}
# TODO: send `body` to f"{OLLAMA}/api/chat" with requests.post(url, json=body, timeout=120)
#       and keep the parsed JSON response in `data` (hint: response.json())
data = requests.post(f"{OLLAMA}/api/chat", json=body, timeout=120).json()

print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])

---- cell 5 (markdown) ----
## 2 · Tokens and time
Find the numbers in the JSON above. Durations are in **nanoseconds** (1 second = 1,000,000,000 ns).

---- cell 6 (code) ----
# TODO: read these from `data`
reply = None        # the reply text (inside data["message"])
tokens_in = None    # prompt_eval_count
tokens_out = None   # eval_count
seconds = None      # total_duration, converted to seconds

reply = data["message"]["content"]
tokens_in = data["prompt_eval_count"]
tokens_out = data["eval_count"]
seconds = data["total_duration"] / 1e9

print(reply)
print(f"{tokens_in} tokens in · {tokens_out} tokens out · {seconds:.2f} s · {tokens_out / seconds:.1f} tokens per second")


---- cell 7 (markdown) ----
## 3 · Same question, five answers
`options.temperature` controls randomness. `options.seed` fixes the dice.

---- cell 8 (code) ----
def ask(temperature, seed=None):
    """Send `body` again with these options and return only the reply text."""
    options = {"temperature": temperature}
    if seed is not None:
        options["seed"] = seed
    # TODO: make a copy of body with "options": options added (dict(body, options=options)),
    #       send it like in step 1, and return the reply text
    
    payload = dict(body, options=options)
    data = requests.post(f"{OLLAMA}/api/chat", json=payload, timeout=120).json()
    return data["message"]["content"]


hot = [ask(0.8) for _ in range(5)]
cold = [ask(0.0, seed=42) for _ in range(5)]
for h, c in zip(hot, cold):
    print(f"0.8 → {h[:100]!r}")
    print(f"0.0 → {c[:100]!r}\n")
print("different answers at 0.8:", len(set(hot)), "| at 0.0:", len(set(cold)))

---- cell 9 (markdown) ----
## 4 · Your observation
Why are the answers at 0.8 different and the ones at 0.0 the same? Write 2 or 3 sentences in **README.md → In my words**. (Project 5 explains exactly why.)

---- cell 10 (code) ----
# ✅ Self-check: run me last. A clear message tells you what to fix.
assert isinstance(data, dict) and "message" in data, "Step 1: `data` should be the JSON response"
assert isinstance(reply, str) and reply.strip(), "Step 2: `reply` should be the reply text"
assert isinstance(tokens_in, int) and isinstance(tokens_out, int), "Step 2: token counts are whole numbers"
assert isinstance(seconds, (int, float)) and 0 < seconds < 600, "Step 2: seconds = total_duration / 1e9"
assert len(hot) == 5 and len(cold) == 5 and all(isinstance(x, str) for x in hot + cold), "Step 3: ask() returns text"
print("All checks passed ✅  Now write 'In my words' in README.md and record your video.")
