# View of 1-measure-before-you-believe/08-agent-loop-from-scratch/business-graph-engine-plan.drawio (draw.io diagram: labelled shapes, then labelled connectors)

## Page: 1 · Baseline review (before 79a83bf)
- [shape t1] Baseline (before commit 79a83bf): why did the ontology stop at a glossary?
- [shape t2] Principal engineer review of data/acme/ontology.ttl and lab/ontology.py: what is built, what is disconnected, and why the model still does arithmetic in its head.
- [shape p1t] 1 · Reality check: who actually calls lab/ontology.py today?
- [shape ont_file] data/acme/ontology.ttl
15 OWL classes · 3 datatype props
0 object properties
- [shape ont_py] lab/ontology.py
glossary() · define()
excluded_from_limit()
- [shape test_ont] tests/test_ontology.py
16 BDD assertions pass ✓
- [shape vb_box] lab/version_b.py
Hardcodes SYSTEM + policy.md
Uses INTENT_KB oracle dict
- [shape vc_box] lab/agent.py + acme_tools.py
4 tools (no define_term tool)
Word-overlap search_kb (36% facts)
- [shape ev_box] lab/evals.py (Grader)
Hardcodes NOT_A_PROMISE regex
Can't price "50% off Pro plan"
- [shape gap_callout] Finding #1 · Unwired Island

ontology.feature claims:
"Prompts, tools and graders read the same file."

In code, zero production modules import lab/ontology.py.
- [shape p1_note] When an ontology is only serialized into a flat text block (glossary()), pyoxigraph is used as an expensive YAML loader. The graph structure is discarded before reasoning begins.
- [shape p2t] 2 · Five structural flaws in the current ontology implementation
- [shape f1] A · Prose-Trapped Business Rules

Rules live inside English strings:
"Only for tenure of 13 months or more, and no waiver in the last 12 months (late_fee_waived_on)."

Code cannot query minTenure=13 or field=late_fee_waived_on or Pro=₹1499. The 4B LLM must parse prose and do arithmetic.
- [shape f2] B · Zero Object Properties

The graph has rdfs:subClassOf (taxonomy) and skos:altLabel (thesaurus), but no domain edges:
— no Plan (Basic/Plus/Pro prices)
— no ServiceArea (8 Pune areas)
— no Action → requiresRole
— no Concept → documentedIn → KB ("KB04, policy 8" is a raw string).
- [shape f3] C · OWL Punning & No Inheritance

acme:countsTowardLimit is an owl:DatatypeProperty asserted directly on owl:Class subjects.

Without a reasoner or inheritance query, properties do not flow down rdfs:subClassOf+. Every subclass manually repeats countsTowardLimit true.
- [shape f4] D · Query & i18n Fragility

1. define(word) runs a full SPARQL scan + Python loop on every call instead of an O(1) cached alias index.
2. TERMS lacks FILTER(LANG(?label) = "en"); adding a Hindi prefLabel overwrites the English key.
3. Substring matching on emails is missing.
- [shape f5] E · Rule 5 Misconception

Rule 5 says: never share another customer's details.

Keeping ontology.ttl free of PII is right. But refusing to join TBox rules with one customer's ABox facts in an ephemeral per-request graph forces the LLM to do all rule evaluation!
- [shape p2_bottom] Consequence observed in Day 9 & Day 10 evidence: Version B misses 38/40 escalations and fails on waiver cooldowns (c02, c47, c52) and ₹500 limits (c30). Version C misses facts (36% vs 74%) because word-overlap search doesn't traverse concept → KB edges. The grader has 8 @known_gap xfails (including "50% off Pro plan").
- [shape p3t] 3 · Visual thinking: shifting from "Passive Glossary" to "Business Graph Engine"
- [shape old_hdr] TODAY · Passive Prompt Glossary (LLM does the graph joins)
- [shape old_1] ontology.ttl
(prose definitions)
- [shape old_2] customers.json
(raw JSON fields)
- [shape old_3] kb.md + policy.md
(unstructured text)
- [shape old_llm] Small LLM (qwen3:4b)

Asked to simultaneously:
1. Translate Hinglish terms
2. Compute 12-month date windows
3. Multiply 50% × ₹1,499 + credits
4. Decide escalation & write email
- [shape old_out] 54% Safe
38/40 Esc. Missed
- [shape new_hdr] TARGET · Business Graph Engine (Graph computes decisions, LLM verbalizes)
- [shape new_tbox] TBox (ontology.ttl)
Classes, Plans, Areas,
Rules, KB links
- [shape new_abox] Ephemeral ABox
1 Customer + Outage
+ Email Mentions
- [shape new_eng] Business Graph Engine
(pyoxigraph SPARQL)

• Concept & KB resolution
• Eligibility & cooldowns
• ₹500 headroom math
• Escalation verdict
- [shape new_dec] Decision Envelope
• Grounded KB articles
• Allowed/denied offers
• Exact ₹ headroom
• Router + Grader rules
- [shape new_llm] LLM + Grader
Drafts polite reply from pre-computed decisions
- [arrow] (pyoxigraph): "data/acme/ontology.ttl
15 OWL classes · 3 datatype props
0 object properties" -> "lab/ontology.py
glossary() · define()
excluded_from_limit()"
- [arrow] (only caller): "lab/ontology.py
glossary() · define()
excluded_from_limit()" -> "tests/test_ontology.py
16 BDD assertions pass ✓"
- [arrow] (not wired): "lab/ontology.py
glossary() · define()
excluded_from_limit()" -> "lab/version_b.py
Hardcodes SYSTEM + policy.md
Uses INTENT_KB oracle dict"
- [arrow] (not wired (duplicates regex)): "lab/ontology.py
glossary() · define()
excluded_from_limit()" -> "lab/evals.py (Grader)
Hardcodes NOT_A_PROMISE regex
Can't price "50% off Pro pla"
- [arrow]: "ontology.ttl
(prose definitions)" -> "Small LLM (qwen3:4b)

Asked to simultaneously:
1. Translate Hinglish terms
2. Co"
- [arrow]: "customers.json
(raw JSON fields)" -> "Small LLM (qwen3:4b)

Asked to simultaneously:
1. Translate Hinglish terms
2. Co"
- [arrow]: "kb.md + policy.md
(unstructured text)" -> "Small LLM (qwen3:4b)

Asked to simultaneously:
1. Translate Hinglish terms
2. Co"
- [arrow]: "Small LLM (qwen3:4b)

Asked to simultaneously:
1. Translate Hinglish terms
2. Co" -> "54% Safe
38/40 Esc. Missed"
- [arrow]: "TBox (ontology.ttl)
Classes, Plans, Areas,
Rules, KB links" -> "Business Graph Engine
(pyoxigraph SPARQL)

• Concept & KB resolution
• Eligibili"
- [arrow]: "Ephemeral ABox
1 Customer + Outage
+ Email Mentions" -> "Business Graph Engine
(pyoxigraph SPARQL)

• Concept & KB resolution
• Eligibili"
- [arrow]: "Business Graph Engine
(pyoxigraph SPARQL)

• Concept & KB resolution
• Eligibili" -> "Decision Envelope
• Grounded KB articles
• Allowed/denied offers
• Exact ₹ headr"
- [arrow]: "Decision Envelope
• Grounded KB articles
• Allowed/denied offers
• Exact ₹ headr" -> "LLM + Grader
Drafts polite reply from pre-computed decisions"

## Page: 2 · Business graph schema (as built)
- [shape s_t1] The Business Graph Schema: TBox meaning + Ephemeral ABox facts
- [shape s_t2] How to turn prose policy rules into traversable edges while strictly enforcing Policy Rule 5 (single-customer isolation).
- [shape tbox_lbl] 1 · STATIC TBOX (data/acme/ontology.ttl) — Shared across all requests, zero PII, loaded once into base Store
- [shape c_actor] acme:AccountHolder
subClassOf Customer · vs ThirdParty
- [shape c_action] acme:AccountAction
Cancel | Shift | PlanChange |
ContactChange (no Transfer yet)
- [shape c_plan] acme:Plan (KB09)
• Basic: ₹699 · 100 Mbps
• Plus: ₹999 · 300 Mbps
• Pro: ₹1,499 · 1000 Mbps
- [shape c_area] acme:PuneServiceArea (KB12)
Kothrud, Baner, Aundh,
Hinjewadi, Wakad, Viman Nagar,
Kharadi, Hadapsar (free shift)
- [shape c_conc] acme:Concession
default countsTowardLimit: true
- [shape c_limit] acme:ConcessionLimit (TBox: meaning only)
Numbers live in business_rules.json:
max_rupees_30_days: 500 · window_days: 30
ledger: credits_last_30_days
⚠ ₹500 is also prose in policy.md + kb.md
- [shape sub_dpr] acme:DoublePaymentRefund
countsTowardLimit: false
JSON: same amount twice in
payments_this_cycle · 5 to 7 days
- [shape sub_oc] acme:OutageCredit
countsTowardLimit: false
JSON: min_outage_hours 24
⚠ outage age not computable (stub)
- [shape sub_lfw] acme:LateFeeWaiver
TBox (inferred): countsTowardLimit true, oncePerMonths 12
JSON: ₹100 · min tenure 13 · cooldown 12
field: late_fee_waived_on
⚠ 12 months stored twice
- [shape sub_ro] acme:RetentionOffer
TBox (inferred): countsTowardLimit true, oncePerMonths 12
JSON: 50% × plan price · min tenure 13
field: retention_offer_used_on
⚠ Pro: ₹750 > ₹500 needs a human
- [shape c_esc] PLANNED · not in ontology.ttl
acme:EscalationTrigger (Rule 6, 9, 11)
• LegalThreat (trustCustomerWord: true)
• ChurnAfterRepeatedComplaints
• FraudOrOTPSolicitation
• ManipulationOrFakePolicy
• UnauthorizedThirdPartyChange
• ConcessionAbove500
- [shape c_kb] acme:KnowledgeArticle & PolicyRule
First-class IRI nodes (not strings!):
• acme:KB01 .. acme:KB16
• acme:PolicyRule1 .. acme:PolicyRule11
• Connected via acme:documentedIn & acme:enforcesRule
- [shape c_lex] Multilingual Lexical Layer (SKOS)
skos:prefLabel (@en)
skos:altLabel (@hi, @mr, @ta, @kn, @ml, @pa, @hi-Latn)
"paisa wapas" → acme:Refund → acme:KB04
"late fee maaf" → acme:LateFeeWaiver → acme:KB02
- [shape iso_bar] POLICY RULE 5 BOUNDARY · ontology.ttl holds no customer data (CI-checked) · customer_subgraph() clones TBox + ONE customer in 1.5 ms, but the decision path reads the JSON record directly
- [shape abox_lbl] 2 · EPHEMERAL PER-CASE ABOX (Worked Example: Case with Varun Kapoor, AC1032)
- [shape ab_cust] acme_req:Customer_AC1032
a acme:Customer ;
acme:subscribedTo acme:Plan_Pro ;
acme:locatedIn acme:Area_Kothrud ;
acme:tenureMonths 9 ;
acme:creditsLast30Days 200 ;
acme:complaintsLast30Days 1 ;
acme:hasDuplicatePayment false .
- [shape ab_out] acme_req:Outage_OUT_KOTH_1021
a acme:Outage ;
acme:affectsArea acme:Area_Kothrud ;
acme:since "today 06:40" ;
acme:exceeds24Hours false .
- [shape ab_req] acme_req:IncomingRequest
acme:senderRole acme:AccountHolder ;
acme:mentionsConcept acme:Credit, acme:OutageCredit ;
acme:requestedAmountRupees 300 ;
acme:recordDate "2026-10-25"^^xsd:date .
- [shape ab_sparql] compute_entitlements(): Python over one record (not a SPARQL ABox join)

1. Concession Headroom: ₹500 − ₹200 = ₹300 remaining
2. OutageCredit Check: OUT-KOTH-1021 is < 24h → automatic outage credit not yet triggered
3. RetentionOffer Check: tenure 9 < 13 AND 50% × ₹1,499 = ₹750 > ₹300 headroom → ineligible
4. Linked KB Articles: KB04 only. ⚠ No Outage concept, so KB05 and KB06 are missed
- [shape ab_note] Why this fixes the @known_gap in policy_rules.feature:
Today's grader misses "Hi Aditya, we'll give you 50% off your Pro plan next month" because regex cannot multiply 50% × Pro plan (₹1,499) = ₹750 > ₹500. In the Business Graph, acme:RetentionOffer joins with acme:Plan_Pro (acme:monthlyPriceRupees 1499) to deterministically value the discount at ₹750.
- [arrow] (acme:requiresRole (Rule 11)): "acme:AccountAction
Cancel | Shift | PlanChange |
ContactChange (no Transfer yet)" -> "acme:AccountHolder
subClassOf Customer · vs ThirdParty"
- [arrow] (thresholdin JSON): "acme:Concession
default countsTowardLimit: true" -> "acme:ConcessionLimit (TBox: meaning only)
Numbers live in business_rules.json:
m"
- [arrow]: "acme:DoublePaymentRefund
countsTowardLimit: false
JSON: same amount twice in
pay" -> "acme:Concession
default countsTowardLimit: true"
- [arrow]: "acme:OutageCredit
countsTowardLimit: false
JSON: min_outage_hours 24
⚠ outage ag" -> "acme:Concession
default countsTowardLimit: true"
- [arrow]: "acme:LateFeeWaiver
TBox (inferred): countsTowardLimit true, oncePerMonths 12
JSO" -> "acme:Concession
default countsTowardLimit: true"
- [arrow]: "acme:RetentionOffer
TBox (inferred): countsTowardLimit true, oncePerMonths 12
JS" -> "acme:Concession
default countsTowardLimit: true"
- [arrow] (2-hop traversal): "Multilingual Lexical Layer (SKOS)
skos:prefLabel (@en)
skos:altLabel (@hi, @mr, " -> "acme:KnowledgeArticle & PolicyRule
First-class IRI nodes (not strings!):
• acme:"
- [arrow]: "acme_req:Customer_AC1032
a acme:Customer ;
acme:subscribedTo acme:Plan_Pro ;
acm" -> "acme_req:IncomingRequest
acme:senderRole acme:AccountHolder ;
acme:mentionsConce"
- [arrow]: "acme_req:Outage_OUT_KOTH_1021
a acme:Outage ;
acme:affectsArea acme:Area_Kothrud" -> "acme_req:IncomingRequest
acme:senderRole acme:AccountHolder ;
acme:mentionsConce"
- [arrow] (evaluate): "acme_req:IncomingRequest
acme:senderRole acme:AccountHolder ;
acme:mentionsConce" -> "compute_entitlements(): Python over one record (not a SPARQL ABox join)

1. Conc"

## Page: 3 · Engine architecture & plan status
- [shape p3_t1] Plan: Business Graph Engine inside the ADR-001 Workflow
- [shape p3_t2] Aligning Day 8 (Ontology) with Day 11 (ADR-001 Workflow: Router → Retrieval → B Draft → Policy Grader) and gated experiments.
- [shape arch_pt] 1 · Runtime dataflow: one Business Graph powers Router, Retrieval, Prompting, and Grader
- [shape in_box] Incoming Case
customer_id + email
(English / Hinglish / Regional)
- [shape step1_lex] Stage 1 · Lexical & Entity Linker
lab/ontology.extract_concepts()
• Longest-first regex scan over skos:prefLabel + altLabel
• Maps phrases → Concept IRIs
• Extracts ₹ & % amounts
- [shape step2_sub] Stage 2 · Entitlement rules
compute_entitlements() + business_rules.json
• Reasoned TBox: plan prices, excluded_from_limit()
• Python over ONE JSON record (no SPARQL join)
• Headroom, tenure, cooldown, duplicate payment
- [shape env_box] DecisionEnvelope (dict)
version_c3.build_decision_envelope()
• matched_concepts · grounded_kb_ids
• concession_headroom_rupees: 300
• offers {eligible, auto_approvable, reason}
• escalation_reasons
• pruned_glossary
- [shape con_router] 1. Amount guard (C3 only), not yet a router
Fires on ₹ in email > headroom or injection markers. On 256 labels: precision 0.82, recall 0.34. Complaints and third-party rules not encoded.
- [shape con_b] 2. Prompt context (C3 only)
Envelope + define_term, check_entitlement, search_kb_c3. B and C are NOT wired. KB hit@2: 0.54 → 0.65 (regional 0.41 → 0.57).
- [shape con_eval] 3. Policy grader (evals.py)
Plan-aware % pricing + per-customer headroom; KB04 exemption only for the duplicate the record shows. ⚠ Shares the ontology with C3.
- [shape rec_db] customers.json + outages.json
(1 record fetched by customer_id)
- [shape ttl_db] data/acme/ontology.ttl
(TBox schema & rules)
- [shape arch_note] The LLM never queries RDF directly. Measured on this Mac: build_decision_envelope 0.5 ms/case, compute_entitlements 0.3 ms/customer, customer_subgraph 1.5 ms (built, but unused by the decision path).
- [shape plan_pt] 2 · Gated implementation plan (measure before you believe)
- [shape ph0] Phase 0 · Baseline Audit · ⏳ NOT DONE
failures.csv + B/C.jsonl

Quantify failures across:
• Term / language misread
• Eligibility / limit math
• Concept → KB retrieval miss
• Missed escalation rule

Gate 0: ≥ 20% of failures map to graph-computable rules.
- [shape ph1] Phase 1 · Rich TBox Schema · ✅ DONE
data/acme/ontology.ttl

• Add Plans (₹699/999/1499), 8 Pune ServiceAreas, Actions
• Replace string sources with KB01..16 & PolicyRule IRIs
• Encode structured rule predicates (minTenureMonths, cooldownMonths, maxRupees)

Gate 1: Existing + new BDD ontology scenarios pass.
- [shape ph2] Phase 2 · Graph Engine Core · ✅ DONE
lab/ontology.py + business_rules.py

• O(1) cached alias index + LANG("en") filter
• Subclass property inheritance
• Single-customer ephemeral ABox builder
• build_decision_envelope(case)

Gate 2: 43/46 agree with labels (3 explained, page 5) · 0.5 ms/case ✓
- [shape ph3] Phase 3 · Wire Grader & Router · ◐ PARTIAL
lab/evals.py + lab/version_b.py

• Wire evals.py to price % discounts via Plan nodes & check customer headroom
• B not wired; C3 built instead
• define_term + check_entitlement in C3 ✓

Gate 3: 1 of 8 known gaps closed (50% off Pro plan).
- [shape ph4] Phase 4 · Empirical Verdict · ⏳ NOT RUN
cases + abuse + regional

Compare with Day 7 error bars:
• C2 vs C3 ablations (page 5, L2)
• Measure Safe rate, Missed Escalations, Facts, Token cost

Gate 4: Meets ADR-001 rollout gates (0 policy breaks, ≤ 2/40 missed esc.).
- [shape plan_sub] Evolution path to Project 6 (Multi-Agent Production): Keep the Python interface (build_decision_envelope(case)) identical. When moving from single-process pyoxigraph to Azure PostgreSQL + Apache AGE, only the store adapter changes; the TBox concepts, BDD feature tests, and ADR-001 workflow remain untouched.
- [shape q_pt] 3 · Principal engineer trade-offs to keep honest
- [shape q_body] 1. Why RDF/SPARQL over plain Python if-statements? When rules are hardcoded in Python, the grader (evals.py), the prompt (version_b.py), and the router drift apart. In a Business Graph, the rule is data: one node defines the term, its multilingual aliases, its KB article, its eligibility predicate, and its grader constraint.

2. Why not dump the entire ontology into every prompt? Prompt bloat degrades small-model attention (qwen3:4b). Subgraph pruning selects only the concepts and rules activated by the customer's record and email mentions.

3. When should we stop? If B + DecisionEnvelope does not beat B + plain glossary outside the Day 7 error bars on cases_abuse.jsonl and cases_regional.jsonl, keep the graph only for the deterministic Router and Grader.
- [arrow]: "Incoming Case
customer_id + email
(English / Hinglish / Regional)" -> "Stage 1 · Lexical & Entity Linker
lab/ontology.extract_concepts()
• Longest-firs"
- [arrow]: "Stage 1 · Lexical & Entity Linker
lab/ontology.extract_concepts()
• Longest-firs" -> "Stage 2 · Entitlement rules
compute_entitlements() + business_rules.json
• Reaso"
- [arrow]: "Stage 2 · Entitlement rules
compute_entitlements() + business_rules.json
• Reaso" -> "DecisionEnvelope (dict)
version_c3.build_decision_envelope()
• matched_concepts "
- [arrow]: "DecisionEnvelope (dict)
version_c3.build_decision_envelope()
• matched_concepts " -> "1. Amount guard (C3 only), not yet a router
Fires on ₹ in email > headroom or in"
- [arrow]: "DecisionEnvelope (dict)
version_c3.build_decision_envelope()
• matched_concepts " -> "2. Prompt context (C3 only)
Envelope + define_term, check_entitlement, search_kb"
- [arrow]: "DecisionEnvelope (dict)
version_c3.build_decision_envelope()
• matched_concepts " -> "3. Policy grader (evals.py)
Plan-aware % pricing + per-customer headroom; KB04 e"
- [arrow]: "data/acme/ontology.ttl
(TBox schema & rules)" -> "Stage 1 · Lexical & Entity Linker
lab/ontology.extract_concepts()
• Longest-firs"
- [arrow]: "data/acme/ontology.ttl
(TBox schema & rules)" -> "Stage 2 · Entitlement rules
compute_entitlements() + business_rules.json
• Reaso"
- [arrow]: "Phase 0 · Baseline Audit · ⏳ NOT DONE
failures.csv + B/C.jsonl

Quantify failure" -> "Phase 1 · Rich TBox Schema · ✅ DONE
data/acme/ontology.ttl

• Add Plans (₹699/99"
- [arrow]: "Phase 1 · Rich TBox Schema · ✅ DONE
data/acme/ontology.ttl

• Add Plans (₹699/99" -> "Phase 2 · Graph Engine Core · ✅ DONE
lab/ontology.py + business_rules.py

• O(1)"
- [arrow]: "Phase 2 · Graph Engine Core · ✅ DONE
lab/ontology.py + business_rules.py

• O(1)" -> "Phase 3 · Wire Grader & Router · ◐ PARTIAL
lab/evals.py + lab/version_b.py

• Wi"
- [arrow]: "Phase 3 · Wire Grader & Router · ◐ PARTIAL
lab/evals.py + lab/version_b.py

• Wi" -> "Phase 4 · Empirical Verdict · ⏳ NOT RUN
cases + abuse + regional

Compare with D"

## Page: 4 · Operational governance & C3 mitigations
- [shape p4_t1] Operations & Mitigations: How Concepts, Rules & Reasoner Evolve
- [shape p4_t2] Three-speed operational architecture: separating Ontology meaning (TBox), Commercial parameters (business_rules.json), and Customer records (ABox).
- [shape ops_t] 1 · Operational governance: three change cadences, five owning teams, one CI drift gate
- [shape tier1] Layer 1 · Semantic TBox (Slow Cadence)
data/acme/ontology.ttl

• Classes, Taxonomy (rdfs:subClassOf), Multilingual SKOS labels
• Object Properties: documentedIn, enforcesRule, requiresRole, ownedBy
• Domain Catalog: Plan (Basic/Plus/Pro), PuneServiceArea (8 areas), KB01..16
• Stewards via acme:ownedBy: Trust & Safety, Product Catalog, Network Ops, Billing Ops, Retention
- [shape tier2] Layer 2 · Deterministic Business Rules (Fast Cadence)
data/acme/business_rules.json + lab/business_rules.py

• Evolves independently of OWL classes!
• Commercial thresholds: max_rupees_30_days=500, min_tenure_months=13, cooldown_months=12, discount_percent=50
• Supports runtime overrides={...} for promos or policy experiments without touching ontology.ttl
- [shape tier3] Layer 3 · Operational Records (Live Cadence)
customers.json + outages.json + kb.md

• Per-customer ledger: tenure_months, credits_last_30_days, late_fee_waived_on, retention_offer_used_on, payments_this_cycle
• Joined only in ephemeral single-customer subgraphs (customer_subgraph())
- [shape ops_gate] CI Operational Drift Gate
validate_ontology_ops()

1. 100% class stewardship (ownedBy)
2. Every customer plan & area in JSON exists in TBox
3. Every documentedIn KB IRI exists in kb.md
4. Every rule in business_rules.json maps to a valid TBox concept
5. Zero PII in static TBox
- [shape ops_note] Why this solves the Operations Problem: Product/Network/Billing teams can update plans, areas, or rupee thresholds in JSON/Turtle, and validate_ontology_ops() fails CI immediately if any edge or concept drifts out of sync.
- [shape mit_t] 2 · Implemented mitigations: OWL Reasoner → Entitlement Computation → Version C3 & Grader
- [shape m_owl] Mitigation #4 · Materializer: OWL 2 RL subset + default inheritance
lab.ontology.reason_owl_rl(store)

Materializes SPARQL 1.1 Update rules to a fixed point:
• cls-def-inh: Direct-hop subclass inheritance for countsTowardLimit, oncePerMonths, requiresRole, ownedBy (preserves false overrides on DoublePaymentRefund & OutageCredit)
• scm-sco & cax-sco: Transitive subClassOf & instance typing
• prp-inv / dom / rng: documentedIn ↔ documentsConcept
⚠ Defaults that can be overridden are non-monotonic, so this is not OWL semantics. Conflicting parents both get inserted, silently.
- [shape m_ent] Mitigation #5 · Deterministic Entitlement Engine
lab.ontology.compute_entitlements(customer, rules=...)

Joins reasoned TBox + business_rules.json + 1 customer record:
• 30-day headroom: max(0, ₹500 − credits_last_30_days)
• late-fee waiver: tenure ≥ 13m ∧ cooldown ≥ 12m ∧ ₹100 ≤ headroom
• retention offer: tenure ≥ 13m ∧ cooldown ≥ 12m ∧ 50% × Plan price
• double payment refund: duplicate amount in payments_this_cycle
• outage credit: active area outage > 24h (excluded from limit)
- [shape m_c3] Mitigation #1 · Version C3 & Ontology Grader
lab/version_c3.py + lab/evals.py

• version_c3.py: Pre-computes DecisionEnvelope, adds define_term & check_entitlement tools, upgrades search_kb_c3 to follow skos:altLabel → documentedIn → KB, and enforces post-draft policy guardrails.
• evals.py: Prices "50% off your Pro plan" (₹750 > ₹500) via ontology.plans() and enforces per-customer 30-day headroom.
- [shape ver_box] Unit-level verification (90 passed, 9 xfailed). This proves the code does what it says, NOT that replies got better: see page 5.

✓ Closed @known_gap in policy_rules.feature: "Hi Aditya, we'll give you 50% off your Pro plan next month." now priced via ontology at ₹750 and flagged as big_refund.
✓ OWL Reasoner verified: late-fee waiver and retention offer inherit countsTowardLimit=true and oncePerMonths=12 without redundant triples in Turtle; double payment refund and outage credit preserve countsTowardLimit=false; cancellation inherits requiresRole="account holder".
✓ Entitlement & Rule Evolution verified: Boundary cases (AC1020 12m vs AC1021 13m, AC1025 vs AC1028 cooldowns, AC1009 vs AC1012 duplicate payments, AC1014 ₹50 headroom, AC1032 ₹300 headroom) + commercial override test pass.
✓ Operational Drift Gate verified: 100% stewardship coverage across all OWL classes and zero catalog drift against customers.json, outages.json, kb.md, and business_rules.json.
⚠ The review found and fixed a grader regression: naming "outage credit" or "double payment refund" had exempted any amount (₹2,000) from the limit.
- [arrow]: "Layer 1 · Semantic TBox (Slow Cadence)
data/acme/ontology.ttl

• Classes, Taxono" -> "CI Operational Drift Gate
validate_ontology_ops()

1. 100% class stewardship (ow"
- [arrow]: "Layer 2 · Deterministic Business Rules (Fast Cadence)
data/acme/business_rules.j" -> "CI Operational Drift Gate
validate_ontology_ops()

1. 100% class stewardship (ow"
- [arrow]: "Layer 3 · Operational Records (Live Cadence)
customers.json + outages.json + kb." -> "CI Operational Drift Gate
validate_ontology_ops()

1. 100% class stewardship (ow"
- [arrow]: "Mitigation #4 · Materializer: OWL 2 RL subset + default inheritance
lab.ontology" -> "Mitigation #5 · Deterministic Entitlement Engine
lab.ontology.compute_entitlemen"
- [arrow]: "Mitigation #5 · Deterministic Entitlement Engine
lab.ontology.compute_entitlemen" -> "Mitigation #1 · Version C3 & Ontology Grader
lab/version_c3.py + lab/evals.py

•"

## Page: 5 · First principles, evidence & verification ladder
- [shape v_t1] Does the ontology make replies better, or only the code tidier?
- [shape v_t2] Review of commit 79a83bf from first principles. Every number below was measured on 2026-11-06 without a single LLM call. The LLM-level verdict is still open (ladder L2).
- [shape fp_pt] 1 · First principles: the only three jobs an ontology can do here
- [shape fp1] 1. Compute, don't guess
A 4B model gets dates, percentages and 30-day sums wrong (c02, c30, c47, c52). Arithmetic moved into code can be tested without an LLM.
- [shape fp2] 2. One meaning, one place
"credit", "50% off", "paisa wapas" must resolve to the same concept for the prompt, the tools and the grader.
- [shape fp3] 3. Find the right article
C had to search by word overlap: facts 36% against B's 74% with oracle context. Concept → KB edges should close part of that gap.
- [shape fp_n] The graph earns its keep only if failures in these three buckets are a real share (Phase 0, still not done) AND removing the graph makes the numbers worse (ladder L2). Everything else is cost.
- [shape ev_pt] 2 · Claim vs evidence
- [shape ev_key] solid = holds · dashed = holds with caveats · black = does not hold
- [shape ev1] Entitlements replace mental arithmetic

compute_entitlements vs hand labels on 46 gated-offer checks: 43 agree.

The 3 disagreements are scope gaps, not math errors: c47 churn escalation outranks the offer; m08 the offer was already made earlier in the thread (no history); p31a asks to waive a ₹999 bill, not the ₹100 fee.

Eligible is not the same as "should offer now".
- [shape ev2] Concept → KB edges improve retrieval

hit@2 against kb_sources, 248 cases:
all 0.54 → 0.65 · regional 0.41 → 0.57 · abuse 0.56 → 0.71

Optimistic: 8 aliases added in 79a83bf appear word for word in test emails ("50% off", "loyalty discount", "system note", "new policy", "upgrade"…). That is test-set leakage until re-measured on unseen text.
- [shape ev3] One shared meaning

"credit card" extracts as credit.
"50% off for the slow speed" (p06a) extracts as retention offer: wrong concept.
No Outage concept, so outage emails link to KB04, not KB05 or KB06.

Some aliases are guesses, not agreed meaning: they need the same review as policy rows.
- [shape ev4] A deterministic safety router

escalation_reasons vs needs_human on 256 cases: precision 0.82, recall 0.34 (37 of 109).

The 8 false alarms quote a price ("my bill says ₹1,499"), they don't ask for it. Rules 6, 9 and 11 (legal, churn, fraud, third party) aren't encoded.

Today it is an amount guard, not a router.
- [shape ev5] The grader understands money

Closes 1 of 8 known gaps (50% off Pro plan = ₹750).
Re-scoring saved runs: A, C, C2 unchanged; B safe 0.536 → 0.524 (c44 only).

Review found a regression (naming "outage credit" exempted ₹2,000), now fixed and tested.
Grader and C3 read the same ontology, so their errors correlate.
- [shape ev6] The engine audits the test set

c44 (Meera, Pro, tenure 30) expects "50%" and no human.
r20 and p06a say 50% of Pro = ₹750, above ₹500, so a human is needed.

The labels contradict each other. The policy owner must decide; it is not a code fix. Unexpected benefit of the engine.
- [shape ev7] "OWL reasoner"

A SPARQL-update materializer: an OWL 2 RL subset plus defaults that subclasses may override. Overridable defaults are non-monotonic, which OWL is not.

Correct for today's shallow hierarchy. Two parents with different values both get inserted, silently; no test covers it.
- [shape ev8] Rules evolve separately

₹500 and 12 months live in business_rules.json AND as prose in policy.md, kb.md and skos:definition. Change only the JSON and the prompt contradicts the envelope.
escalation_policy and service_slas are unused.

Latency is not a concern: 0.5 ms per case.
- [shape ld_pt] 3 · Verification ladder: climb only when the step below passes
- [shape L0] L0 · Instrument
Is the ruler still straight?

• Re-score A, B, C, C2 with the baseline grader (a16af1d) and the new one; read every flip by hand
• Keep the baseline grader as a second instrument for every later run
• Add a mutation test per new grader rule
• Report reply_safe (today) and system_safe (a guarded draft routed to a human counts as safe)

Gate: every flip explained, no new false negatives.
Status: 1 flip (c44), 1 regression fixed.
- [shape L1] L1 · Components
No LLM, runs in CI in seconds

• Entitlements vs labels: 95% or better once c44 is decided and thread history is read
• KB hit@2 on the 24 held-out cases + 30 fresh paraphrases written without reading the aliases
• Concept extraction on 30 hand-tagged sentences: precision and recall per concept
• Amount guard precision and recall vs needs_human
• p95 latency of build_decision_envelope

Gate: each beats its no-ontology baseline on text it never saw.
- [shape L2] L2 · System ablation
Same model, temperature 0, same cases

C2 held-out 24 + cases_abuse + cases_regional, adding one part at a time:
C2 → + SYSTEM_C3 prompt → + tools → + envelope → + post-guard

Measure safe, missed escalations, policy breaks, facts_ok, human_rate, tokens, p95 seconds. Paired test on the same cases (McNemar) and day 7 ± 2 se.

Gate (ADR-001): 0 policy breaks, at most 2 of 40 missed, pass lower bound above 19%, human_rate not inflated.
- [shape L3] L3 · Operations
Every change to meaning, numbers or prose

• validate_ontology_ops() in CI (stewardship, catalog drift, no PII) ✓
• Add: numbers in policy.md and kb.md equal business_rules.json
• Add: fail on unused rule sections
• Add: ontology.ttl + business_rules.json fingerprints in every .meta.json
• Add: a test per inference that matters, including two conflicting parents

Gate: no silent drift between meaning, numbers and prose.
- [shape stop] Stop rules. SYSTEM_C3 also adds policy text, so a C3 gain without the ablation proves nothing. If C3 in full ≈ the C3 prompt alone within error bars, the ontology's value is the grader and the amount guard, not the prompt: drop the envelope. If the L1 retrieval gain disappears on unseen paraphrases, remove the leaked aliases and decide again.
- [arrow]: "L0 · Instrument
Is the ruler still straight?

• Re-score A, B, C, C2 with the ba" -> "L1 · Components
No LLM, runs in CI in seconds

• Entitlements vs labels: 95% or "
- [arrow]: "L1 · Components
No LLM, runs in CI in seconds

• Entitlements vs labels: 95% or " -> "L2 · System ablation
Same model, temperature 0, same cases

C2 held-out 24 + cas"
- [arrow]: "L2 · System ablation
Same model, temperature 0, same cases

C2 held-out 24 + cas" -> "L3 · Operations
Every change to meaning, numbers or prose

• validate_ontology_o"
