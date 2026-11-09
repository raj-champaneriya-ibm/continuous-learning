# View of 1-measure-before-you-believe/09-success-cost-latency/day9-success-cost-latency.drawio (draw.io diagram: labelled shapes, then labelled connectors)

## Page: Day 9 · Success, cost, latency
- [shape t1] Day 9 · Is the extra intelligence worth its price and its wait?
- [shape t2] Same emails, same grader. Three versions, three numbers: success, cost, latency.
- [shape p1t] 1 · What we are doing
- [shape e] 84 test emails
cases.jsonl
- [shape va] A · rules, no model
- [shape vb] B · one model call
- [shape vc] C · agent loop
up to 6 model calls
- [shape m] For every email we record
reply · tokens in · tokens out · seconds
- [shape g] grader
pass or fail
- [shape tb] One table per version

success: pass rate ± 2 SE
latency: median and p95 seconds
cost: ₹ per 1,000 emails
value: ₹ per correct reply
- [shape d] Which version
would you ship?
- [shape p2t] 2 · Latency: why p95 and not the average
- [shape bcap] 10 emails, sorted by seconds
- [shape lmed] median
rank 5
- [shape lp95] p95
rank 10
- [shape n1] Nearest rank: sort the times, take the value at rank q% of n
- [shape n2] Few cases decide the tail: p95 is rank 80 of 84, the 4 slowest emails set it.
- [shape n3] Counted: model calls on this Mac.Not counted: tool time, network, queues, cold start.
- [shape n4] For email, seconds decide capacity (1,200 a day on one machine), not customer happiness.
- [shape p3t] 3 · What really drives the cost of one resolved email
- [shape p3l] Thick border = usually the biggest share · Dashed = not counted
- [shape hub] ₹ per
resolved email
- [shape hubn] Version A shows ₹0 for tokens, yet it still pays for hosting, rule upkeep and escalations.
- [shape gtlt] Measured today, in the notebook
- [shape c11] tokens in (prompt, tools, history)
- [shape c12] tokens out (the reply)
- [shape c13] price per million tokens
- [shape c14] rupees per US dollar
- [shape c15] model calls per email (agent steps)
- [shape c16] pass rate (spreads cost of failures)
- [shape gtrt] Hidden inside today's estimate
- [shape c21] paid model counts tokens differently
- [shape c22] retries, timeouts, bad JSON
- [shape c23] hidden reasoning tokens
- [shape c24] history grows in long conversations
- [shape c25] cached-prompt and batch discounts
- [shape c26] exchange rate moves, GST on invoices
- [shape gblt] Per email, beyond tokens
- [shape c31] staff time on escalations
- [shape c32] wrong answers: refunds, complaints, churn
- [shape c33] guardrail and judge calls
- [shape c34] help-article search, embeddings
- [shape c35] human review of drafts
- [shape gbrt] Fixed month cost, spread over all emails
- [shape c41] hosting: API, GPU or Mac
- [shape c42] database, logs and traces
- [shape c43] engineers: prompt and rule upkeep
- [shape c44] eval re-runs and expert labels
- [shape c45] monitoring and alerts
- [shape c46] personal-data compliance
- [shape p4t] 4 · Levers to pull, and check each one against the pass rate
- [shape l1] fewer agent steps
- [shape l2] shorter prompts and tool lists
- [shape l3] smaller or cheaper model
- [shape l4] cache repeated prompts
- [shape l5] send easy emails routed to rules
- [shape l6] escalate less, only where safe
- [shape q] Which version would you ship today, and what number would change your mind?
- [arrow]: "84 test emails
cases.jsonl" -> "A · rules, no model"
- [arrow]: "84 test emails
cases.jsonl" -> "B · one model call"
- [arrow]: "84 test emails
cases.jsonl" -> "C · agent loop
up to 6 model calls"
- [arrow]: "A · rules, no model" -> "For every email we record
reply · tokens in · tokens out · seconds"
- [arrow]: "B · one model call" -> "For every email we record
reply · tokens in · tokens out · seconds"
- [arrow]: "C · agent loop
up to 6 model calls" -> "For every email we record
reply · tokens in · tokens out · seconds"
- [arrow]: "For every email we record
reply · tokens in · tokens out · seconds" -> "grader
pass or fail"
- [arrow]: "grader
pass or fail" -> "One table per version

success: pass rate ± 2 SE
latency: median and p95 seconds"
- [arrow]: "One table per version

success: pass rate ± 2 SE
latency: median and p95 seconds" -> "Which version
would you ship?"
- [arrow]: "" -> "₹ per
resolved email"
- [arrow]: "" -> "₹ per
resolved email"
- [arrow]: "" -> "₹ per
resolved email"
- [arrow]: "" -> "₹ per
resolved email"
