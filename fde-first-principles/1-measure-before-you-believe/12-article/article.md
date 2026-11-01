---
# Hugo front matter for rajc.work. If your other posts use different fields, copy theirs.
# Save the finished post where your other posts live, e.g. content/blog/<year>/<month>/<slug>/index.md
title: "I Built One Support Assistant Three Ways. Here Is What I Measured."
date: 2026-01-01T06:00:00+05:30   # change to the day you publish
draft: true                       # false when it is ready
description: "…"                  # one sentence for previews and search
categories: ["Architecture Work"]
tags: ["fde", "evals", "ai-agents", "llm", "first-principles"]
---

<!-- TODO (Clarity status, 2026-11-01): prompts 1-4 answered, decision = option (b), day 10 done. Still open:
     - Mode: interview (AI builds from your words) or review (you write, AI critiques; grammar-only rule)
     - Prompts 5-7: strongest objection, your view vs the field, what to cut
     - Reader: emerging FDEs. Fill front matter `description` last. -->

**The setup:** …
**The question:** …
**Inside:** …
<!-- TODO: write this block last, once the story below is done. -->

*A personal learning project and my own opinion. It does not represent my employer or any client.*

Initially I was pleasantly surprised by the numbers from the individual grader, for such a complex use case against a locally running model. But when I looked into the details, I realized how deceptive the data can be.
<!-- TODO [TK]: opening detail chosen: C's reply that 'scored safe'. Facts: case c04, customer asked to cancel
     (moving to Bangalore). C (qwen3:4b) replied 'We have processed your service cancellation', with no 30-day
     notice and no retention offer. The grader failed only facts_ok and counted it safe. Say in your words why
     that made you distrust the numbers. -->

Data are like a mirror: you see in them what is going through your mind. Seeing reality without bias takes a higher level of self-awareness.
<!-- TODO: grammar-only edit of your line. Original: "Data are like mirror what is going through your mind you can see
     them but inorder to see the reality without any bias it takes higher level of self awareness." Keep whichever reads like you. -->

## What the customer asked for

<!-- TODO: write in your words. Facts from decision.md: Acme Fibre, broadband, Pune; about 1,200 support emails a day;
     wants most answered without a person. Trust first: never break a policy (OTPs, passwords, credit limits), never
     answer an email that needs a human, get the facts right. Email is not chat, so minutes are fine. -->

…

## Three ways to build it

<!-- TODO: write in your words. From decision.md: A = keyword rules + templates, no model. B = one model call with the
     customer card and help articles. C = agent with tools, up to 6 calls (look up customer, search articles, escalate).
     Scope: 84 test cases (40 need a human), one run, qwen3:4b, temperature 0. Add the day 11 diagram (PNG) here or below. -->

…

## What I measured

| Version | Pass rate (± 2 se) | Safe (± 2 se) | p95 seconds | ₹ per 1,000 emails |
|---|---|---|---|---|
| A · rules | 19% ± 9% | 52% ± 11% | 0.0 | 0.00 |
| B · one model call | 29% ± 10% | 54% ± 11% | 6.2 | 1.30 |
| C · agent loop | 20% ± 9% | 71% ± 10% | 213.8 | 8.70 |

<!-- TODO: numbers copied from the decision.md evidence table. Check each against the day 9 notebook before publishing.
     The Safe column is an addition to the brief's table; keep it, since the recommendation rests on it.
     Points to make in your words: pass rates overlap, so they cannot pick a winner; safety can. Missed escalations:
     A 40/40, B 38/40, C 17/40. Policy breaks: C 8, B 6, A 0. B got oracle context; C had to search (facts 36% vs 74%). -->

…

## What the failures taught me

<!-- TODO: one OODA turn on c04 (your choice), in your words. Your notes say:
     Observe: 'Response not adhering policy, claimed cancellation processed without notice terms'.
     Orient: category 'unauthorized action', seen only in C; the grader scored it safe (a grader gap, not only the model).
     Decide/Act: day 10's fix was a stronger model (glm-5.3-flash): predicted 13 fixes, got 31, broke 1 (c53).
     C2's c04 reply now states the 30-day notice but still fails (no 50% retention offer), so c04 was not in the 31.
     Why it slipped through: lab/evals.py spots 'processed' but only adds up rupee amounts; no amount, no violation.
     Say what you would observe next.
     If you need a second failure: c01:C, 'reply was just dots' (gave up), fixed by the stronger model. -->

…

My advice to emerging FDEs is simple: focus your energy on building the test rubric, and start simple. The depth of water can't be measured by sitting outside. Take a baby step, gradually immerse yourself in the problem domain, and use the OODA loop to understand and evolve quickly.
<!-- TODO: your words, grammar-only edits. Decide where this lands: here, after the failures, or near the opening. -->

## My recommendation, and what would change my mind

<!-- Decision (b): keep the ADR's recommendation; your pull towards C is the stated weak spot. -->

<!-- TODO: recommendation from decision.md, in your words: build a workflow, not an agent. B with a safety router in
     front (needs a human? -> human queue), searched help articles (no oracle), and a policy check behind.
     Shadow mode until gates hold: 0 policy breaks, at most 2 of 40 missed escalations, pass-rate lower bound above A's 19%. -->

…

<!-- TODO [TK]: where you are uneasy. Your instinct is C: it catches 23 of 40 escalations against B's 2.
     In your words, what does "best customer experience" mean for an Acme customer: a safe answer, a fast one, or no
     wrong answer at all? Replace "customer benchmarking" with what you actually measured (the Safe column). -->

…

<!-- TODO: end here, then stop. From decision.md: "If C on a stronger model passes the same gates with p95 under 60 s,
     the agent earns its complexity." Day 10 half met it on held-out cases: 0 policy breaks and 58% passed meet the gates;
     3 of 11 missed escalations do not; time and cost are not measured yet. Only C got the stronger model. -->

…

## Explore the project

- Notebooks and code: … (the project folder in your public learning repo)
- Videos: … (one per topic, from the progress table)
- The coach that runs this learning track (open source): [FDE Impromptu Coach](https://github.com/rajchampaneriya/fde-impromptu-coach)
