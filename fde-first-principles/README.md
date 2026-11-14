# FDE First Principles

A public learning log. A topic drops in the morning at 06:00 (IST) and gets one to three mornings, depending on
its size. I learn it, build it (a notebook, code or an Excalidraw diagram) and explain it on video. Each project
ends with an article on my site. The goal: build and ship AI systems the way a Forward Deployed Engineer needs
to: measure before believing, ground agents in the customer's context, make the evals run without me, ship a
production-shaped agent, know what inside the model changes a decision, and hand it over.

Six projects, 53 topics: 1. Measure before you believe, 2. Grounding: meaning as numbers and enterprise context,
3. Evals that run without you, 4. A production-shaped full-stack agent, 5. Inside the model: mechanics that
change decisions, 6. The 6-week enterprise engagement rehearsal.

The plan follows the FDE curriculum review of November 2026.
The from-scratch builds (micrograd, makemore and a tiny GPT) moved to an optional, unscheduled track.

Maths shows up only on the day a project needs it. Most work runs on my own Mac (Ollama) for free; from project 3
each project may use one capped cloud budget (a managed runtime, a cloud evaluator, a frontier model run). The
drops, deadlines and this table are managed by
[fde-coach learn](https://github.com/rajchampaneriya/fde-impromptu-coach).

## Progress
<!-- learn:progress -->
| Day | Date | Topic | Proof | Status |
|---|---|---|---|---|
| 1 | 2026-10-13 | [One model call: tokens, time and randomness](1-measure-before-you-believe/01-an-llm-call-is-http/README.md) |  | ❌ missed |
| 1 | 2026-10-14 | [One model call: tokens, time and randomness](1-measure-before-you-believe/01-an-llm-call-is-http/README.md) (attempt 2) | [▶](https://youtu.be/vc5h1lX4Rwo) | ✅ shipped |
| 2 | 2026-10-15 | [Workflow or agent? Map the decisions first](1-measure-before-you-believe/02-workflow-or-agent/README.md) | [▶](https://youtu.be/i51y2NiYdDo) | ✅ shipped |
| 3 | 2026-10-16 | [Write the test set before the system](1-measure-before-you-believe/03-test-set-first/README.md) | [▶](https://youtu.be/9N7xmktXyYg) | 🕒 late |
| 4 | 2026-10-18 | [Version A: rules and templates (the honest baseline)](1-measure-before-you-believe/04-rules-baseline/README.md) |  | ❌ missed |
| 4 | 2026-10-20 | [Version A: rules and templates (the honest baseline)](1-measure-before-you-believe/04-rules-baseline/README.md) (attempt 2) | [▶](https://youtu.be/_oQJGEakSrY) | ✅ shipped |
| 5 | 2026-10-20 | [A grader you can trust](1-measure-before-you-believe/05-a-grader-you-can-trust/README.md) |  | ❌ missed |
| 5 | 2026-10-22 | [A grader you can trust](1-measure-before-you-believe/05-a-grader-you-can-trust/README.md) (attempt 2) |  | ❌ missed |
| 5 | 2026-10-23 | [A grader you can trust](1-measure-before-you-believe/05-a-grader-you-can-trust/README.md) (attempt 3) | [▶](https://youtu.be/ec4bJ2_Jb-Y) | ✅ shipped |
| 6 | 2026-10-23 | [Version B: one model call with the right context](1-measure-before-you-believe/06-one-llm-call/README.md) | [▶](https://youtu.be/Sc_RauiP3xw) | ✅ shipped |
| 7 | 2026-10-24 | [Why 30 test cases can lie: error bars](1-measure-before-you-believe/07-error-bars/README.md) |  | ❌ missed |
| 7 | 2026-10-27 | [Why 30 test cases can lie: error bars](1-measure-before-you-believe/07-error-bars/README.md) (attempt 2) |  | ❌ missed |
| 7 | 2026-10-28 | [Why 30 test cases can lie: error bars](1-measure-before-you-believe/07-error-bars/README.md) (attempt 3) | [▶](https://youtu.be/K7KUVnZvZM4) | ✅ shipped |
| 8 | 2026-10-28 | [Version C: an agent loop from scratch](1-measure-before-you-believe/08-agent-loop-from-scratch/README.md) | [▶](https://youtu.be/yXcNNqTxFW8) | ✅ shipped |
| 9 | 2026-10-29 | [Run all three: success, cost, latency](1-measure-before-you-believe/09-success-cost-latency/README.md) | [▶](https://youtu.be/dsue_wyekpY) | ✅ shipped |
| 10 | 2026-10-30 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) |  | ❌ missed |
| 10 | 2026-11-02 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 2) |  | ❌ missed |
| 10 | 2026-11-03 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 3) |  | ❌ missed |
| 10 | 2026-11-04 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 4) |  | ❌ missed |
| 10 | 2026-11-05 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 5) |  | ❌ missed |
| 10 | 2026-11-06 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 6) |  | ❌ missed |
| 10 | 2026-11-07 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 7) |  | ❌ missed |
| 10 | 2026-11-09 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 8) |  | ❌ missed |
| 10 | 2026-11-10 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 9) |  | ❌ missed |
| 10 | 2026-11-11 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 10) |  | ❌ missed |
| 10 | 2026-11-12 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 11) |  | ❌ missed |
| 10 | 2026-11-13 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 12) |  | ❌ missed |
| 10 | 2026-11-14 | [Read the failures, not the averages](1-measure-before-you-believe/10-read-the-failures/README.md) (attempt 13) |  | ⏳ open |

**9 of 53 topics shipped.**
<!-- /learn:progress -->
