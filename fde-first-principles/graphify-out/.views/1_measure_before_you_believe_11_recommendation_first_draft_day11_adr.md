# View of 1-measure-before-you-believe/11-recommendation-first-draft/day11-adr.drawio (draw.io diagram: labelled shapes, then labelled connectors)

## Page: Day 11 · ADR-001
- [shape title] ADR-001 · How Acme Fibre should answer customer emails
- [shape subtitle] Status: Draft · 2026-10-31 · Raj Champaneriya · evidence from day 9 runs in data/results/
- [shape ctxLabel] 01 · CONTEXT
- [shape ctxBody] Acme Fibre · broadband · Pune
About 1,200 support emails a day

Trust comes first:
— never break a policy (OTP, password, credit limits)
— never answer an email that needs a human
— get the facts right

Email is not chat: minutes are fine.

Scope: 84 cases (40 need a human) · one run · qwen3:4b · temperature 0
- [shape optLabel] 02 · OPTIONS
- [shape optA] A · Rules and templates
Keyword rules fill a template. No model.
- [shape optB] B · One model call with context
Customer card + help articles. Core of the decision.
- [shape optC] C · Agent with tools
Up to 6 calls: look up, search, escalate.
- [shape evLabel] 03 · EVIDENCE (DAY 9)
- [shape evTable] PASSSAFEMISSED ESC.MEDIAN SP95 S₹ / 1,000A19% ± 9%52% ± 11%40 of 400.00.00.00B29% ± 10%54% ± 11%38 of 404.36.21.30C20% ± 9%71% ± 10%17 of 40104.2213.88.70
- [shape evNote] ± 2 se · 84 cases · top failure category added after day 10
- [shape evReadLabel] WHAT IT SAYS
- [shape evRead] Pass rates overlap. They cannot pick a winner. Safety can.

A and B miss almost every escalation. C catches 23 of 40, but breaks a policy in 8 replies (B 6, A 0).

B is flattered. It got the articles for the expected intent (oracle context). C had to search: facts 36% against B's 74%.

C is too slow for one Mac. 1,200 emails × 104 s ≈ 35 hours of compute a day.

Cost is not the issue. B ≈ ₹1.60 a day, C ≈ ₹10 a day.
- [shape decLabel] 04 · DECISION
- [shape decText] Build a workflow, not an agent: B with a safety router in front and a policy check behind.
- [shape n1] Email in
- [shape n2] Load customer card and outages
- [shape n3] Router: needs a human?
rules + 1 model call
- [shape n4] Search the help articles (no oracle)
- [shape n5] One model call (B) drafts the reply
- [shape n6] Policy check
grader rules, in code
- [shape n7] Human approves the draft
shadow mode until the gates hold
- [shape n8] Reply out
- [shape hq] Human queue
a person writes the reply.
Over-escalating costs time,
not safety.
- [shape gLabel] 05 · GATES BEFORE UNREVIEWED REPLIES
- [shape gBody] Measured once on held-out cases:

0 policy breaks

≤ 2 of 40 missed escalations

> 19% pass-rate lower bound (beats A)
- [shape cLabel] 06 · CONSEQUENCES
- [shape cBody] Good · escalation is its own step, measured and fixed alone. One or two calls per email. The policy check is code, not hope.

Bad · more emails reach people at first. Searched context will lower B's numbers by an unmeasured amount.

Risks · the router is the single point of failure. The grader has known false alarms. B and C runs lack prompt fingerprints.
- [shape mLabel] 07 · WHAT WOULD CHANGE MY MIND
- [shape mBody] Router misses more than 2 of 40
→ do not automate replies: A's templates plus human triage.

C on a stronger model passes the gates, p95 under 60 s
→ the agent earns its complexity.

Searched context costs B more than 10 points of facts
→ retrieval comes first, before any rollout.
- [shape qLabel] 08 · OPEN QUESTIONS (PROJECTS 2 TO 6)
- [shape qBody] 1 How good is searched context, and how much of B's lead was the answer key? P2

2 Can a small learned classifier route escalations better than rules plus a prompt? P3

3 Which failures come from model size, and which from the prompt or grader? P4, P5

4 Do the numbers hold on a stronger model and real Acme emails? P6
- [arrow]: "Email in" -> "Load customer card and outages"
- [arrow]: "Load customer card and outages" -> "Router: needs a human?
rules + 1 model call"
- [arrow] (no): "Router: needs a human?
rules + 1 model call" -> "Search the help articles (no oracle)"
- [arrow]: "Search the help articles (no oracle)" -> "One model call (B) drafts the reply"
- [arrow]: "One model call (B) drafts the reply" -> "Policy check
grader rules, in code"
- [arrow] (clean): "Policy check
grader rules, in code" -> "Human approves the draft
shadow mode until the gates hold"
- [arrow]: "Human approves the draft
shadow mode until the gates hold" -> "Reply out"
- [arrow] (yes): "Router: needs a human?
rules + 1 model call" -> "Human queue
a person writes the reply.
Over-escalating costs time,
not safety."
- [arrow] (needs_human): "One model call (B) drafts the reply" -> "Human queue
a person writes the reply.
Over-escalating costs time,
not safety."
- [arrow] (any break): "Policy check
grader rules, in code" -> "Human queue
a person writes the reply.
Over-escalating costs time,
not safety."
