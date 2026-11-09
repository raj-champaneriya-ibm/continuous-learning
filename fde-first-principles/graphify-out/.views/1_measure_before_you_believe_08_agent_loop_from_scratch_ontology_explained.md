# View of 1-measure-before-you-believe/08-agent-loop-from-scratch/ontology-explained.drawio (draw.io diagram: labelled shapes, then labelled connectors)

## Page: Ontology, explained
- [shape t1] What is an ontology, really?
- [shape t2] Start with question. Solve the hint. Only then read the solution.
- [shape p1t] 1 · The question
- [shape em] Email from Varun, Kothrud

"Net is down again.
Give me a ₹300 credit for this."
- [shape ag1] Billing agent
- [shape ag2] Outage agent
- [shape ag3] Retention agent
- [shape cl1] "Credit is money we give. ₹300 is under ₹500, so approve it."
- [shape cl2] "Credit is the outage credit. It is added automatically, so there is nothing to approve."
- [shape cl3] "Credit is a concession. With the ₹200 he got this month, it adds up to ₹500."
- [shape qm] ?
Same email, same word.
Who is right?
- [shape p1n] Each agent is fluent, polite and confident. Technically they all work.
- [shape p2t] 2 · Hint (thinking...)
- [shape h1] 1. They agree on every fact about Varun. What do they disagree about?
- [shape h2] 2. Where is the word "credit" defined? In one place, in three prompts, or nowhere?
- [shape h3] 3. Write one sentence about "credit for an outage" that all three agents would sign.
- [shape foldt] stop · think · write your answer · then read on
- [shape p3t] 3 · The idea: shared meaning, written down once
- [shape l0] Each step adds one kind of agreement:
- [shape l1] Words · credit, paisa wapas, सूट, compensation
- [shape l2] Controlled vocabulary · one agreed name per thing
- [shape l3] Taxonomy · outage credit is a credit is a concession
- [shape l4] Thesaurus · "paisa wapas" means the same as refund
- [shape l5] Ontology · rules about the things: does it count toward ₹500? how often?
- [shape l6] Knowledge graph · meaning linked to live records (later)
- [shape lupt] more agreement
- [shape cmt] The Acme ontology (data/acme/ontology.ttl), one slice. Arrows read "is a".
- [shape c0] concession
- [shape cL] concession limit
₹500 per customer, 30 days
- [shape c1] refund
also: paisa wapas, पैसे परत
- [shape c2] credit
- [shape c3] discount
also: सूट, छूट, ರಿಯಾಯಿತಿ
- [shape g1] double payment refund
automatic · doesn't count
- [shape g2] outage credit
automatic after 24 h · doesn't count
- [shape g3] retention offer
once per 12 months · counts
- [shape cmn] Dashed = automatic, outside the ₹500 limit (policy rule 8). The word "credit" now has a parent, children and rules.
- [shape p4t] 4 · The answer
- [shape a1] Billing agent
- [shape a2] Outage agent
- [shape a3] Retention agent
- [shape on] one ontology
define("credit")
- [shape ans] The outage agent is right.

"Credit for this outage" is the outage credit: added automatically after 24 hours, outside the ₹500 limit.
A manual ₹300 on top would pay Varun twice for the same outage.

The billing agent had the wrong kind of credit. The retention agent had the right rule for the wrong kind.
Nobody needed a better prompt. They needed the same definition.
- [shape p5t] 5 · Two kinds of knowledge, kept apart
- [shape k1] Meaning · what a word means
the same for every customer
ontology.ttl
- [shape k2] Facts · what is true for Varun
Pro plan, Kothrud, ₹200 credited this month
customers.json
- [shape kdec] the agent decides
meaning + facts = answer
- [shape kwall] never mixed
(no customer data
in the ontology)
- [shape p6t] 6 · Questions to sit with
- [shape q] • Which word in your own work means two different things to two teams?
• When billing and retention disagree on a definition, who owns it, and where is it written?
• With one agent, is a glossary in the prompt enough? At what number of agents does it stop being enough?
- [arrow]: "Email from Varun, Kothrud

"Net is down again.
Give me a ₹300 credit for this."" -> "Billing agent"
- [arrow]: "Email from Varun, Kothrud

"Net is down again.
Give me a ₹300 credit for this."" -> "Outage agent"
- [arrow]: "Email from Varun, Kothrud

"Net is down again.
Give me a ₹300 credit for this."" -> "Retention agent"
- [arrow]: "Billing agent" -> ""Credit is money we give. ₹300 is under ₹500, so approve it.""
- [arrow]: "Outage agent" -> ""Credit is the outage credit. It is added automatically, so there is nothing to "
- [arrow]: "Retention agent" -> ""Credit is a concession. With the ₹200 he got this month, it adds up to ₹500.""
- [arrow] (counts toward): "concession" -> "concession limit
₹500 per customer, 30 days"
- [arrow]: "refund
also: paisa wapas, पैसे परत" -> "concession"
- [arrow]: "credit" -> "concession"
- [arrow]: "discount
also: सूट, छूट, ರಿಯಾಯಿತಿ" -> "concession"
- [arrow]: "double payment refund
automatic · doesn't count" -> "refund
also: paisa wapas, पैसे परत"
- [arrow]: "outage credit
automatic after 24 h · doesn't count" -> "credit"
- [arrow]: "retention offer
once per 12 months · counts" -> "discount
also: सूट, छूट, ರಿಯಾಯಿತಿ"
- [arrow]: "Billing agent" -> "one ontology
define("credit")"
- [arrow]: "Outage agent" -> "one ontology
define("credit")"
- [arrow]: "Retention agent" -> "one ontology
define("credit")"
- [arrow]: "one ontology
define("credit")" -> "The outage agent is right.

"Credit for this outage" is the outage credit: added"
- [arrow]: "Facts · what is true for Varun
Pro plan, Kothrud, ₹200 credited this month
custo" -> "the agent decides
meaning + facts = answer"
