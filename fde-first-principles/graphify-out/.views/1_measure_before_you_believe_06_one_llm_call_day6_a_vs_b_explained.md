# View of 1-measure-before-you-believe/06-one-llm-call/day6-a-vs-b-explained.drawio (draw.io diagram: labelled shapes, then labelled connectors)

## Page: Day 6 · A vs B
- [shape t1] Day 6 · What changed between Version A and Version B?
- [shape t2] Same 84 emails. Same grader. Only the box in the middle changed.
- [shape t3] Question of the day: what does the model need to see to answer like a trained support agent?
- [shape p1t] 1 · Same test, new brain
- [shape b2tag] the only part that changes
- [shape b1] 84 customer emails
(cases.jsonl)
- [shape b2] Assistant
A = rulesB = one LLM call
- [shape b3] Answer
{ intent, reply, needs_human }
- [shape b4] Grader (Day 5)
intent · facts · policy · human
- [shape b5] Score
% of cases passed
- [shape p1c] A fair race: when only one thing changes, any change in the score comes from that one thing.
- [shape pAt] 2a · Version A: rules (Day 4)
- [shape pAs] Plain code. It looks for words.
- [shape a1] Customer email
- [shape a2] Keyword match
'bill', 'refund' → billing
- [shape a3] Fill a template
name · area · ticket
- [shape a4] { intent, reply, needs_human }
- [shape a5] What A cannot see

✗ the customer's account card
✗ the help articles
✗ meaning: Hinglish or new words get no keyword hit
✗ judgment: when a human is really needed
- [shape a6] Cheap · instant · predictable
- [shape pBt] 2b · Version B: one model call (Day 6)
- [shape pBs] A model reads the meaning, if you hand it the right context.
- [shape cB] What the model sees (the context)
- [shape sLbl] SYSTEM message
- [shape s1] Who you are + Acme's rules
(policy.md, in my own words)
- [shape uLbl] USER message
- [shape u1] Customer card: name, area, plan
- [shape u2] Help articles (KB)
hand-picked by expected intent ('oracle')
- [shape u3] Customer email
- [shape schema] JSON schema
forces the answer's shape
- [shape llm] LLM
(Ollama)
- [shape outB] { intent,
reply,
needs_human }
- [shape bNote] Costs tokens + seconds.
Cached, so re-runs are free.
Broken JSON = a counted parse failure.
- [shape p3t] 3 · What changed, row by row
- [shape h2] A · Rules
- [shape h3] B · One model call
- [shape r1q] Picks the intent
- [shape r1a] Keyword list
- [shape r1b] Reads the meaning: Hinglish, synonyms, mixed requests
- [shape r2q] Writes the reply
- [shape r2a] One fixed template per intent
- [shape r2b] Drafts a reply from the customer card + help articles
- [shape r3q] Knows Acme's rules
- [shape r3a] Hard-coded in Python
- [shape r3b] Written in plain English in the system prompt
- [shape r4q] Decides 'needs a human'
- [shape r4a] Simple if-rules
- [shape r4b] Told when: asks for a person, fake 'system notes', not the account holder
- [shape r5q] Answer shape
- [shape r5a] Python dict, always valid
- [shape r5b] JSON schema; parse failures are counted
- [shape r6q] Cost per email
- [shape r6a] Free and instant
- [shape r6b] Tokens + seconds (cached after the first run)
- [shape p4t] 4 · Scoreboard on 84 cases
- [shape sbHA] A · Rules
- [shape sbHB] B · One call
- [shape m1l] Intent right
- [shape m1p] 67%
- [shape m1bp] 90%
- [shape m2l] Facts included
- [shape m2p] 60%
- [shape m2bp] 73%
- [shape m3l] Policy clean
- [shape m3p] 99%
- [shape m3bp] 94%
- [shape m4l] Human call right
- [shape m4p] 50%
- [shape m4bp] 52%
- [shape m5l] All 4 pass
- [shape m5p] 18%
- [shape m5bp] 26%
- [shape p4c] Both real: data/results/A.jsonl · B.jsonl · 0 JSON parse failures · B won 11 cases, lost 4 · intent +23 pts, policy −5 pts.
- [shape p5t] 5 · Day 6 objectives (done when)
- [shape goals] ☒ Run B on all 84 cases (answers cached)
☒ Score table: A and B side by side
☒ Count JSON parse failures (0)
☐ 3 cases B won and 3 it lost, one line each
- [shape take] The context is the product.
One well-fed call often beats an agent.
- [shape fine] Fine print: 'oracle' articles
Today B is handed the right articles, so its score is a best case. Project 2 swaps in real search.
- [arrow]: "84 customer emails
(cases.jsonl)" -> "Assistant
A = rulesB = one LLM call"
- [arrow]: "Assistant
A = rulesB = one LLM call" -> "Answer
{ intent, reply, needs_human }"
- [arrow]: "Answer
{ intent, reply, needs_human }" -> "Grader (Day 5)
intent · facts · policy · human"
- [arrow]: "Grader (Day 5)
intent · facts · policy · human" -> "Score
% of cases passed"
- [arrow]: "Customer email" -> "Keyword match
'bill', 'refund' → billing"
- [arrow]: "Keyword match
'bill', 'refund' → billing" -> "Fill a template
name · area · ticket"
- [arrow]: "Fill a template
name · area · ticket" -> "{ intent, reply, needs_human }"
- [arrow]: "What the model sees (the context)" -> "LLM
(Ollama)"
- [arrow]: "JSON schema
forces the answer's shape" -> "LLM
(Ollama)"
- [arrow]: "LLM
(Ollama)" -> "{ intent,
reply,
needs_human }"
