# ADR-001: How Acme Fibre should answer customer emails

**Status:** Draft · **Date:** 2026-10-31 · **Author:** Raj Champaneriya

## Context
Acme Fibre (broadband, Pune) gets about 1,200 support emails a day and wants most answered without a person. Trust matters most: never break a policy (OTPs, passwords, credit limits), never answer an email that needs a human, and get the facts right. Email is not chat, so minutes are fine.

Scope: 84 test cases (40 need a human), one run on one small local model (`qwen3:4b`, temperature 0).

## Options
| Option | What it is |
|---|---|
| A · Rules and templates | Keyword rules pick the intent and fill a template. No model. |
| B · One model call with context | One call with the customer card and help articles. |
| C · Agent with tools | Up to 6 calls that look up the customer, search articles and escalate. |

## Evidence (from day 9)
| | Pass rate (± 2 se) | Safe (± 2 se) | Missed escalations | Median s | p95 s | ₹ per 1,000 emails | Top failure category |
|---|---|---|---|---|---|---|---|
| A | 19% ± 9% | 52% ± 11% | 40 of 40 | 0.0 | 0.0 | 0.00 | day 10 |
| B | 29% ± 10% | 54% ± 11% | 38 of 40 | 4.3 | 6.2 | 1.30 | day 10 |
| C | 20% ± 9% | 71% ± 10% | 17 of 40 | 104.2 | 213.8 | 8.70 | day 10 |

- Pass rates overlap, so they cannot pick a winner. Safety can.
- A and B miss almost every escalation. C catches 23, but breaks a policy in 8 replies (B 6, A 0).
- B got the articles for the *expected* intent (oracle context). C had to search: facts 36% against B's 74%.
- C is too slow for one Mac: 1,200 emails at 104 s is about 35 hours of compute a day.
- Cost is not the issue: B is about ₹1.60 a day, C about ₹10.

## Decision
Build a workflow, not an agent: B with a safety router in front and a policy check behind.

1. Router: rules plus one model call ask "needs a human?" first. Any yes goes to the human queue.
2. Search the help articles (no oracle), then one B-style call drafts the reply.
3. Policy check: the grader's policy rules run on every draft. Any break goes to a human.
4. Shadow mode: a person approves every draft until the gates hold.

Gates before replies go out unreviewed, on held-out cases: 0 policy breaks, at most 2 of 40 missed escalations, and a pass rate whose lower bound beats A's 19%.

## Consequences
- Good: escalation is its own step, measured and fixed alone. Each email costs one or two calls, and the policy check is code, not hope.
- Bad: more emails reach people at first. Searched context will lower B's numbers by an unmeasured amount.
- Risks: the router is the single point of failure for safety. The grader has known false alarms ("5-7 working days", "Rs. 100"). The B and C runs did not record prompt fingerprints.

## What would change my mind
- If the router cannot get missed escalations to 2 of 40 or fewer, I would not automate replies: A's templates plus human triage.
- If C on a stronger model passes the same gates with p95 under 60 s, the agent earns its complexity.
- If searched context costs B more than 10 points of facts, retrieval comes first, before any rollout.

## Open questions (projects 2 to 6)
1. How good is searched context for B, and how much of B's lead was the answer key? (project 2)
2. Can a small learned classifier route escalations better than rules plus a prompt? (project 3)
3. Which failures come from model size, and which from the prompt or the grader? (projects 4 and 5)
4. Do the numbers hold on a stronger model and on real Acme emails? (project 6)
