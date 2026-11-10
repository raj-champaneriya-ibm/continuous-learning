# Graph Report - fde-first-principles  (2026-11-10)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1789 nodes · 4969 edges · 89 communities (69 shown, 20 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 880 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `691a05cf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- llm.py
- Version
- ontology.py
- policy_violations
- pytest
- app.py
- Span
- test_ontology.py
- Review Studio server
- score
- test_c3_provider.py
- build_decision_envelope
- test_policy_rules.py
- needs_human escalation
- Studio report metric tests
- refresh_versions
- test_review_flow.py
- import_cases.py
- Capabilities
- Day 9 · Run all three: success, cost, latency
- Studio evidence frame
- RunResult
- Release gates and error costs (thresholds.yml)
- RunStore
- test_guardrails.py
- Build a workflow, not an agent: B + safety router + policy verifier
- acme_metrics.py
- Rule 8 · ₹500 limit is per customer over 30 days
- lab.py
- Day 1: one model call
- RunInput
- version_c3
- version_c3.py
- load_business_rules
- load_cases
- Acme Fibre (fictional Pune broadband ISP)
- test_simulator_http.py
- Grader mutation tests
- Day 8: agent loop and failures
- review_page
- version_a
- version_b
- Evaluation evidence Quarto site
- Review dashboard (when do humans help?)
- Day 3 · Write the test set before the system
- Evaluation report (release decision)
- privacy.py
- define
- Round 1 Principal Engineer review of the Acme Fibre email drafting solution
- test_adapter_contract.py
- test_expert_review.py
- json
- Dataset card (Acme test set)
- studio-c3.yaml
- ReviewStore
- evals.py
- config
- Acme labelled test set (cases.jsonl)
- KB slow speed and technician
- KB new installation
- KB search queries
- Project config
- C3Provider
- versions.py
- c3-agent.yaml
- judge_round1.py
- studio-offline.yaml
- version-b.yaml
- ClaudeCodeProvider
- resume
- offline-direct.yaml
- Load customer card and outages
- Step 6 · check claims and facts
- Expert reviews data and errors are fixed
- Adapter
- Version parameter and legacy round alias
- ScriptedResponse

## God Nodes (most connected - your core abstractions)
1. `server()` - 129 edges
2. `Version` - 61 edges
3. `policy_violations()` - 54 edges
4. `score()` - 52 edges
5. `RunInput` - 51 edges
6. `RunResult` - 46 edges
7. `VersionRegistry` - 42 edges
8. `SimulationService` - 36 edges
9. `build_decision_envelope()` - 35 edges
10. `compute_entitlements()` - 35 edges

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

## Communities (89 total, 20 thin omitted)

### Community 0 - "llm.py"
Cohesion: 0.05
Nodes (42): qwen3:4b chat model (reads text only), Similarity search (cosine, top 3), Day 06 notebook (one-llm-call), evaluate(), unit(), user_message(), version_b(), Final answer JSON {intent, reply, needs_human} (+34 more)

### Community 1 - "Version"
Cohesion: 0.30
Nodes (3): OrchestratedAdapter, RecordedProvider, Version

### Community 2 - "ontology.py"
Cohesion: 0.11
Nodes (24): KnowledgeArticle and PolicyRule IRIs (documentedIn, enforcesRule), Multilingual lexical layer (SKOS labels), acme:Plan catalog (Basic ₹699, Plus ₹999, Pro ₹1,499), duplicate_payment_amount(), _alias_index(), _asserted_store(), _bool_value(), customer_reported_outage() (+16 more)

### Community 3 - "policy_violations"
Cohesion: 0.12
Nodes (10): draft_cases(), Case c04: C claimed a processed cancellation, scored safe, KB03 · Payment methods, KB05 · Outages and restoration updates, KB13 · Router and Wi-Fi password, outages.json (current outages by area), _negated(), policy_violations() (+2 more)

### Community 4 - "pytest"
Cohesion: 0.07
Nodes (26): pipeline(), Elements, test_icons_have_no_network_or_accessible_name(), test_pipeline_keyboard_order_and_untrusted_details(), Safety scoreboard (safe, missed escalations, human intervention, passed), summary(), pytest_bdd_apply_tag(), Scenario Outline: The grader summary reports escalation recall and precision (+18 more)

### Community 5 - "app.py"
Cohesion: 0.17
Nodes (6): _button(), _text(), _topology(), _tree(), branch(), highlight()

### Community 6 - "Span"
Cohesion: 0.11
Nodes (5): DirectAdapter, VersionBAdapter, HttpAdapter, DeclarativeAdapter, Span

### Community 7 - "test_ontology.py"
Cohesion: 0.06
Nodes (47): acme:AccountAction requiresRole AccountHolder, Ephemeral per-case ABox (one customer), Varun's ₹300 credit: three agents, three meanings, KB02 · Late payment fee, Account holder, data/acme/business_rules.json (commercial thresholds), Concession (refund, credit, waiver, discount value), Credit (+39 more)

### Community 8 - "Review Studio server"
Cohesion: 0.05
Nodes (40): sample_spread(), chip(), customer_chips(), server(), batch_rev(), batch_status(), case_editor(), case_header() (+32 more)

### Community 9 - "score"
Cohesion: 0.15
Nodes (13): Three graders: factual grounding, escalation correctness, response quality, Day 05 notebook (a-grader-you-can-trust), Day 07 notebook (error-bars), Day 10 notebook (read-the-failures), Failure category: grader wrong, passed(), scoreboard(), show() (+5 more)

### Community 10 - "test_c3_provider.py"
Cohesion: 0.10
Nodes (20): c3_fails(), c3_given_case(), c3_given_history(), c3_replies(), draft_cites(), draft_needs_human(), draft_reason(), draft_says() (+12 more)

### Community 11 - "build_decision_envelope"
Cohesion: 0.06
Nodes (30): Phase 2 · Graph engine core, Phase 3 · Wire grader and router, customer_text(), amounts_asked_for(), build_decision_envelope(), check_entitlement(), define_term(), _envelope_brief() (+22 more)

### Community 12 - "test_policy_rules.py"
Cohesion: 0.11
Nodes (20): @known_gap scenarios as strict xfail, _promises_concession(), unearned_concession(), @known_gap Scenario Outline: Known gaps: correct replies the grader still fails, Feature: The grader enforces the Acme Fibre reply policy, @known_gap Scenario Outline: Known gaps the grader does not handle yet, @known_gap Scenario Outline: Known gaps in the concession check, @known_gap Scenario Outline: Known gaps in the restated-request check (+12 more)

### Community 13 - "needs_human escalation"
Cohesion: 0.07
Nodes (40): decide(), Unsafe-to-automate case category, Amount guard (C3 only, not yet a router), acme:EscalationTrigger (planned), acme:PuneServiceArea (8 areas), Failure category: missed escalation, Open question: can a learned classifier route escalations better? (project 3), KB10 · Cancellation and notice period (+32 more)

### Community 14 - "Studio report metric tests"
Cohesion: 0.07
Nodes (37): banner(), cases_run(), code_saves(), demo(), escalated(), escalated_by_code(), layer_fired(), missed() (+29 more)

### Community 15 - "refresh_versions"
Cohesion: 0.13
Nodes (21): _apply_retention(), case_list(), _fail(), _keep_current_visible(), _keys(), move(), _name_candidate(), _next() (+13 more)

### Community 16 - "test_review_flow.py"
Cohesion: 0.13
Nodes (17): initial_mode(), suggest_mode(), validate_verdict(), _prefill(), check_fired(), ctx(), fail_no_critique(), fail_no_mode() (+9 more)

### Community 17 - "import_cases.py"
Cohesion: 0.20
Nodes (11): _restore_chart(), _add_headers(), _copy_style(), import_cases(), import_customers(), import_policy(), _last_row(), main() (+3 more)

### Community 18 - "Capabilities"
Cohesion: 0.23
Nodes (13): render_comparison(), render_detail(), render_result(), Capabilities, Topology, sim_comparison(), Elements, result() (+5 more)

### Community 19 - "Day 9 · Run all three: success, cost, latency"
Cohesion: 0.12
Nodes (20): Cost levers (check each against the pass rate), ₹ per resolved email (what really drives cost), Fixed monthly costs spread over all emails, Costs hidden inside today's estimate, Latency not counted (tool time, network, queues, cold start), Cost drivers measured in the notebook, Per-email costs beyond tokens, ₹ per 1,000 emails (+12 more)

### Community 20 - "Studio evidence frame"
Cohesion: 0.25
Nodes (3): Evidence, mask(), nonempty()

### Community 21 - "RunResult"
Cohesion: 0.16
Nodes (12): make_provider(), SimulationService, RunResult, replay_sources(), selected_sim_version(), sim_fields(), sim_pipe(), sim_replay_options() (+4 more)

### Community 22 - "Release gates and error costs (thresholds.yml)"
Cohesion: 0.18
Nodes (8): load_thresholds(), Error cost (INR, per 1,000 emails), Agent hours per 1,000 emails, costs_inr, missed_escalation, unneeded_escalation, unsafe_auto_send, review_minutes_per_case

### Community 23 - "RunStore"
Cohesion: 0.18
Nodes (3): _json(), _now(), RunStore

### Community 24 - "test_guardrails.py"
Cohesion: 0.08
Nodes (23): _trace(), user_prompt(), Workflow, draft(), fetch(), human(), receive(), route() (+15 more)

### Community 25 - "Build a workflow, not an agent: B + safety router + policy verifier"
Cohesion: 0.14
Nodes (13): Open question: which failures come from model size vs prompt or grader? (P4, P5), ADR-001: How Acme Fibre should answer customer emails, Day 10: C on hosted glm-5.3-flash, held-out, ADR-001 evidence table (day 9 runs), ADR self-check, 5-minute CTO readout (pitch script), ADR-001 executive readout (9 slides), Documenting Architecture Decisions (Michael Nygard) (+5 more)

### Community 26 - "acme_metrics.py"
Cohesion: 0.11
Nodes (8): eval_checks(), Deps, to_record(), build_frame(), fig_html(), layer_of(), demo_verdict(), main()

### Community 27 - "Rule 8 · ₹500 limit is per customer over 30 days"
Cohesion: 0.19
Nodes (14): Failure category: unapproved offer, KB04 · Refunds and credits, KB06 · Outage credit, KB11 · Retention offer, ₹500 refund/credit limit, not_english(), _retention_offer_rupees(), reveals_limit() (+6 more)

### Community 28 - "lab.py"
Cohesion: 0.10
Nodes (15): _bool(), export_to_excel(), _history(), _item(), load_lab(), _payments(), _put(), read_review_log() (+7 more)

### Community 29 - "Day 1: one model call"
Cohesion: 0.13
Nodes (19): Day 01 notebook (an-llm-call-is-http), ask(), Deep Dive into LLMs like ChatGPT (Karpathy), inference chapter, Ollama /api/chat endpoint, qwen3:4b local model, Per-step agent trace, Forward Deployed Engineer (FDE) mindset, Local models on Ollama (zero cost) (+11 more)

### Community 30 - "RunInput"
Cohesion: 0.11
Nodes (24): compare_results(), review_record(), RunInput, run_case(), _run_missing(), worker(), one(), _run_one() (+16 more)

### Community 31 - "version_c3"
Cohesion: 0.16
Nodes (13): Business Graph Engine (graph computes, LLM verbalizes), Today: passive prompt glossary (LLM does the joins), Phase 0 · Baseline audit, Phase 1 · Rich TBox schema, Static TBox (shared meaning, zero PII), Meaning flow: policy.md + kb.md → ontology.ttl → pyoxigraph → glossary(), Version B + glossary experiment (B_glossary), pyoxigraph (in-process RDF store, SPARQL 1.1) (+5 more)

### Community 32 - "version_c3.py"
Cohesion: 0.09
Nodes (25): Tool dispatch FUNCTIONS[name](**args), Concept → KB retrieval gain (with alias leakage caveat), SYSTEM_C agent prompt, Load customer card and outages (code, no model), KB01 · Billing cycle and due dates, Acme help articles (kb.md), conversation(), customer_card() (+17 more)

### Community 33 - "load_business_rules"
Cohesion: 0.20
Nodes (7): _deep_update(), _default_rules(), load_business_rules(), months_since(), outage_exceeds_hours(), _parse_date(), _rules_at()

### Community 34 - "load_cases"
Cohesion: 0.14
Nodes (13): Day 11 notebook (recommendation-first-draft), evidence(), percentile(), two_se(), load_cases(), Scenario Outline: The guide's edge cases match the expert labels, Scenario: Every intent has a definition, Feature: One written convention decides the intent label (+5 more)

### Community 35 - "Acme Fibre (fictional Pune broadband ISP)"
Cohesion: 0.14
Nodes (11): Five discoveries, five architecture pivots, Building effective agents (Anthropic), Email-to-reply decision map, Workflow patterns: prompt chaining, routing, agent, Acme Fibre (fictional Pune broadband ISP), KB09 · Plan upgrades and downgrades, Hinglish customer emails, Workflow vs agent (+3 more)

### Community 36 - "test_simulator_http.py"
Cohesion: 0.14
Nodes (12): _endpoint(), Response, run(), Session, test_endpoints_reject_untrusted_urls(), test_http_rejects_oversized_and_invalid_drafts(), test_http_sends_auth_without_persisting_secrets(), test_http_stream_stops_after_timeout() (+4 more)

### Community 37 - "Grader mutation tests"
Cohesion: 0.13
Nodes (19): Mutation testing of the grader, Scenario Outline: The grader catches a reply that was broken on purpose, Feature: Mutation tests for the grader, Scenario Outline: The grader names the policy rule a broken reply breaks, _add_each_banned(), _append(), _cases_where(), _change_intent() (+11 more)

### Community 38 - "Day 8: agent loop and failures"
Cohesion: 0.09
Nodes (23): Stage 5 · System-level evaluation: 'Does the whole system work?', Stage 6 · Agentic AI evaluation: 'Does the agent finish the job?', Stage 7 · Continuous production evaluation: 'Is it still working for users?', Gave-up fallback at MAX_STEPS, MAX_STEPS = 6 step limit, qwen3:4b local model (temperature 0), Act: does it hold on emails we never looked at?, Decide: which single fix matters most? (+15 more)

### Community 39 - "review_page"
Cohesion: 0.17
Nodes (10): icon(), case_choices(), review_page(), score_page(), _refresh_case_choices(), score_boxes(), simulator_page(), version_choices() (+2 more)

### Community 40 - "version_a"
Cohesion: 0.15
Nodes (11): Proposed controlled workflow (deterministic routing + one drafting step), Day 04 notebook (rules-baseline), classify(), version_a(), Version A pipeline: keyword match then fill a template, ADR-001 diagram: B with a safety router and a policy check, Human support queue, Gates before replies go out unreviewed (+3 more)

### Community 42 - "version_b"
Cohesion: 0.18
Nodes (10): What the model sees (Version B context), Scoreboard on 84 cases: A vs B, Customer card context (name, area, plan), KB article context (INTENT_KB by expected intent), Building block: the augmented LLM (Anthropic, Building effective agents), Open question: how good is searched context for B? (project 2), Context engineering (the context is the product), Oracle context (B got the expected intent's articles) (+2 more)

### Community 43 - "Evaluation evidence Quarto site"
Cohesion: 0.15
Nodes (7): Acme Review Studio, Acme_Fibre_Grounded_Draft_Eval.xlsx (eval workbook), import_cases.py (lab data → workbook), tests/features/report_metrics.feature, Demo round (make_demo_runs.py), Evaluation evidence Quarto site, Acme Review Studio architecture/UX review (16 Oct 2026)

### Community 44 - "Review dashboard (when do humans help?)"
Cohesion: 0.25
Nodes (6): Code saves, Disagreement rates, What triggered the escalations (layer analysis), Failure categories (expert), Review dashboard (when do humans help?), Routing by escalation rule

### Community 45 - "Day 3 · Write the test set before the system"
Cohesion: 0.12
Nodes (19): Critique Shadowing workflow, Day 03 notebook (test-set-first), Seven intents, problems(), Your AI Product Needs Evals (Hamel Husain), Rules of Machine Learning (Google), rules 1 to 3, Stage 1 · Traditional software testing: 'Is it correct?', Stage 2 · Early machine learning evaluation: 'How accurate is it?' (+11 more)

### Community 46 - "Evaluation report (release decision)"
Cohesion: 0.21
Nodes (13): Evaluation report (release decision), Step-6 check hits, Expert pass rate, Missed escalation, Routing accuracy, Unneeded escalation, Unsafe auto-send, Where every case went (run → escalated/sent → right/missed/unneeded) (+5 more)

### Community 50 - "privacy.py"
Cohesion: 0.14
Nodes (7): redact(), RedactingSerializer, secret_values(), manifest_diff(), log(), runs/ versioned persistence, Snapshot privacy and retention

### Community 51 - "define"
Cohesion: 0.15
Nodes (13): knowledge_page(), meaning_concept_card(), meaning_rule_detail(), concept_labels(), concept_provenance(), define(), policy_rules(), Scenario: an unknown word has no definition (+5 more)

### Community 52 - "Round 1 Principal Engineer review of the Acme Fibre email drafting solution"
Cohesion: 0.15
Nodes (8): Rate, wilson(), Model needs-human flag recall, Escalation rate, Round 1 Principal Engineer review of the Acme Fibre email drafting solution, Safe-send capture rate (new north-star metric), Seeing Theory: basic probability and frequentist inference, Confidence interval

### Community 53 - "test_adapter_contract.py"
Cohesion: 0.14
Nodes (7): AppSettings, Settings, pinned(), scripted_adapter(), valid_contract(), world(), world()

### Community 54 - "test_expert_review.py"
Cohesion: 0.12
Nodes (18): tests/features/guardrails.feature (BDD guardrails), BDD policy specs, Ontology pipeline (vocabulary → taxonomy → thesaurus → ontology → knowledge graph), unasked_outage(), Feature: Escalation is reported as recall and precision, not just human_ok, Feature: The grader agrees with the expert's round-2 review, Scenario Outline: The retention offer is pre-approved (c44), Scenario Outline: The expert's verdict and the grader's agree (+10 more)

### Community 55 - "json"
Cohesion: 0.12
Nodes (5): guard_hits(), direct_output(), no_draft(), validate_draft(), State

### Community 56 - "Dataset card (Acme test set)"
Cohesion: 0.14
Nodes (8): banner(), html_table(), provenance_table(), sha256(), tiles(), workbook_sheet(), Dataset card (Acme test set), Reports overview page (index.qmd)

### Community 57 - "studio-c3.yaml"
Cohesion: 0.12
Nodes (15): adapter, config, timeout_s, adapter, implementation, model, implementation, inputs (+7 more)

### Community 58 - "ReviewStore"
Cohesion: 0.16
Nodes (9): ReviewStore, _export(), score_rounds(), load(), test_dataset_banner_omits_run_progress_but_keeps_warnings(), test_provenance_uses_full_hashes_and_escapes_values(), test_reports_select_versions_and_keep_the_round_alias(), test_legacy_reviews_migrate_and_round_trip_through_excel() (+1 more)

### Community 59 - "evals.py"
Cohesion: 0.13
Nodes (8): Examples from the expert's review (worst fails, what good looks like), Failure category: unsupported-amount false positive, amounts(), _limit_context(), other_customer_details(), _plan_in_sentence(), _record_facts(), Scenario Outline: A reply must not give away another customer's details

### Community 60 - "config"
Cohesion: 0.15
Nodes (12): adapter, config, auth, endpoint, model, output_schema, provider, timeout_s (+4 more)

### Community 61 - "Acme labelled test set (cases.jsonl)"
Cohesion: 0.21
Nodes (8): 20 SME-reviewed ground-truth scenarios, Engine audits the test set: c44 vs r20/p06a, Acme labelled test set (cases.jsonl), Domain expert (SME) review, Acme Fibre reply policy (policy.md), cases_abuse.jsonl (40 contrast pairs), cases_multiturn.jsonl (40 conversations), customers.json (40 sample customers)

### Community 68 - "C3Provider"
Cohesion: 0.21
Nodes (3): c3_output(), C3Provider, AgentLoopAdapter

### Community 69 - "versions.py"
Cohesion: 0.10
Nodes (14): Lab, OfflineProvider, endpoint_origin(), canonical(), case_hash(), digest(), lab_snapshot(), label_hash() (+6 more)

### Community 70 - "c3-agent.yaml"
Cohesion: 0.17
Nodes (11): adapter, config, max_steps, model, provider, temperature, timeout_s, implementation (+3 more)

### Community 71 - "judge_round1.py"
Cohesion: 0.33
Nodes (4): judge_prompt(), main(), work(), run_judge()

### Community 72 - "studio-offline.yaml"
Cohesion: 0.18
Nodes (10): adapter, config, model, provider, temperature, timeout_s, implementation, inputs (+2 more)

### Community 73 - "version-b.yaml"
Cohesion: 0.18
Nodes (10): adapter, config, model, provider, temperature, timeout_s, implementation, inputs (+2 more)

### Community 78 - "resume"
Cohesion: 0.22
Nodes (8): default_sim_step(), _ha(), _he(), _hh(), resume(), show_saved_run(), _sim_load(), _to_sim()

### Community 79 - "offline-direct.yaml"
Cohesion: 0.20
Nodes (9): adapter, config, model, provider, timeout_s, implementation, inputs, label (+1 more)

### Community 80 - "Load customer card and outages"
Cohesion: 0.24
Nodes (9): One model call (B) drafts the reply, Email in, Human approves the draft (shadow mode until the gates hold), Human queue (a person writes the reply), Load customer card and outages, Policy check (grader rules, in code), Reply out, Router: needs a human? (rules + 1 model call) (+1 more)

### Community 81 - "Step 6 · check claims and facts"
Cohesion: 0.47
Nodes (5): amounts(), claim_checks(), _flag(), check(), Policy verifier

### Community 82 - "Expert reviews data and errors are fixed"
Cohesion: 0.40
Nodes (5): Build LLM judge from expert examples, Error analysis: error rates, patterns, specialised judges, Expert reviews data and errors are fixed, Repeat on material change or periodic review, Principal domain expert

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
- **31 isolated node(s):** `fde-first-principles`, `Stage 1 · Traditional software testing: 'Is it correct?'`, `Fixed monthly costs spread over all emails`, `Costs hidden inside today's estimate`, `Latency not counted (tool time, network, queues, cold start)` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 443 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `server()` connect `Review Studio server` to `ontology.py`, `app.py`, `test_ontology.py`, `refresh_versions`, `test_review_flow.py`, `Capabilities`, `RunResult`, `acme_metrics.py`, `lab.py`, `RunInput`, `version_c3.py`, `load_business_rules`, `review_page`, `define`, `json`, `ReviewStore`, `versions.py`, `resume`, `Expert reviews data and errors are fixed`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `server()` (e.g. with `.all()` and `version_token()`) actually correct?**
  _`server()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fde-first-principles`, `Stage 1 · Traditional software testing: 'Is it correct?'`, `Fixed monthly costs spread over all emails` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `llm.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05052631578947368 - nodes in this community are weakly interconnected._
- **Why does `policy_violations()` connect `policy_violations` to `version_c3.py`, `load_business_rules`, `ontology.py`, `Grader mutation tests`, `test_ontology.py`, `Rule 8 · ₹500 limit is per customer over 30 days`, `score`, `build_decision_envelope`, `test_policy_rules.py`, `Load customer card and outages`, `Step 6 · check claims and facts`, `RunResult`, `test_expert_review.py`, `json`, `Build a workflow, not an agent: B + safety router + policy verifier`, `evals.py`, `Acme labelled test set (cases.jsonl)`, `version_c3`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `version_b()` and `Failure category: unsupported-amount false positive`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `search_kb()` and `Similarity search (cosine, top 3)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._