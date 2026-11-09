# Shared extraction brief for the fde-first-principles graph

Project: a 12-day learning log. One customer-support assistant for "Acme Fibre" (a Pune ISP) is built
three ways and measured: Version A (rules, day 4), Version B (one LLM call with context, day 6),
Version C (agent loop with tools, day 8; hardened later as C3 in lab/version_c3.py). A grader
(lab/evals.py, day 5) scores replies against a labelled test set (day 3) and a reply policy.
Day 11 recommends a design; day 12 turns it into an article. acme-review-studio is a Shiny +
LangGraph app where a domain expert reviews drafts and the verdicts flow back into policy and tests.

## Canonical IDs: reuse these exactly; never invent variants

Days (one node per day; label "Day N · <topic>"; file_type "document"):
fde_day_01 One model call: tokens, time and randomness
fde_day_02 Workflow or agent? Map the decisions first
fde_day_03 Write the test set before the system
fde_day_04 Version A: rules and templates (the honest baseline)
fde_day_05 A grader you can trust
fde_day_06 Version B: one model call with the right context
fde_day_07 Why 30 test cases can lie: error bars
fde_day_08 Version C: an agent loop from scratch
fde_day_09 Run all three: success, cost, latency
fde_day_10 Read the failures, not the averages
fde_day_11 Recommendation, first draft
fde_day_12 The article

Policy rules in data/acme/policy.md: acme_policy_rule_01 ... acme_policy_rule_13 (two digits).
KB articles in data/acme/kb.md: acme_kb01 ... acme_kb16.
Acme Fibre itself: acme_fibre. The labelled test set (cases): acme_test_set.

The three designs (these are code node IDs that already exist; edge to them, do not redefine):
- Version A: 1_measure_before_you_believe_04_rules_baseline_notebook_version_a
- Version B: lab_version_b_version_b
- Version C agent loop: lab_agent_run_agent
- Version C3 (hardened agent): lab_version_c3_version_c3
- The grader: lab_evals_score and lab_evals_policy_violations
- Ontology / entitlements: lab_ontology_compute_entitlements
- Decision envelope: lab_version_c3_build_decision_envelope

Other code: graphify-out/.views/code_ids.tsv lists every code node (id, label, source_file).
Link a document concept to code ONLY with an id that appears in that file (search it). Never invent
a code id. Use relation "implements" (code implements concept), "references" (doc names the code),
or "rationale_for" (doc explains why the code is the way it is).

Cross-file concepts: id "concept_<snake_case_name>", file_type "concept". Before creating one,
prefer these if they fit: concept_grader, concept_test_set_first, concept_error_bars,
concept_needs_human_escalation, concept_refund_limit_500, concept_agent_loop,
concept_workflow_vs_agent, concept_context_engineering, concept_cost_and_latency,
concept_failure_analysis, concept_ontology_layer, concept_llm_as_judge, concept_shadow_mode,
concept_safety_router, concept_policy_verifier, concept_prompt_injection,
concept_known_gap_xfail, concept_bdd_policy_specs, concept_domain_expert_review,
concept_token_and_latency, concept_temperature_randomness, concept_embeddings_retrieval,
concept_confidence_interval.

Edges that make this graph useful (prioritise these):
- fde_day_NN --references--> code, concepts, policy rules and KB articles that day uses or introduces
- fde_day_NN --conceptually_related_to--> an earlier day it builds on (INFERRED 0.85 unless stated)
- concept --rationale_for--> code or decision it justifies
- feature scenario groups --references--> acme_policy_rule_NN they test, and --references--> the
  lab function the steps call (find it in code_ids.tsv; tests/test_*.py step files are in it)
- measured results (pass rate, cost, latency) as attributes on the version or day node, not nodes

Put numbers and rationale in node attributes ("rationale", "summary"), not in separate nodes.
Keep nodes meaningful: skip headings like "Checklist", "Watch", "Steps", link lists and video copy.
Target 15 to 40 nodes per file for dense files, fewer for short ones.

## Files that are views of formats graphify cannot read

graphify-out/.views/*_notebook.md is a text view of a notebook; graphify-out/.views/day*.md (and
agent_loop, business_graph_engine_plan, ontology_explained) are views of .drawio diagrams. For
nodes and edges from a view, set source_file to the ORIGINAL file given next to it in your file list,
never to the view path. Notebook functions already exist as code nodes named
<notebook_stem>_<function> (for example 1_measure_before_you_believe_06_one_llm_call_notebook_version_b);
do not recreate them; edge to them.
