# Graph Report - fde-first-principles  (2026-11-09)

## Corpus Check
- 52 files · ~61,759 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 55 file(s) not represented in the graph (top: .feature 13, .drawio 11, .jsonl 11)
- WARNING: 55 of 140 files seen (39%) have no supported extractor and are missing from this graph entirely. It may look complete while representing only part of the codebase.

## Summary
- 1351 nodes · 3540 edges · 75 communities (59 shown, 16 thin omitted)
- Extraction: 80% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 679 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `64e7efe7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- json
- chat
- ontology.py
- ._build
- Escalation metrics specs
- plans
- Review Studio app shell
- Ontology BDD specs
- Review Studio server
- acme.py
- Studio C3 provider tests
- version_c3.py
- policy_violations
- providers.py
- Studio report metric tests
- Studio workflow and demo runs
- Studio review flow and verdicts
- version_c3
- Studio workbook import and lab
- Day 4 and 9: cost, latency, Version A
- Studio evidence frame
- needs_human escalation
- Safety router
- Day 11-12: recommendation and article
- Entitlements and the 500 rupee limit
- Day 7: error bars and evidence
- Studio metrics module
- Refund limit and expert findings
- Studio guardrail tests
- Day 1: one model call
- Studio case import script
- Ontology layer for Acme Fibre
- load_customers
- evals.py
- define
- Test set data checks
- load_cases
- Grader mutation tests
- Day 8: agent loop and failures
- app.py
- Studio UI cards
- judge_round1.py
- Day 6: Version B and context
- Step 6 · check claims and facts
- Review dashboard metrics
- ADR-001 diagram: B with a safety router and a policy check
- Evaluation report (release decision)
- embed
- Studio scoring rounds
- Pivot 4: guardrails and human approval for commitments
- Acme labelled test set (cases.jsonl)
- extract_json
- Wilson intervals and rates
- Expert reviews data and errors are fixed
- Dataset card
- LLM as judge and eval history
- Day 11 notebook (recommendation-first-draft)
- Article lessons and grader gaps
- ReviewStore
- validate_ontology_ops
- Load customer card and outages
- domain_edges
- KB slow speed and technician
- KB new installation
- KB search queries
- Project config
- Lab
- api_usage

## God Nodes (most connected - your core abstractions)
1. `server()` - 97 edges
2. `score()` - 52 edges
3. `policy_violations()` - 52 edges
4. `compute_entitlements()` - 35 edges
5. `run_agent()` - 34 edges
6. `build_decision_envelope()` - 33 edges
7. `needs_human escalation` - 33 edges
8. `Day 9 · Run all three: success, cost, latency` - 32 edges
9. `Acme labelled test set (cases.jsonl)` - 32 edges
10. `version_b()` - 30 edges

## Surprising Connections (you probably didn't know these)
- `Similarity search (cosine, top 3)` --semantically_similar_to--> `search_kb()`  [AMBIGUOUS] [semantically similar]
  1-measure-before-you-believe/06-one-llm-call/day6-embedding-compatibility.drawio → lab/acme_tools.py
- `version_b()` --semantically_similar_to--> `version_b()`  [INFERRED] [semantically similar]
  1-measure-before-you-believe/06-one-llm-call/notebook.ipynb → lab/version_b.py
- `ask()` --semantically_similar_to--> `chat()`  [INFERRED] [semantically similar]
  1-measure-before-you-believe/01-an-llm-call-is-http/notebook.ipynb → lab/llm.py
- `run_agent()` --semantically_similar_to--> `run_agent()`  [INFERRED] [semantically similar]
  1-measure-before-you-believe/08-agent-loop-from-scratch/notebook.ipynb → lab/version_c3.py
- `run_agent()` --semantically_similar_to--> `run_agent()`  [INFERRED] [semantically similar]
  1-measure-before-you-believe/09-success-cost-latency/notebook.ipynb → lab/version_c3.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Release gate metrics from acme_metrics and thresholds.yml** — 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_evaluation_report_metric_expert_pass_rate, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_evaluation_report_metric_routing_accuracy, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_evaluation_report_metric_missed_escalation, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_evaluation_report_metric_unsafe_auto_send, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_readme_release_gates_thresholds [EXTRACTED 1.00]
- **Round 1 failure modes and their fixes** — 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_mode1_amount_check_false_positive, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_mode2_model_over_escalation, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_mode3_unapproved_retention_offer, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_measurement_framework, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_fix_order [EXTRACTED 1.00]
- **Acme concession taxonomy and the ₹500 limit** — concept_concession, concept_refund_term, concept_credit_term, concept_discount_term, concept_double_payment_refund, concept_outage_credit, concept_retention_offer, concept_late_fee_waiver, concept_refund_limit_500 [EXTRACTED 1.00]
- **ADR-001 reply pipeline** — 1_measure_before_you_believe_11_recommendation_first_draft_diagram_load_customer_card, concept_safety_router, 1_measure_before_you_believe_11_recommendation_first_draft_diagram_search_help_articles, lab_version_b_version_b, concept_policy_verifier, concept_shadow_mode [EXTRACTED 1.00]
- **ADR-001 falsification triggers** — 1_measure_before_you_believe_11_recommendation_first_draft_decision_change_mind_router_misses, 1_measure_before_you_believe_11_recommendation_first_draft_decision_change_mind_c_stronger_model, 1_measure_before_you_believe_11_recommendation_first_draft_decision_change_mind_searched_context, 1_measure_before_you_believe_11_recommendation_first_draft_decision_recommendation [EXTRACTED 1.00]
- **Business Graph Engine runtime: concept linker → entitlements → decision envelope → guard, prompt, grader** — lab_ontology_extract_concepts, lab_ontology_compute_entitlements, lab_version_c3_build_decision_envelope, 1_measure_before_you_believe_08_agent_loop_from_scratch_business_graph_engine_plan_amount_guard, lab_version_c3_version_c3, lab_evals_policy_violations [EXTRACTED 1.00]
- **What must match between the chat and embedding models** — 1_measure_before_you_believe_06_one_llm_call_day6_embedding_compatibility_same_embedding_model, 1_measure_before_you_believe_06_one_llm_call_day6_embedding_compatibility_same_input_format, 1_measure_before_you_believe_06_one_llm_call_day6_embedding_compatibility_both_handle_hinglish, 1_measure_before_you_believe_06_one_llm_call_day6_embedding_compatibility_fits_context_limit, 1_measure_before_you_believe_06_one_llm_call_day6_embedding_compatibility_fit_in_memory [EXTRACTED 1.00]
- **Day 10 OODA error-analysis loop** — 1_measure_before_you_believe_10_read_the_failures_day10_read_the_failures_observe, 1_measure_before_you_believe_10_read_the_failures_day10_read_the_failures_orient, 1_measure_before_you_believe_10_read_the_failures_day10_read_the_failures_decide, 1_measure_before_you_believe_10_read_the_failures_day10_read_the_failures_act, 1_measure_before_you_believe_10_read_the_failures_readme_ooda_loop [EXTRACTED 1.00]
- **Recommended workflow: email in → card → router → search → B draft → policy check → shadow approval → reply out** — 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_email_in, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_load_customer_card_outages, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_router_needs_human, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_search_help_articles, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_draft_reply_b, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_policy_check, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_human_approves_draft, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_reply_out, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_human_queue [EXTRACTED 1.00]
- **Grading the grader: three bugs fixed and locked in by regression tests** — 1_measure_before_you_believe_05_a_grader_you_can_trust_notebook_otp_safety_advice_false_alarm, 1_measure_before_you_believe_05_a_grader_you_can_trust_notebook_kb_times_as_fix_promises, 1_measure_before_you_believe_05_a_grader_you_can_trust_notebook_cross_sentence_refund, 1_measure_before_you_believe_05_a_grader_you_can_trust_notebook_grader_regression_tests, lab_evals_policy_violations [EXTRACTED 1.00]
- **score(): four yes/no checks that must all pass** — lab_evals_score, 1_measure_before_you_believe_05_a_grader_you_can_trust_day5_grader_explained_intent_ok, 1_measure_before_you_believe_05_a_grader_you_can_trust_day5_grader_explained_facts_ok, 1_measure_before_you_believe_05_a_grader_you_can_trust_day5_grader_explained_policy_ok, 1_measure_before_you_believe_05_a_grader_you_can_trust_day5_grader_explained_human_ok, 1_measure_before_you_believe_05_a_grader_you_can_trust_day5_grader_explained_passed [EXTRACTED 1.00]
- **Version C agent loop cycle (model call, tool dispatch, result back, stop or step limit)** — lab_llm_chat, 1_measure_before_you_believe_08_agent_loop_from_scratch_agent_loop_tool_dispatch, 1_measure_before_you_believe_08_agent_loop_from_scratch_agent_loop_tool_result_message, 1_measure_before_you_believe_08_agent_loop_from_scratch_agent_loop_stop_condition, 1_measure_before_you_believe_08_agent_loop_from_scratch_notebook_max_steps, 1_measure_before_you_believe_08_agent_loop_from_scratch_agent_loop_final_answer, lab_agent_run_agent [EXTRACTED 1.00]
- **What drives the cost of one resolved email** — 1_measure_before_you_believe_09_success_cost_latency_day9_success_cost_latency_cost_per_resolved_email, 1_measure_before_you_believe_09_success_cost_latency_day9_success_cost_latency_measured_cost_drivers, 1_measure_before_you_believe_09_success_cost_latency_day9_success_cost_latency_hidden_cost_drivers, 1_measure_before_you_believe_09_success_cost_latency_day9_success_cost_latency_per_email_costs_beyond_tokens, 1_measure_before_you_believe_09_success_cost_latency_day9_success_cost_latency_fixed_monthly_costs [EXTRACTED 1.00]
- **Seven stages of AI evaluation evolution** — 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage1_traditional_testing, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage2_early_ml_eval, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage3_foundation_model_eval, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage4_statistical_eval, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage5_system_level_eval, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage6_agentic_eval, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage7_continuous_production_eval [EXTRACTED 1.00]
- **@known_gap scenario groups run as strict xfail** — concept_known_gap_xfail, tests_features_policy_rules_known_gaps, tests_features_policy_rules_known_gaps_restated_request, tests_features_policy_rules_known_gaps_concession, tests_features_grader_mutations_known_gaps [EXTRACTED 1.00]
- **Project 1 · Measure before you believe: the 12 days** — concept_measure_before_you_believe, fde_day_01, fde_day_02, fde_day_03, fde_day_04, fde_day_05, fde_day_06, fde_day_07, fde_day_08, fde_day_09, fde_day_10, fde_day_11, fde_day_12 [EXTRACTED 1.00]
- **Five discoveries that turn an agent into a workflow** — 1_measure_before_you_believe_02_workflow_or_agent_acme_fiber_storyboard_pivot_remove_ai_classification, 1_measure_before_you_believe_02_workflow_or_agent_acme_fiber_storyboard_pivot_fact_retrieval, 1_measure_before_you_believe_02_workflow_or_agent_acme_fiber_storyboard_pivot_verified_sources, 1_measure_before_you_believe_02_workflow_or_agent_acme_fiber_storyboard_pivot_guardrails, 1_measure_before_you_believe_02_workflow_or_agent_acme_fiber_storyboard_pivot_measure_before_committing [EXTRACTED 1.00]
- **Everything Version B feeds the model in one call** — 1_measure_before_you_believe_06_one_llm_call_notebook_system_prompt, 1_measure_before_you_believe_06_one_llm_call_notebook_customer_card_context, 1_measure_before_you_believe_06_one_llm_call_notebook_kb_article_context, 1_measure_before_you_believe_06_one_llm_call_notebook_answer_schema, lab_version_b_version_b, lab_llm_chat [EXTRACTED 1.00]
- **Expert review → policy and tests feedback loop** — 1_measure_before_you_believe_03_test_set_first_acme_review_studio_readme_critique_shadowing_loop, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_readme_review_page, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_readme_eval_workbook, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_label_corrections, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_fix_order, concept_domain_expert_review, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_readme_report_metrics_feature [INFERRED 0.85]
- **needs_human escalation triggers** — concept_needs_human_escalation, data_acme_policy_rule_06, data_acme_policy_rule_09, data_acme_policy_rule_11, acme_kb15, acme_kb16, lab_escalation_escalation_triggers [INFERRED 0.85]
- **₹500 money limit across policy, KB and grader** — concept_refund_limit_500, data_acme_policy_rule_03, data_acme_policy_rule_08, data_acme_policy_rule_13, acme_kb04, acme_kb16, lab_evals_reveals_limit, lab_escalation_amounts_asked_for [INFERRED 0.85]
- **ADR-001 options: chosen guarded B vs rejected A, plain B and C** — 1_measure_before_you_believe_11_recommendation_first_draft_decision_recommendation, 1_measure_before_you_believe_11_recommendation_first_draft_decision_rejected_option_a_rules, 1_measure_before_you_believe_11_recommendation_first_draft_decision_rejected_plain_b, 1_measure_before_you_believe_11_recommendation_first_draft_decision_rejected_option_c_agent [INFERRED 0.85]
- **Version C3 escalation sources (rule, guard, offer, model)** — lab_escalation_escalation_triggers, lab_version_c3_offers_not_allowed, lab_evals_not_english, lab_version_c3_run_agent, tests_features_escalation_rules_every_escalation_records_source [INFERRED 0.85]

## Communities (75 total, 16 thin omitted)

### Community 0 - "json"
Cohesion: 0.18
Nodes (13): Tool result appended as a 'tool' message, _cache_file(), chat(), _chat_anthropic(), _chat_api(), embed(), _env(), _key() (+5 more)

### Community 1 - "chat"
Cohesion: 0.14
Nodes (11): What the model sees (Version B context), Day 06 notebook (one-llm-call), Customer card context (name, area, plan), evaluate(), KB article context (INTENT_KB by expected intent), unit(), user_message(), version_b() (+3 more)

### Community 2 - "ontology.py"
Cohesion: 0.16
Nodes (13): knowledge_page(), _alias_index(), _asserted_store(), _bool_value(), concept_labels(), _edge_metadata(), extract_concepts(), _int_value() (+5 more)

### Community 3 - "._build"
Cohesion: 0.27
Nodes (9): _trace(), draft(), fetch(), human(), log(), receive(), route(), send() (+1 more)

### Community 4 - "Escalation metrics specs"
Cohesion: 0.08
Nodes (28): Act: does it hold on emails we never looked at?, Decide: which single fix matters most?, Observe: what does a pass rate hide?, Orient: have we seen this failure before?, Safety scoreboard (safe, missed escalations, human intervention, passed), intent_guide(), summary(), Feature: Escalation is reported as recall and precision, not just human_ok (+20 more)

### Community 5 - "plans"
Cohesion: 0.16
Nodes (10): acme:Plan catalog (Basic ₹699, Plus ₹999, Pro ₹1,499), KB09 · Plan upgrades and downgrades, Acme plans: Basic, Plus, Pro, customer_subgraph(), plans(), price_discount_rupees(), pune_service_areas(), reason_owl_rl() (+2 more)

### Community 6 - "Review Studio app shell"
Cohesion: 0.13
Nodes (4): AppSettings, Settings, State, user_prompt()

### Community 7 - "Ontology BDD specs"
Cohesion: 0.14
Nodes (20): glossary(), Scenario: the glossary holds definitions, never customer records, Scenario: OWL reasoner inherits class properties and respects overrides, answer_is(), apply_commercial_rule_override(), ask_glossary(), check_headroom(), check_inherited_props() (+12 more)

### Community 8 - "Review Studio server"
Cohesion: 0.07
Nodes (25): server(), batch_rev(), batch_status(), case_editor(), case_list(), case_of(), _ed_save(), edit_case() (+17 more)

### Community 9 - "acme.py"
Cohesion: 0.11
Nodes (14): Day 04 notebook (rules-baseline), classify(), Day 07 notebook (error-bars), Day 10 notebook (read-the-failures), passed(), Run provenance (.meta.json: model, prompt fingerprint, settings), scoreboard(), show() (+6 more)

### Community 10 - "Studio C3 provider tests"
Cohesion: 0.10
Nodes (20): c3_fails(), c3_given_case(), c3_given_history(), c3_replies(), draft_cites(), draft_needs_human(), draft_reason(), draft_says() (+12 more)

### Community 11 - "version_c3.py"
Cohesion: 0.07
Nodes (35): Phase 2 · Graph engine core, Phase 3 · Wire grader and router, conversation(), customer_text(), build_decision_envelope(), check_entitlement(), define_term(), _envelope_brief() (+27 more)

### Community 12 - "policy_violations"
Cohesion: 0.08
Nodes (29): Examples from the expert's review (worst fails, what good looks like), draft_cases(), Failure category: unapproved offer, KB03 · Payment methods, KB05 · Outages and restoration updates, KB13 · Router and Wi-Fi password, @known_gap scenarios as strict xfail, _negated() (+21 more)

### Community 13 - "providers.py"
Cohesion: 0.24
Nodes (3): ClaudeCodeProvider, _parse_json_text(), _result()

### Community 14 - "Studio report metric tests"
Cohesion: 0.13
Nodes (22): banner(), cases_run(), code_saves(), demo(), escalated(), escalated_by_code(), layer_fired(), missed() (+14 more)

### Community 15 - "Studio workflow and demo runs"
Cohesion: 0.18
Nodes (6): OfflineProvider, Deps, to_record(), Workflow, demo_verdict(), main()

### Community 16 - "Studio review flow and verdicts"
Cohesion: 0.13
Nodes (17): initial_mode(), suggest_mode(), validate_verdict(), _prefill(), check_fired(), ctx(), fail_no_critique(), fail_no_mode() (+9 more)

### Community 17 - "version_c3"
Cohesion: 0.06
Nodes (23): c3_output(), C3Provider, outages.json (current outages by area), unasked_outage(), customer_reported_outage(), version_c3(), Scenario Outline: The expert's verdict and the grader's agree, Scenario Outline: The envelope shows the outage only when the customer reports one (+15 more)

### Community 18 - "Studio workbook import and lab"
Cohesion: 0.16
Nodes (11): _bool(), export_to_excel(), _history(), _item(), load_lab(), _payments(), _put(), read_review_log() (+3 more)

### Community 19 - "Day 4 and 9: cost, latency, Version A"
Cohesion: 0.14
Nodes (18): version_a(), Per-step agent trace, Cost levers (check each against the pass rate), ₹ per resolved email (what really drives cost), Fixed monthly costs spread over all emails, Costs hidden inside today's estimate, Latency not counted (tool time, network, queues, cold start), Cost drivers measured in the notebook (+10 more)

### Community 20 - "Studio evidence frame"
Cohesion: 0.22
Nodes (3): Evidence, mask(), nonempty()

### Community 21 - "needs_human escalation"
Cohesion: 0.11
Nodes (24): acme:AccountAction requiresRole AccountHolder, acme:EscalationTrigger (planned), acme:PuneServiceArea (8 areas), Failure category: missed escalation, Human support queue, KB10 · Cancellation and notice period, KB12 · Shifting your connection, KB15 · Account security (+16 more)

### Community 22 - "Safety router"
Cohesion: 0.23
Nodes (7): guard_hits(), decide(), Unsafe-to-automate case category, Amount guard (C3 only, not yet a router), Open question: can a learned classifier route escalations better? (project 3), Prompt injection / manipulation attempts, Safety router

### Community 23 - "Day 11-12: recommendation and article"
Cohesion: 0.13
Nodes (17): Day 11 ADR-001 diagram, Open question: which failures come from model size vs prompt or grader? (P4, P5), ADR-001: How Acme Fibre should answer customer emails, ADR-001 evidence table (day 9 runs), Open question: how good is searched context for B? (project 2), Open question: do numbers hold on a stronger model and real emails? (project 6), ADR self-check, 5-minute CTO readout (pitch script) (+9 more)

### Community 24 - "Entitlements and the 500 rupee limit"
Cohesion: 0.18
Nodes (17): Ephemeral per-case ABox (one customer), Varun's ₹300 credit: three agents, three meanings, data/acme/business_rules.json (commercial thresholds), Concession (refund, credit, waiver, discount value), Credit, Discount (also: सूट, छूट, ರಿಯಾಯಿತಿ), Double payment refund, Late-fee waiver (+9 more)

### Community 25 - "Day 7: error bars and evidence"
Cohesion: 0.17
Nodes (12): Stage 4 · Statistical evaluation: 'How sure are we?', Stage 5 · System-level evaluation: 'Does the whole system work?', Stage 6 · Agentic AI evaluation: 'Does the agent finish the job?', Stage 7 · Continuous production evaluation: 'Is it still working for users?', A statistical approach to model evaluations (Anthropic), Seeing Theory: basic probability and frequentist inference, Phase 4 · Empirical verdict, Evidence table rebuilt from saved runs (data/results) (+4 more)

### Community 26 - "Studio metrics module"
Cohesion: 0.08
Nodes (11): tests/features/report_metrics.feature, banner(), build_frame(), fig_html(), layer_of(), load(), sha256(), tiles() (+3 more)

### Community 27 - "Refund limit and expert findings"
Cohesion: 0.12
Nodes (20): KB02 · Late payment fee, KB04 · Refunds and credits, KB06 · Outage credit, KB11 · Retention offer, BDD policy specs, Ontology pipeline (vocabulary → taxonomy → thesaurus → ontology → knowledge graph), ₹500 refund/credit limit, duplicate_payment_amount() (+12 more)

### Community 28 - "Studio guardrail tests"
Cohesion: 0.12
Nodes (14): tests/features/guardrails.feature (BDD guardrails), email_from(), flags(), human_chooses(), lab(), model_drafts(), not_called(), outcome() (+6 more)

### Community 29 - "Day 1: one model call"
Cohesion: 0.15
Nodes (17): Day 01 notebook (an-llm-call-is-http), ask(), Deep Dive into LLMs like ChatGPT (Karpathy), inference chapter, Ollama /api/chat endpoint, qwen3:4b local model, Forward Deployed Engineer (FDE) mindset, Local models on Ollama (zero cost), Project 1 · Measure before you believe (+9 more)

### Community 30 - "Studio case import script"
Cohesion: 0.22
Nodes (11): _restore_chart(), _add_headers(), _copy_style(), import_cases(), import_customers(), import_policy(), _last_row(), main() (+3 more)

### Community 31 - "Ontology layer for Acme Fibre"
Cohesion: 0.13
Nodes (10): Phase 0 · Baseline audit, Phase 1 · Rich TBox schema, Static TBox (shared meaning, zero PII), Meaning flow: policy.md + kb.md → ontology.ttl → pyoxigraph → glossary(), pyoxigraph (in-process RDF store, SPARQL 1.1), issue_refund tool (data-changing, deferred), data/acme/ontology.ttl, Ontology layer for Acme Fibre (+2 more)

### Community 32 - "load_customers"
Cohesion: 0.11
Nodes (19): Tool dispatch FUNCTIONS[name](**args), SYSTEM_C agent prompt, Failure category: wrong tool, Email in, Load customer card and outages, Search the help articles (retrieved, not oracle context), KB01 · Billing cycle and due dates, Acme help articles (kb.md) (+11 more)

### Community 33 - "evals.py"
Cohesion: 0.11
Nodes (10): Day 05 notebook (a-grader-you-can-trust), _deep_update(), _default_rules(), load_business_rules(), outage_exceeds_hours(), _parse_date(), amounts(), _limit_context() (+2 more)

### Community 34 - "define"
Cohesion: 0.24
Nodes (8): meaning_concept_card(), meaning_rule_detail(), concept_provenance(), define(), Scenario outline: every money and identity term is defined and cites its policy, Scenario: an unknown word has no definition, look_up(), test_concept_provenance_distinguishes_stated_and_inherited_facts()

### Community 35 - "Test set data checks"
Cohesion: 0.18
Nodes (8): cases_regional.jsonl (52 regional-language cases), cases(), _problems(), test_cases_match_the_customer_record(), test_labels_are_valid(), check(), test_language_label_matches_the_script(), test_regional_cases_carry_an_english_gloss()

### Community 36 - "load_cases"
Cohesion: 0.19
Nodes (10): Day 08 notebook (agent-loop-from-scratch), run_agent(), show(), load_cases(), Feature: The grader agrees with the expert's round-2 review, Scenario Outline: The retention offer is pre-approved (c44), a_draft_handed_off(), a_draft_sent() (+2 more)

### Community 37 - "Grader mutation tests"
Cohesion: 0.08
Nodes (29): Three graders: factual grounding, escalation correctness, response quality, Failure category x version table, Failure category: grader wrong, Failure category: over-escalation on an answerable case, Failure category: unsupported-amount false positive, failures.csv (tuning failures with note and category), Grader false alarms ('5-7 working days', 'Rs. 100'), Grader (+21 more)

### Community 38 - "Day 8: agent loop and failures"
Cohesion: 0.12
Nodes (19): Gave-up fallback at MAX_STEPS, Business Graph Engine (graph computes, LLM verbalizes), Today: passive prompt glossary (LLM does the joins), Version B + glossary experiment (B_glossary), term_misread failure tag, MAX_STEPS = 6 step limit, qwen3:4b local model (temperature 0), Failure category: gave up (+11 more)

### Community 39 - "app.py"
Cohesion: 0.07
Nodes (15): highlight(), icon(), pipeline(), review_page(), score_page(), case_header(), score_boxes(), sim_pipe() (+7 more)

### Community 40 - "Studio UI cards"
Cohesion: 0.10
Nodes (22): eval_checks(), chip(), customer_chips(), cur(), draft_meta(), email_card(), expected_card(), guard_try_result() (+14 more)

### Community 41 - "judge_round1.py"
Cohesion: 0.29
Nodes (4): judge_prompt(), main(), work(), run_judge()

### Community 42 - "Day 6: Version B and context"
Cohesion: 0.24
Nodes (7): Scoreboard on 84 cases: A vs B, Version A pipeline: keyword match then fill a template, Building block: the augmented LLM (Anthropic, Building effective agents), Context engineering (the context is the product), Oracle context (B got the expected intent's articles), Day 6 · Version B: one model call with the right context, version_b()

### Community 43 - "Step 6 · check claims and facts"
Cohesion: 0.38
Nodes (5): amounts(), claim_checks(), _flag(), check(), Policy verifier

### Community 44 - "Review dashboard metrics"
Cohesion: 0.29
Nodes (7): Code saves, Disagreement rates, What triggered the escalations (layer analysis), Escalation rate, Failure categories (expert), Review dashboard (when do humans help?), Routing by escalation rule

### Community 45 - "ADR-001 diagram: B with a safety router and a policy check"
Cohesion: 0.27
Nodes (8): Proposed controlled workflow (deterministic routing + one drafting step), Building effective agents (Anthropic), Email-to-reply decision map, Workflow patterns: prompt chaining, routing, agent, ADR-001 diagram: B with a safety router and a policy check, Gates before replies go out unreviewed, Workflow vs agent, Day 2 · Workflow or agent? Map the decisions first

### Community 46 - "Evaluation report (release decision)"
Cohesion: 0.10
Nodes (22): load_thresholds(), Evaluation report (release decision), Step-6 check hits, Error cost (INR, per 1,000 emails), Expert pass rate, Missed escalation, Model needs-human flag recall, Routing accuracy (+14 more)

### Community 47 - "embed"
Cohesion: 0.24
Nodes (6): qwen3:4b chat model (reads text only), Similarity search (cosine, top 3), embeddinggemma (EMBED_MODEL), Embeddings and retrieval, Hinglish handling, Recall@3 (retrieval metric)

### Community 48 - "Studio scoring rounds"
Cohesion: 0.16
Nodes (13): make_provider(), run_case(), _prefill_key(), progress(), rnd(), round_data(), _run_missing(), worker() (+5 more)

### Community 50 - "Acme labelled test set (cases.jsonl)"
Cohesion: 0.12
Nodes (24): Acme Review Studio, Acme_Fibre_Grounded_Draft_Eval.xlsx (eval workbook), import_cases.py (lab data → workbook), runs/ persistence (reviews.json, runs.jsonl, checkpoints.sqlite, settings.json), Round 1 Principal Engineer review of the Acme Fibre email drafting solution, Safe-send capture rate (new north-star metric), Day 03 notebook (test-set-first), Seven intents (+16 more)

### Community 51 - "extract_json"
Cohesion: 0.18
Nodes (9): Final answer JSON {intent, reply, needs_human}, Stop condition: reply has no tool_calls, Day 09 notebook (success-cost-latency), cost_inr(), percentile(), row(), run_agent(), Failure category: bad JSON (+1 more)

### Community 53 - "Expert reviews data and errors are fixed"
Cohesion: 0.40
Nodes (5): Build LLM judge from expert examples, Error analysis: error rates, patterns, specialised judges, Expert reviews data and errors are fixed, Repeat on material change or periodic review, Principal domain expert

### Community 54 - "Dataset card"
Cohesion: 0.25
Nodes (3): html_table(), workbook_sheet(), Dataset card (Acme test set)

### Community 55 - "LLM as judge and eval history"
Cohesion: 0.25
Nodes (5): Critique Shadowing workflow, Stage 1 · Traditional software testing: 'Is it correct?', Stage 2 · Early machine learning evaluation: 'How accurate is it?', Stage 3 · Foundation model evaluation: 'Is it good, safe, and grounded?', LLM as judge

### Community 56 - "Day 11 notebook (recommendation-first-draft)"
Cohesion: 0.60
Nodes (4): Day 11 notebook (recommendation-first-draft), evidence(), percentile(), two_se()

### Community 58 - "ReviewStore"
Cohesion: 0.20
Nodes (3): ReviewStore, _export(), Acme Review Studio architecture/UX review (16 Oct 2026)

### Community 59 - "validate_ontology_ops"
Cohesion: 0.50
Nodes (3): validate_ontology_ops(), Scenario: operational governance has zero catalog drift, run_ops_validation()

### Community 60 - "Load customer card and outages"
Cohesion: 0.38
Nodes (7): One model call (B) drafts the reply, Human approves the draft (shadow mode until the gates hold), Human queue (a person writes the reply), Policy check (grader rules, in code), Reply out, Router: needs a human? (rules + 1 model call), Search the help articles (no oracle)

### Community 61 - "domain_edges"
Cohesion: 0.32
Nodes (5): KnowledgeArticle and PolicyRule IRIs (documentedIn, enforcesRule), Concept → KB retrieval gain (with alias leakage caveat), Multilingual lexical layer (SKOS labels), domain_edges(), search_kb_c3()

## Ambiguous Edges - Review These
- `version_b()` → `Failure category: unsupported-amount false positive`  [AMBIGUOUS]
  1-measure-before-you-believe/10-read-the-failures/notebook.ipynb · relation: references
- `search_kb()` → `Similarity search (cosine, top 3)`  [AMBIGUOUS]
  1-measure-before-you-believe/06-one-llm-call/day6-embedding-compatibility.drawio · relation: semantically_similar_to
- `run_agent()` → `Failure category: unapproved offer`  [AMBIGUOUS]
  1-measure-before-you-believe/10-read-the-failures/notebook.ipynb · relation: references
- `Open question: can a learned classifier route escalations better? (project 3)` → `Roadmap claim: transformer classifier drops router latency from 500 ms to under 20 ms`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/presentation.md · relation: conceptually_related_to
- `Pitch claim: router adds under 500 ms and ₹0.10 per 1,000 emails` → `ADR-001 evidence table (day 9 runs)`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/pitch.md · relation: conceptually_related_to
- `Open question: which failures come from model size vs prompt or grader? (P4, P5)` → `ADR-001: How Acme Fibre should answer customer emails`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/day11-adr.drawio · relation: conceptually_related_to
- `ADR-001: How Acme Fibre should answer customer emails` → `Pitch claim: drafts cut handle time 40-60% in Phase 1`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/pitch.md · relation: conceptually_related_to
- `ADR-001 evidence table (day 9 runs)` → `Pitch claim: Option A missed 40 of 40 (0% safety)`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/pitch.md · relation: conceptually_related_to
- `Build a workflow, not an agent: B + safety router + policy verifier` → `Pitch claim: deterministic workflow topology with hard guarantees`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/pitch.md · relation: conceptually_related_to
- `Build a workflow, not an agent: B + safety router + policy verifier` → `Phased rollout: shadow mode, then automated egress per intent`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/presentation.md · relation: conceptually_related_to
- `Build a workflow, not an agent: B + safety router + policy verifier` → `Author's unease: instinct favours C`  [AMBIGUOUS]
  1-measure-before-you-believe/12-article/article.md · relation: conceptually_related_to
- `Pitch claim: drafts cut handle time 40-60% in Phase 1` → `Phased rollout: shadow mode, then automated egress per intent`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/presentation.md · relation: conceptually_related_to
- `Cost is not the issue (B ≈ ₹1.60/day, C ≈ ₹10/day)` → `Pitch claim: agent fails unit economics`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/pitch.md · relation: conceptually_related_to

## Knowledge Gaps
- **28 isolated node(s):** `fde-first-principles`, `KB03 · Payment methods`, `KB13 · Router and Wi-Fi password`, `Fixed monthly costs spread over all emails`, `Costs hidden inside today's estimate` (+23 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 304 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `server()` connect `Review Studio server` to `load_customers`, `evals.py`, `define`, `ontology.py`, `app.py`, `Studio UI cards`, `Studio workflow and demo runs`, `Studio scoring rounds`, `Studio review flow and verdicts`, `Studio workbook import and lab`, `Expert reviews data and errors are fixed`, `Safety router`, `ReviewStore`, `validate_ontology_ops`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `server()` (e.g. with `.all()` and `Expert reviews data and errors are fixed`) actually correct?**
  _`server()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fde-first-principles`, `KB03 · Payment methods`, `KB13 · Router and Wi-Fi password` to the rest of the system?**
  _28 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `chat` be split into smaller, more focused modules?**
  _Cohesion score 0.14035087719298245 - nodes in this community are weakly interconnected._
- **Why does `policy_violations()` connect `policy_violations` to `evals.py`, `Grader mutation tests`, `plans`, `Ontology BDD specs`, `version_c3.py`, `Step 6 · check claims and facts`, `version_c3`, `Acme labelled test set (cases.jsonl)`, `Day 4 and 9: cost, latency, Version A`, `Day 11-12: recommendation and article`, `Article lessons and grader gaps`, `Refund limit and expert findings`, `Load customer card and outages`, `Ontology layer for Acme Fibre`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `version_b()` and `Failure category: unsupported-amount false positive`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `search_kb()` and `Similarity search (cosine, top 3)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._