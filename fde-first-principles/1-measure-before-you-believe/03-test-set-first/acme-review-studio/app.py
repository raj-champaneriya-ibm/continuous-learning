"""Acme Review Studio: run the controlled draft workflow and review it as the domain expert.

    shiny run app.py --launch-browser
"""
from __future__ import annotations

import asyncio
import html
import os
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from langgraph.checkpoint.sqlite import SqliteSaver  # noqa: E402
from shiny import App, reactive, render, ui  # noqa: E402

from acme.checks import eval_checks, guard_hits  # noqa: E402
from acme.lab import INTENTS, export_to_excel, load_lab, read_review_log  # noqa: E402
from acme.providers import make_provider  # noqa: E402
from acme.store import AppSettings, ReviewStore  # noqa: E402
from acme.ui_bits import CSS, JS, chip, highlight, icon, pipeline  # noqa: E402
from acme.workflow import PORTALS, Deps, Workflow, to_record  # noqa: E402

ROOT = Path(__file__).parent
XLSX = Path(os.environ.get("ACME_XLSX", ROOT / "data" / "Acme_Fibre_Grounded_Draft_Eval.xlsx"))
RUNS = ROOT / "runs"
RUNS.mkdir(exist_ok=True)

LAB = load_lab(XLSX)
STORE = ReviewStore(RUNS / "reviews.json")
if not STORE.all():
    STORE.import_rows(read_review_log(XLSX))
SETTINGS = AppSettings(RUNS / "settings.json")
DEPS = Deps(lab=LAB, provider=make_provider(SETTINGS.provider, SETTINGS.model), settings=SETTINGS.workflow,
            log_path=RUNS / "runs.jsonl")
WF = Workflow(DEPS, SqliteSaver(sqlite3.connect(RUNS / "checkpoints.sqlite", check_same_thread=False)))
BATCH = {"running": False, "done": 0, "total": 0, "errors": 0}
CASE_IDS = [c["id"] for c in LAB.cases]


def run_case(case: dict, rnd: int, portal: str = "email") -> dict:
    view = WF.start(customer_id=case["customer_id"], message=case["message"], portal=portal, case_id=case["id"])
    rec = to_record(view)
    STORE.save_run(rnd, case["id"], rec)
    return view


def suggest_mode(case: dict, rec: dict) -> str:
    ev = eval_checks(case, rec)
    flags = {f["check"] for f in rec.get("flags", [])}
    if ev["routing_ok"] is False and case["needs_human"]:
        return "Missed escalation"                      # the costliest failure comes first
    for flag, mode in [("time promise", "Promised fix time"), ("financial promise", "Financial promise > ₹500"),
                       ("other customer's data", "Privacy leak"), ("asks for a secret", "Asked for a secret"),
                       ("unsupported ticket", "Unsupported claim"), ("unsupported amount", "Unsupported claim")]:
        if flag in flags:
            return mode
    if ev["banned"]:
        return "Unsupported claim"
    if ev["missing"]:
        return "Missing required fact"
    if ev["routing_ok"] is False:
        return "Unneeded escalation"
    if ev["intent_ok"] is False:
        return "Wrong intent"
    return ""


def customer_chips(cust: dict | None) -> str:
    if not cust:
        return chip("unknown customer", "bad")
    outage = LAB.outage_for(cust)
    parts = [chip(f"{cust['name']} · {cust['id']}"), chip(f"{cust['plan']} · {cust['area']}"),
             chip(f"{cust['tenure_months']} mo tenure"),
             chip(f"₹{cust['balance_due']} due", "warn" if cust["balance_due"] else "ok"),
             chip(f"{cust['complaints_30d']} complaints/30d", "bad" if cust["complaints_30d"] >= 2 else ""),
             chip(outage["ticket"] if outage else "no area outage", "warn" if outage else "")]
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
            ui.input_select("sim_case", "Start from a case", {"": "Write my own", **{
                c["id"]: f"{c['id']} · {c['message'][:46]}…" for c in LAB.cases}}, width="100%"),
            ui.input_select("sim_customer", "Customer", cust_choices, width="100%"),
            ui.input_select("sim_portal", "Portal", {k: v["label"] for k, v in PORTALS.items()}, width="100%"),
            ui.input_text_area("sim_message", "Message", rows=7, width="100%"),
            ui.input_action_button("sim_run", "Run the workflow", icon=icon("play"), class_="btn-primary w-100"),
            ui.div("Runs of a dataset case also become that case's draft on the Review page.", class_="muted mt-2"),
        ),
        ui.div(
            ui.card(ui.card_header("Workflow · click a step to see what it did"), ui.output_ui("sim_pipe"),
                    ui.output_ui("sim_step_detail")),
            ui.output_ui("sim_human"),
            ui.output_ui("sim_outcome"),
        ),
        col_widths=(4, 8),
    )


def cases_page():
    return ui.div(
        ui.div("Ground truth for each case. Select a row to change its label; changes save to Excel with "
               "'Save to Excel'.", class_="hint"),
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
            ui.nav_panel("Escalation guards",
                         ui.div("Code rules checked at step 7. They escalate whatever the model said.", class_="muted mb-2"),
                         ui.output_data_frame("guards_grid"),
                         ui.input_switch("block_high", "Escalate when a step-6 check finds a blocking problem",
                                         SETTINGS.workflow.block_on_high_flags),
                         ui.input_text_area("guard_try", "Try a message", rows=2, width="100%",
                                            placeholder="I'll take this to consumer court"),
                         ui.output_ui("guard_try_result")),
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
            ui.card(ui.card_header("By round"), ui.output_ui("score_rounds")),
            col_widths=(4, 5, 3),
        ),
    )


settings_popover = ui.popover(
    ui.input_action_link("open_settings", "Model", icon=icon("settings")),
    ui.input_radio_buttons("provider", "Drafting model", {"claude-code": "Claude Code", "offline": "Offline stand-in"},
                           selected=SETTINGS.provider),
    ui.input_select("model", "Claude model", {"sonnet": "Sonnet", "opus": "Opus", "haiku": "Haiku"}, selected=SETTINGS.model),
    ui.input_numeric("round", "Review round", SETTINGS.round, min=1, step=1),
    ui.input_slider("concurrency", "Parallel drafts", 1, 6, SETTINGS.concurrency),
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
    current = reactive.value(CASE_IDS[0])
    sim_view = reactive.value(None)
    sim_step = reactive.value("5")
    review_step = reactive.value(None)

    @reactive.poll(lambda: (len(STORE.all()), STORE.path.stat().st_mtime_ns if STORE.path.exists() else 0), 1)
    def store_rev():
        return STORE.path.stat().st_mtime_ns if STORE.path.exists() else 0

    @reactive.poll(lambda: (BATCH["running"], BATCH["done"]), 0.7)
    def batch_rev():
        return dict(BATCH)

    def rnd() -> int:
        settings_rev()
        return SETTINGS.round

    @reactive.calc
    def round_data() -> dict[str, dict]:
        store_rev(), local()
        return STORE.round(rnd())

    def case_of(cid):
        data_rev()
        return LAB.case(cid)

    # ------------------------------------------------ settings
    @reactive.effect
    @reactive.event(input.provider, input.model, input.round, input.concurrency, ignore_init=True)
    def _settings():
        SETTINGS.provider, SETTINGS.model = input.provider(), input.model()
        SETTINGS.round = int(input.round() or 1)
        SETTINGS.concurrency = int(input.concurrency())
        DEPS.provider = make_provider(SETTINGS.provider, SETTINGS.model)
        SETTINGS.save()
        settings_rev.set(settings_rev() + 1)

    @render.ui
    def provider_status():
        settings_rev()
        ok, msg = DEPS.provider.status()
        return ui.div(ui.HTML(chip("ready" if ok else "not ready", "ok" if ok else "bad")), ui.span(msg, class_="muted"))

    # ------------------------------------------------ review: list + navigation
    @reactive.calc
    def visible_ids() -> list[str]:
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
        ids = visible_ids() or CASE_IDS
        cid = current()
        idx = ids.index(cid) if cid in ids else -1
        current.set(ids[max(0, min(len(ids) - 1, idx + step))] if idx >= 0 else ids[0])

    @reactive.effect
    @reactive.event(input.pick_case)
    def _pick():
        current.set(input.pick_case())

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
            ui.notification_show("Pick a failure mode, write the critique, then Ctrl+Enter.", duration=3)
        elif key == "save":
            await save_verdict("Fail")

    @render.ui
    def progress():
        data = round_data()
        drafted = sum(1 for c in CASE_IDS if data.get(c, {}).get("decision"))
        reviewed = sum(1 for c in CASE_IDS if data.get(c, {}).get("verdict"))
        pct = int(100 * reviewed / len(CASE_IDS))
        return ui.div(
            ui.div(ui.strong(f"Round {rnd()}"), ui.span(f" · {reviewed}/{len(CASE_IDS)} reviewed · {drafted} drafted",
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
                      class_="muted mt-2")

    @reactive.effect
    @reactive.event(input.run_missing)
    def _run_missing():
        if BATCH["running"]:
            return
        r, data = rnd(), round_data()
        todo = [c for c in LAB.cases if not data.get(c["id"], {}).get("decision")]   # imported rows count as not run
        if not todo:
            ui.notification_show("Every case in this round has been run. Use Re-run on a case, or start a new round.")
            return
        ok, msg = DEPS.provider.status()
        if not ok:
            ui.notification_show(msg, type="error", duration=8)
            return
        BATCH.update(running=True, done=0, total=len(todo), errors=0)

        def worker():
            def one(case):
                try:
                    view = run_case(case, r)
                    if (view.get("llm") or {}).get("error"):
                        BATCH["errors"] += 1
                except Exception:  # noqa: BLE001
                    BATCH["errors"] += 1
                BATCH["done"] += 1
            with ThreadPoolExecutor(SETTINGS.concurrency) as pool:
                list(pool.map(one, todo))
            BATCH["running"] = False

        threading.Thread(target=worker, daemon=True).start()
        ui.notification_show(f"Drafting {len(todo)} cases with {DEPS.provider.label}. You can start reviewing now.")

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
        return ui.div(ui.HTML(customer_chips(LAB.customers.get(c["customer_id"]))),
                      ui.HTML(f'<div class="email mt-2">{html.escape(c["message"])}</div>'))

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
        return ui.HTML(f'Workflow run · <span style="font-weight:500">{label}</span>'
                       + (f' <span class="muted">· {html.escape(meta)}</span>' if meta else ""))

    @render.ui
    def run_card():
        c, rec = cur()
        buttons = ui.div(ui.input_action_button("run_one", "Re-run" if rec.get("decision") else "Draft this case",
                                                class_="btn-sm btn-primary"),
                         ui.input_action_button("to_sim", "Open in simulator", class_="btn-sm btn-outline-secondary ms-1"),
                         class_="mt-2")
        if not rec.get("trace"):
            note = ("Draft imported from the workbook; run it to see the workflow." if rec.get("reply")
                    else "No draft yet for this round.")
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
        r = rnd()
        ok, msg = DEPS.provider.status()
        if not ok:
            ui.notification_show(msg, type="error", duration=8)
            return
        ui.notification_show(f"Drafting {c['id']} with {DEPS.provider.label}…", id="drafting", duration=None)
        await asyncio.to_thread(run_case, c, r)
        ui.notification_remove("drafting")
        local.set(local() + 1)

    @reactive.effect
    @reactive.event(input.to_sim)
    def _to_sim():
        c, _ = cur()
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
        mode = rec.get("failure_mode") or ""
        if not rec.get("verdict") and (rec.get("reply") or rec.get("decision")):
            suggestion = suggest_mode(c, rec)
            if suggestion:
                modes[suggestion] = f"{suggestion} (suggested)"
                mode = suggestion
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
        if verdict == "Fail" and (not mode or not critique):
            ui.notification_show("For a Fail, pick a failure mode and write a short critique.", type="warning")
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
            if ids and current() not in ids:
                current.set(ids[0])

    # ------------------------------------------------ simulator
    @reactive.effect
    @reactive.event(input.sim_case)
    def _sim_case():
        cid = input.sim_case()
        if cid:
            c = case_of(cid)
            ui.update_select("sim_customer", selected=c["customer_id"])
            ui.update_text_area("sim_message", value=c["message"])

    @reactive.effect
    @reactive.event(input.sim_run)
    async def _sim_run():
        msg = (input.sim_message() or "").strip()
        if not msg:
            ui.notification_show("Write a message first.", type="warning")
            return
        ok, status = DEPS.provider.status()
        if not ok:
            ui.notification_show(status, type="error", duration=8)
            return
        cid = input.sim_case()
        case = case_of(cid) if cid else None
        same = case and case["message"] == msg and case["customer_id"] == input.sim_customer()
        r, portal, customer = rnd(), input.sim_portal(), input.sim_customer()
        ui.notification_show("Running the workflow…", id="sim", duration=None)
        view = await asyncio.to_thread(WF.start, customer_id=customer, message=msg, portal=portal,
                                       case_id=cid if same else "custom")
        ui.notification_remove("sim")
        if same:
            STORE.save_run(r, cid, to_record(view))
            local.set(local() + 1)
        sim_view.set({**view, "_case": cid if same else None, "_round": r})
        sim_step.set("H" if view.get("waiting_for_human") else "5")

    @reactive.effect
    @reactive.event(input.sim_step_click)
    def _sim_click():
        sim_step.set(input.sim_step_click())

    @render.ui
    def sim_pipe():
        v = sim_view()
        if not v:
            return ui.div(ui.HTML(pipeline([], False, None, "sim_step_click")),
                          ui.div("Pick a case or write an email, then run the workflow.", class_="muted"))
        return ui.HTML(pipeline(v.get("trace", []), v.get("waiting_for_human"), sim_step(), "sim_step_click"))

    @render.ui
    def sim_step_detail():
        v, s = sim_view(), sim_step()
        if not v:
            return ui.div()
        t = next((t for t in reversed(v.get("trace", [])) if t["step"] == s), None)
        waiting = s == "H" and v.get("waiting_for_human")
        what = (f"{html.escape(t['detail'])} · {t['ms']} ms" if t else
                "waiting for your decision below" if waiting else "did not run")
        head = f'<div class="mt-2"><b>Step {s}</b> · {what}</div>'
        body = ""
        if s == "4" and v.get("user_prompt"):
            body = f'<pre class="prompt">{html.escape(v["user_prompt"])}</pre>'
        elif s == "5":
            d = v.get("draft") or {}
            body = (f'<pre class="prompt">{html.escape(str(d) if d else "no draft")}</pre>'
                    f'<details><summary class="muted">System prompt sent to the model</summary>'
                    f'<pre class="prompt">{html.escape(v.get("system_prompt") or "")}</pre></details>')
        elif s == "6":
            body = "".join(f'<div>{chip(f["check"], "bad" if f["severity"] == "high" else "warn")} '
                           f'<span class="muted">{html.escape(f["detail"])}</span></div>' for f in v.get("flags", [])) \
                   or '<div class="muted">No problems found.</div>'
        elif s == "7":
            body = "".join(chip(r, "warn") for r in v.get("reasons", [])) or chip("safe to send", "ok")
        return ui.HTML(head + f'<div class="mt-2">{body}</div>')

    @render.ui
    def sim_human():
        v = sim_view()
        if not v or not v.get("waiting_for_human"):
            return ui.div()
        draft = (v.get("draft") or {}).get("reply") or ""
        return ui.card(
            ui.card_header("You are the human agent · this reply was held for review"),
            ui.HTML('<div class="chips">' + "".join(chip(r, "warn") for r in v.get("reasons", [])) + "</div>"),
            ui.input_text_area("human_reply", "Reply to send", value=draft, rows=8, width="100%"),
            ui.div(ui.input_action_button("h_approve", "Send the draft as is", class_="btn-pass"),
                   ui.input_action_button("h_edit", "Send my edited reply", class_="btn-primary ms-2"),
                   ui.input_action_button("h_hold", "Don't send", class_="btn-fail ms-2")),
        )

    async def resume(action: str):
        v = sim_view()
        view = await asyncio.to_thread(WF.resume, v["thread_id"], action,
                                       input.human_reply() if action == "edit" else None)
        if v.get("_case"):
            STORE.save_run(v["_round"], v["_case"], to_record(view))
            local.set(local() + 1)
        sim_view.set({**view, "_case": v.get("_case"), "_round": v.get("_round")})
        sim_step.set("8")

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
        v = sim_view()
        if not v or not v.get("outcome"):
            return ui.div()
        label = {"sent": "Sent automatically", "sent_after_review": "Sent after human review",
                 "held": "Held: nothing was sent"}[v["outcome"]]
        final = v.get("final_reply")
        return ui.card(ui.card_header(f"Outcome · {label}"),
                       ui.HTML(f'<div class="reply">{html.escape(final)}</div>' if final else '<div class="muted">—</div>'))

    # ------------------------------------------------ cases
    @render.data_frame
    def cases_grid():
        data_rev()
        df = pd.DataFrame([{"id": c["id"], "intent": c["expected_intent"], "human?": "yes" if c["needs_human"] else "no",
                            "rule": c["rule"], "customer": c["customer_id"], "message": c["message"][:90],
                            "tags": ", ".join(c["tags"]), "expert check": c["expert_check"]} for c in LAB.cases])
        return render.DataGrid(df, selection_mode="row", filters=True, height="360px", width="100%")

    @reactive.calc
    def edit_case():
        sel = cases_grid.data_view(selected=True)
        return case_of(sel.iloc[0]["id"]) if len(sel) else None

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
                 must_include=[t.strip() for t in input.ed_inc().split("|") if t.strip()],
                 must_not=[t.strip() for t in input.ed_not().split("|") if t.strip()],
                 tags=[t.strip() for t in input.ed_tags().split(",") if t.strip()])
        data_rev.set(data_rev() + 1)
        ui.notification_show(f"{c['id']} updated. 'Save to Excel' writes it to the workbook.")

    # ------------------------------------------------ knowledge
    CUST_COLS = ["id", "name", "area", "plan", "status", "tenure_months", "balance_due", "complaints_30d"]

    @render.data_frame
    def customers_grid():
        return render.DataGrid(pd.DataFrame([{k: c[k] for k in CUST_COLS} for c in LAB.customers.values()]),
                               editable=True, width="100%")

    @customers_grid.set_patch_fn
    def _(*, patch):
        cust = list(LAB.customers.values())[patch["row_index"]]
        key = CUST_COLS[patch["column_index"]]
        if key == "id":
            return cust["id"]
        value = patch["value"]
        if key in ("tenure_months", "balance_due", "complaints_30d"):
            value = int(float(value or 0))
        cust[key] = value
        return value

    OUT_COLS = ["ticket", "area", "since", "cause", "status"]

    @render.data_frame
    def outages_grid():
        data_rev()
        return render.DataGrid(pd.DataFrame(LAB.outages, columns=OUT_COLS), editable=True, selection_mode="row",
                               width="100%")

    @outages_grid.set_patch_fn
    def _(*, patch):
        LAB.outages[patch["row_index"]][OUT_COLS[patch["column_index"]]] = patch["value"]
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
        ui.notification_show(f"{input.kb_pick()} saved. The next run uses it.")

    GUARD_COLS = ["name", "enabled", "pattern"]

    @render.data_frame
    def guards_grid():
        return render.DataGrid(pd.DataFrame([{"name": g["name"], "enabled": "yes" if g["enabled"] else "no",
                                              "pattern": g["pattern"]} for g in SETTINGS.workflow.guards]),
                               editable=True, width="100%")

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
        return value

    @reactive.effect
    @reactive.event(input.block_high, ignore_init=True)
    def _block():
        SETTINGS.workflow.block_on_high_flags = input.block_high()
        SETTINGS.save()

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
            ui.value_box("Drafted", f"{int(df.drafted.sum())}/{len(df)}", max_height="105px"),
            ui.value_box("Reviewed", f"{len(rev)}/{len(df)}", max_height="105px"),
            ui.value_box("Pass rate", pass_rate, max_height="105px"),
            ui.value_box("Routing correct", routing, max_height="105px"),
            ui.value_box("Missed escalations", str(missed), max_height="105px"),
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
            rows.append(f'<tr><td>{rule}</td><td>{ok}/{len(g)}</td><td>{chip("✓", "ok") if ok == len(g) else chip("check", "bad")}</td></tr>')
        return ui.HTML('<table class="table table-sm" style="font-size:13px"><thead><tr><th>Rule</th><th>Routed right</th>'
                       f'<th></th></tr></thead><tbody>{"".join(rows)}</tbody></table>')

    @render.ui
    def score_rounds():
        store_rev(), local()
        rows = []
        for r in STORE.rounds():
            data = STORE.round(r)
            rev = [v for v in data.values() if v.get("verdict")]
            rate = f"{sum(v['verdict'] == 'Pass' for v in rev) / len(rev):.0%}" if rev else "—"
            rows.append(f"<tr><td>Round {r}</td><td>{len(rev)} reviewed</td><td><b>{rate}</b></td></tr>")
        return ui.HTML(f'<table class="table table-sm" style="font-size:13px"><tbody>{"".join(rows)}</tbody></table>'
                       if rows else '<div class="muted">No reviews yet.</div>')

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
