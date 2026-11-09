# Graph Report - fde-first-principles  (2026-11-09)

## Corpus Check
- 85 files · ~60,240 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 55 file(s) not represented in the graph (top: .feature 13, .drawio 11, .jsonl 11)
- WARNING: 55 of 140 files seen (39%) have no supported extractor and are missing from this graph entirely. It may look complete while representing only part of the codebase.

## Summary
- 1329 nodes · 3474 edges · 68 communities (59 shown, 9 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 679 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- LLM client and model calls
- Shared Acme data helpers and Version B
- Ontology store and glossary
- Claim checks and policy verifier
- Escalation metrics specs
- Version C3 hardened agent
- Review Studio app shell
- Ontology BDD specs
- Review Studio server
- Grader scoring and saved runs
- Studio C3 provider tests
- Decision envelope escalation specs
- Policy rule specs and known gaps
- Studio drafting providers
- Studio report metric tests
- Studio workflow and demo runs
- Studio review flow and verdicts
- Outage scope and C3 envelope
- Studio workbook import and lab
- Day 4 and 9: cost, latency, Version A
- Studio evidence frame
- needs_human escalation rules
- Grader policy violations
- Day 11-12: recommendation and article
- Entitlements and the 500 rupee limit
- Day 7: error bars and evidence
- Studio metrics module
- Refund limit and expert findings
- Studio guardrail tests
- Day 1: one model call
- Studio case import script
- Day 8: ontology layer plan
- Agent tools and KB search
- Business rules config
- Intent guide and test cases
- Test set data checks
- Expert review agreement specs
- Grader mutation tests
- Day 8: agent loop and failures
- Review Studio overview and review
- Studio UI cards
- Day 10: read the failures
- Day 6: Version B and context
- Safety router and injection guards
- Review dashboard metrics
- Acme domain, SME review, prompts
- Evaluation report release gates
- Day 2: workflow or agent
- Studio scoring rounds
- Quarto evidence site
- Day 3: test set first
- Grader checks under mutation
- Wilson intervals and rates
- Studio review page UI
- Dataset card
- LLM as judge and eval history
- Studio score plots
- Article lessons and grader gaps
- Studio resume and audit
- Day 11 evidence notebook
- Escalation triggers as code
- OWL reasoning
- KB slow speed and technician
- KB new installation
- KB search queries
- Project config

## God Nodes (most connected - your core abstractions)
1. `server()` - 84 edges
2. `policy_violations()` - 52 edges
3. `score()` - 52 edges
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
- `run_agent()` --semantically_similar_to--> `run_agent()`  [INFERRED] [semantically similar]
  1-measure-before-you-believe/08-agent-loop-from-scratch/notebook.ipynb → lab/agent.py
- `run_agent()` --semantically_similar_to--> `run_agent()`  [INFERRED] [semantically similar]
  1-measure-before-you-believe/09-success-cost-latency/notebook.ipynb → lab/agent.py
- `Parked: privacy preservation LLM judge (binary)` --semantically_similar_to--> `other_customer_details()`  [INFERRED] [semantically similar]
  1-measure-before-you-believe/05-a-grader-you-can-trust/later.md → lab/evals.py
- `Feature: The area outage is in scope only when the customer reports that their service is down` --semantically_similar_to--> `unasked_outage()`  [INFERRED] [semantically similar]
  tests/features/outage_scope.feature → lab/evals.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Project 1 · Measure before you believe: the 12 days** — concept_measure_before_you_believe, fde_day_01, fde_day_02, fde_day_03, fde_day_04, fde_day_05, fde_day_06, fde_day_07, fde_day_08, fde_day_09, fde_day_10, fde_day_11, fde_day_12 [EXTRACTED 1.00]
- **₹500 money limit across policy, KB and grader** — concept_refund_limit_500, data_acme_policy_rule_03, data_acme_policy_rule_08, data_acme_policy_rule_13, acme_kb04, acme_kb16, lab_evals_reveals_limit, lab_escalation_amounts_asked_for [INFERRED 0.85]
- **needs_human escalation triggers** — concept_needs_human_escalation, data_acme_policy_rule_06, data_acme_policy_rule_09, data_acme_policy_rule_11, acme_kb15, acme_kb16, lab_escalation_escalation_triggers [INFERRED 0.85]
- **Expert review → policy and tests feedback loop** — 1_measure_before_you_believe_03_test_set_first_acme_review_studio_readme_critique_shadowing_loop, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_readme_review_page, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_readme_eval_workbook, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_label_corrections, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_fix_order, concept_domain_expert_review, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_readme_report_metrics_feature [INFERRED 0.85]
- **Round 1 failure modes and their fixes** — 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_mode1_amount_check_false_positive, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_mode2_model_over_escalation, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_mode3_unapproved_retention_offer, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_measurement_framework, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_round1_principal_engineer_review_fix_order [EXTRACTED 1.00]
- **Release gate metrics from acme_metrics and thresholds.yml** — 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_evaluation_report_metric_expert_pass_rate, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_evaluation_report_metric_routing_accuracy, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_evaluation_report_metric_missed_escalation, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_evaluation_report_metric_unsafe_auto_send, 1_measure_before_you_believe_03_test_set_first_acme_review_studio_reports_readme_release_gates_thresholds [EXTRACTED 1.00]
- **score(): four yes/no checks that must all pass** — lab_evals_score, 1_measure_before_you_believe_05_a_grader_you_can_trust_day5_grader_explained_intent_ok, 1_measure_before_you_believe_05_a_grader_you_can_trust_day5_grader_explained_facts_ok, 1_measure_before_you_believe_05_a_grader_you_can_trust_day5_grader_explained_policy_ok, 1_measure_before_you_believe_05_a_grader_you_can_trust_day5_grader_explained_human_ok, 1_measure_before_you_believe_05_a_grader_you_can_trust_day5_grader_explained_passed [EXTRACTED 1.00]
- **Grading the grader: three bugs fixed and locked in by regression tests** — 1_measure_before_you_believe_05_a_grader_you_can_trust_notebook_otp_safety_advice_false_alarm, 1_measure_before_you_believe_05_a_grader_you_can_trust_notebook_kb_times_as_fix_promises, 1_measure_before_you_believe_05_a_grader_you_can_trust_notebook_cross_sentence_refund, 1_measure_before_you_believe_05_a_grader_you_can_trust_notebook_grader_regression_tests, lab_evals_policy_violations [EXTRACTED 1.00]
- **@known_gap scenario groups run as strict xfail** — concept_known_gap_xfail, tests_features_policy_rules_known_gaps, tests_features_policy_rules_known_gaps_restated_request, tests_features_policy_rules_known_gaps_concession, tests_features_grader_mutations_known_gaps [EXTRACTED 1.00]
- **Everything Version B feeds the model in one call** — 1_measure_before_you_believe_06_one_llm_call_notebook_system_prompt, 1_measure_before_you_believe_06_one_llm_call_notebook_customer_card_context, 1_measure_before_you_believe_06_one_llm_call_notebook_kb_article_context, 1_measure_before_you_believe_06_one_llm_call_notebook_answer_schema, lab_version_b_version_b, lab_llm_chat [EXTRACTED 1.00]
- **What must match between the chat and embedding models** — 1_measure_before_you_believe_06_one_llm_call_day6_embedding_compatibility_same_embedding_model, 1_measure_before_you_believe_06_one_llm_call_day6_embedding_compatibility_same_input_format, 1_measure_before_you_believe_06_one_llm_call_day6_embedding_compatibility_both_handle_hinglish, 1_measure_before_you_believe_06_one_llm_call_day6_embedding_compatibility_fits_context_limit, 1_measure_before_you_believe_06_one_llm_call_day6_embedding_compatibility_fit_in_memory [EXTRACTED 1.00]
- **Seven stages of AI evaluation evolution** — 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage1_traditional_testing, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage2_early_ml_eval, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage3_foundation_model_eval, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage4_statistical_eval, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage5_system_level_eval, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage6_agentic_eval, 1_measure_before_you_believe_07_error_bars_day7_evolution_of_ai_evals_stage7_continuous_production_eval [EXTRACTED 1.00]
- **Version C agent loop cycle (model call, tool dispatch, result back, stop or step limit)** — lab_llm_chat, 1_measure_before_you_believe_08_agent_loop_from_scratch_agent_loop_tool_dispatch, 1_measure_before_you_believe_08_agent_loop_from_scratch_agent_loop_tool_result_message, 1_measure_before_you_believe_08_agent_loop_from_scratch_agent_loop_stop_condition, 1_measure_before_you_believe_08_agent_loop_from_scratch_notebook_max_steps, 1_measure_before_you_believe_08_agent_loop_from_scratch_agent_loop_final_answer, lab_agent_run_agent [EXTRACTED 1.00]
- **Business Graph Engine runtime: concept linker → entitlements → decision envelope → guard, prompt, grader** — lab_ontology_extract_concepts, lab_ontology_compute_entitlements, lab_version_c3_build_decision_envelope, 1_measure_before_you_believe_08_agent_loop_from_scratch_business_graph_engine_plan_amount_guard, lab_version_c3_version_c3, lab_evals_policy_violations [EXTRACTED 1.00]
- **Acme concession taxonomy and the ₹500 limit** — concept_concession, concept_refund_term, concept_credit_term, concept_discount_term, concept_double_payment_refund, concept_outage_credit, concept_retention_offer, concept_late_fee_waiver, concept_refund_limit_500 [EXTRACTED 1.00]
- **Day 10 OODA error-analysis loop** — 1_measure_before_you_believe_10_read_the_failures_day10_read_the_failures_observe, 1_measure_before_you_believe_10_read_the_failures_day10_read_the_failures_orient, 1_measure_before_you_believe_10_read_the_failures_day10_read_the_failures_decide, 1_measure_before_you_believe_10_read_the_failures_day10_read_the_failures_act, 1_measure_before_you_believe_10_read_the_failures_readme_ooda_loop [EXTRACTED 1.00]
- **What drives the cost of one resolved email** — 1_measure_before_you_believe_09_success_cost_latency_day9_success_cost_latency_cost_per_resolved_email, 1_measure_before_you_believe_09_success_cost_latency_day9_success_cost_latency_measured_cost_drivers, 1_measure_before_you_believe_09_success_cost_latency_day9_success_cost_latency_hidden_cost_drivers, 1_measure_before_you_believe_09_success_cost_latency_day9_success_cost_latency_per_email_costs_beyond_tokens, 1_measure_before_you_believe_09_success_cost_latency_day9_success_cost_latency_fixed_monthly_costs [EXTRACTED 1.00]
- **Version C3 escalation sources (rule, guard, offer, model)** — lab_escalation_escalation_triggers, lab_version_c3_offers_not_allowed, lab_evals_not_english, lab_version_c3_run_agent, tests_features_escalation_rules_every_escalation_records_source [INFERRED 0.85]
- **Recommended workflow: email in → card → router → search → B draft → policy check → shadow approval → reply out** — 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_email_in, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_load_customer_card_outages, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_router_needs_human, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_search_help_articles, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_draft_reply_b, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_policy_check, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_human_approves_draft, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_reply_out, 1_measure_before_you_believe_11_recommendation_first_draft_day11_adr_human_queue [EXTRACTED 1.00]
- **ADR-001 falsification triggers** — 1_measure_before_you_believe_11_recommendation_first_draft_decision_change_mind_router_misses, 1_measure_before_you_believe_11_recommendation_first_draft_decision_change_mind_c_stronger_model, 1_measure_before_you_believe_11_recommendation_first_draft_decision_change_mind_searched_context, 1_measure_before_you_believe_11_recommendation_first_draft_decision_recommendation [EXTRACTED 1.00]
- **ADR-001 options: chosen guarded B vs rejected A, plain B and C** — 1_measure_before_you_believe_11_recommendation_first_draft_decision_recommendation, 1_measure_before_you_believe_11_recommendation_first_draft_decision_rejected_option_a_rules, 1_measure_before_you_believe_11_recommendation_first_draft_decision_rejected_plain_b, 1_measure_before_you_believe_11_recommendation_first_draft_decision_rejected_option_c_agent [INFERRED 0.85]
- **Five discoveries that turn an agent into a workflow** — 1_measure_before_you_believe_02_workflow_or_agent_acme_fiber_storyboard_pivot_remove_ai_classification, 1_measure_before_you_believe_02_workflow_or_agent_acme_fiber_storyboard_pivot_fact_retrieval, 1_measure_before_you_believe_02_workflow_or_agent_acme_fiber_storyboard_pivot_verified_sources, 1_measure_before_you_believe_02_workflow_or_agent_acme_fiber_storyboard_pivot_guardrails, 1_measure_before_you_believe_02_workflow_or_agent_acme_fiber_storyboard_pivot_measure_before_committing [EXTRACTED 1.00]
- **ADR-001 reply pipeline** — 1_measure_before_you_believe_11_recommendation_first_draft_diagram_load_customer_card, concept_safety_router, 1_measure_before_you_believe_11_recommendation_first_draft_diagram_search_help_articles, lab_version_b_version_b, concept_policy_verifier, concept_shadow_mode [EXTRACTED 1.00]

## Communities (68 total, 9 thin omitted)

### Community 0 - "LLM client and model calls"
Cohesion: 0.05
Nodes (40): judge_prompt(), main(), work(), run_judge(), Build LLM judge from expert examples, Error analysis: error rates, patterns, specialised judges, Expert reviews data and errors are fixed, Repeat on material change or periodic review (+32 more)

### Community 1 - "Shared Acme data helpers and Version B"
Cohesion: 0.08
Nodes (22): What the model sees (Version B context), Day 06 notebook (one-llm-call), Customer card context (name, area, plan), evaluate(), KB article context (INTENT_KB by expected intent), unit(), user_message(), version_b() (+14 more)

### Community 2 - "Ontology store and glossary"
Cohesion: 0.11
Nodes (21): KnowledgeArticle and PolicyRule IRIs (documentedIn, enforcesRule), acme:Plan catalog (Basic ₹699, Plus ₹999, Pro ₹1,499), acme:PuneServiceArea (8 areas), KB09 · Plan upgrades and downgrades, KB12 · Shifting your connection, Acme plans: Basic, Plus, Pro, _alias_index(), _bool_value() (+13 more)

### Community 3 - "Claim checks and policy verifier"
Cohesion: 0.09
Nodes (23): Five discoveries, five architecture pivots, amounts(), claim_checks(), _flag(), _trace(), user_prompt(), check(), draft() (+15 more)

### Community 4 - "Escalation metrics specs"
Cohesion: 0.10
Nodes (20): pipeline(), sim_pipe(), Elements, test_icons_have_no_network_or_accessible_name(), test_pipeline_keyboard_order_and_untrusted_details(), Safety scoreboard (safe, missed escalations, human intervention, passed), summary(), pytest_bdd_apply_tag() (+12 more)

### Community 5 - "Version C3 hardened agent"
Cohesion: 0.10
Nodes (19): Concept → KB retrieval gain (with alias leakage caveat), Phase 3 · Wire grader and router, cases_multiturn.jsonl (40 conversations), conversation(), intent_guide(), extract_concepts(), check_entitlement(), define_term() (+11 more)

### Community 6 - "Review Studio app shell"
Cohesion: 0.09
Nodes (5): AppSettings, highlight(), Settings, State, runs/ persistence (reviews.json, runs.jsonl, checkpoints.sqlite, settings.json)

### Community 7 - "Ontology BDD specs"
Cohesion: 0.12
Nodes (28): glossary(), ontology.feature: every agent gets the same meaning for policy words, Scenario: business rules evolve without changing the ontology, Scenario outline: entitlement computation joins ontology, rules and one record, Scenario: the glossary holds definitions, never customer records, Scenario: operational governance has zero catalog drift, Scenario: OWL reasoner inherits class properties and respects overrides, Scenario outline: every money and identity term is defined and cites its policy (+20 more)

### Community 8 - "Review Studio server"
Cohesion: 0.09
Nodes (19): server(), batch_rev(), batch_status(), case_editor(), case_list(), case_of(), _ed_save(), edit_case() (+11 more)

### Community 9 - "Grader scoring and saved runs"
Cohesion: 0.11
Nodes (18): Three graders: factual grounding, escalation correctness, response quality, Day 10 notebook (read-the-failures), Failure category: grader wrong, Failure category: unsupported-amount false positive, passed(), Run provenance (.meta.json: model, prompt fingerprint, settings), scoreboard(), show() (+10 more)

### Community 10 - "Studio C3 provider tests"
Cohesion: 0.10
Nodes (20): c3_fails(), c3_given_case(), c3_given_history(), c3_replies(), draft_cites(), draft_needs_human(), draft_reason(), draft_says() (+12 more)

### Community 11 - "Decision envelope escalation specs"
Cohesion: 0.13
Nodes (21): Phase 2 · Graph engine core, build_decision_envelope(), Scenario: An amount the agent wrote in an earlier turn is not the customer's ask, Scenario: No rule fires on any case the experts labelled "no human needed", Scenario Outline: A draft that offers more than its decision allows goes to a person, agent_finishes(), agent_replied(), customer_earlier_wrote() (+13 more)

### Community 12 - "Policy rule specs and known gaps"
Cohesion: 0.11
Nodes (22): Failure category: unapproved offer, @known_gap scenarios as strict xfail, _promises_concession(), unearned_concession(), Feature: The grader enforces the Acme Fibre reply policy, @known_gap Scenario Outline: Known gaps the grader does not handle yet, @known_gap Scenario Outline: Known gaps in the concession check, @known_gap Scenario Outline: Known gaps in the restated-request check (+14 more)

### Community 13 - "Studio drafting providers"
Cohesion: 0.11
Nodes (8): c3_output(), C3Provider, ClaudeCodeProvider, make_provider(), OfflineProvider, _parse_json_text(), _result(), _settings()

### Community 14 - "Studio report metric tests"
Cohesion: 0.13
Nodes (22): banner(), cases_run(), code_saves(), demo(), escalated(), escalated_by_code(), layer_fired(), missed() (+14 more)

### Community 15 - "Studio workflow and demo runs"
Cohesion: 0.14
Nodes (8): eval_checks(), ReviewStore, Deps, to_record(), Workflow, run_case(), demo_verdict(), main()

### Community 16 - "Studio review flow and verdicts"
Cohesion: 0.13
Nodes (17): initial_mode(), suggest_mode(), validate_verdict(), _prefill(), check_fired(), ctx(), fail_no_critique(), fail_no_mode() (+9 more)

### Community 17 - "Outage scope and C3 envelope"
Cohesion: 0.11
Nodes (14): customer_reported_outage(), _envelope_brief(), version_c3(), Scenario Outline: The envelope shows the outage only when the customer reports one, Scenario: The customer-record tools show the outage when the customer reports one, test_blank_or_cut_off_reply_is_never_sendable(), agent_finishes(), customer_writes() (+6 more)

### Community 18 - "Studio workbook import and lab"
Cohesion: 0.13
Nodes (13): _bool(), export_to_excel(), _history(), _item(), Lab, load_lab(), _payments(), _put() (+5 more)

### Community 19 - "Day 4 and 9: cost, latency, Version A"
Cohesion: 0.12
Nodes (19): Day 04 notebook (rules-baseline), classify(), version_a(), Per-step agent trace, Cost levers (check each against the pass rate), ₹ per resolved email (what really drives cost), Fixed monthly costs spread over all emails, Costs hidden inside today's estimate (+11 more)

### Community 20 - "Studio evidence frame"
Cohesion: 0.21
Nodes (4): Evidence, mask(), nonempty(), Code saves

### Community 21 - "needs_human escalation rules"
Cohesion: 0.15
Nodes (19): Gave-up fallback at MAX_STEPS, acme:EscalationTrigger (planned), MAX_STEPS = 6 step limit, Failure category: missed escalation, KB10 · Cancellation and notice period, KB15 · Account security, KB16 · Talking to a human, BDD policy specs (+11 more)

### Community 22 - "Grader policy violations"
Cohesion: 0.14
Nodes (11): Examples from the expert's review (worst fails, what good looks like), KB03 · Payment methods, KB05 · Outages and restoration updates, KB13 · Router and Wi-Fi password, _negated(), not_english(), policy_violations(), _retention_offer_rupees() (+3 more)

### Community 23 - "Day 11-12: recommendation and article"
Cohesion: 0.14
Nodes (15): Safe-send capture rate (new north-star metric), Day 11 ADR-001 diagram, Open question: which failures come from model size vs prompt or grader? (P4, P5), ADR-001: How Acme Fibre should answer customer emails, Day 10: C on hosted glm-5.3-flash, held-out, Open question: how good is searched context for B? (project 2), ADR self-check, 5-minute CTO readout (pitch script) (+7 more)

### Community 24 - "Entitlements and the 500 rupee limit"
Cohesion: 0.13
Nodes (21): acme:AccountAction requiresRole AccountHolder, Ephemeral per-case ABox (one customer), Varun's ₹300 credit: three agents, three meanings, Account holder, data/acme/business_rules.json (commercial thresholds), Concession (refund, credit, waiver, discount value), Credit, Customer (+13 more)

### Community 25 - "Day 7: error bars and evidence"
Cohesion: 0.16
Nodes (16): Stage 4 · Statistical evaluation: 'How sure are we?', A statistical approach to model evaluations (Anthropic), Seeing Theory: basic probability and frequentist inference, Phase 4 · Empirical verdict, ADR-001 evidence table (day 9 runs), Open question: do numbers hold on a stronger model and real emails? (project 6), Evidence table rebuilt from saved runs (data/results), Technical Writing One (Google): Short sentences (+8 more)

### Community 26 - "Studio metrics module"
Cohesion: 0.11
Nodes (9): banner(), build_frame(), fig_html(), layer_of(), load(), sha256(), tiles(), Reports overview page (index.qmd) (+1 more)

### Community 27 - "Refund limit and expert findings"
Cohesion: 0.22
Nodes (11): Round 1 Principal Engineer review of the Acme Fibre email drafting solution, Multilingual lexical layer (SKOS labels), KB02 · Late payment fee, KB04 · Refunds and credits, KB06 · Outage credit, KB11 · Retention offer, ₹500 refund/credit limit, reveals_limit() (+3 more)

### Community 28 - "Studio guardrail tests"
Cohesion: 0.13
Nodes (13): email_from(), flags(), human_chooses(), lab(), model_drafts(), not_called(), outcome(), reason() (+5 more)

### Community 29 - "Day 1: one model call"
Cohesion: 0.14
Nodes (17): Day 01 notebook (an-llm-call-is-http), ask(), Deep Dive into LLMs like ChatGPT (Karpathy), inference chapter, Ollama /api/chat endpoint, qwen3:4b local model, Forward Deployed Engineer (FDE) mindset, Local models on Ollama (zero cost), Project 1 · Measure before you believe (+9 more)

### Community 30 - "Studio case import script"
Cohesion: 0.20
Nodes (12): _restore_chart(), _add_headers(), _copy_style(), import_cases(), import_customers(), import_policy(), _last_row(), main() (+4 more)

### Community 31 - "Day 8: ontology layer plan"
Cohesion: 0.13
Nodes (10): Business Graph Engine (graph computes, LLM verbalizes), Phase 0 · Baseline audit, Phase 1 · Rich TBox schema, Static TBox (shared meaning, zero PII), Meaning flow: policy.md + kb.md → ontology.ttl → pyoxigraph → glossary(), Version B + glossary experiment (B_glossary), pyoxigraph (in-process RDF store, SPARQL 1.1), term_misread failure tag (+2 more)

### Community 32 - "Agent tools and KB search"
Cohesion: 0.17
Nodes (11): Tool dispatch FUNCTIONS[name](**args), KB01 · Billing cycle and due dates, Acme help articles (kb.md), first_name(), kb_by_id(), load_kb(), escalate(), get_article() (+3 more)

### Community 33 - "Business rules config"
Cohesion: 0.15
Nodes (7): _deep_update(), _default_rules(), duplicate_payment_amount(), load_business_rules(), months_since(), outage_exceeds_hours(), _parse_date()

### Community 34 - "Intent guide and test cases"
Cohesion: 0.14
Nodes (10): Day 05 notebook (a-grader-you-can-trust), load_cases(), Scenario Outline: The guide's edge cases match the expert labels, Scenario: Every intent has a definition, Feature: One written convention decides the intent label, Scenario Outline (@known_gap): Labels that disagree with the guide, case_is_labelled(), every_intent_defined() (+2 more)

### Community 35 - "Test set data checks"
Cohesion: 0.16
Nodes (9): Hinglish customer emails, cases_regional.jsonl (52 regional-language cases), cases(), _problems(), test_cases_match_the_customer_record(), test_labels_are_valid(), check(), test_language_label_matches_the_script() (+1 more)

### Community 36 - "Expert review agreement specs"
Cohesion: 0.19
Nodes (11): Feature: The grader agrees with the expert's round-2 review, Scenario Outline: The retention offer is pre-approved (c44), Scenario Outline: The expert's verdict and the grader's agree, a_draft_handed_off(), a_draft_sent(), checks_that_fail(), given_test_case(), grader_flags() (+3 more)

### Community 37 - "Grader mutation tests"
Cohesion: 0.19
Nodes (13): _add_each_banned(), _append(), _cases_where(), _drop_each_fact(), grader_fails(), grader_flags(), grader_passes(), mutate() (+5 more)

### Community 38 - "Day 8: agent loop and failures"
Cohesion: 0.17
Nodes (11): issue_refund tool (data-changing, deferred), qwen3:4b local model (temperature 0), Failure category: bad JSON, Failure category: gave up, Failure category: over-escalation on an answerable case, Failure category: wrong tool, Fix: stronger model behind C's agent loop (C2), Agent loop (+3 more)

### Community 39 - "Review Studio overview and review"
Cohesion: 0.13
Nodes (8): _export(), simulator_page(), Acme Review Studio, Acme_Fibre_Grounded_Draft_Eval.xlsx (eval workbook), tests/features/guardrails.feature (BDD guardrails), Simulator page, Demo round (make_demo_runs.py), Acme Review Studio architecture/UX review (16 Oct 2026)

### Community 40 - "Studio UI cards"
Cohesion: 0.16
Nodes (16): chip(), customer_chips(), cur(), draft_meta(), email_card(), expected_card(), guard_try_result(), provider_status() (+8 more)

### Community 41 - "Day 10: read the failures"
Cohesion: 0.16
Nodes (14): Stage 5 · System-level evaluation: 'Does the whole system work?', Stage 6 · Agentic AI evaluation: 'Does the agent finish the job?', Stage 7 · Continuous production evaluation: 'Is it still working for users?', Today: passive prompt glossary (LLM does the joins), Act: does it hold on emails we never looked at?, Decide: which single fix matters most?, Observe: what does a pass rate hide?, Orient: have we seen this failure before? (+6 more)

### Community 42 - "Day 6: Version B and context"
Cohesion: 0.22
Nodes (7): Scoreboard on 84 cases: A vs B, Version A pipeline: keyword match then fill a template, Building block: the augmented LLM (Anthropic, Building effective agents), Context engineering (the context is the product), Oracle context (B got the expected intent's articles), Day 6 · Version B: one model call with the right context, version_b()

### Community 43 - "Safety router and injection guards"
Cohesion: 0.21
Nodes (8): guard_hits(), decide(), 20 SME-reviewed ground-truth scenarios, Unsafe-to-automate case category, Amount guard (C3 only, not yet a router), Open question: can a learned classifier route escalations better? (project 3), Prompt injection / manipulation attempts, Safety router

### Community 44 - "Review dashboard metrics"
Cohesion: 0.15
Nodes (12): Error cost (INR, per 1,000 emails), Agent hours per 1,000 emails, Disagreement rates, Escalation rate, Failure categories (expert), Review dashboard (when do humans help?), Routing by escalation rule, costs_inr (+4 more)

### Community 45 - "Acme domain, SME review, prompts"
Cohesion: 0.19
Nodes (10): draft_cases(), Engine audits the test set: c44 vs r20/p06a, SYSTEM_C agent prompt, Acme Fibre (fictional Pune broadband ISP), Domain expert (SME) review, Acme Fibre reply policy (policy.md), cases_abuse.jsonl (40 contrast pairs), customers.json (40 sample customers) (+2 more)

### Community 46 - "Evaluation report release gates"
Cohesion: 0.21
Nodes (13): Evaluation report (release decision), Step-6 check hits, Expert pass rate, Missed escalation, Routing accuracy, Unneeded escalation, Unsafe auto-send, Where every case went (run → escalated/sent → right/missed/unneeded) (+5 more)

### Community 47 - "Day 2: workflow or agent"
Cohesion: 0.21
Nodes (10): Proposed controlled workflow (deterministic routing + one drafting step), Building effective agents (Anthropic), Email-to-reply decision map, Workflow patterns: prompt chaining, routing, agent, ADR-001 diagram: B with a safety router and a policy check, Human support queue, Gates before replies go out unreviewed, Search the help articles (retrieved, not oracle context) (+2 more)

### Community 48 - "Studio scoring rounds"
Cohesion: 0.21
Nodes (10): _prefill_key(), progress(), rnd(), round_data(), _run_missing(), worker(), one(), _run_one() (+2 more)

### Community 49 - "Quarto evidence site"
Cohesion: 0.18
Nodes (3): tests/features/report_metrics.feature, load_thresholds(), Evaluation evidence Quarto site

### Community 50 - "Day 3: test set first"
Cohesion: 0.31
Nodes (8): Day 03 notebook (test-set-first), Seven intents, problems(), Your AI Product Needs Evals (Hamel Husain), Rules of Machine Learning (Google), rules 1 to 3, Acme labelled test set (cases.jsonl), Write the test set before the system, Day 3 · Write the test set before the system

### Community 51 - "Grader checks under mutation"
Cohesion: 0.20
Nodes (7): Mutation testing of the grader, Scenario Outline: The grader catches a reply that was broken on purpose, Feature: Mutation tests for the grader, Scenario Outline: The grader ignores changes that keep the reply correct, @known_gap Scenario Outline: Known gaps: correct replies the grader still fails, _change_intent(), passing_replies()

### Community 52 - "Wilson intervals and rates"
Cohesion: 0.29
Nodes (3): Rate, wilson(), Model needs-human flag recall

### Community 53 - "Studio review page UI"
Cohesion: 0.25
Nodes (6): icon(), review_page(), score_page(), case_header(), score_boxes(), Review page

### Community 54 - "Dataset card"
Cohesion: 0.25
Nodes (3): html_table(), workbook_sheet(), Dataset card (Acme test set)

### Community 55 - "LLM as judge and eval history"
Cohesion: 0.25
Nodes (5): Critique Shadowing workflow, Stage 1 · Traditional software testing: 'Is it correct?', Stage 2 · Early machine learning evaluation: 'How accurate is it?', Stage 3 · Foundation model evaluation: 'Is it good, safe, and grounded?', LLM as judge

### Community 56 - "Studio score plots"
Cohesion: 0.33
Nodes (5): score_confusion(), score_modes(), score_plot(), score_rules(), scored()

### Community 58 - "Studio resume and audit"
Cohesion: 0.40
Nodes (4): _ha(), _he(), _hh(), resume()

### Community 59 - "Day 11 evidence notebook"
Cohesion: 0.60
Nodes (4): Day 11 notebook (recommendation-first-draft), evidence(), percentile(), two_se()

## Ambiguous Edges - Review These
- `search_kb()` → `Similarity search (cosine, top 3)`  [AMBIGUOUS]
  1-measure-before-you-believe/06-one-llm-call/day6-embedding-compatibility.drawio · relation: semantically_similar_to
- `run_agent()` → `Failure category: unapproved offer`  [AMBIGUOUS]
  1-measure-before-you-believe/10-read-the-failures/notebook.ipynb · relation: references
- `version_b()` → `Failure category: unsupported-amount false positive`  [AMBIGUOUS]
  1-measure-before-you-believe/10-read-the-failures/notebook.ipynb · relation: references
- `ADR-001: How Acme Fibre should answer customer emails` → `Open question: which failures come from model size vs prompt or grader? (P4, P5)`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/day11-adr.drawio · relation: conceptually_related_to
- `ADR-001: How Acme Fibre should answer customer emails` → `Pitch claim: drafts cut handle time 40-60% in Phase 1`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/pitch.md · relation: conceptually_related_to
- `Build a workflow, not an agent: B + safety router + policy verifier` → `Pitch claim: deterministic workflow topology with hard guarantees`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/pitch.md · relation: conceptually_related_to
- `Build a workflow, not an agent: B + safety router + policy verifier` → `Phased rollout: shadow mode, then automated egress per intent`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/presentation.md · relation: conceptually_related_to
- `Build a workflow, not an agent: B + safety router + policy verifier` → `Author's unease: instinct favours C`  [AMBIGUOUS]
  1-measure-before-you-believe/12-article/article.md · relation: conceptually_related_to
- `ADR-001 evidence table (day 9 runs)` → `Pitch claim: Option A missed 40 of 40 (0% safety)`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/pitch.md · relation: conceptually_related_to
- `ADR-001 evidence table (day 9 runs)` → `Pitch claim: router adds under 500 ms and ₹0.10 per 1,000 emails`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/pitch.md · relation: conceptually_related_to
- `Open question: can a learned classifier route escalations better? (project 3)` → `Roadmap claim: transformer classifier drops router latency from 500 ms to under 20 ms`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/presentation.md · relation: conceptually_related_to
- `Cost is not the issue (B ≈ ₹1.60/day, C ≈ ₹10/day)` → `Pitch claim: agent fails unit economics`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/pitch.md · relation: conceptually_related_to
- `Pitch claim: drafts cut handle time 40-60% in Phase 1` → `Phased rollout: shadow mode, then automated egress per intent`  [AMBIGUOUS]
  1-measure-before-you-believe/11-recommendation-first-draft/presentation.md · relation: conceptually_related_to

## Knowledge Gaps
- **28 isolated node(s):** `fde-first-principles`, `Project 2 · Meaning as numbers`, `Project 3 · Learn a formula from data`, `Project 4 · Backprop by hand (micrograd)`, `Project 5 · Tiny GPT` (+23 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 294 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `server()` connect `Review Studio server` to `LLM client and model calls`, `Escalation metrics specs`, `Review Studio app shell`, `Review Studio overview and review`, `Studio UI cards`, `Safety router and injection guards`, `Studio drafting providers`, `Studio workflow and demo runs`, `Studio review flow and verdicts`, `Studio scoring rounds`, `Studio workbook import and lab`, `Studio review page UI`, `Studio score plots`, `Studio resume and audit`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `server()` (e.g. with `.all()` and `Expert reviews data and errors are fixed`) actually correct?**
  _`server()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fde-first-principles`, `Project 2 · Meaning as numbers`, `Project 3 · Learn a formula from data` to the rest of the system?**
  _28 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `LLM client and model calls` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._
- **Why does `policy_violations()` connect `Grader policy violations` to `Agent tools and KB search`, `Shared Acme data helpers and Version B`, `Intent guide and test cases`, `Claim checks and policy verifier`, `Business rules config`, `Version C3 hardened agent`, `Ontology store and glossary`, `Ontology BDD specs`, `Grader scoring and saved runs`, `Policy rule specs and known gaps`, `Acme domain, SME review, prompts`, `Day 11-12: recommendation and article`, `Entitlements and the 500 rupee limit`, `Article lessons and grader gaps`, `Refund limit and expert findings`, `Day 8: ontology layer plan`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `search_kb()` and `Similarity search (cosine, top 3)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `run_agent()` and `Failure category: unapproved offer`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._