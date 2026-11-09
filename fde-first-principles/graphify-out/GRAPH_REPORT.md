# Graph Report - fde-first-principles  (2026-11-09)

## Corpus Check
- 52 files · ~61,893 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 55 file(s) not represented in the graph (top: .feature 13, .drawio 11, .jsonl 11)
- WARNING: 55 of 140 files seen (39%) have no supported extractor and are missing from this graph entirely. It may look complete while representing only part of the codebase.

## Summary
- 1352 nodes · 3546 edges · 69 communities (55 shown, 14 thin omitted)
- Extraction: 80% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 679 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6ccbc9b9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- json
- chat
- ontology.py
- score
- Escalation metrics specs
- plans
- workflow.py
- Ontology BDD specs
- Review Studio server
- acme.py
- test_c3_provider.py
- version_c3.py
- policy_violations
- test_escalation_rules.py
- Studio report metric tests
- Studio workflow and demo runs
- Studio review flow and verdicts
- version_c3
- Studio workbook import and lab
- Day 4 and 9: cost, latency, Version A
- Studio evidence frame
- needs_human escalation
- evals.py
- Day 11-12: recommendation and article
- excluded_from_limit
- Day 7: error bars and evidence
- Studio metrics module
- Refund limit and expert findings
- Studio guardrail tests
- Day 1: one model call
- Studio case import script
- Ontology layer for Acme Fibre
- load_customers
- load_business_rules
- concept_provenance
- Test set data checks
- Day 08 notebook (agent-loop-from-scratch)
- Grader mutation tests
- Day 8: agent loop and failures
- app.py
- Studio UI cards
- judge_round1.py
- version_b
- Evaluation evidence Quarto site
- Review dashboard (when do humans help?)
- ADR-001 diagram: B with a safety router and a policy check
- Evaluation report (release decision)
- embed
- Studio scoring rounds
- Scenario outline: regional or informal word maps to the policy term
- Domain expert (SME) review
- extract_json
- Wilson intervals and rates
- reason_owl_rl
- Article lessons and grader gaps
- Acme Review Studio architecture/UX review (16 Oct 2026)
- domain_edges
- KB slow speed and technician
- KB new installation
- KB search queries
- Project config
- Lab

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

## Communities (69 total, 14 thin omitted)

### Community 0 - "json"
Cohesion: 0.16
Nodes (13): api_usage(), _cache_file(), chat(), _chat_anthropic(), _chat_api(), embed(), _env(), _key() (+5 more)

### Community 1 - "chat"
Cohesion: 0.17
Nodes (10): What the model sees (Version B context), Day 06 notebook (one-llm-call), Customer card context (name, area, plan), evaluate(), KB article context (INTENT_KB by expected intent), unit(), user_message(), version_b() (+2 more)

### Community 2 - "ontology.py"
Cohesion: 0.24
Nodes (8): _bool_value(), _edge_metadata(), extract_concepts(), _int_value(), _semantic_model_findings(), terms(), validate_ontology_ops(), _value()

### Community 3 - "score"
Cohesion: 0.14
Nodes (17): Three graders: factual grounding, escalation correctness, response quality, Failure category x version table, Failure category: grader wrong, Failure category: unsupported-amount false positive, failures.csv (tuning failures with note and category), Grader false alarms ('5-7 working days', 'Rs. 100'), Error analysis as an OODA loop, Acme labelled test set (cases.jsonl) (+9 more)

### Community 4 - "Escalation metrics specs"
Cohesion: 0.19
Nodes (14): Safety scoreboard (safe, missed escalations, human intervention, passed), summary(), Scenario Outline: The grader summary reports escalation recall and precision, bot_escalates(), cases(), _graded(), human_ok_is(), human_rate_is() (+6 more)

### Community 5 - "plans"
Cohesion: 0.23
Nodes (9): acme:Plan catalog (Basic ₹699, Plus ₹999, Pro ₹1,499), KB09 · Plan upgrades and downgrades, Acme plans: Basic, Plus, Pro, customer_subgraph(), plans(), price_discount_rupees(), pune_service_areas(), _store() (+1 more)

### Community 6 - "workflow.py"
Cohesion: 0.05
Nodes (31): Five discoveries, five architecture pivots, amounts(), claim_checks(), _flag(), guard_hits(), AppSettings, Settings, State (+23 more)

### Community 7 - "Ontology BDD specs"
Cohesion: 0.13
Nodes (26): glossary(), ontology.feature: every agent gets the same meaning for policy words, Scenario: business rules evolve without changing the ontology, Scenario outline: entitlement computation joins ontology, rules and one record, Scenario: the glossary holds definitions, never customer records, Scenario: operational governance has zero catalog drift, Scenario: OWL reasoner inherits class properties and respects overrides, Scenario outline: every money and identity term is defined and cites its policy (+18 more)

### Community 8 - "Review Studio server"
Cohesion: 0.06
Nodes (29): server(), batch_rev(), batch_status(), case_editor(), case_list(), case_of(), _ed_save(), edit_case() (+21 more)

### Community 9 - "acme.py"
Cohesion: 0.10
Nodes (20): Day 04 notebook (rules-baseline), Day 07 notebook (error-bars), Day 10 notebook (read-the-failures), passed(), Run provenance (.meta.json: model, prompt fingerprint, settings), scoreboard(), show(), Day 11 notebook (recommendation-first-draft) (+12 more)

### Community 10 - "test_c3_provider.py"
Cohesion: 0.05
Nodes (29): c3_output(), C3Provider, ClaudeCodeProvider, make_provider(), OfflineProvider, _parse_json_text(), _result(), c3_fails() (+21 more)

### Community 11 - "version_c3.py"
Cohesion: 0.09
Nodes (24): Phase 2 · Graph engine core, Phase 3 · Wire grader and router, conversation(), customer_text(), build_decision_envelope(), check_entitlement(), define_term(), _envelope_brief() (+16 more)

### Community 12 - "policy_violations"
Cohesion: 0.08
Nodes (30): Examples from the expert's review (worst fails, what good looks like), draft_cases(), KB03 · Payment methods, KB13 · Router and Wi-Fi password, @known_gap scenarios as strict xfail, amounts(), _negated(), not_english() (+22 more)

### Community 13 - "test_escalation_rules.py"
Cohesion: 0.15
Nodes (17): Failure category: unapproved offer, Scenario: An amount the agent wrote in an earlier turn is not the customer's ask, Scenario: No rule fires on any case the experts labelled "no human needed", Scenario Outline: A draft that offers more than its decision allows goes to a person, agent_replied(), customer_earlier_wrote(), customer_now_writes(), escalation_sources_are() (+9 more)

### Community 14 - "Studio report metric tests"
Cohesion: 0.13
Nodes (22): banner(), cases_run(), code_saves(), demo(), escalated(), escalated_by_code(), layer_fired(), missed() (+14 more)

### Community 15 - "Studio workflow and demo runs"
Cohesion: 0.13
Nodes (10): Email-to-reply decision map, ReviewStore, Deps, to_record(), Workflow, run_case(), _run_one(), _sim_run() (+2 more)

### Community 16 - "Studio review flow and verdicts"
Cohesion: 0.13
Nodes (17): initial_mode(), suggest_mode(), validate_verdict(), _prefill(), check_fired(), ctx(), fail_no_critique(), fail_no_mode() (+9 more)

### Community 17 - "version_c3"
Cohesion: 0.08
Nodes (25): outages.json (current outages by area), unasked_outage(), customer_reported_outage(), Feature: The grader agrees with the expert's round-2 review, Scenario Outline: The retention offer is pre-approved (c44), Scenario Outline: The expert's verdict and the grader's agree, Scenario Outline: The envelope shows the outage only when the customer reports one, Feature: The area outage is in scope only when the customer reports that their service is down (+17 more)

### Community 18 - "Studio workbook import and lab"
Cohesion: 0.15
Nodes (12): _bool(), export_to_excel(), _history(), _item(), load_lab(), _payments(), _put(), read_review_log() (+4 more)

### Community 19 - "Day 4 and 9: cost, latency, Version A"
Cohesion: 0.22
Nodes (13): Cost levers (check each against the pass rate), ₹ per resolved email (what really drives cost), Fixed monthly costs spread over all emails, Costs hidden inside today's estimate, Latency not counted (tool time, network, queues, cold start), Cost drivers measured in the notebook, Per-email costs beyond tokens, ₹ per 1,000 emails (+5 more)

### Community 20 - "Studio evidence frame"
Cohesion: 0.22
Nodes (3): Evidence, mask(), nonempty()

### Community 21 - "needs_human escalation"
Cohesion: 0.10
Nodes (24): tests/features/guardrails.feature (BDD guardrails), Amount guard (C3 only, not yet a router), acme:EscalationTrigger (planned), acme:PuneServiceArea (8 areas), SYSTEM_C agent prompt, Failure category: missed escalation, KB10 · Cancellation and notice period, KB12 · Shifting your connection (+16 more)

### Community 22 - "evals.py"
Cohesion: 0.13
Nodes (8): Day 05 notebook (a-grader-you-can-trust), _limit_context(), other_customer_details(), _plan_in_sentence(), _promises_concession(), _record_facts(), unearned_concession(), Scenario Outline: A reply must not give away another customer's details

### Community 23 - "Day 11-12: recommendation and article"
Cohesion: 0.16
Nodes (16): Day 11 ADR-001 diagram, Open question: which failures come from model size vs prompt or grader? (P4, P5), ADR-001: How Acme Fibre should answer customer emails, Open question: how good is searched context for B? (project 2), ADR self-check, 5-minute CTO readout (pitch script), ADR-001 executive readout (9 slides), Documenting Architecture Decisions (Michael Nygard) (+8 more)

### Community 24 - "excluded_from_limit"
Cohesion: 0.22
Nodes (9): Ephemeral per-case ABox (one customer), Varun's ₹300 credit: three agents, three meanings, Credit, Outage credit, Retention offer, excluded_from_limit(), Scenario: automatic money and retention offer don't count toward ₹500, answer_is() (+1 more)

### Community 25 - "Day 7: error bars and evidence"
Cohesion: 0.13
Nodes (15): Stage 4 · Statistical evaluation: 'How sure are we?', Stage 5 · System-level evaluation: 'Does the whole system work?', Stage 6 · Agentic AI evaluation: 'Does the agent finish the job?', Stage 7 · Continuous production evaluation: 'Is it still working for users?', A statistical approach to model evaluations (Anthropic), Seeing Theory: basic probability and frequentist inference, Phase 4 · Empirical verdict, ADR-001 evidence table (day 9 runs) (+7 more)

### Community 26 - "Studio metrics module"
Cohesion: 0.11
Nodes (8): banner(), build_frame(), fig_html(), html_table(), load(), sha256(), tiles(), Reports overview page (index.qmd)

### Community 27 - "Refund limit and expert findings"
Cohesion: 0.14
Nodes (17): Round 1 Principal Engineer review of the Acme Fibre email drafting solution, KB02 · Late payment fee, KB04 · Refunds and credits, KB05 · Outages and restoration updates, KB06 · Outage credit, KB11 · Retention offer, data/acme/business_rules.json (commercial thresholds), Double payment refund (+9 more)

### Community 28 - "Studio guardrail tests"
Cohesion: 0.13
Nodes (13): email_from(), flags(), human_chooses(), lab(), model_drafts(), not_called(), outcome(), reason() (+5 more)

### Community 29 - "Day 1: one model call"
Cohesion: 0.14
Nodes (17): Day 01 notebook (an-llm-call-is-http), ask(), Deep Dive into LLMs like ChatGPT (Karpathy), inference chapter, Ollama /api/chat endpoint, qwen3:4b local model, Forward Deployed Engineer (FDE) mindset, Local models on Ollama (zero cost), Project 1 · Measure before you believe (+9 more)

### Community 30 - "Studio case import script"
Cohesion: 0.22
Nodes (12): _restore_chart(), _add_headers(), _copy_style(), import_cases(), import_customers(), import_policy(), _last_row(), main() (+4 more)

### Community 31 - "Ontology layer for Acme Fibre"
Cohesion: 0.14
Nodes (13): Business Graph Engine (graph computes, LLM verbalizes), Today: passive prompt glossary (LLM does the joins), Phase 0 · Baseline audit, Phase 1 · Rich TBox schema, Static TBox (shared meaning, zero PII), Meaning flow: policy.md + kb.md → ontology.ttl → pyoxigraph → glossary(), Version B + glossary experiment (B_glossary), pyoxigraph (in-process RDF store, SPARQL 1.1) (+5 more)

### Community 32 - "load_customers"
Cohesion: 0.14
Nodes (13): Tool dispatch FUNCTIONS[name](**args), Tool result appended as a 'tool' message, Email in, Load customer card and outages, KB01 · Billing cycle and due dates, Acme help articles (kb.md), first_name(), load_customers() (+5 more)

### Community 33 - "load_business_rules"
Cohesion: 0.24
Nodes (5): _deep_update(), _default_rules(), load_business_rules(), outage_exceeds_hours(), _parse_date()

### Community 34 - "concept_provenance"
Cohesion: 0.18
Nodes (10): knowledge_page(), meaning_concept_card(), meaning_rule_detail(), _asserted_store(), concept_labels(), concept_provenance(), policy_rules(), test_all_concept_aliases_and_policy_rule_impacts_are_consistent() (+2 more)

### Community 35 - "Test set data checks"
Cohesion: 0.18
Nodes (8): kb_by_id(), cases(), _problems(), test_cases_match_the_customer_record(), test_labels_are_valid(), check(), test_language_label_matches_the_script(), test_regional_cases_carry_an_english_gloss()

### Community 36 - "Day 08 notebook (agent-loop-from-scratch)"
Cohesion: 0.67
Nodes (3): Day 08 notebook (agent-loop-from-scratch), run_agent(), show()

### Community 37 - "Grader mutation tests"
Cohesion: 0.14
Nodes (16): Scenario Outline: The grader catches a reply that was broken on purpose, @known_gap Scenario Outline: Known gaps: correct replies the grader still fails, _add_each_banned(), _append(), _cases_where(), _change_intent(), _drop_each_fact(), grader_fails() (+8 more)

### Community 38 - "Day 8: agent loop and failures"
Cohesion: 0.12
Nodes (19): Gave-up fallback at MAX_STEPS, Per-step agent trace, MAX_STEPS = 6 step limit, qwen3:4b local model (temperature 0), Act: does it hold on emails we never looked at?, Decide: which single fix matters most?, Observe: what does a pass rate hide?, Orient: have we seen this failure before? (+11 more)

### Community 39 - "app.py"
Cohesion: 0.08
Nodes (15): highlight(), icon(), pipeline(), review_page(), score_page(), case_header(), score_boxes(), sim_pipe() (+7 more)

### Community 40 - "Studio UI cards"
Cohesion: 0.13
Nodes (17): eval_checks(), chip(), customer_chips(), cur(), draft_meta(), email_card(), expected_card(), guard_try_result() (+9 more)

### Community 41 - "judge_round1.py"
Cohesion: 0.29
Nodes (4): judge_prompt(), main(), work(), run_judge()

### Community 42 - "version_b"
Cohesion: 0.14
Nodes (11): classify(), version_a(), Scoreboard on 84 cases: A vs B, Version A pipeline: keyword match then fill a template, Building block: the augmented LLM (Anthropic, Building effective agents), Acme Fibre (fictional Pune broadband ISP), Context engineering (the context is the product), Honest rules baseline (+3 more)

### Community 43 - "Evaluation evidence Quarto site"
Cohesion: 0.15
Nodes (4): tests/features/report_metrics.feature, load_thresholds(), Demo round (make_demo_runs.py), Evaluation evidence Quarto site

### Community 44 - "Review dashboard (when do humans help?)"
Cohesion: 0.12
Nodes (16): layer_of(), Code saves, Error cost (INR, per 1,000 emails), Agent hours per 1,000 emails, Disagreement rates, What triggered the escalations (layer analysis), Escalation rate, Failure categories (expert) (+8 more)

### Community 45 - "ADR-001 diagram: B with a safety router and a policy check"
Cohesion: 0.21
Nodes (10): Proposed controlled workflow (deterministic routing + one drafting step), Building effective agents (Anthropic), Workflow patterns: prompt chaining, routing, agent, ADR-001 diagram: B with a safety router and a policy check, Human support queue, Load customer card and outages (code, no model), Gates before replies go out unreviewed, Search the help articles (retrieved, not oracle context) (+2 more)

### Community 46 - "Evaluation report (release decision)"
Cohesion: 0.21
Nodes (13): Evaluation report (release decision), Step-6 check hits, Expert pass rate, Missed escalation, Routing accuracy, Unneeded escalation, Unsafe auto-send, Where every case went (run → escalated/sent → right/missed/unneeded) (+5 more)

### Community 47 - "embed"
Cohesion: 0.20
Nodes (6): qwen3:4b chat model (reads text only), Similarity search (cosine, top 3), embeddinggemma (EMBED_MODEL), Embeddings and retrieval, Hinglish handling, Recall@3 (retrieval metric)

### Community 48 - "Studio scoring rounds"
Cohesion: 0.24
Nodes (9): _prefill_key(), progress(), rnd(), round_data(), _run_missing(), worker(), one(), score_rounds() (+1 more)

### Community 49 - "Scenario outline: regional or informal word maps to the policy term"
Cohesion: 0.31
Nodes (8): acme:AccountAction requiresRole AccountHolder, Account holder, Concession (refund, credit, waiver, discount value), Customer, Discount (also: सूट, छूट, ರಿಯಾಯಿತಿ), Late-fee waiver, Refund (also: paisa wapas, पैसे परत), Scenario outline: regional or informal word maps to the policy term

### Community 50 - "Domain expert (SME) review"
Cohesion: 0.05
Nodes (37): Acme Review Studio, workbook_sheet(), Dataset card (Acme test set), Build LLM judge from expert examples, Critique Shadowing workflow, Error analysis: error rates, patterns, specialised judges, Expert reviews data and errors are fixed, Repeat on material change or periodic review (+29 more)

### Community 51 - "extract_json"
Cohesion: 0.19
Nodes (8): Final answer JSON {intent, reply, needs_human}, Stop condition: reply has no tool_calls, Day 09 notebook (success-cost-latency), cost_inr(), percentile(), row(), run_agent(), extract_json()

### Community 52 - "Wilson intervals and rates"
Cohesion: 0.29
Nodes (3): Rate, wilson(), Model needs-human flag recall

### Community 58 - "Acme Review Studio architecture/UX review (16 Oct 2026)"
Cohesion: 0.20
Nodes (3): _export(), _settings(), Acme Review Studio architecture/UX review (16 Oct 2026)

### Community 61 - "domain_edges"
Cohesion: 0.18
Nodes (9): KnowledgeArticle and PolicyRule IRIs (documentedIn, enforcesRule), Concept → KB retrieval gain (with alias leakage caveat), Multilingual lexical layer (SKOS labels), _alias_index(), define(), domain_edges(), search_kb_c3(), Scenario: an unknown word has no definition (+1 more)

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
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `server()` connect `Review Studio server` to `load_business_rules`, `concept_provenance`, `Test set data checks`, `ontology.py`, `workflow.py`, `app.py`, `Studio UI cards`, `test_c3_provider.py`, `Studio workflow and demo runs`, `Studio review flow and verdicts`, `Studio scoring rounds`, `Studio workbook import and lab`, `Domain expert (SME) review`, `Acme Review Studio architecture/UX review (16 Oct 2026)`, `domain_edges`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `server()` (e.g. with `.all()` and `Expert reviews data and errors are fixed`) actually correct?**
  _`server()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fde-first-principles`, `KB03 · Payment methods`, `KB13 · Router and Wi-Fi password` to the rest of the system?**
  _28 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `score` be split into smaller, more focused modules?**
  _Cohesion score 0.14461538461538462 - nodes in this community are weakly interconnected._
- **Why does `policy_violations()` connect `policy_violations` to `load_business_rules`, `score`, `plans`, `workflow.py`, `Ontology BDD specs`, `version_b`, `version_c3.py`, `version_c3`, `Domain expert (SME) review`, `evals.py`, `Day 11-12: recommendation and article`, `Article lessons and grader gaps`, `Refund limit and expert findings`, `Ontology layer for Acme Fibre`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `version_b()` and `Failure category: unsupported-amount false positive`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `search_kb()` and `Similarity search (cosine, top 3)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._