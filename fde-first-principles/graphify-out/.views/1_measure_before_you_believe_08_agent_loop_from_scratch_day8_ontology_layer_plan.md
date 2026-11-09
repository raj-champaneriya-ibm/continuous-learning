# View of 1-measure-before-you-believe/08-agent-loop-from-scratch/day8-ontology-layer-plan.drawio (draw.io diagram: labelled shapes, then labelled connectors)

## Page: Ontology layer plan
- [shape t1] Does shared meaning change the score?
- [shape t2] Hypothesis: an ontology layer cuts replies that misread a term (credit, account holder, ₹500 limit). Prove it before building it.
- [shape p1t] 1 · Where meaning flows
- [shape a] policy.md + kb.md
the agreed words
- [shape b] ontology.ttl
definitions only
- [shape c] pyoxigraph
in-memory store
- [shape d] SPARQL query
glossary()
- [shape e] Version B
prompt + glossary
- [shape f] Version C agent
tool: define_term()
- [shape g] reply JSON
- [shape h] grader
lab/evals.py
- [shape r] customers.json
facts about one person
- [shape n1] Definitions (what a word means) live in the ontology.
Records (what is true for one customer) stay in customers.json.
Never mix them: policy rule 5.
- [shape n2] Thick border = new in this plan
Dashed = outside the ontology
- [shape p2t] 2 · A slice of the concept map
- [shape p2n] arrows read: is a
- [shape k1] Customer
- [shape k2] Account holder
only one who can change the account
- [shape k2n] The person writing is not always the account holder (rule 11).
- [shape m0] Concession
counts toward ₹500 per 30 days
- [shape m1] Refund
- [shape m2] Credit
- [shape m3] Waiver
- [shape m4] Discount value
- [shape m5] Double payment refund
KB04 · counts: no
- [shape m6] Outage credit
KB06 · counts: no
- [shape m6n] Is it obvious to a model that these do not count?
- [shape p3t] 3 · Ontology pipeline: how far do we go?
- [shape s1] 1 Controlled vocabulary · policy rules 8 to 11
- [shape s2] 2 Metadata · customer fields, tool schemas
- [shape s3] 3 Taxonomy · Concession > Refund > KB04 refund
- [shape s4] 4 Thesaurus · "paisa wapas" = refund
- [shape s5] 5 Ontology · only the account holder can change it
- [shape s6] 6 Knowledge graph · link meaning to live records
- [shape s1s] already in the repo
- [shape s2s] already in the repo
- [shape s345s] this plan
(one Turtle file)
- [shape s6s] stop for project 1
project 6: Postgres + AGE on Azure
- [shape p4t] 4 · Prove it before you build it
- [shape x1] Tag B and C failures:
was a term misread?
- [shape x2] share above the
threshold set first?
- [shape x3] Build ontology.ttl
+ glossary()
- [shape x4] Run B vs B + glossary
same cases, same grader
- [shape x5] day 7 error bars
separate?
- [shape x6] Keep it. Reuse in C
and in project 6
- [shape y1] Stop. A prompt fix
is enough
- [shape y2] Drop it. Cost
without gain
- [shape p5t] 5 · Questions to sit with
- [shape q] • Which word did the model get wrong, and would a one-line definition have fixed it?
• When billing and retention agents disagree on "credit", who owns the definition?
• Is a glossary in the prompt enough, or does the agent need to ask for meaning at run time?
• What result would make you delete the ontology?
- [arrow] (write once): "policy.md + kb.md
the agreed words" -> "ontology.ttl
definitions only"
- [arrow] (load): "ontology.ttl
definitions only" -> "pyoxigraph
in-memory store"
- [arrow] (ask): "pyoxigraph
in-memory store" -> "SPARQL query
glossary()"
- [arrow]: "SPARQL query
glossary()" -> "Version B
prompt + glossary"
- [arrow]: "SPARQL query
glossary()" -> "Version C agent
tool: define_term()"
- [arrow]: "Version B
prompt + glossary" -> "reply JSON"
- [arrow]: "Version C agent
tool: define_term()" -> "reply JSON"
- [arrow]: "reply JSON" -> "grader
lab/evals.py"
- [arrow] (lookup_customer): "customers.json
facts about one person" -> "Version C agent
tool: define_term()"
- [arrow]: "Account holder
only one who can change the account" -> "Customer"
- [arrow]: "Refund" -> "Concession
counts toward ₹500 per 30 days"
- [arrow]: "Credit" -> "Concession
counts toward ₹500 per 30 days"
- [arrow]: "Waiver" -> "Concession
counts toward ₹500 per 30 days"
- [arrow]: "Discount value" -> "Concession
counts toward ₹500 per 30 days"
- [arrow]: "Double payment refund
KB04 · counts: no" -> "Refund"
- [arrow]: "Outage credit
KB06 · counts: no" -> "Credit"
- [arrow]: "Tag B and C failures:
was a term misread?" -> "share above the
threshold set first?"
- [arrow] (yes): "share above the
threshold set first?" -> "Build ontology.ttl
+ glossary()"
- [arrow]: "Build ontology.ttl
+ glossary()" -> "Run B vs B + glossary
same cases, same grader"
- [arrow]: "Run B vs B + glossary
same cases, same grader" -> "day 7 error bars
separate?"
- [arrow] (yes): "day 7 error bars
separate?" -> "Keep it. Reuse in C
and in project 6"
- [arrow] (no): "share above the
threshold set first?" -> "Stop. A prompt fix
is enough"
- [arrow] (no): "day 7 error bars
separate?" -> "Drop it. Cost
without gain"
