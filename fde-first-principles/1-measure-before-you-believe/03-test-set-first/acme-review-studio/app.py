"""Acme Review Studio: run the controlled draft workflow and review it as the domain expert.

    shiny run app.py --launch-browser
"""
from __future__ import annotations

import asyncio
import copy
import html
import json
import os
import re
import sqlite3
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from shiny import App, reactive, render, ui  # noqa: E402

from acme.checks import eval_checks, guard_hits  # noqa: E402
from acme.lab import INTENTS, export_to_excel, load_lab, read_review_log  # noqa: E402
from acme.providers import make_provider  # noqa: E402
from acme.review import initial_mode, suggest_mode, validate_verdict  # noqa: E402
from acme.sim.render import render_comparison, render_detail, render_result  # noqa: E402
from acme.sim.service import SimulationService, compare_reviews, review_record, sample_spread  # noqa: E402
from acme.sim.trace import RunInput  # noqa: E402
from acme.sim.versions import label_hash  # noqa: E402
from acme.store import AppSettings, ReviewStore  # noqa: E402
from acme.ui_bits import CSS, JS, chip, highlight, icon  # noqa: E402
from acme.workflow import PORTALS  # noqa: E402

ROOT = Path(__file__).parent
LAB_ROOT = ROOT.parents[2]
if str(LAB_ROOT) not in sys.path:
    sys.path.append(str(LAB_ROOT))

from lab.acme import kb_by_id as lab_kb_by_id  # noqa: E402
from lab.business_rules import load_business_rules  # noqa: E402
from lab.ontology import (  # noqa: E402
    concept_provenance,
    concept_labels,
    define,
    policy_rules,
    terms as ontology_terms,
    validate_ontology_ops,
)

XLSX = Path(os.environ.get("ACME_XLSX", ROOT / "data" / "Acme_Fibre_Grounded_Draft_Eval.xlsx"))
RUNS = Path(os.environ.get("ACME_RUNS_DIR", ROOT / "runs"))
RUNS.mkdir(parents=True, exist_ok=True)

LAB = load_lab(XLSX)
STORE = ReviewStore(RUNS / "reviews.json")
if not STORE.all():
    STORE.import_rows(read_review_log(XLSX))
SETTINGS = AppSettings(RUNS / "settings.json")
SIM = SimulationService(ROOT, LAB, SETTINGS, runs_dir=RUNS)
SIM.registry.import_legacy_rounds([int(v.removeprefix("legacy-round-")) for v in STORE.versions()
                                   if v.startswith("legacy-round-") and v.removeprefix("legacy-round-").isdigit()])
SIM.seed_manifests()
BATCH = {"running": False, "done": 0, "total": 0, "errors": 0}
BATCH_LOCK = threading.Lock()
VERSION_DESCRIPTIONS = {
    "studio-c3": "Studio 9-step workflow, drafted by the C3 agent (glm-5.3-flash, ontology-grounded)",
    "studio-offline": "Studio 9-step workflow, drafted by offline rules — no model, deliberate flaws for demos",
    "studio-declarative": "Studio workflow built from the spec (declarative graph), full checks + human review",
    "c3-agent": "C3 agent loop run directly — no studio graph, no step checks",
    "version-b": "Version B — one LLM call, no tools, no loop",
    "offline-direct": "Offline rules run directly — no model, no graph",
    "remote-agent": "Agent behind an HTTP endpoint (remote deployment)",
}


def version_choices() -> dict[str, str]:
    versions = SIM.registry.list()
    named = [v for v in versions if v.label or v.status == "legacy"]
    recent = [v for v in versions if not v.label and v.status == "snapshot"][:20]

    def label_for(v) -> str:
        if v.status == "legacy":
            return f"Round {v.name.removeprefix('legacy-round-')} reviews — imported from the workbook"
        description = VERSION_DESCRIPTIONS.get(v.name)
        if description:
            return f"{v.name} (v{v.label}) — {description}"
        return f"{v.name} (v{v.label}) — {v.status} snapshot {v.id[:8]}"

    return {"working": "Working copy — editable current config, auto-snapshots on change", **{
        v.id: label_for(v) for v in named + recent}}


def case_choices() -> dict[str, str]:
    return {"": "Write my own", **{c["id"]: f"{c['id']} · {c['message'][:46]}…" for c in LAB.cases}}


def default_sim_step(result):
    if result.state == "waiting_for_human":
        return "step-H"
    return next((span.id for span in result.spans if span.status == "error"),
                next((span.id for span in result.spans if span.id == "step-5"),
                     result.spans[0].id if result.spans else None))


def run_case(case: dict, version_id: str, portal: str = "email"):
    result = SIM.run(version_id, RunInput.from_case(case, portal))
    STORE.save_run(version_id, case["id"], review_record(result))
    return result


def customer_chips(cust: dict | None) -> str:
    if not cust:
        return chip("unknown customer", "bad")
    outage = LAB.outage_for(cust)
    parts = [chip(f"{cust['name']} · {cust['id']}"), chip(f"{cust['plan']} · {cust['area']}"),
             chip(f"{cust['tenure_months']} mo tenure"),
             chip(f"₹{cust['balance_due']} due", "warn" if cust["balance_due"] else "ok"),
             chip(f"{cust['complaints_30d']} complaints/30d", "bad" if cust["complaints_30d"] >= 2 else ""),
             chip(outage["ticket"] if outage else "no area outage", "warn" if outage else "")]
    if cust.get("credits_30d"):
        parts.append(chip(f"₹{cust['credits_30d']} credited/30d", "warn"))
    if cust.get("late_fee_waived_on"):
        parts.append(chip(f"waiver used {cust['late_fee_waived_on']}"))
    if cust.get("retention_offer_used_on"):
        parts.append(chip(f"retention used {cust['retention_offer_used_on']}"))
    payments = cust.get("payments_this_cycle") or []
    parts.append(chip("paid " + " + ".join(f"₹{p:,}" for p in payments) if payments else "no payment this cycle",
                      "warn" if len(payments) > 1 else ""))
    return "".join(parts)


# =================================================================== UI
def review_page():
    return ui.layout_sidebar(
        ui.sidebar(
            ui.output_ui("progress"),
            ui.input_radio_buttons("show", None, {"todo": "To review", "all": "All", "fail": "Failed",
                                                   "mismatch": "Wrong routing"}, selected="todo", inline=True),
            ui.input_select("intent_filter", None, {"": "All intents", **{i: i for i in INTENTS}}),
            ui.output_ui("case_list"),
            ui.input_action_button("run_missing", "Run all cases not yet run", icon=icon("play"), class_="btn-primary btn-sm w-100"),
            ui.output_ui("batch_status"),
            width=320, open="always", bg="#fff",
        ),
        ui.output_ui("case_header"),
        ui.layout_columns(
            ui.card(ui.card_header("Customer email"), ui.output_ui("email_card"), class_="customer-card"),
            ui.card(ui.card_header("What good looks like"), ui.output_ui("expected_card"), class_="expected-card"),
            col_widths=(7, 5),
        ),
        ui.card(ui.card_header(ui.output_ui("run_header", inline=True)), ui.output_ui("run_card"), class_="review-workflow"),
        ui.layout_columns(
            ui.card(ui.card_header(ui.span("Draft reply"), ui.output_ui("draft_meta", inline=True)), ui.output_ui("reply_card"), class_="draft-card"),
            ui.card(
                ui.card_header(ui.span("Your verdict"), ui.output_ui("saved_badge", inline=True)),
                ui.div(ui.input_action_button("btn_pass", ui.span("Pass", ui.tags.small("Press P")), icon=icon("check"), class_="btn-pass"),
                       ui.input_action_button("btn_fail", ui.span("Fail", ui.tags.small("Press F")), icon=icon("close"), class_="btn-fail"),
                       class_="verdict d-flex gap-2 align-items-center mb-3"),
                ui.input_select("failure_mode", "Failure mode (for Fail)", {"": "—"}, width="100%"),
                ui.input_text_area("critique", "Critique: what a new agent should learn from this reply",
                                   rows=5, width="100%",
                                   placeholder="e.g. Grounded on the ticket, but promises a fix time the record "
                                               "doesn't have. A passing reply shares OUT-KOTH-1021 and the app updates."),
                ui.div(ui.HTML("<kbd>P</kbd> pass &nbsp;<kbd>F</kbd> fail &nbsp;<kbd>J</kbd>/<kbd>K</kbd> next/prev "
                               "&nbsp;<kbd>Ctrl</kbd>+<kbd>Enter</kbd> save fail"), class_="muted review-shortcuts"),
                class_="verdict-card",
            ),
            col_widths=(7, 5),
        ),
    )


def simulator_page():
    cust_choices = {cid: f"{c['name']} · {cid}" for cid, c in LAB.customers.items()}
    cust_choices["AC9999"] = "Unknown customer · AC9999"
    return ui.layout_columns(
        ui.card(
            ui.card_header("Incoming email"),
            ui.input_select("sim_version", "Workflow version", version_choices(), selected="working", width="100%"),
            ui.output_ui("sim_version_status"),
            ui.input_select("sim_case", "Start from a case", case_choices(), width="100%"),
            ui.input_select("sim_customer", "Customer", cust_choices, width="100%"),
            ui.output_ui("sim_optional_inputs"),
            ui.input_text_area("sim_message", "Message", rows=7, width="100%"),
            ui.input_numeric("sim_samples", "Samples", 1, min=1, max=100, step=1),
            ui.output_ui("sim_replay_options"),
            ui.input_select("sim_compare_version", "Compare with", {"": "No comparison", **version_choices()},
                            selected="", width="100%"),
            ui.input_switch("sim_audit", "Run as audit", False),
            ui.output_ui("sim_run_control"),
            ui.output_ui("sim_history_controls"),
            ui.div("Runs of a dataset case also become that case's draft on the Review page.", class_="muted mt-2"),
        ),
        ui.div(
            ui.output_ui("sim_version_banner"),
            ui.card(ui.card_header("Run view · select a span to inspect it"), ui.output_ui("sim_pipe"),
                    ui.output_ui("sim_step_detail")),
            ui.output_ui("sim_human"),
            ui.output_ui("sim_outcome"),
            ui.output_ui("sim_comparison"),
        ),
        col_widths=(4, 8),
    )


def cases_page():
    return ui.div(
        ui.layout_columns(
            ui.div("Ground truth for each case. Select a row to change its label; changes save to Excel with "
                   "'Save to Excel'.", class_="hint"),
            ui.div(ui.input_action_button("new_case", "New case", class_="btn-outline-primary btn-sm"),
                   class_="text-end"),
            col_widths=(9, 3),
        ),
        ui.card(ui.output_data_frame("cases_grid")),
        ui.output_ui("case_editor"),
    )


def knowledge_page():
    return ui.div(
        ui.div("What the workflow knows. Edits apply to the next run straight away.", class_="hint"),
        ui.navset_card_underline(
            ui.nav_panel("Customers", ui.output_data_frame("customers_grid"),
                         ui.div("Double-click a cell to edit.", class_="muted mt-2")),
            ui.nav_panel("Outages",
                         ui.output_data_frame("outages_grid"),
                         ui.layout_columns(
                             ui.input_select("new_out_area", "Area", sorted({c["area"] for c in LAB.customers.values()})),
                             ui.input_text("new_out_cause", "Cause", "Fibre cut"),
                             ui.div(ui.input_action_button("add_outage", "Add outage", class_="btn-outline-primary mt-4"),
                                    ui.input_action_button("remove_outage", "Remove selected", class_="btn-outline-secondary mt-4 ms-2")),
                             col_widths=(3, 5, 4))),
            ui.nav_panel("Help articles & policy",
                         ui.input_select("kb_pick", None, {k: f"{k} · {v['title']}" for k, v in LAB.kb.items()}),
                         ui.input_text("kb_title", "Title", width="100%"),
                         ui.input_text_area("kb_text", "Text", rows=6, width="100%"),
                         ui.input_action_button("kb_save", "Save article", class_="btn-primary")),
            ui.nav_panel("Meaning",
                         ui.div("A concept lists its governing rules. A rule lists affected concepts; select one to open its card.",
                                class_="hint"),
                         ui.layout_columns(
                             ui.input_select("meaning_rule", "Policy rule",
                                             {"": "No linked rule", **{
                                                 str(number): f"Rule {number}" for number in policy_rules()
                                             }}, selected="10"),
                             ui.input_select("meaning_affected_concept", "Concepts affected by rule",
                                             sorted(ontology_terms()), selected="retention offer"),
                             ui.input_selectize("meaning_concept", "Business concept",
                                                sorted(concept_labels()), selected="retention offer",
                                                options={"placeholder": "Search any label"}),
                             col_widths=(4, 4, 4)),
                         ui.output_ui("meaning_concept_card"),
                         ui.output_ui("meaning_rule_detail"),
                         ui.output_data_frame("meaning_checks")),
            ui.nav_panel("Escalation guards",
                         ui.div("Code rules checked at step 7. They escalate whatever the model said.", class_="muted mb-2"),
                         ui.output_data_frame("guards_grid"),
                         ui.input_switch("block_high", "Escalate when a step-6 check finds a blocking problem",
                                         SETTINGS.workflow.block_on_high_flags),
                         ui.input_text_area("guard_try", "Try a message", rows=2, width="100%",
                                            placeholder="I'll take this to consumer court"),
                         ui.output_ui("guard_try_result")),
            ui.nav_panel("Workflow spec", ui.output_ui("workflow_spec")),
        ),
    )


def score_page():
    return ui.div(
        ui.output_ui("score_boxes"),
        ui.layout_columns(
            ui.card(ui.card_header("Pass rate by intent"), ui.output_plot("score_plot", height="280px")),
            ui.card(ui.card_header("Routing vs. what should happen"), ui.output_ui("score_confusion")),
            col_widths=(7, 5),
        ),
        ui.layout_columns(
            ui.card(ui.card_header("Failure modes"), ui.output_ui("score_modes")),
            ui.card(ui.card_header("By escalation rule"), ui.output_ui("score_rules")),
            ui.card(ui.card_header("By version"), ui.output_ui("score_rounds")),
            col_widths=(4, 5, 3),
        ),
        ui.card(ui.card_header("Compare versions and release evidence"),
                ui.input_select("score_compare", "Compare selected review version with",
                                {"": "Choose a version", **version_choices()}, selected=""),
                ui.output_ui("score_regressions"),
                ui.input_text("candidate_label", "Name a working-copy snapshot", placeholder="1.0.0"),
                ui.input_action_button("name_candidate", "Name snapshot", class_="btn-outline-primary btn-sm"),
                ui.input_text("release_signoff", "Reviewer sign-off", placeholder="Reviewer name"),
                ui.input_action_button("release_version", "Release candidate", class_="btn-primary btn-sm"),
                ui.input_action_button("retire_version", "Retire version", class_="btn-outline-secondary btn-sm ms-2")),
    )


settings_popover = ui.popover(
    ui.input_action_link("open_settings", "Model", icon=icon("settings")),
    ui.input_radio_buttons("provider", "Drafting model",
                           {"claude-code": "Claude Code", "c3": "C3 ontology agent (lab)", "offline": "Offline stand-in"},
                           selected=SETTINGS.provider),
    ui.input_select("model", "Claude model", {"sonnet": "Sonnet", "opus": "Opus", "haiku": "Haiku"}, selected=SETTINGS.model),
    ui.input_select("review_version", "Review version", version_choices(), selected="working", width="100%"),
    ui.input_switch("critique_first", "Critique-first review (mode optional on Fail)", SETTINGS.critique_first),
    ui.input_slider("concurrency", "Parallel drafts", 1, 10, SETTINGS.concurrency),
    ui.input_numeric("retention_days", "Run retention in days (0 keeps runs)", SETTINGS.run_retention_days, min=0, step=1),
    ui.input_action_button("apply_retention", "Apply retention", class_="btn-outline-secondary btn-sm"),
    ui.output_ui("provider_status"),
    title="Settings", placement="bottom",
)

app_ui = ui.page_navbar(
    ui.nav_panel("Review", review_page(), value="review", icon=icon("review")),
    ui.nav_panel("Simulator", simulator_page(), value="simulator", icon=icon("play")),
    ui.nav_panel("Cases", cases_page(), value="cases", icon=icon("cases")),
    ui.nav_panel("Knowledge", knowledge_page(), value="knowledge", icon=icon("knowledge")),
    ui.nav_panel("Scoreboard", score_page(), value="score", icon=icon("score")),
    ui.nav_spacer(),
    ui.nav_control(settings_popover),
    ui.nav_control(ui.input_action_button("export", "Save to Excel", icon=icon("save"), class_="btn-outline-primary btn-sm")),
    ui.nav_control(ui.div(ui.span("RC", class_="profile-monogram"), ui.span("Raj Champaneriya"), class_="profile-signature")),
    title=ui.span(ui.span("A", class_="app-monogram"), "Acme Review Studio"),
    window_title="Acme Review Studio",
    id="nav",
    header=ui.head_content(ui.tags.style(CSS), ui.tags.script(JS)),
    fillable=False,
)


# =================================================================== server
def server(input, output, session):
    local = reactive.value(0)            # bumped after saves in this session
    settings_rev = reactive.value(0)
    data_rev = reactive.value(0)          # cases / knowledge edits
    current = reactive.value(LAB.cases[0]["id"])
    sim_view = reactive.value(None)
    sim_compare_view = reactive.value(None)
    sim_samples_view = reactive.value([])
    sim_step = reactive.value("step-5")
    sim_compare_step = reactive.value(None)
    sim_loaded_input = reactive.value(None)
    sim_replay_mode = reactive.value("fresh")
    working_review_version = reactive.value(None)
    review_step = reactive.value(None)

    @reactive.poll(lambda: (len(STORE.all()), STORE.path.stat().st_mtime_ns if STORE.path.exists() else 0), 1)
    def store_rev():
        return STORE.path.stat().st_mtime_ns if STORE.path.exists() else 0

    @reactive.poll(lambda: (BATCH["running"], BATCH["done"]), 0.7)
    def batch_rev():
        return dict(BATCH)

    def version_token():
        return tuple((row["id"], row["label"], row["status"]) for row in SIM.store.versions())

    @reactive.poll(version_token, 2)
    def versions_rev():
        return version_token()

    def rnd() -> str | None:
        settings_rev()
        selected = input.review_version()
        return working_review_version() if selected == "working" else selected

    @reactive.calc
    def round_data() -> dict[str, dict]:
        store_rev(), local()
        version_id = rnd()
        return STORE.version(version_id) if version_id else {}

    def refresh_versions():
        choices = version_choices()
        ui.update_select("review_version", choices=choices, selected=input.review_version())
        ui.update_select("sim_version", choices=choices, selected=input.sim_version())
        ui.update_select("sim_compare_version", choices={"": "No comparison", **choices},
                         selected=input.sim_compare_version())
        ui.update_select("score_compare", choices={"": "Choose a version", **choices},
                         selected=input.score_compare())

    @reactive.effect
    def _refresh_shared_versions():
        versions_rev()
        with reactive.isolate():
            refresh_versions()

    def selected_review_version():
        if input.review_version() == "working":
            version = SIM.freeze_working()
            working_review_version.set(version.id)
            refresh_versions()
            return version
        return SIM.registry.get(input.review_version())

    def case_of(cid):
        data_rev()
        return LAB.case(cid)

    @reactive.effect
    def _refresh_case_choices():
        data_rev()
        with reactive.isolate():
            ui.update_select("sim_case", choices=case_choices(), selected=input.sim_case())

    # ------------------------------------------------ settings
    @reactive.effect
    @reactive.event(input.provider, input.model, input.concurrency, input.critique_first, input.retention_days,
                    ignore_init=True)
    def _settings():
        SETTINGS.provider, SETTINGS.model = input.provider(), input.model()
        SETTINGS.concurrency = int(input.concurrency())
        SETTINGS.critique_first = input.critique_first()
        SETTINGS.run_retention_days = max(0, int(input.retention_days() or 0))
        SETTINGS.save()
        settings_rev.set(settings_rev() + 1)

    @render.ui
    def provider_status():
        settings_rev()
        ok, msg = make_provider(SETTINGS.provider, SETTINGS.model).status()
        return ui.div(ui.HTML(chip("ready" if ok else "not ready", "ok" if ok else "bad")), ui.span(msg, class_="muted"))

    @reactive.effect
    @reactive.event(input.apply_retention)
    def _apply_retention():
        try:
            days = SETTINGS.run_retention_days
            deleted, logs = SIM.apply_retention(days) if days else (0, 0)
            collected = SIM.registry.collect_unreferenced_snapshots(STORE.versions())
            refresh_versions()
            local.set(local() + 1)
            ui.notification_show(f"Removed {deleted} expired runs, {logs} log entries and {collected} unreferenced snapshots.")
        except (ValueError, OSError, sqlite3.Error) as exc:
            ui.notification_show(str(exc), type="error", duration=8)

    # ------------------------------------------------ review: list + navigation
    @reactive.calc
    def visible_ids() -> list[str]:
        data_rev()
        data, show, intent = round_data(), input.show(), input.intent_filter()
        out = []
        for c in LAB.cases:
            rec = data.get(c["id"], {})
            if intent and c["expected_intent"] != intent:
                continue
            if show == "todo" and rec.get("verdict"):
                continue
            if show == "fail" and rec.get("verdict") != "Fail":
                continue
            if show == "mismatch" and eval_checks(c, rec)["routing_ok"] is not False:
                continue
            out.append(c["id"])
        return out

    def move(step: int):
        ids = visible_ids() or [case["id"] for case in LAB.cases]
        cid = current()
        idx = ids.index(cid) if cid in ids else -1
        current.set(ids[max(0, min(len(ids) - 1, idx + step))] if idx >= 0 else ids[0])

    @reactive.effect
    @reactive.event(input.pick_case)
    def _pick():
        current.set(input.pick_case())

    # Deep link: /?case=c19 selects that case on the review tab (used by data/results/monitor.html).
    deeplinked = reactive.value(False)

    @reactive.effect
    def _deeplink():
        data_rev()
        m = re.search(r"[?&]case=(c\d+)", input[".clientdata_url_search"]() or "")
        if m and m.group(1) in {case["id"] for case in LAB.cases}:
            deeplinked.set(True)
            current.set(m.group(1))
            ui.update_radio_buttons("show", selected="all")
            ui.update_navs("nav", selected="review")

    @reactive.effect
    @reactive.event(input.kbd)
    async def _keys():
        key = input.kbd()
        if input.nav() != "review":
            return
        if key == "next":
            move(1)
        elif key == "prev":
            move(-1)
        elif key == "pass":
            await save_verdict("Pass")
        elif key == "fail":
            await session.send_custom_message("focus", "critique")
            hint = "Write the critique, then Ctrl+Enter." if SETTINGS.critique_first else \
                   "Pick a failure mode, write the critique, then Ctrl+Enter."
            ui.notification_show(hint, duration=3)
        elif key == "save":
            await save_verdict("Fail")

    @render.ui
    def progress():
        data_rev()
        data = round_data()
        ids = [case["id"] for case in LAB.cases]
        drafted = sum(1 for c in ids if data.get(c, {}).get("reply") or data.get(c, {}).get("decision"))
        reviewed = sum(1 for c in ids if data.get(c, {}).get("verdict"))
        pct = int(100 * reviewed / len(ids)) if ids else 0
        return ui.div(
            ui.div(ui.strong(f"Version {rnd() or 'working copy'}"), ui.span(f" · {reviewed}/{len(ids)} reviewed · {drafted} drafted",
                                                         class_="muted")),
            ui.HTML(f'<div class="progress my-2" style="height:6px"><div class="progress-bar" '
                    f'style="width:{pct}%;background:#2E6DB4"></div></div>'))

    @render.ui
    def case_list():
        data, cid = round_data(), current()
        items = []
        for i in visible_ids():
            c, rec = case_of(i), data.get(i, {})
            dot = ("pass" if rec.get("verdict") == "Pass" else "fail" if rec.get("verdict") == "Fail" else
                   "err" if rec.get("error") else "drafted" if rec.get("reply") or rec.get("decision") else "")
            items.append(f'<button type="button" aria-current="{"true" if i == cid else "false"}" '
                         f'class="caseitem {"active" if i == cid else ""}" data-case="{i}">'
                         f'<span class="case-row-title"><span class="dot {dot}"></span><span class="id">{i}</span>'
                         f'<span class="case-intent">{html.escape(c["expected_intent"])}</span></span>'
                         f'<span class="case-preview">{html.escape(c["message"])}</span>'
                         f'<span class="visually-hidden">{dot or "not run"}</span></button>')
        if not items:
            return ui.div("Nothing here. Change the filter above.", class_="muted my-3")
        return ui.HTML(f'<div class="caselist">{"".join(items)}</div>')

    @render.ui
    def batch_status():
        b = batch_rev()
        if not b["total"]:
            return ui.div()
        state = "Drafting" if b["running"] else "Done"
        return ui.div(f"{state}: {b['done']}/{b['total']}" + (f" · {b['errors']} errors" if b["errors"] else ""),
                      ui.div(b.get("last_error", ""), class_="text-danger") if b.get("last_error") else None,
                      class_="muted mt-2")

    @reactive.effect
    @reactive.event(input.run_missing)
    def _run_missing():
        if BATCH["running"]:
            return
        try:
            version = selected_review_version()
            ready, msg = SIM.status(version.id)
        except (ValueError, KeyError, OSError) as exc:
            ui.notification_show(str(exc), type="error", duration=8)
            return
        if not ready:
            ui.notification_show(msg, type="error", duration=8)
            return
        data = STORE.version(version.id)
        todo = [copy.deepcopy(c) for c in LAB.cases if not data.get(c["id"], {}).get("decision")]
        if not todo:
            ui.notification_show("Every case in this version has been run. Re-run a case or select another version.")
            return
        concurrency = SETTINGS.concurrency
        BATCH.update(running=True, done=0, total=len(todo), errors=0, last_error="", version_id=version.id)

        def worker():
            def one(case):
                try:
                    result = run_case(case, version.id)
                    if result.state == "failed":
                        with BATCH_LOCK:
                            BATCH["errors"] += 1
                            BATCH["last_error"] = review_record(result).get("error") or "A run failed."
                except Exception as exc:  # surface a failure even if persistence itself failed
                    with BATCH_LOCK:
                        BATCH["errors"] += 1
                        BATCH["last_error"] = str(exc)
                finally:
                    with BATCH_LOCK:
                        BATCH["done"] += 1
            try:
                with ThreadPoolExecutor(concurrency) as pool:
                    list(pool.map(one, todo))
            finally:
                BATCH["running"] = False

        threading.Thread(target=worker, daemon=True).start()
        ui.notification_show(f"Drafting {len(todo)} cases with {version.name} · {version.id}.")

    # ------------------------------------------------ review: case panels
    @reactive.calc
    def cur():
        c = case_of(current())
        return c, round_data().get(c["id"], {})

    @render.ui
    def case_header():
        c, rec = cur()
        expected = chip("should go to a human", "warn", True) if c["needs_human"] else chip("can be sent", "ok", True)
        return ui.div(
            ui.div(ui.HTML(f'<h4 class="m-0" style="color:#1F3A5F">{c["id"]}</h4>'),
                   ui.HTML(chip(c["expected_intent"], big=True) + expected +
                           "".join(chip(t, "bad" if t == "angry" else "") for t in c["tags"])), class_="case-heading-chips d-flex gap-3 align-items-center"),
            ui.div(ui.input_action_button("prev", "Prev", icon=icon("back"), class_="btn-sm btn-outline-secondary"),
                   ui.input_action_button("next", "Next", icon=icon("next"), class_="btn-sm btn-outline-secondary ms-1")),
            class_="case-heading d-flex justify-content-between align-items-center mb-3")

    @reactive.effect
    @reactive.event(input.next)
    def _next():
        move(1)

    @reactive.effect
    @reactive.event(input.prev)
    def _prev():
        move(-1)

    @render.ui
    def email_card():
        c, _ = cur()
        earlier = "".join(
            f'<div class="turn turn-{html.escape(t["role"])}"><span class="muted">{html.escape(t["role"].capitalize())}</span>'
            f'<div class="email">{html.escape(t["text"])}</div></div>' for t in c.get("history") or [])
        latest = '<span class="muted">Customer · latest message, the run drafts the reply to this</span>' if earlier else ""
        return ui.div(ui.HTML(customer_chips(LAB.customers.get(c["customer_id"]))),
                      ui.HTML(f'<div class="history mt-2">{earlier}</div>' if earlier else ""),
                      ui.HTML(f'{latest}<div class="email mt-2">{html.escape(c["message"])}</div>'))

    @render.ui
    def expected_card():
        c, _ = cur()
        inc = "".join(chip(t, "ok") for t in c["must_include"]) or '<span class="muted">—</span>'
        bad = "".join(chip(t, "bad") for t in c["must_not"]) or '<span class="muted">—</span>'
        return ui.HTML(
            f'<dl class="kv"><dt>Routing spec</dt><dd class="routing-spec {"risk" if c["needs_human"] else "safe"}">{"Human review" if c["needs_human"] else "Send automatically"}'
            f' · rule {html.escape(c["rule"])}</dd><dt>Must include entities</dt><dd>{inc}</dd>'
            + (f'<dt>Must not say</dt><dd>{bad}</dd>' if c["must_not"] else "") +
            f'<dt>Why this routing is expected</dt><dd class="muted">{html.escape(c["rationale"])}</dd></dl>')

    @render.ui
    def run_header():
        _, rec = cur()
        if not (rec.get("reply") or rec.get("decision")):
            return ui.span("Workflow run")
        routed = rec.get("decision")
        label = {"escalate": "Routed to a human", "send": "Sent automatically"}.get(routed, "Imported from Excel")
        meta = " ".join(str(x) for x in (rec.get("provider"), rec.get("model"),
                                         f"{rec['latency_s']}s" if rec.get("latency_s") else None) if x)
        stale = rec.get("label_hash") and rec["label_hash"] != label_hash(cur()[0])
        return ui.HTML(f'Workflow run · <span style="font-weight:500">{label}</span>'
                       + (f' <span class="muted">· {html.escape(meta)}</span>' if meta else "")
                       + (' <span class="text-warning">· graded against an earlier label</span>' if stale else ""))

    @render.ui
    def run_card():
        c, rec = cur()
        buttons = ui.div(ui.input_action_button("run_one", "Re-run" if rec.get("decision") else "Draft this case",
                                                class_="btn-sm btn-primary"),
                         ui.input_action_button("to_sim", "Open in simulator", class_="btn-sm btn-outline-secondary ms-1"),
                         class_="mt-2")
        if not rec.get("trace"):
            note = ("Draft imported from the workbook; run it to see the workflow." if rec.get("reply")
                    else "No draft yet for this version.")
            return ui.div(ui.div(note, class_="muted"), buttons)
        mismatch = eval_checks(c, rec)["routing_ok"] is False
        reasons = (chip(f"Expected human review · rule {c['rule']}", "bad")
                   if mismatch and c["needs_human"] else
                   "".join(chip(r, "warn") for r in rec.get("reasons", [])) or chip("no escalation reasons", "ok"))
        sel = review_step()
        detail = ""
        if sel:
            t = next((t for t in rec["trace"] if t["step"] == sel), None)
            detail = f'<div class="muted mt-2"><b>Step {sel}:</b> {html.escape(t["detail"]) if t else "did not run"}</div>'
        steps = {t["step"]: t for t in rec["trace"]}
        cells = []
        for key, label in [("1", "Normalize"), ("2", "Route"), ("4", "CRM + policy"), ("5", "Grounded draft"), ("7", "Risk check")]:
            t = steps.get(key)
            status = "Missed escalation" if key == "7" and mismatch and c["needs_human"] else t["status"] if t else "not run"
            cls = "bad" if status == "Missed escalation" else "model" if key == "5" else ""
            cells.append(f'<button type="button" class="summary-step {cls}" data-step="{key}" '
                         f'data-target="review_step_click" title="{html.escape(t["detail"] if t else "Not run")}">'
                         f'{key}: {label}<span>{html.escape(status)}</span></button>')
        return ui.div(ui.HTML('<div class="review-pipeline">' + "".join(cells) + '</div>'),
                      ui.HTML(f'<div class="mt-3">{reasons}</div>{detail}'), buttons)

    @reactive.effect
    @reactive.event(input.review_step_click)
    def _rstep():
        review_step.set(None if review_step() == input.review_step_click() else input.review_step_click())

    @reactive.effect
    @reactive.event(input.run_one)
    async def _run_one():
        c, _ = cur()
        try:
            version = selected_review_version()
            ready, msg = SIM.status(version.id)
        except (ValueError, KeyError, OSError) as exc:
            ui.notification_show(str(exc), type="error", duration=8)
            return
        if not ready:
            ui.notification_show(msg, type="error", duration=8)
            return
        ui.notification_show(f"Drafting {c['id']} with {version.name}…", id="drafting", duration=None)
        try:
            result = await asyncio.to_thread(run_case, copy.deepcopy(c), version.id)
            if result.state == "failed":
                ui.notification_show(review_record(result).get("error") or "Run failed.", type="error", duration=8)
        except (ValueError, KeyError, OSError) as exc:
            ui.notification_show(str(exc), type="error", duration=8)
        finally:
            ui.notification_remove("drafting")
        local.set(local() + 1)

    @reactive.effect
    @reactive.event(input.to_sim)
    def _to_sim():
        c, rec = cur()
        if rec.get("run_id"):
            try:
                result, run_input = SIM.store.get(rec["run_id"])
                show_saved_run(result, run_input)
            except KeyError:
                ui.notification_show("The saved simulator run is no longer available.", type="warning")
                ui.update_select("sim_case", selected=c["id"])
        else:
            ui.update_select("sim_case", selected=c["id"])
        ui.update_navs("nav", selected="simulator")

    @render.ui
    def draft_meta():
        _, rec = cur()
        provider = " ".join(str(rec[k]) for k in ("provider", "model") if rec.get(k))
        return ui.span(provider or "No draft yet", class_="draft-meta")

    @render.ui
    def reply_card():
        c, rec = cur()
        if rec.get("error"):
            return ui.div(ui.HTML(chip("model error", "bad")), ui.div(rec["error"], class_="muted mt-2"))
        if not rec.get("reply"):
            return ui.div("No draft." if not rec.get("decision") else
                          "The workflow stopped before the model (see the run above).", class_="muted")
        ev = eval_checks(c, rec)

        def mark(ok, yes, no):
            return "" if ok is None else chip(yes, "ok") if ok else chip(no, "bad")
        checks = (mark(ev["intent_ok"], f"intent {rec.get('model_intent')} ✓", f"intent {rec.get('model_intent')} ✗")
                  + mark(ev["routing_ok"], "routing ✓", "routing ✗")
                  + mark(ev["model_escalation_ok"], "model's own flag ✓", "model's own flag ✗")
                  + "".join(chip(f"missing: {m}", "bad") for m in ev["missing"])
                  + "".join(chip(f"says: {b}", "bad") for b in ev["banned"])
                  + "".join(chip(f["check"], "bad" if f["severity"] == "high" else "warn") for f in rec.get("flags", [])))
        prev = rec.get("previous_verdict")
        prev_note = (f'<div class="muted mt-2">Earlier draft was marked {prev.get("verdict")}.</div>'
                     if prev and prev.get("verdict") else "")
        return ui.HTML(f'<div class="reply">{highlight(rec["reply"], c["must_include"], c["must_not"])}</div>'
                       f'<div class="reply-checkpoints"><span>Checkpoints:</span> {checks}</div>{prev_note}')

    # ------------------------------------------------ review: verdict
    prefill_key = reactive.value(None)

    @reactive.effect
    def _prefill_key():
        # Only refill the verdict inputs when the case or its draft/review changes, not on every
        # background save (a running batch would otherwise wipe what the SME is typing).
        c, rec = cur()
        prefill_key.set((c["id"], rnd(), rec.get("thread_id") or rec.get("reply"), rec.get("verdict"),
                         rec.get("critique"), rec.get("failure_mode")))

    @reactive.effect
    @reactive.event(prefill_key)
    def _prefill():
        with reactive.isolate():
            c, rec = cur()
        modes = {"": "—", **{m: m for m in LAB.failure_modes}}
        mode = rec.get("failure_mode") or initial_mode(c, rec, SETTINGS.critique_first)
        if not rec.get("verdict") and (rec.get("reply") or rec.get("decision")):
            suggestion = suggest_mode(c, rec)
            if suggestion:
                modes[suggestion] = f"{suggestion} (suggested)" if not SETTINGS.critique_first else f"{suggestion} · hint"
        with reactive.isolate():
            ui.update_select("failure_mode", choices=modes, selected=mode)
            ui.update_text_area("critique", value=rec.get("critique") or "")

    @render.ui
    def saved_badge():
        _, rec = cur()
        if rec.get("verdict"):
            return ui.span(f"Saved: {rec['verdict']}", class_=f"saved {rec['verdict'].lower()}")
        return ui.span("Not reviewed yet", class_="muted")

    async def save_verdict(verdict: str):
        c, rec = cur()
        if not (rec.get("reply") or rec.get("decision")):
            ui.notification_show("Draft this case first.", type="warning")
            return
        critique = (input.critique() or "").strip()
        mode = input.failure_mode() or ""
        refusal = validate_verdict(verdict, mode, critique, SETTINGS.critique_first)
        if refusal:
            ui.notification_show(f"For a Fail, {refusal}.", type="warning")
            await session.send_custom_message("focus", "critique")
            return
        ids = visible_ids()
        idx = ids.index(c["id"]) if c["id"] in ids else -1
        nxt = ids[idx + 1] if 0 <= idx < len(ids) - 1 else c["id"]
        STORE.save_review(rnd(), c["id"], verdict=verdict, failure_mode=mode if verdict == "Fail" else "",
                          critique=critique)
        local.set(local() + 1)
        current.set(nxt)

    @reactive.effect
    @reactive.event(input.btn_pass)
    async def _pass():
        await save_verdict("Pass")

    @reactive.effect
    @reactive.event(input.btn_fail)
    async def _fail():
        await save_verdict("Fail")

    @reactive.effect
    def _keep_current_visible():
        ids = visible_ids()
        with reactive.isolate():
            if deeplinked():  # skip the first re-filter after a deep link; it would snap back to ids[0]
                deeplinked.set(False)
                return
            if ids and current() not in ids:
                current.set(ids[0])

    # ------------------------------------------------ simulator
    def selected_sim_version():
        selected = input.sim_version()
        return None if selected == "working" else SIM.registry.get(selected)

    def sim_fields() -> set[str]:
        version = selected_sim_version()
        if version is None:
            return {"customer_id", "message", "portal", "history"}
        if version.status == "legacy":
            return set()
        return set(SIM.adapter(version).input_schema(version)["properties"])

    def replay_sources(version):
        return {result.run_id: f"{result.run_id[:8]} · {result.state}"
                for result in SIM.store.list(version_id=version.id, limit=100)
                if any("recorded_response" in span.attrs for span in result.spans)}

    def show_saved_run(result, run_input):
        sim_loaded_input.set(run_input)
        sim_view.set(result)
        sim_samples_view.set([result])
        sim_compare_view.set(None)
        sim_step.set(default_sim_step(result))
        ui.update_select("sim_version", selected=result.version_id)
        ui.update_select("sim_case", selected=run_input.case_id if run_input.case else "")
        ui.update_select("sim_customer", selected=run_input.customer_id)
        ui.update_text_area("sim_message", value=run_input.message)

    @render.ui
    def workflow_spec():
        version = selected_sim_version()
        if version is None or version.implementation != "declarative":
            return ui.div("Select a declarative version in the Simulator to inspect its frozen spec.", class_="muted")
        return ui.div(ui.div(f"{version.name} · {version.id}", class_="muted"),
                      ui.pre(json.dumps(version.content["spec"], ensure_ascii=False, indent=2)))

    @render.ui
    def sim_version_status():
        settings_rev(), data_rev(), local()
        try:
            version = selected_sim_version()
            if version is None:
                ready, message = make_provider(SETTINGS.provider, SETTINGS.model).status()
                drift = []
            else:
                recorded = (version.status != "legacy" and SIM.adapter(version).capabilities(version).recorded_replay
                            and sim_replay_mode() == "recorded")
                ready, message = SIM.status(version.id, audit=input.sim_audit(), recorded=recorded)
                if recorded and not replay_sources(version):
                    ready, message = False, "No recorded model response is available for this version."
                drift = [] if version.status == "legacy" else SIM.drift(version)
            return ui.div(ui.HTML(chip("ready" if ready else "not ready", "ok" if ready else "bad")),
                          ui.span(message, class_="muted"),
                          ui.div("Changed since freeze: " + ", ".join(drift), class_="sim-warning") if drift else None)
        except (ValueError, KeyError, OSError) as exc:
            return ui.div(str(exc), class_="text-danger")

    @render.ui
    def sim_run_control():
        settings_rev(), data_rev(), local()
        try:
            version = selected_sim_version()
            if version is None:
                ready = make_provider(SETTINGS.provider, SETTINGS.model).status()[0]
            else:
                recorded = (version.status != "legacy" and SIM.adapter(version).capabilities(version).recorded_replay
                            and sim_replay_mode() == "recorded")
                ready = SIM.status(version.id, audit=input.sim_audit(), recorded=recorded)[0]
                if recorded and not replay_sources(version):
                    ready = False
        except (ValueError, KeyError, OSError):
            ready = False
        return ui.input_action_button("sim_run", "Run the workflow", icon=icon("play"),
                                      class_="btn-primary w-100", disabled=not ready)

    @render.ui
    def sim_optional_inputs():
        fields = sim_fields()
        cid = input.sim_case()
        case = case_of(cid) if cid else None
        loaded = sim_loaded_input()
        matches = loaded and ((case and loaded.case_id == cid) or (not case and loaded.case_id == "custom"))
        portal = loaded.portal if matches else "email"
        history = loaded.history if matches else (case.get("history") or [] if case else [])
        return ui.div(
            ui.input_select("sim_portal", "Portal", {k: v["label"] for k, v in PORTALS.items()},
                            selected=portal, width="100%") if "portal" in fields else None,
            ui.input_text_area("sim_history", "Earlier turns (JSON)", rows=3, width="100%",
                               value=json.dumps(history, ensure_ascii=False)) if "history" in fields else None,
        )

    @render.ui
    def sim_replay_options():
        local()
        version = selected_sim_version()
        if version is None or version.status == "legacy":
            return ui.div()
        try:
            if not SIM.adapter(version).capabilities(version).recorded_replay:
                return ui.div()
        except (ValueError, OSError):
            return ui.div()
        choices = replay_sources(version)
        selected = sim_view().run_id if sim_view() and sim_view().run_id in choices else None
        return ui.div(ui.input_select("sim_mode", "Replay mode", {"fresh": "Fresh", "recorded": "Recorded"},
                                      selected=sim_replay_mode()),
                      ui.input_select("sim_replay_source", "Recorded run", choices, selected=selected, width="100%") if choices else
                      ui.div("Run this version once to make a recording available.", class_="muted"))

    @reactive.effect
    @reactive.event(input.sim_mode)
    def _sim_mode():
        sim_replay_mode.set(input.sim_mode())

    @render.ui
    def sim_history_controls():
        local()
        version = selected_sim_version()
        runs = SIM.store.list(version_id=version.id if version else None, limit=30)
        choices = {}
        for result in runs:
            _, run_input = SIM.store.get(result.run_id)
            choices[result.run_id] = f"{run_input.case_id} · {result.state} · {result.version_id} · {result.run_id[:8]}"
        if not choices:
            return ui.div("No saved simulator runs yet.", class_="muted mt-2")
        return ui.div(ui.input_select("sim_history_pick", "Run history", choices, width="100%"),
                      ui.input_action_button("sim_load", "Open saved run", class_="btn-outline-secondary btn-sm"))

    @reactive.effect
    @reactive.event(input.sim_case)
    def _sim_case():
        cid = input.sim_case()
        if cid:
            c = case_of(cid)
            loaded = sim_loaded_input()
            if loaded and loaded.case_id == cid:
                ui.update_select("sim_customer", selected=loaded.customer_id)
                ui.update_text_area("sim_message", value=loaded.message)
            else:
                sim_loaded_input.set(None)
                ui.update_select("sim_customer", selected=c["customer_id"])
                ui.update_text_area("sim_message", value=c["message"])

    @reactive.effect
    @reactive.event(input.sim_run)
    async def _sim_run():
        msg = (input.sim_message() or "").strip()
        if not msg:
            ui.notification_show("Write a message first.", type="warning")
            return
        fields = sim_fields()
        try:
            history = json.loads(input.sim_history() or "[]") if "history" in fields else []
            portal = input.sim_portal() if "portal" in fields else "email"
            version = selected_sim_version() or SIM.freeze_working()
            comparison_id = input.sim_compare_version()
            comparison = (SIM.freeze_working() if comparison_id == "working" else
                          SIM.registry.get(comparison_id) if comparison_id else None)
            caps = SIM.adapter(version).capabilities(version)
            mode = (sim_replay_mode() if input.sim_version() != "working" and caps.recorded_replay else "fresh")
            if mode == "recorded" and not replay_sources(version):
                raise ValueError("No recorded model response is available for this version.")
            replay_of = input.sim_replay_source() if mode == "recorded" else None
            if mode == "recorded" and not replay_of:
                raise ValueError("Choose a recorded run first.")
            count = int(input.sim_samples() or 1)
            if replay_of and count != 1:
                raise ValueError("Recorded replay uses one sample.")
            ready, status = SIM.status(version.id, audit=input.sim_audit(), recorded=bool(replay_of))
            if not ready:
                raise ValueError(status)
            if comparison:
                ready, status = SIM.status(comparison.id, audit=input.sim_audit())
                if not ready:
                    raise ValueError(f"Comparison version: {status}")
        except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
            ui.notification_show(str(exc), type="error", duration=8)
            return
        cid = input.sim_case()
        case = case_of(cid) if cid else None
        same = bool(case and case["message"] == msg and case["customer_id"] == input.sim_customer()
                    and (case.get("history") or []) == history)
        run_input = RunInput(customer_id=input.sim_customer(), message=msg, portal=portal,
                             case_id=cid if same else "custom", history=history,
                             case=copy.deepcopy(case) if same else None)
        audit = input.sim_audit()
        if input.sim_version() == "working":
            working_review_version.set(version.id)
        refresh_versions()
        ui.notification_show("Running the workflow…", id="sim", duration=None)
        try:
            if replay_of:
                results = [await asyncio.to_thread(SIM.run, version.id, run_input, audit=audit, replay_of=replay_of)]
            else:
                results = await asyncio.to_thread(SIM.run_samples, version.id, run_input, count, audit=audit)
            result = results[0]
            sim_view.set(result)
            sim_samples_view.set(results)
            sim_compare_view.set(None)
            sim_step.set(default_sim_step(result))
            if same:
                STORE.save_run(version.id, cid, review_record(result))
                if input.sim_version() != "working":
                    ui.update_select("review_version", selected=version.id)
                local.set(local() + 1)
            if result.state == "failed":
                ui.notification_show(review_record(result).get("error") or "Run failed.", type="error", duration=8)
            if comparison:
                other_results = await asyncio.to_thread(SIM.run_samples, comparison.id, run_input, count, audit=audit)
                other = other_results[0]
                sim_compare_view.set(other)
                if same:
                    STORE.save_run(comparison.id, cid, review_record(other))
                    local.set(local() + 1)
                if other.state == "failed":
                    ui.notification_show(review_record(other).get("error") or "Comparison run failed.",
                                         type="error", duration=8)
        except (ValueError, KeyError, OSError) as exc:
            ui.notification_show(str(exc), type="error", duration=8)
        finally:
            ui.notification_remove("sim")
            local.set(local() + 1)

    @reactive.effect
    @reactive.event(input.sim_load)
    def _sim_load():
        try:
            result, run_input = SIM.store.get(input.sim_history_pick())
            show_saved_run(result, run_input)
        except (ValueError, KeyError, OSError) as exc:
            ui.notification_show(str(exc), type="error", duration=8)

    @reactive.effect
    @reactive.event(input.sim_step_click)
    def _sim_click():
        sim_step.set(input.sim_step_click())

    @reactive.effect
    @reactive.event(input.sim_compare_step_click)
    def _sim_compare_click():
        sim_compare_step.set(input.sim_compare_step_click())

    @render.ui
    def sim_version_banner():
        data_rev(), settings_rev()
        result = sim_view()
        if not result:
            return ui.div()
        version = SIM.registry.get(result.version_id)
        drift = SIM.drift(version)
        return ui.card(ui.card_header(f"{version.name} · {version.implementation} · {version.status} · {version.id}"),
                       ui.div(f"Code, model, prompts, guards and {len(version.pins.get('lab_files', {}))} lab files pinned."),
                       ui.div("Changed since freeze: " + ", ".join(drift), class_="sim-warning") if drift else
                       ui.div("Pinned files are current.", class_="muted"),
                       ui.div("This run was made as an audit.", class_="muted") if result.audit else None)

    @render.ui
    def sim_pipe():
        result = sim_view()
        if not result:
            return ui.div("Pick a version and a case or write an email, then run the workflow.", class_="muted")
        version = SIM.registry.get(result.version_id)
        return ui.HTML(render_result(result, SIM.adapter(version).topology(version), version.implementation, sim_step()))

    @render.ui
    def sim_step_detail():
        result = sim_view()
        if not result:
            return ui.div()
        version = SIM.registry.get(result.version_id)
        return ui.HTML(render_detail(result, sim_step(), SIM.adapter(version).capabilities(version)))

    @render.ui
    def sim_human():
        result = sim_view()
        if not result or result.state != "waiting_for_human":
            return ui.div()
        version = SIM.registry.get(result.version_id)
        if version.status == "retired":
            return ui.card(ui.card_header("Run held for review"),
                           ui.div("This version was retired; the held run is read-only."))
        draft = (result.output or {}).get("reply") or ""
        return ui.card(
            ui.card_header("You are the human agent · this reply was held for review"),
            ui.HTML('<div class="chips">' + "".join(chip(r, "warn") for r in (result.output or {}).get("reasons", [])) + "</div>"),
            ui.input_text_area("human_reply", "Reply to send", value=draft, rows=8, width="100%"),
            ui.div(ui.input_action_button("h_approve", "Send the draft as is", class_="btn-pass"),
                   ui.input_action_button("h_edit", "Send my edited reply", class_="btn-primary ms-2"),
                   ui.input_action_button("h_hold", "Don't send", class_="btn-fail ms-2")),
        )

    async def resume(action: str):
        result = sim_view()
        try:
            resumed = await asyncio.to_thread(SIM.resume, result.run_id,
                                               {"action": action, "reply": input.human_reply() if action == "edit" else None})
            _, run_input = SIM.store.get(result.run_id)
            if run_input.case:
                STORE.save_run(resumed.version_id, run_input.case_id, review_record(resumed))
                local.set(local() + 1)
            sim_view.set(resumed)
            sim_samples_view.set([resumed if item.run_id == resumed.run_id else item for item in sim_samples_view()])
            sim_step.set(default_sim_step(resumed) if resumed.state == "failed" else "step-8")
            if resumed.state == "failed":
                ui.notification_show(review_record(resumed).get("error") or "Resume failed.", type="error", duration=8)
        except (ValueError, KeyError, OSError) as exc:
            ui.notification_show(str(exc), type="error", duration=8)

    @reactive.effect
    @reactive.event(input.h_approve)
    async def _ha():
        await resume("approve")

    @reactive.effect
    @reactive.event(input.h_edit)
    async def _he():
        await resume("edit")

    @reactive.effect
    @reactive.event(input.h_hold)
    async def _hh():
        await resume("hold")

    @render.ui
    def sim_outcome():
        result = sim_view()
        if not result:
            return ui.div()
        output = result.output or {}
        label = {"sent": "Sent automatically", "sent_after_review": "Sent after human review",
                 "held": "Held: nothing was sent"}.get(output.get("outcome"), result.state.replace("_", " "))
        final = output.get("final_reply")
        spread = sample_spread(sim_samples_view())
        summary = (f"{spread['passed']}/{spread['graded']} graded samples passed · "
                   f"95% interval {spread['interval'][0]:.0%}–{spread['interval'][1]:.0%}"
                   if spread["interval"] else f"{spread['graded']}/{spread['total']} samples graded")
        return ui.card(ui.card_header(f"Outcome · {label}"),
                       ui.div(review_record(result).get("error"), class_="text-danger") if result.state == "failed" else None,
                       ui.HTML(f'<div class="reply">{html.escape(final)}</div>' if final else '<div class="muted">—</div>'),
                       ui.pre(json.dumps(result.grade, ensure_ascii=False, indent=2)) if result.grade else
                       ui.div("Grade is available after the run completes.", class_="muted"),
                       ui.div(summary, class_="muted"),
                       ui.div(f"Latency: {result.usage.get('latency_s')} s · Cost: {result.usage.get('cost_usd')}",
                              class_="muted"))

    @render.ui
    def sim_comparison():
        left, right = sim_view(), sim_compare_view()
        if not left or not right:
            return ui.div()
        a, b = SIM.registry.get(left.version_id), SIM.registry.get(right.version_id)
        left_view = render_result(left, SIM.adapter(a).topology(a), a.implementation, sim_step())
        right_view = render_result(right, SIM.adapter(b).topology(b), b.implementation, sim_compare_step(),
                                   target="sim_compare_step_click")
        right_detail = render_detail(right, sim_compare_step(), SIM.adapter(b).capabilities(b),
                                     target="sim_compare_step_click")
        return ui.card(ui.card_header("Version comparison"),
                       ui.HTML(render_comparison(left, right, a, b)),
                       ui.HTML(f'<div class="sim-comparison-views"><section><h4>{html.escape(a.name)}</h4>{left_view}</section>'
                               f'<section><h4>{html.escape(b.name)}</h4>{right_view}{right_detail}</section></div>'))

    # ------------------------------------------------ cases
    @render.data_frame
    def cases_grid():
        data_rev()
        df = pd.DataFrame([{"id": c["id"], "intent": c["expected_intent"], "human?": "yes" if c["needs_human"] else "no",
                            "ground truth": c["ground_truth"], "rule": c["rule"], "customer": c["customer_id"],
                            "message": c["message"][:90], "turns": len(c.get("history") or []) + 1,
                            "pair": f'{c["pair_id"]} {c["twin"]}'.strip() if c.get("pair_id") else "",
                            "must include": " | ".join(c["must_include"]),
                            "must not say": " | ".join(c["must_not"]),
                            "tags": ", ".join(c["tags"]), "expert check": c["expert_check"]} for c in LAB.cases])
        return render.DataGrid(df, selection_mode="row", filters=True, height="auto", width="100%")

    @reactive.calc
    def edit_case():
        sel = cases_grid.data_view(selected=True)
        return case_of(sel.iloc[0]["id"]) if len(sel) else None

    @reactive.effect
    @reactive.event(input.new_case)
    def _new_case():
        n = max((int(c["id"][1:]) for c in LAB.cases if c["id"][1:].isdigit()), default=0) + 1
        cid = f"c{n:02d}"
        LAB.cases.append({"id": cid, "customer_id": "AC1001", "message": "", "expected_intent": "other",
                          "needs_human": False, "rule": "", "must_include": [], "must_not": [], "kb": "",
                          "tags": [], "language": "", "tone": "", "difficulty": "", "kaggle": "",
                          "rationale": "", "expert_check": "", "expert_note": "", "ground_truth": ""})
        data_rev.set(data_rev() + 1)
        ui.notification_show(f"{cid} added below. Click its row to edit, then 'Save to Excel' to keep it.")

    @render.ui
    def case_editor():
        c = edit_case()
        if not c:
            return ui.div("Select a row to edit that case.", class_="muted")
        return ui.card(
            ui.card_header(f"Edit {c['id']}"),
            ui.layout_columns(
                ui.div(ui.input_text_area("ed_message", "Message", c["message"], rows=5, width="100%"),
                       ui.div(f"Why: {c['rationale']}", class_="muted")),
                ui.div(ui.input_select("ed_intent", "Expected intent", INTENTS, selected=c["expected_intent"]),
                       ui.input_switch("ed_human", "Should go to a human", c["needs_human"]),
                       ui.input_text("ed_rule", "Escalation rule", c["rule"]),
                       ui.input_select("ed_gt", "Ground truth", ["", "straightforward", "ambiguous",
                                                                "escalation", "unsafe-to-automate"],
                                       selected=c["ground_truth"]),
                       ui.input_select("ed_check", "Expert check", ["", "Agree", "Change label",
                                                                   "Change must_include/must_not", "Rewrite message", "Drop case"],
                                       selected=c["expert_check"])),
                ui.div(ui.input_text("ed_inc", "Must include ( | between)", " | ".join(c["must_include"]), width="100%"),
                       ui.input_text("ed_not", "Must not say ( | between)", " | ".join(c["must_not"]), width="100%"),
                       ui.input_text("ed_tags", "Tags (comma between)", ", ".join(c["tags"]), width="100%"),
                       ui.input_text_area("ed_note", "Expert note", c["expert_note"], rows=2, width="100%")),
                col_widths=(5, 3, 4)),
            ui.input_action_button("ed_save", "Save case", class_="btn-primary"),
        )

    @reactive.effect
    @reactive.event(input.ed_save)
    def _ed_save():
        c = edit_case()
        if not c:
            return
        c.update(message=input.ed_message(), expected_intent=input.ed_intent(), needs_human=input.ed_human(),
                 rule=input.ed_rule(), expert_check=input.ed_check(), expert_note=input.ed_note(),
                 ground_truth=input.ed_gt(),
                 must_include=[t.strip() for t in input.ed_inc().split("|") if t.strip()],
                 must_not=[t.strip() for t in input.ed_not().split("|") if t.strip()],
                 tags=[t.strip() for t in input.ed_tags().split(",") if t.strip()])
        data_rev.set(data_rev() + 1)
        ui.notification_show(f"{c['id']} updated. 'Save to Excel' writes it to the workbook.")

    # ------------------------------------------------ knowledge
    @reactive.effect
    @reactive.event(input.meaning_rule)
    def _meaning_rule_changed():
        selected_rule = input.meaning_rule()
        if not selected_rule:
            ui.update_select(
                "meaning_affected_concept",
                choices={"": "No Business concepts linked to this rule"},
                selected="",
            )
            return
        affected = {
            name: name for name, info in ontology_terms().items()
            if int(selected_rule) in info["policy_rules"]
        }
        if not affected:
            ui.update_select(
                "meaning_affected_concept",
                choices={"": "No Business concepts linked to this rule"},
                selected="",
            )
            ui.update_selectize("meaning_concept", selected="")
            return
        current_concept = input.meaning_concept()
        selected_concept = current_concept if current_concept in affected else next(iter(affected), "")
        ui.update_select("meaning_affected_concept", choices=affected, selected=selected_concept)
        if selected_concept and selected_concept != current_concept:
            ui.update_selectize("meaning_concept", selected=selected_concept)

    @reactive.effect
    @reactive.event(input.meaning_concept)
    def _meaning_concept_changed():
        selected_concept = input.meaning_concept()
        concept = define(selected_concept) if selected_concept else None
        if not concept:
            return
        concept_name = concept["term"]
        rule_numbers = concept["policy_rules"]
        current_rule = input.meaning_rule()
        rule = current_rule if current_rule and int(current_rule) in rule_numbers else (
            str(rule_numbers[0]) if rule_numbers else ""
        )
        if rule != current_rule:
            ui.update_select("meaning_rule", selected=rule)
        if not rule:
            ui.update_select(
                "meaning_affected_concept",
                choices={"": "No Business concepts linked to this rule"},
                selected="",
            )
            return
        affected = {
            name: name for name, info in ontology_terms().items()
            if int(rule) in info["policy_rules"]
        }
        ui.update_select("meaning_affected_concept", choices=affected, selected=concept_name)

    @reactive.effect
    @reactive.event(input.meaning_affected_concept)
    def _meaning_affected_concept_changed():
        selected_concept = input.meaning_affected_concept()
        if selected_concept and selected_concept != input.meaning_concept():
            ui.update_selectize("meaning_concept", selected=selected_concept)

    @render.ui
    def meaning_concept_card():
        selected = input.meaning_concept()
        concept = define(selected) if selected else None
        if not concept:
            return ui.div("Select a concept to inspect its meaning and sources.", class_="muted")

        facts = concept_provenance(concept["term"]) or []
        articles = lab_kb_by_id()
        terms_by_id = {info["iri"].rsplit("#", 1)[-1]: name for name, info in ontology_terms().items()}
        config = load_business_rules()
        parameters = []
        for section in ("concession_limit", "offers"):
            entries = config.get(section, {})
            candidates = [entries] if section == "concession_limit" else entries.values()
            for entry in candidates:
                if entry.get("concept") == concept["term"]:
                    parameters.extend(
                        f"{key.replace('_', ' ')}: {value}"
                        for key, value in entry.items()
                        if key not in ("concept", "policy_rules", "kb_article", "cooldown_field",
                                       "customer_ledger_field")
                    )

        def fact_rows(property_name):
            rows = []
            labels = {
                "subClassOf": "Is a",
                "altLabel": "Also known as",
                "countsTowardLimit": "Counts toward concession limit",
                "oncePerMonths": "Offer cadence (months)",
                "scopeNote": "Business note",
                "requiresRole": "Required role",
                "documentedIn": "Help article",
                "ownedBy": "Business owner",
            }
            for fact in facts:
                if fact["property"] != property_name:
                    continue
                value = fact["value"]
                if property_name == "documentedIn":
                    article = articles.get(value, {})
                    value = f"{value} · {article.get('title', '')}"
                if property_name == "subClassOf":
                    value = terms_by_id.get(value, value)
                if property_name == "requiresRole":
                    value = terms_by_id.get(value, value)
                if property_name == "ownedBy":
                    value = concept.get("owner_team") or value
                origin = fact["origin"]
                if fact["inherited_from"]:
                    origin += f" from {fact['inherited_from']}"
                rows.append(
                    f"<li>{html.escape(labels.get(property_name, property_name))}: "
                    f"<strong>{html.escape(value)}</strong> "
                    f"<span class='muted'>({html.escape(origin)}; ontology.ttl)</span></li>"
                )
            return "".join(rows)

        rules = [fact for fact in facts if fact["property"] == "enforcesRule"]
        rule_rows = "".join(
            f"<li>Rule {html.escape(fact['value'].removeprefix('PolicyRule'))} "
            f"<span class='muted'>({html.escape(fact['origin'])}" +
            (f" from {html.escape(fact['inherited_from'])}" if fact["inherited_from"] else "") +
            "; policy.md)</span></li>"
            for fact in rules
        ) or "<li class='muted'>No linked policy rules</li>"
        definition = html.escape(concept["definition"] or "No definition recorded")
        parameter_rows = "".join(
            f"<li>{html.escape(item)} <span class='muted'>(business_rules.json)</span></li>"
            for item in parameters
        )
        if not parameter_rows:
            parameter_rows = "<li class='muted'>No linked parameters</li>"
        return ui.HTML(
            f"<section class='mt-3'><h4>{html.escape(concept['term'])}</h4>"
            f"<p>{definition} <span class='muted'>(ontology.ttl)</span></p>"
            "<p class='muted'>Semantic source: fde-first-principles/data/acme</p>"
            f"<div class='row'><div class='col-md-6'><h5>Hierarchy and business facts</h5><ul>"
            f"{fact_rows('subClassOf')}{fact_rows('altLabel')}"
            f"{fact_rows('countsTowardLimit')}{fact_rows('oncePerMonths')}"
            f"{fact_rows('scopeNote')}{fact_rows('requiresRole')}"
            f"</ul><h5>Business-rule parameters</h5><ul>{parameter_rows}</ul></div>"
            f"<div class='col-md-6'><h5>Policy rules</h5><ul>{rule_rows}</ul>"
            f"<h5>Evidence</h5><ul>{fact_rows('documentedIn')}"
            f"<li><span class='muted'>Article text: kb.md</span></li></ul>"
            f"<h5>Owner</h5><ul>{fact_rows('ownedBy')}</ul></div></div></section>"
        )

    @render.ui
    def meaning_rule_detail():
        selected = input.meaning_rule()
        if not selected:
            return ui.div()
        number = int(selected)
        text = policy_rules().get(number)
        if text is None:
            return ui.div("Policy text is missing for this rule.", class_="text-warning")
        affected = []
        for name, info in ontology_terms().items():
            if number not in info["policy_rules"]:
                continue
            facts = concept_provenance(name) or []
            edge = next((fact for fact in facts
                         if fact["property"] == "enforcesRule" and fact["value"] == f"PolicyRule{number}"), {})
            suffix = f" ({edge['origin']})" if edge else ""
            affected.append(f"<li>{html.escape(name)}{html.escape(suffix)}</li>")
        affected_rows = "".join(affected) or "<li class='muted'>No Business concepts linked to this rule</li>"
        return ui.HTML(
            f"<section class='mt-4'><h5>Rule {number}</h5><p>{html.escape(text)}</p>"
            f"<h6>Concepts affected</h6><ul>{affected_rows}</ul></section>"
        )

    @render.data_frame
    def meaning_checks():
        health = validate_ontology_ops()
        rows = ([{"type": "Operational", "finding": finding} for finding in health["drift_errors"]]
                + [{"type": "Semantic", "finding": finding} for finding in health["semantic_findings"]])
        if not rows:
            rows = [{"type": "Status", "finding": "No cross-file findings"}]
        return render.DataGrid(pd.DataFrame(rows), height="auto", width="100%")

    CUST_COLS = ["id", "name", "area", "plan", "status", "tenure_months", "balance_due", "complaints_30d",
                 "credits_30d", "late_fee_waived_on", "retention_offer_used_on", "payments_this_cycle"]

    @render.data_frame
    def customers_grid():
        rows = [{k: ", ".join(map(str, c.get(k) or [])) if k == "payments_this_cycle" else c.get(k) for k in CUST_COLS}
                for c in LAB.customers.values()]
        return render.DataGrid(pd.DataFrame(rows), editable=True, height="auto", width="100%")

    @customers_grid.set_patch_fn
    def _(*, patch):
        cust = list(LAB.customers.values())[patch["row_index"]]
        key = CUST_COLS[patch["column_index"]]
        if key == "id":
            return cust["id"]
        value = patch["value"]
        if key in ("tenure_months", "balance_due", "complaints_30d", "credits_30d"):
            value = int(float(value or 0))
        if key in ("late_fee_waived_on", "retention_offer_used_on"):
            value = str(value or "").strip()[:10] or None
        if key == "payments_this_cycle":
            cust[key] = [int(p) for p in str(value or "").replace(",", " ").split() if p.isdigit()]
            data_rev.set(data_rev() + 1)
            return ", ".join(map(str, cust[key]))
        cust[key] = value
        data_rev.set(data_rev() + 1)
        return value

    OUT_COLS = ["ticket", "area", "since", "cause", "status"]

    @render.data_frame
    def outages_grid():
        data_rev()
        return render.DataGrid(pd.DataFrame(LAB.outages, columns=OUT_COLS), editable=True, selection_mode="row",
                               height="auto", width="100%")

    @outages_grid.set_patch_fn
    def _(*, patch):
        LAB.outages[patch["row_index"]][OUT_COLS[patch["column_index"]]] = patch["value"]
        data_rev.set(data_rev() + 1)
        return patch["value"]

    @reactive.effect
    @reactive.event(input.add_outage)
    def _add_outage():
        area = input.new_out_area()
        LAB.outages = [o for o in LAB.outages if o["area"] != area]
        LAB.outages.append({"ticket": f"OUT-{area[:4].upper().replace(' ', '')}-{len(LAB.outages) + 1:04d}", "area": area,
                            "since": "today", "cause": input.new_out_cause(),
                            "status": "Engineers are on site. Updates are sent by email and in the Acme app."})
        data_rev.set(data_rev() + 1)

    @reactive.effect
    @reactive.event(input.remove_outage)
    def _remove_outage():
        sel = outages_grid.data_view(selected=True)
        if len(sel):
            LAB.outages = [o for o in LAB.outages if o["ticket"] != sel.iloc[0]["ticket"]]
            data_rev.set(data_rev() + 1)

    @reactive.effect
    def _kb_load():
        a = LAB.kb[input.kb_pick()]
        ui.update_text("kb_title", value=a["title"])
        ui.update_text_area("kb_text", value=a["text"])

    @reactive.effect
    @reactive.event(input.kb_save)
    def _kb_save():
        LAB.kb[input.kb_pick()].update(title=input.kb_title(), text=input.kb_text())
        data_rev.set(data_rev() + 1)
        ui.notification_show(f"{input.kb_pick()} saved. The next run uses it.")

    GUARD_COLS = ["name", "enabled", "pattern"]

    @render.data_frame
    def guards_grid():
        return render.DataGrid(pd.DataFrame([{"name": g["name"], "enabled": "yes" if g["enabled"] else "no",
                                              "pattern": g["pattern"]} for g in SETTINGS.workflow.guards]),
                               editable=True, height="auto", width="100%")

    @guards_grid.set_patch_fn
    def _(*, patch):
        g = SETTINGS.workflow.guards[patch["row_index"]]
        key, value = GUARD_COLS[patch["column_index"]], patch["value"]
        if key == "enabled":
            g["enabled"] = str(value).strip().lower() in ("yes", "y", "true", "1", "on")
            value = "yes" if g["enabled"] else "no"
        else:
            g[key] = value
        SETTINGS.save()
        settings_rev.set(settings_rev() + 1)
        return value

    @reactive.effect
    @reactive.event(input.block_high, ignore_init=True)
    def _block():
        SETTINGS.workflow.block_on_high_flags = input.block_high()
        SETTINGS.save()
        settings_rev.set(settings_rev() + 1)

    @render.ui
    def guard_try_result():
        msg = input.guard_try()
        if not msg:
            return ui.div()
        hits = guard_hits(msg, SETTINGS.workflow.guards)
        return ui.HTML("".join(chip(h, "warn") for h in hits) or chip("no guard fires", "ok"))

    # ------------------------------------------------ scoreboard
    @reactive.calc
    def scored():
        data_rev()
        data = round_data()
        rows = []
        for c in LAB.cases:
            rec = data.get(c["id"], {})
            ev = eval_checks(c, rec)
            rows.append({"id": c["id"], "intent": c["expected_intent"], "rule": c["rule"], "expected": c["needs_human"],
                         "routed": rec.get("decision"), "drafted": bool(rec.get("reply") or rec.get("decision")),
                         "verdict": rec.get("verdict"), "mode": rec.get("failure_mode"), "routing_ok": ev["routing_ok"]})
        return pd.DataFrame(rows)

    @render.ui
    def score_boxes():
        df = scored()
        rev = df[df.verdict.notna() & (df.verdict != "")]
        routed = df[df.routed.notna()]
        missed = int(((routed.expected) & (routed.routed == "send")).sum())
        pass_rate = f"{(rev.verdict == 'Pass').mean():.0%}" if len(rev) else "—"
        routing = f"{routed.routing_ok.mean():.0%}" if len(routed) else "—"
        return ui.layout_columns(
            ui.value_box("Drafted", f"{int(df.drafted.sum())}/{len(df)}"),
            ui.value_box("Reviewed", f"{len(rev)}/{len(df)}"),
            ui.value_box("Pass rate", pass_rate),
            ui.value_box("Routing correct", routing),
            ui.value_box("Missed escalations", str(missed)),
            col_widths=(2, 2, 3, 3, 2))

    @render.plot
    def score_plot():
        df = scored()
        rev = df[df.verdict.notna() & (df.verdict != "")]
        fig, ax = plt.subplots(figsize=(7, 2.8))
        rates = [((rev[rev.intent == i].verdict == "Pass").mean() if len(rev[rev.intent == i]) else 0) for i in INTENTS]
        counts = [len(rev[rev.intent == i]) for i in INTENTS]
        bars = ax.bar(INTENTS, rates, color="#2E6DB4", width=0.6)
        for b, rate, n in zip(bars, rates, counts):
            ax.text(b.get_x() + b.get_width() / 2, rate + 0.03, f"{rate:.0%}\n{n} rev." if n else "—",
                    ha="center", fontsize=8, color="#1F3A5F")
        ax.set_ylim(0, 1.25)
        ax.set_yticks([0, .5, 1], ["0%", "50%", "100%"])
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.tick_params(colors="#5B6B80", labelsize=9)
        ax.grid(axis="y", color="#E3EAF3")
        ax.set_axisbelow(True)
        fig.tight_layout()
        return fig

    @render.ui
    def score_confusion():
        df = scored()
        d = df[df.routed.notna()]

        def n(expected, routed):
            return int(((d.expected == expected) & (d.routed == routed)).sum())
        return ui.HTML(f"""
        <table class="table table-sm" style="font-size:14px"><thead><tr><th></th><th>Routed to human</th><th>Sent</th></tr></thead>
        <tbody><tr><th>Should go to human</th><td>{chip(n(True, 'escalate'), 'ok')}</td><td>{chip(n(True, 'send'), 'bad')} missed</td></tr>
        <tr><th>Fine to send</th><td>{chip(n(False, 'escalate'), 'warn')} extra</td><td>{chip(n(False, 'send'), 'ok')}</td></tr></tbody></table>
        <div class="muted">Missed escalations cost most: the customer gets an unchecked reply.</div>""")

    @render.ui
    def score_modes():
        df = scored()
        counts = df[df.verdict == "Fail"]["mode"].value_counts()
        if counts.empty:
            return ui.div("No fails recorded yet.", class_="muted")
        return ui.HTML("".join(f'<div class="d-flex justify-content-between"><span>{html.escape(str(m))}</span><b>{v}</b></div>'
                               for m, v in counts.items()))

    @render.ui
    def score_rules():
        df = scored()
        d = df[df.routed.notna()]
        if d.empty:
            return ui.div("No runs yet.", class_="muted")
        rows = []
        for rule, g in d.groupby("rule"):
            ok = int(g.routing_ok.sum())
            rows.append(f'<tr><td>{html.escape(str(rule))}</td><td>{ok}/{len(g)}</td><td>{chip("✓", "ok") if ok == len(g) else chip("check", "bad")}</td></tr>')
        return ui.HTML('<table class="table table-sm" style="font-size:13px"><thead><tr><th>Rule</th><th>Routed right</th>'
                       f'<th></th></tr></thead><tbody>{"".join(rows)}</tbody></table>')

    @render.ui
    def score_rounds():
        store_rev(), local()
        rows = []
        for version_id in STORE.versions():
            data = STORE.version(version_id)
            rev = [v for v in data.values() if v.get("verdict")]
            rate = f"{sum(v['verdict'] == 'Pass' for v in rev) / len(rev):.0%}" if rev else "—"
            rows.append(f"<tr><td>{html.escape(version_id)}</td><td>{len(rev)} reviewed</td><td><b>{rate}</b></td></tr>")
        return ui.HTML(f'<table class="table table-sm" style="font-size:13px"><tbody>{"".join(rows)}</tbody></table>'
                       if rows else '<div class="muted">No reviews yet.</div>')

    @render.ui
    def score_regressions():
        store_rev(), local(), data_rev()
        current_id = rnd()
        baseline_id = input.score_compare()
        if baseline_id == "working":
            baseline_id = working_review_version()
        if not current_id or not baseline_id:
            return ui.div("Select two versions with saved runs to compare.", class_="muted")
        rows = compare_reviews(LAB.cases, STORE.version(current_id), STORE.version(baseline_id))
        if not rows:
            return ui.div("Neither version has saved evidence yet.", class_="muted")
        body = "".join(
            "<tr>" + "".join(f"<td>{html.escape(str(row[key]))}</td>" for key in
                              ("case_id", "change", "baseline", "current", "baseline_decision", "decision")) + "</tr>"
            for row in rows
        )
        return ui.HTML('<div class="table-responsive"><table class="table table-sm"><thead><tr>'
                       '<th>Case</th><th>Change</th><th>Baseline verdict</th><th>Selected verdict</th>'
                       '<th>Baseline routing</th><th>Selected routing</th></tr></thead>'
                       f'<tbody>{body}</tbody></table></div>')

    @reactive.effect
    @reactive.event(input.name_candidate)
    def _name_candidate():
        try:
            version_id = rnd()
            if not version_id:
                raise ValueError("Run the working copy first to create a snapshot.")
            version = SIM.registry.name(version_id, input.candidate_label())
            refresh_versions()
            settings_rev.set(settings_rev() + 1)
            ui.notification_show(f"Named {version.id} as {version.label}.")
        except (ValueError, KeyError, OSError) as exc:
            ui.notification_show(str(exc), type="error", duration=8)

    @reactive.effect
    @reactive.event(input.release_version)
    def _release_version():
        try:
            version_id = rnd()
            if not version_id:
                raise ValueError("Select a candidate version first.")
            version = SIM.registry.release(version_id, LAB.cases, input.release_signoff())
            refresh_versions()
            settings_rev.set(settings_rev() + 1)
            ui.notification_show(f"Released {version.name} · {version.id}.")
        except (ValueError, KeyError, OSError) as exc:
            ui.notification_show(str(exc), type="error", duration=8)

    @reactive.effect
    @reactive.event(input.retire_version)
    def _retire_version():
        try:
            version_id = rnd()
            if not version_id:
                raise ValueError("Select a candidate or released version first.")
            version = SIM.registry.retire(version_id)
            refresh_versions()
            settings_rev.set(settings_rev() + 1)
            ui.notification_show(f"Retired {version.name} · {version.id}; saved runs remain available.")
        except (ValueError, KeyError, OSError) as exc:
            ui.notification_show(str(exc), type="error", duration=8)

    # ------------------------------------------------ export
    @reactive.effect
    @reactive.event(input.export)
    def _export():
        try:
            path = export_to_excel(LAB, STORE.all(), XLSX)
            ui.notification_show(f"Saved to {path.name} (a backup of the previous file is next to it).", duration=6)
        except Exception as exc:  # noqa: BLE001
            ui.notification_show(f"Couldn't save: {exc}", type="error", duration=8)


app = App(app_ui, server)
