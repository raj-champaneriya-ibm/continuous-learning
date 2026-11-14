# Graph Report - continuous-learning  (2026-11-14)

## Corpus Check
- 140 files · ~123,711 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 68 file(s) not represented in the graph (top: .drawio 18, .feature 15, .jsonl 13)
- WARNING: 68 of 214 files seen (32%) have no supported extractor and are missing from this graph entirely. It may look complete while representing only part of the codebase.

## Summary
- 1863 nodes · 4056 edges · 119 communities (103 shown, 16 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 340 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `820eda0c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- llm.py
- acme_metrics.py
- test_report_metrics.py
- versioned-simulator.md
- service.py
- server
- test_out_of_steps.py
- RunResult
- VersionRegistry
- ontology.py
- RunInput
- test_ontology.py
- Span
- test_review_flow.py
- evaluation-report.qmd
- version_c3.py
- 3. Lab reference
- Acme Review Studio
- validate_ontology_ops
- app.py
- test_outage_scope.py
- chip
- test_guardrails.py
- evals.py
- versions.py
- lab.py
- OrchestratedAdapter
- policy_violations
- Workflow
- Version
- test_simulator_http.py
- test_c3_provider.py
- test_escalation_metrics.py
- test_escalation_rules.py
- json
- re
- RunStore
- version_c4.py
- test_grader_mutations.py
- ZAVAAirlines Fabric Data Agents - Q&A
- import_cases.py
- define
- kb.md
- load_customers
- run_agent
- refresh_versions
- Ranked actionable findings
- studio-c3.yaml
- ADR-001: Support Email Automation Strategy
- acme.py
- .adapter
- DirectAdapter
- compute_entitlements
- ._build
- Day 10 · Read the failures, not the averages
- config
- studio-declarative.yaml
- build_decision_envelope
- C3Provider
- c3-agent.yaml
- Later: an ontology layer for Acme Fibre
- Implementation plan
- Day 12 · Article: measure before you believe
- Word Search
- gates
- studio-offline.yaml
- version-b.yaml
- Day 3 · Write the test set before the system
- Day 8 · Version C: an agent loop from scratch
- Day 9 · Run all three: success, cost, latency
- Day 11 · The recommendation, first draft (an ADR)
- Think, Build & Repeat
- Combination Sum
- Combination Sum II
- Letter Combinations of a Phone Number
- N-Queens
- Palindrome Partitioning
- Permutations
- Subsets
- Subsets II
- Day 1 · An LLM call is just an HTTP request
- Day 2 · Workflow or agent? Map the decisions first
- offline-direct.yaml
- Day 5 · A grader you can trust
- Day 6 · Version B: one model call with the right context
- Day 7 · Why 30 test cases can lie: error bars
- Spoken script
- 🎙️ Spoken Script & Presentation Guide
- Adapter
- Day 4 · Version A: rules and templates (the honest baseline)
- ADR-001: How Acme Fibre should answer customer emails
- .start
- resume
- test_adapter_contract.py
- ScriptedResponse
- search_kb
- AGENTS.md
- fde-first-principles/README.md
- scored
- world
- article.md
- Conversation Summary
- Continuous Learning
- score
- subsets.py
- Response
- Later: grader ideas parked on day 5
- Agent 365
- Backtracking
- customer_reported_outage
- Boosted Trees at the Chai Stall
- The problem
- CLAUDE.md
- .claude/CLAUDE.md
- fde-first-principles

## God Nodes (most connected - your core abstractions)
1. `server()` - 128 edges
2. `Version` - 61 edges
3. `RunInput` - 52 edges
4. `RunResult` - 49 edges
5. `VersionRegistry` - 40 edges
6. `SimulationService` - 35 edges
7. `when` - 33 edges
8. `ReviewStore` - 32 edges
9. `build_decision_envelope()` - 31 edges
10. `load_lab()` - 30 edges

## Surprising Connections (you probably didn't know these)
- `Testing approach` --references--> `RunResult`  [INFERRED]
  kata-use-cases/versioned-simulator.md → fde-first-principles/1-measure-before-you-believe/03-test-set-first/acme-review-studio/acme/sim/trace.py
- `Adding an implementation model` --references--> `Adapter`  [INFERRED]
  kata-use-cases/versioned-simulator.md → fde-first-principles/1-measure-before-you-believe/03-test-set-first/acme-review-studio/acme/sim/trace.py
- `Rounds become versions` --references--> `ReviewStore`  [INFERRED]
  kata-use-cases/versioned-simulator.md → fde-first-principles/1-measure-before-you-believe/03-test-set-first/acme-review-studio/acme/store.py
- `How the BDD tests work` --references--> `policy_violations()`  [INFERRED]
  AGENTS.md → fde-first-principles/lab/evals.py
- `Project 2 · Meaning across fragmented data (Module H, 14 mornings)` --references--> `validate_ontology_ops()`  [INFERRED]
  kata-use-cases/FDE curriculum review — November 2026.md → fde-first-principles/lab/ontology.py

## Import Cycles
- None detected.

## Communities (119 total, 16 thin omitted)

### Community 0 - "llm.py"
Cohesion: 0.05
Nodes (33): fingerprint(), load_cases(), save_results(), api_usage(), _cache_file(), chat(), _chat_anthropic(), _chat_api() (+25 more)

### Community 1 - "acme_metrics.py"
Cohesion: 0.06
Nodes (25): banner(), build_frame(), Evidence, fig_html(), html_table(), layer_of(), mask(), nonempty() (+17 more)

### Community 2 - "test_report_metrics.py"
Cohesion: 0.08
Nodes (29): ReviewStore, score_rounds(), load(), banner(), cases_run(), code_saves(), demo(), escalated() (+21 more)

### Community 3 - "versioned-simulator.md"
Cohesion: 0.05
Nodes (40): ClaudeCodeProvider, _result(), Accessibility, Adding an implementation model, Compare mode, Decisions to record, Demo in three minutes, Done when (+32 more)

### Community 4 - "service.py"
Cohesion: 0.08
Nodes (7): DeclarativeAdapter, redact(), secret_values(), compare_reviews(), Settings, State, test_review_comparison_puts_new_missed_escalations_first()

### Community 5 - "server"
Cohesion: 0.06
Nodes (23): server(), batch_rev(), batch_status(), case_editor(), case_of(), _ed_save(), edit_case(), _export() (+15 more)

### Community 6 - "test_out_of_steps.py"
Cohesion: 0.09
Nodes (21): pipeline(), Elements, test_icons_have_no_network_or_accessible_name(), test_pipeline_keyboard_order_and_untrusted_details(), customer_writes(), marked_out_of_steps(), model_called(), not_marked_out_of_steps() (+13 more)

### Community 7 - "RunResult"
Cohesion: 0.11
Nodes (13): compare_results(), review_record(), sample_spread(), SimulationService, RunResult, AppSettings, sim_outcome(), world() (+5 more)

### Community 8 - "VersionRegistry"
Cohesion: 0.16
Nodes (7): canonical(), case_hash(), digest(), lab_snapshot(), label_hash(), _sheet_hashes(), VersionRegistry

### Community 9 - "ontology.py"
Cohesion: 0.17
Nodes (19): data_root(), _alias_index(), _asserted_store(), _bool_value(), customer_subgraph(), _data_cache(), cached(), get() (+11 more)

### Community 10 - "RunInput"
Cohesion: 0.15
Nodes (16): RunInput, run_case(), run_case(), test_adapter_errors_and_timeouts_are_saved(), test_c3_concurrent_versions_read_their_own_lab_snapshots(), test_release_requires_current_graded_cases_and_retired_resume_stays_held(), test_retention_removes_expired_runs_and_checkpoints_but_keeps_held_runs(), test_secrets_are_redacted_from_runs_checkpoints_and_logs() (+8 more)

### Community 11 - "test_ontology.py"
Cohesion: 0.11
Nodes (24): run_case(), run_email(), read(), read_round(), when, excluded_from_limit(), answer_is(), apply_commercial_rule_override() (+16 more)

### Community 12 - "Span"
Cohesion: 0.18
Nodes (19): _button(), render_comparison(), render_detail(), render_result(), _text(), _topology(), _tree(), branch() (+11 more)

### Community 13 - "test_review_flow.py"
Cohesion: 0.13
Nodes (17): initial_mode(), suggest_mode(), validate_verdict(), _prefill(), check_fired(), ctx(), fail_no_critique(), fail_no_mode() (+9 more)

### Community 14 - "evaluation-report.qmd"
Cohesion: 0.08
Nodes (22): At a glance, Composition, Escalation rules, Label review, Provenance, What this set can't tell you, Where the cases come from, Examples from the expert's review (+14 more)

### Community 15 - "version_c3.py"
Cohesion: 0.12
Nodes (12): intent_guide(), check_entitlement(), define_term(), _grants(), lookup_customer_c3(), offer_decisions(), _offer_mention(), offers_not_allowed() (+4 more)

### Community 16 - "3. Lab reference"
Cohesion: 0.08
Nodes (23): 1. The plan on one page, 3. Lab reference, 4. Not now, 5. What this revision changed, and why (14 November), 6. Evidence, Added on 11 November 2026, not re-opened in the 14 November review, Findings and changes, Governance spine (Module G, inside the labs) (+15 more)

### Community 17 - "Acme Review Studio"
Cohesion: 0.09
Nodes (21): Acme Review Studio, How the Claude Code call works, Project layout, Reference Review layout, Reports (Quarto), Reviewing the C3 agent's drafts, Run it, Set up (once) (+13 more)

### Community 18 - "validate_ontology_ops"
Cohesion: 0.11
Nodes (18): kb_by_id(), reason_owl_rl(), validate_ontology_ops(), Build on what already exists, Checks, Code changes, Concept card, Demo in three minutes (+10 more)

### Community 19 - "app.py"
Cohesion: 0.13
Nodes (7): highlight(), case_choices(), score_page(), _refresh_case_choices(), simulator_page(), version_choices(), _deep_update()

### Community 20 - "test_outage_scope.py"
Cohesion: 0.11
Nodes (12): _envelope_brief(), version_c3(), test_blank_or_cut_off_reply_is_never_sendable(), agent_finishes(), agent_finishes(), customer_writes(), envelope_is_built(), envelope_shows() (+4 more)

### Community 21 - "chip"
Cohesion: 0.12
Nodes (20): make_provider(), chip(), icon(), customer_chips(), review_page(), case_header(), cur(), draft_meta() (+12 more)

### Community 22 - "test_guardrails.py"
Cohesion: 0.13
Nodes (13): email_from(), flags(), human_chooses(), lab(), model_drafts(), not_called(), outcome(), reason() (+5 more)

### Community 23 - "evals.py"
Cohesion: 0.14
Nodes (10): amounts(), _limit_context(), _negated(), other_customer_details(), _plan_in_sentence(), _promises_concession(), _record_facts(), _retention_offer_rupees() (+2 more)

### Community 25 - "lab.py"
Cohesion: 0.16
Nodes (10): _bool(), export_to_excel(), _history(), _item(), load_lab(), _payments(), _put(), read_review_log() (+2 more)

### Community 26 - "OrchestratedAdapter"
Cohesion: 0.19
Nodes (3): OrchestratedAdapter, RecordedProvider, RedactingSerializer

### Community 27 - "policy_violations"
Cohesion: 0.13
Nodes (12): not_english(), policy_violations(), reveals_limit(), customer_wrote(), flags(), flags_nothing(), grader_checks(), grader_checks_against_ask() (+4 more)

### Community 28 - "Workflow"
Cohesion: 0.16
Nodes (7): eval_checks(), OfflineProvider, Deps, to_record(), Workflow, demo_verdict(), main()

### Community 29 - "Version"
Cohesion: 0.18
Nodes (4): VersionBAdapter, HttpAdapter, Capabilities, Version

### Community 30 - "test_simulator_http.py"
Cohesion: 0.20
Nodes (11): _endpoint(), run(), Session, test_endpoints_reject_untrusted_urls(), test_http_rejects_oversized_and_invalid_drafts(), test_http_sends_auth_without_persisting_secrets(), test_http_stream_stops_after_timeout(), test_loopback_http_is_allowed_only_when_explicitly_allowlisted() (+3 more)

### Community 31 - "test_c3_provider.py"
Cohesion: 0.18
Nodes (14): c3_fails(), c3_given_case(), c3_given_history(), c3_replies(), draft_cites(), draft_needs_human(), draft_reason(), draft_says() (+6 more)

### Community 32 - "test_escalation_metrics.py"
Cohesion: 0.18
Nodes (12): summary(), bot_escalates(), cases(), _graded(), human_ok_is(), human_rate_is(), _percent(), precision_is() (+4 more)

### Community 33 - "test_escalation_rules.py"
Cohesion: 0.16
Nodes (13): agent_replied(), customer_earlier_wrote(), customer_now_writes(), customer_writes(), escalation_sources_are(), every_labelled_case(), model_drafts(), needs_human_is() (+5 more)

### Community 34 - "json"
Cohesion: 0.18
Nodes (6): _parse_json_text(), judge_prompt(), main(), work(), run_judge(), run_agent()

### Community 35 - "re"
Cohesion: 0.22
Nodes (9): amounts(), claim_checks(), _flag(), guard_hits(), Lab, direct_output(), no_draft(), validate_draft() (+1 more)

### Community 36 - "RunStore"
Cohesion: 0.22
Nodes (3): _json(), _now(), RunStore

### Community 37 - "version_c4.py"
Cohesion: 0.16
Nodes (9): Acme Fibre: the project brief (fictional), The files, conversation(), extract_json(), system_prompt(), _envelope_brief_c4(), _excerpt(), run_agent() (+1 more)

### Community 38 - "test_grader_mutations.py"
Cohesion: 0.19
Nodes (13): _add_each_banned(), _append(), _cases_where(), _drop_each_fact(), grader_fails(), grader_flags(), grader_passes(), mutate() (+5 more)

### Community 39 - "ZAVAAirlines Fabric Data Agents - Q&A"
Cohesion: 0.11
Nodes (17): 10. Unstructured Data Support, 11. Consistent Responses Across Teams, Excel, and Copilot Studio, 12. Fabric Data Agent as Knowledge Source, 13. Direct OneLake Access vs Data Agents, 14. Architecture Responsibilities, 15. External AI Access Pattern, 16. Fabric Data Agents vs Power BI Copilot, 1. Improve Query Generation Accuracy (+9 more)

### Community 40 - "import_cases.py"
Cohesion: 0.24
Nodes (11): _restore_chart(), _add_headers(), _copy_style(), import_cases(), import_customers(), import_policy(), _last_row(), main() (+3 more)

### Community 41 - "define"
Cohesion: 0.15
Nodes (12): knowledge_page(), meaning_concept_card(), meaning_rule_detail(), concept_labels(), concept_provenance(), define(), policy_rules(), look_up() (+4 more)

### Community 42 - "kb.md"
Cohesion: 0.12
Nodes (16): KB01 · Billing cycle and due dates, KB02 · Late payment fee, KB03 · Payment methods, KB04 · Refunds and credits, KB05 · Outages and restoration updates, KB06 · Outage credit, KB07 · Slow speed or no internet: first checks, KB08 · Technician visits (+8 more)

### Community 43 - "load_customers"
Cohesion: 0.21
Nodes (8): load_customers(), load_outages(), _problems(), test_cases_match_the_customer_record(), test_labels_are_valid(), check(), test_language_label_matches_the_script(), test_regional_cases_carry_an_english_gloss()

### Community 44 - "run_agent"
Cohesion: 0.18
Nodes (10): customer_text(), _default_rules(), load_business_rules(), _rules_at(), run_agent(), _answer(), _finish(), _finish() (+2 more)

### Community 45 - "refresh_versions"
Cohesion: 0.17
Nodes (16): _apply_retention(), case_list(), _fail(), _keep_current_visible(), _name_candidate(), _pass(), progress(), refresh_versions() (+8 more)

### Community 46 - "Ranked actionable findings"
Cohesion: 0.12
Nodes (15): _settings(), Acme Review Studio review, Architecture, Delivered, P1 — Mutable process globals can mix evaluation conditions, P1 — Parsed model output lacks local schema validation, P1 — Repeated-complaint routing depends on model judgment, P2 — Grounding language overstates heuristic coverage (+7 more)

### Community 47 - "studio-c3.yaml"
Cohesion: 0.12
Nodes (15): adapter, config, timeout_s, adapter, implementation, model, implementation, inputs (+7 more)

### Community 48 - "ADR-001: Support Email Automation Strategy"
Cohesion: 0.12
Nodes (15): 5-Minute Executive Readout for Acme Fibre, ADR-001: Support Email Automation Strategy, Core Operating Reality, Phased Operational Strategy:, Principal Engineer Insights:, Slide 1: Executive Summary & Recommendation, Slide 2: Three Competing Paradigms Evaluated, Slide 3: Empirical Scorecard (Statistical Error Bars) (+7 more)

### Community 49 - "acme.py"
Cohesion: 0.17
Nodes (6): customer_card(), first_name(), load_kb(), load_meta(), load_results(), lookup_customer()

### Community 50 - ".adapter"
Cohesion: 0.26
Nodes (12): replay_sources(), _run_missing(), worker(), one(), _run_one(), selected_review_version(), selected_sim_version(), sim_fields() (+4 more)

### Community 52 - "compute_entitlements"
Cohesion: 0.15
Nodes (7): outage_for(), duplicate_payment_amount(), months_since(), outage_exceeds_hours(), _parse_date(), compute_entitlements(), compute_for_customer()

### Community 53 - "._build"
Cohesion: 0.27
Nodes (11): _trace(), check(), decide(), draft(), fetch(), human(), log(), receive() (+3 more)

### Community 54 - "Day 10 · Read the failures, not the averages"
Cohesion: 0.15
Nodes (11): 1 · Learn (about 15 minutes), 2 · Build (about 70 minutes), 3 · Record (5 minutes or less), Before you start: three things the day 9 numbers hide, Day 10 · Read the failures, not the averages, Done when, How I used AI, In my words (+3 more)

### Community 55 - "config"
Cohesion: 0.15
Nodes (12): adapter, config, auth, endpoint, model, output_schema, provider, timeout_s (+4 more)

### Community 56 - "studio-declarative.yaml"
Cohesion: 0.15
Nodes (12): adapter, config, model, provider, timeout_s, implementation, inputs, label (+4 more)

### Community 57 - "build_decision_envelope"
Cohesion: 0.18
Nodes (7): amounts_asked_for(), escalation_triggers(), _trigger(), build_decision_envelope(), envelope_decides(), rules_read_each(), rules_read_it()

### Community 58 - "C3Provider"
Cohesion: 0.21
Nodes (3): c3_output(), C3Provider, AgentLoopAdapter

### Community 59 - "c3-agent.yaml"
Cohesion: 0.17
Nodes (11): adapter, config, max_steps, model, provider, temperature, timeout_s, implementation (+3 more)

### Community 60 - "Later: an ontology layer for Acme Fibre"
Cohesion: 0.17
Nodes (10): Decision: where the ontology lives (2026-10-28), Do we need it now, How to prove it first (measure before you believe), Later: an ontology layer for Acme Fibre, Recommended tool: pyoxigraph, Sketch, When it becomes worth building, Acme Fibre reply policy (+2 more)

### Community 61 - "Implementation plan"
Cohesion: 0.18
Nodes (11): Implementation plan, Out of scope until project 6, Phase 0: Measure the problem (no new code), Phase 1: Write the ontology (definitions only), Phase 2: Loader and tests, Phase 3: Version B with the glossary, Phase 4: Version C with a lookup tool (optional), Phase 5: Decide with evidence (+3 more)

### Community 62 - "Day 12 · Article: measure before you believe"
Cohesion: 0.17
Nodes (11): 1 · Learn (about 40 minutes), 2 · Write and publish (about 185 minutes), 3 · Record (optional for an article), Before you start, Day 12 · Article: measure before you believe, Done when, How I used AI, Set up (+3 more)

### Community 63 - "Word Search"
Cohesion: 0.18
Nodes (10): Complexity, E-Prime Pseudocode, Greg Tang Explains, Pattern Takeaway, Problem, Related, Solutions, Visual (+2 more)

### Community 64 - "gates"
Cohesion: 0.18
Nodes (10): costs_inr, missed_escalation, unneeded_escalation, unsafe_auto_send, gates, missed_escalations, pass_rate_ci_low, routing_accuracy (+2 more)

### Community 65 - "studio-offline.yaml"
Cohesion: 0.18
Nodes (10): adapter, config, model, provider, temperature, timeout_s, implementation, inputs (+2 more)

### Community 66 - "version-b.yaml"
Cohesion: 0.18
Nodes (10): adapter, config, model, provider, temperature, timeout_s, implementation, inputs (+2 more)

### Community 67 - "Day 3 · Write the test set before the system"
Cohesion: 0.18
Nodes (11): 1 · Learn (about 30 minutes), 2 · Build (about 90 minutes), 3 · Record (5 minutes or less), Day 3 · Write the test set before the system, Done when, Ground truth · 20 SME-reviewed scenarios, How I used AI, In my words (+3 more)

### Community 68 - "Day 8 · Version C: an agent loop from scratch"
Cohesion: 0.18
Nodes (10): 1 · Learn (about 30 minutes), 2 · Build (about 60 minutes), 3 · Record (5 minutes or less), Day 8 · Version C: an agent loop from scratch, Done when, How I used AI, In my words, Set up (+2 more)

### Community 69 - "Day 9 · Run all three: success, cost, latency"
Cohesion: 0.18
Nodes (10): 1 · Learn (about 25 minutes), 2 · Build (about 70 minutes), 3 · Record (5 minutes or less), Day 9 · Run all three: success, cost, latency, Done when, How I used AI, In my words, Set up (+2 more)

### Community 70 - "Day 11 · The recommendation, first draft (an ADR)"
Cohesion: 0.18
Nodes (10): 1 · Learn (about 15 minutes), 2 · Build (about 45 minutes), 3 · Record (5 minutes or less), Before you start: what your evidence already says, Day 11 · The recommendation, first draft (an ADR), Done when, How I used AI, In my words (+2 more)

### Community 71 - "Think, Build & Repeat"
Cohesion: 0.18
Nodes (10): Continuous operational-state evaluation with policy-driven action orchestration, Cross-domain enterprise contextual federation, Eval enhancements, generative orchastration - copilot studio, oAuth Identity Passthrough, Problem 1, Problem 2, Problem 3 (+2 more)

### Community 72 - "Combination Sum"
Cohesion: 0.20
Nodes (10): Combination Sum, Complexity, E-Prime Pseudocode, Greg Tang Explains, Pattern Takeaway, Problem, Related, Solutions (+2 more)

### Community 73 - "Combination Sum II"
Cohesion: 0.20
Nodes (10): Combination Sum II, Complexity, E-Prime Pseudocode, Greg Tang Explains, Pattern Takeaway, Problem, Related, Solutions (+2 more)

### Community 74 - "Letter Combinations of a Phone Number"
Cohesion: 0.20
Nodes (10): Complexity, E-Prime Pseudocode, Greg Tang Explains, Letter Combinations of a Phone Number, Pattern Takeaway, Problem, Related, Solutions (+2 more)

### Community 75 - "N-Queens"
Cohesion: 0.20
Nodes (10): Complexity, E-Prime Pseudocode, Greg Tang Explains, N-Queens, Pattern Takeaway, Problem, Related, Solutions (+2 more)

### Community 76 - "Palindrome Partitioning"
Cohesion: 0.20
Nodes (10): Complexity, E-Prime Pseudocode, Greg Tang Explains, Palindrome Partitioning, Pattern Takeaway, Problem, Related, Solutions (+2 more)

### Community 77 - "Permutations"
Cohesion: 0.20
Nodes (10): Complexity, E-Prime Pseudocode, Greg Tang Explains, Pattern Takeaway, Permutations, Problem, Related, Solutions (+2 more)

### Community 78 - "Subsets"
Cohesion: 0.20
Nodes (10): Complexity, E-Prime Pseudocode, Greg Tang Explains Visually, Subsets, Pattern Takeaway, Problem, Related, Solutions (+2 more)

### Community 79 - "Subsets II"
Cohesion: 0.20
Nodes (10): Complexity, E-Prime Pseudocode, Greg Tang Explains, Pattern Takeaway, Problem, Related, Solutions, Subsets II (+2 more)

### Community 80 - "Day 1 · An LLM call is just an HTTP request"
Cohesion: 0.20
Nodes (10): 1 · Learn (about 20 minutes), 2 · Build (about 40 minutes), 3 · Record (5 minutes or less), Day 1 · An LLM call is just an HTTP request, Done when, How I used AI, In my words, Set up (+2 more)

### Community 81 - "Day 2 · Workflow or agent? Map the decisions first"
Cohesion: 0.20
Nodes (9): 1 · Learn (about 20 minutes), 2 · Build (about 40 minutes), 3 · Record (5 minutes or less), Day 2 · Workflow or agent? Map the decisions first, Done when, How I used AI, In my words, Video (+1 more)

### Community 82 - "offline-direct.yaml"
Cohesion: 0.20
Nodes (9): adapter, config, model, provider, timeout_s, implementation, inputs, label (+1 more)

### Community 83 - "Day 5 · A grader you can trust"
Cohesion: 0.20
Nodes (9): 1 · Learn (about 25 minutes), 2 · Build (about 50 minutes), 3 · Record (5 minutes or less), Day 5 · A grader you can trust, Done when, How I used AI, In my words, Video (+1 more)

### Community 84 - "Day 6 · Version B: one model call with the right context"
Cohesion: 0.20
Nodes (10): 1 · Learn (about 25 minutes), 2 · Build (about 60 minutes), 3 · Record (5 minutes or less), Day 6 · Version B: one model call with the right context, Done when, How I used AI, In my words, Set up (+2 more)

### Community 85 - "Day 7 · Why 30 test cases can lie: error bars"
Cohesion: 0.20
Nodes (9): 1 · Learn (about 30 minutes), 2 · Build (about 85 minutes), 3 · Record (5 minutes or less), Day 7 · Why 30 test cases can lie: error bars, Done when, How I used AI, In my words, Video (+1 more)

### Community 86 - "Spoken script"
Cohesion: 0.20
Nodes (9): Part 1: The question and the loop (0:00 to 0:30), Part 2: Observe (0:30 to 1:30), Part 3: Orient (1:30 to 2:30), Part 4: Decide and act (2:30 to 3:45), Part 5: What it does not prove and the next loop (3:45 to 4:45), Pitch timeline, Q&A cheat sheet, Readout details (+1 more)

### Community 87 - "🎙️ Spoken Script & Presentation Guide"
Cohesion: 0.20
Nodes (9): 5-Minute CTO Readout: Acme Fibre Support Automation, 🎯 Executive Q&A Defense Cheat-Sheet, Part 1: The Decision & Bottom Line (0:00 – 0:45), Part 2: The Empirical Evidence (0:45 – 1:45), Part 3: Architecture Walkthrough (1:45 – 3:15), Part 4: Go-Live Gates & Risk Controls (3:15 – 4:00), Part 5: What Would Change My Mind & Next Steps (4:00 – 4:45), ⏱️ Pitch Timeline & Structure (+1 more)

### Community 90 - "Day 4 · Version A: rules and templates (the honest baseline)"
Cohesion: 0.22
Nodes (9): 1 · Learn (about 30 minutes), 2 · Build (about 60 minutes), 3 · Record (5 minutes or less), Day 4 · Version A: rules and templates (the honest baseline), Done when, How I used AI, In my words, Video (+1 more)

### Community 91 - "ADR-001: How Acme Fibre should answer customer emails"
Cohesion: 0.22
Nodes (8): ADR-001: How Acme Fibre should answer customer emails, Consequences, Context, Decision, Evidence (from day 9), Open questions (projects 2 to 6), Options, What would change my mind

### Community 92 - ".start"
Cohesion: 0.32
Nodes (5): world(), system_prompt(), user_message(), version_b(), Phase 2: run contract and adaptive views

### Community 93 - "resume"
Cohesion: 0.25
Nodes (8): default_sim_step(), _ha(), _he(), _hh(), resume(), show_saved_run(), _sim_load(), _to_sim()

### Community 94 - "test_adapter_contract.py"
Cohesion: 0.29
Nodes (3): pinned(), scripted_adapter(), valid_contract()

### Community 96 - "search_kb"
Cohesion: 0.25
Nodes (5): escalate(), get_article(), search_kb(), _words(), 2. Inventory: what the plan asked for and what already exists

### Community 97 - "AGENTS.md"
Cohesion: 0.29
Nodes (6): Codebase knowledge graph, Debugging in VS Code, Environment setup, How the BDD tests work, Repository layout, Running the tests

### Community 99 - "scored"
Cohesion: 0.29
Nodes (6): score_boxes(), score_confusion(), score_modes(), score_plot(), score_rules(), scored()

### Community 100 - "world"
Cohesion: 0.29
Nodes (3): lab(), StandInC3, world()

### Community 101 - "article.md"
Cohesion: 0.29
Nodes (6): Explore the project, My recommendation, and what would change my mind, Three ways to build it, What I measured, What the customer asked for, What the failures taught me

### Community 102 - "Conversation Summary"
Cohesion: 0.29
Nodes (6): Conversation Summary, Correct Answers, Correct Mapping, Explanation, Question 1, Question 2

### Community 103 - "Continuous Learning"
Cohesion: 0.29
Nodes (6): Approach, Areas of Exploration, Continuous Learning, Engineering Principles, Repository Philosophy, Watch & Read

### Community 104 - "score"
Cohesion: 0.33
Nodes (4): score(), passing_replies(), test_evals_enforces_customer_headroom_and_plan_discounts(), grader_scores_no_concession()

### Community 107 - "Later: grader ideas parked on day 5"
Cohesion: 0.40
Nodes (4): Grader false positives still open, Graders to add, Later: grader ideas parked on day 5, Test cases to add

### Community 108 - "Agent 365"
Cohesion: 0.40
Nodes (4): Agent 365, Governance, Identity, observability

### Community 109 - "Backtracking"
Cohesion: 0.50
Nodes (4): Backtracking, Covered, Source, Understand recursion visually

### Community 112 - "The problem"
Cohesion: 0.67
Nodes (3): user_prompt(), sim_step_detail(), The problem

## Knowledge Gaps
- **1 isolated node(s):** `fde-first-principles`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 821 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Round 1 — Principal Engineer Review of the Acme Fibre Email Drafting Solution` connect `acme_metrics.py` to `Day 10 · Read the failures, not the averages`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `server()` (e.g. with `.all()` and `version_token()`) actually correct?**
  _`server()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fde-first-principles` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `llm.py` be split into smaller, more focused modules?**
  _Cohesion score 0.054244306418219465 - nodes in this community are weakly interconnected._
- **Why does `claim_checks()` connect `re` to `acme_metrics.py`, `service.py`, `._build`, `Ranked actionable findings`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `Version` (e.g. with `AgentLoopAdapter` and `DirectAdapter`) actually correct?**
  _`Version` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Should `acme_metrics.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05926251097453907 - nodes in this community are weakly interconnected._