# Acme Review Studio review

Update: footer branding removed per request. Knowledge/Scoreboard spacing standardized; metric-card overlap corrected. Earlier footer screenshots describe the prior iteration.

Reviewed 16 October 2026. Source: supplied ZIP and two supplied desktop screenshots.

## Delivered

- Bundled official Google Material SVG artwork used by MUI Icons; no runtime icon downloads or React dependency. Text labels retained; decorative SVGs hidden from assistive technology.
- Navigation, Model, Excel save, workflow run, previous/next and verdict actions updated.
- Raj Champaneriya footer with RC monogram and restrained product attribution; normal document flow avoids covering controls.
- Requested spacing refinement: 24px navigation side inset, 16px nav-item padding, 10px icon-to-label gap, softer icons, 9px/12px sidebar row padding, roomier workflow nodes and footer.
- Native buttons for case and workflow selection; visible keyboard focus; case status available to screen readers. Global shortcuts no longer intercept tab navigation or contenteditable fields.
- Mobile workflow stacks in logical order. Review header wraps without page overflow.
- Fixed literal escaped HTML in provider readiness and model-error chips.

## Architecture

`app.py` owns Shiny page definitions, reactive state, event handlers, batch execution and global services. `acme/lab.py` translates the Excel workbook into cases, CRM fixtures, outages and policy. `acme/workflow.py` owns the LangGraph steps and interrupt/resume boundary. `acme/providers.py` separates offline rules from Claude Code subprocess calls. `acme/checks.py` contains deterministic heuristics. `acme/store.py` persists latest run/review records as JSON; SQLite persists graph checkpoints.

Strengths: model call isolated to drafting; deterministic routing guard layer; real human interrupt; workbook interoperability; useful expected-answer context; deliberately flawed offline provider makes failures visible without model cost. Existing visual hierarchy and blue/amber/green status palette are worth retaining.

This is a credible local evaluation prototype. Shared state and file persistence need hardening before multi-user deployment. Step 8 only records a simulated send; no customer email delivery exists in this code.

## Ranked actionable findings

### P1 — Repeated-complaint routing depends on model judgment

Evidence: `acme/workflow.py:45` and `acme/workflow.py:220`. Defaults cover legal threats, injection and monetary requests; no deterministic rule combines complaint count with a switching threat. Actual offline c08 run returned `send` although the workbook requires E2 human review. Screenshot shows both the expected routing and mismatch. Offline mode intentionally has flaws, so this is not a claim about Claude accuracy; the missing deterministic backstop also affects any model that misses this escalation.

Next: add a CRM-aware E2 rule and positive/negative fixtures (repeated complaint + threat, isolated outage, historical complaint without threat). Do not use evaluation labels as runtime routing logic.

### P1 — Mutable process globals can mix evaluation conditions

Evidence: `app.py:36` initializes LAB, SETTINGS, DEPS, WF and BATCH globally; `_settings` at `app.py:270` mutates DEPS.provider, and batch workers read shared dependencies. Another session or a settings edit during a batch can change provider, knowledge or guards midway. Knowledge revision counters are session-local, so another browser can retain stale views.

Next: snapshot immutable provider/model, policy, guards and dataset version per run/batch. Add session ownership or explicitly restrict deployment to one reviewer. Test settings changes during a paused draft and from two sessions.

### P1 — Parsed model output lacks local schema validation

Evidence: `acme/providers.py:84` accepts a truthy structured or parsed JSON value; `acme/workflow.py:188` then assumes mapping fields and downstream checks assume string replies. Windows fallback relies only on prompt instructions. A list, wrong field type or malformed result can crash a workflow instead of yielding a controlled provider error.

Next: validate every provider output against DRAFT_SCHEMA locally, including type checks and allowed intents. Add malformed-object, wrong-type, empty-reply, nonzero-exit and timeout fixtures. Treat failures as reviewable errors.

### P2 — JSON store locking covers writes, not consistent reads

Evidence: `acme/store.py:28-35` iterates `_data` without the lock used by background writers. Concurrent dictionary insertions can raise iteration errors; shallow copies still share nested values. Process-local locking does not coordinate multiple server workers. AppSettings writes directly to its target file.

Next: lock read snapshots as well as writes for the single-process version; use database transactions for multi-worker deployment. Atomically replace settings files. Exercise concurrent read/write and interrupted-write tests.

### P2 — Grounding language overstates heuristic coverage

Evidence: `acme/workflow.py:217` reports “All claims grounded” when `claim_checks` returns no flags. Checks use regexes and known token matches, not exhaustive entailment. For example, amounts appearing in the customer's message count as known; absence of a regex hit does not establish policy support.

Next: label this “No configured checks triggered,” expose coverage limitations, and add adversarial paraphrase tests. Show heuristic checks separately from SME factual assessment.

### P2 — Resume and audit trail need product support

Evidence: graph checkpoints persist, but `sim_view` starts as None per session (`app.py:243`) and the UI offers no queue of saved waiting thread IDs. `ReviewStore.save_run` stores the latest run per round/case and only limited prior-verdict metadata. Restarting loses the convenient human-review entry point; repeated reruns are difficult to audit.

Next: add a pending-review list keyed by thread ID, an immutable run ID, reviewer identity, and a configuration/dataset snapshot. Test restart-to-resume and rerun history.

### P2 — Workbook instruction becomes a selectable failure mode

Evidence: `acme/lab.py:101` reads every nonempty first-column cell in Failure_Modes. Browser dropdown includes “Shaded rows are free: add modes as they emerge in error analysis...” as an option.

Next: load a defined Excel table/range or explicit valid mode rows, excluding instructional/footer content. Add a fixture containing both custom modes and footer guidance.

### P3 — Remaining UX polish

Mobile Review stacks its case selector below the long review form: no horizontal overflow, but expensive navigation. Add a compact case picker above the form on small screens. Give unlabeled intent and knowledge selectors explicit accessible names. Distinguish “simulated send” in outcomes. Make offline provider visible outside the settings popover. Align the Review and Scoreboard definition of “drafted”: imported c01 counts on Scoreboard but not Review (observed 3 vs 2). Display denominators alongside percentage metrics; current 50% routing score represents only two executed cases.

## Validation evidence

- Python 3.12.12, Shiny 1.8.0; full resolved packages in requirements-tested.txt.
- Original suite: 11/11 passed. Updated suite: 13/13 passed, including keyboard-order/HTML-escaping and bundled-icon checks.
- Browser: Review c08 selected with Enter; workflow step selected with Enter; Cases and Knowledge data tables loaded; Scoreboard loaded.
- Offline c08 drafted and showed missed escalation. Offline c16 paused for legal threat and resumed using the edited-reply action. No external email is sent by this app.
- Captured and visually examined final desktop Review/Simulator/Scoreboard and mobile Review/Simulator screenshots. Desktop viewport 1440×1000; mobile 390×844. Document width 390px at mobile size, no horizontal overflow. Screenshots exclude transient workflow notifications.
- Final browser navigation showed zero console errors and no Shiny output errors. Five upstream bootstrap-datepicker deprecation warnings remain; an initial favicon request returned 404.
- Quarto starter's Python cells executed successfully against saved validation records. Quarto CLI was unavailable; full Quarto HTML render was not tested.
- No live Claude calls, full 84-case batch, multi-user stress test, Excel writeback or deployment performed. Automatic approval review rejected the broad batch; limited verified-offline sample tests completed instead.
- Generated validation runs are excluded from the deliverable source. Screenshot metrics are demonstration evidence, not a full evaluation score. Original workbook retained unchanged.

## Quarto: practical fit

Keep Shiny as the place to edit cases, run workflows and capture judgments. Use Quarto as a reproducible reporting and publication layer reading saved snapshots. Quarto supports Python computations and multiple publication formats; MUI's icon package itself targets React, which is why this Shiny update bundles the underlying Material artwork.

Sources: [Quarto overview](https://quarto.org/), [MUI Material Icons](https://mui.com/material-ui/material-icons/).

1. **Round sign-off report — start here.** One report per round: reviewed/total, routed/total, missed escalations, failure modes, costs/latency where recorded, screenshots and release decision. Included `reports/round-review.qmd` already reads reviews and workbook, computes coverage and missed escalations, and hashes both inputs. It never reruns models. Add provider/configuration provenance before relying on comparisons. [Quarto parameters](https://quarto.org/docs/computations/parameters.html).
2. **Failure atlas.** Create one redacted page per failure pattern: incoming request, expected routing, actual response, highlighted issue, expert critique and regression test. Group pages by policy and intent. Use as reviewer onboarding material and curated judge examples. [Quarto websites](https://quarto.org/docs/websites/).
3. **Stakeholder dashboard.** Publish a read-only dashboard with routing confusion, case coverage, pass rates and latency by provider/round. Static HTML avoids keeping the editing app online; browser-side interactions can support exploration. Server-side Python interactions require a backend. [Quarto dashboards](https://quarto.org/docs/dashboards/).
4. **Release review deck.** Turn the same evidence into a short slide deck: scope, worst misses, before/after examples, open risks and decision. Quarto supports presentations and report formats from text-based sources. [Quarto overview](https://quarto.org/).

Suggested loop: finish review → snapshot workbook/reviews/config/source revision → render parameterized report → inspect numbers and screenshots → share approved report. Keep live customer data and unredacted critiques out of public publishing targets.

Do not rely on `freeze: auto` to notice changes in input JSON/Excel: it tracks document source changes during global project rendering. Render the individual report explicitly when input data changes, or use a deliberate snapshot/build pipeline. [Execution and freeze behavior](https://quarto.org/docs/projects/code-execution.html).
