"""Styling and small HTML helpers for the Shiny app. Minimal blue, matching the eval workbook."""
from __future__ import annotations

import html
import re
from functools import lru_cache
from pathlib import Path

from shiny import ui

from .workflow import STEPS

@lru_cache(maxsize=None)
def icon(name: str):
    """Bundled Google Material icon, decorative beside a visible text label."""
    if name not in {"review", "play", "cases", "knowledge", "score", "settings", "save", "check", "close", "back", "next"}:
        raise ValueError(f"Unknown icon: {name}")
    svg = (Path(__file__).parent / "icons" / f"{name}.svg").read_text("utf-8")
    return ui.HTML(svg.replace('<svg ', '<svg class="material-icon" aria-hidden="true" focusable="false" ', 1)
                   .replace('fill="#000000"', 'fill="currentColor"'))


CSS = """
:root{--navy:#1F3A5F;--blue:#2E6DB4;--pale:#EEF5FC;--line:#D6E0EC;--muted:#5B6B80;--green:#2F7D5B;--red:#B4513C;--amber:#9A6412}
.material-icon{width:1.1em;height:1.1em;fill:currentColor;vertical-align:-.18em;flex:none}
.navbar>.container-fluid{padding-left:24px;padding-right:24px}
.navbar-brand{margin-right:24px}
#nav .nav-link{padding-left:16px!important;padding-right:16px!important}
#nav>li:has(>.action-button),#nav>li:has(>bslib-popover){padding-left:12px}
.nav-link .material-icon{width:18px;height:18px;margin-right:10px;opacity:.78}
.btn .material-icon,.action-link .material-icon{margin-right:6px;opacity:.85}
.btn{padding-left:14px;padding-right:14px}
.caseitem{width:100%;border:0;background:transparent;text-align:left;color:inherit;font-family:inherit}
.step{text-align:left;color:inherit;font-family:inherit}
.caseitem:focus-visible,.step:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
body{background:#F6F9FC;color:#1A2433}
.navbar{background:#fff!important;border-bottom:1px solid var(--line)}
.navbar-brand{color:var(--navy)!important;font-weight:700}
.nav-link.active{color:var(--blue)!important;font-weight:600}
.card{border:1px solid var(--line);box-shadow:none;border-radius:10px}
.card-header{background:#fff;color:var(--navy);font-weight:600;border-bottom:1px solid var(--line)}
.btn-primary{--bs-btn-bg:var(--blue);--bs-btn-border-color:var(--blue);--bs-btn-hover-bg:#245a95;--bs-btn-hover-border-color:#245a95}
.btn-outline-primary{--bs-btn-color:var(--blue);--bs-btn-border-color:var(--blue);--bs-btn-hover-bg:var(--blue);--bs-btn-hover-border-color:var(--blue)}
.muted{color:var(--muted);font-size:13px}
.hint{color:var(--muted);font-size:13px;margin:-4px 0 12px}
.chips{display:flex;flex-wrap:wrap;align-items:flex-start}
.chip{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12px;background:var(--pale);color:var(--navy);margin:0 4px 4px 0;border:1px solid #dbe6f3}
.chip.ok{background:#E7F4EE;color:var(--green);border-color:#cfe8dc}
.chip.bad{background:#FBEAE6;color:var(--red);border-color:#f3d2ca}
.chip.warn{background:#FDF3E1;color:var(--amber);border-color:#f3e0bd}
.chip.big{font-size:13px;padding:4px 12px;font-weight:600}
.email{white-space:pre-wrap;font-size:15px;line-height:1.55}
.reply{white-space:pre-wrap;font-size:15px;line-height:1.6;border-left:3px solid var(--blue);padding:4px 0 4px 14px}
mark.ok{background:#D9F0E4;color:inherit;border-radius:3px;padding:0 2px}
mark.bad{background:#F6D3CB;color:inherit;border-radius:3px;padding:0 2px;font-weight:600}
.caselist{max-height:58vh;overflow:auto;margin:0;padding:3px}
.caseitem{display:flex;gap:10px;padding:9px 12px;border-radius:6px;cursor:pointer;font-size:13px;line-height:1.3}
.caseitem:hover{background:#F0F5FB}.caseitem.active{background:var(--pale);outline:1px solid #c7d8ee}
.caseitem .id{font-weight:600;color:var(--navy);width:30px;flex:none}
.dot{width:9px;height:9px;border-radius:50%;margin-top:4px;flex:none;background:#CBD5E1}
.dot.drafted{background:var(--blue)}.dot.pass{background:var(--green)}.dot.fail{background:var(--red)}.dot.err{background:var(--amber)}
.pipe{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px 22px;margin:4px 0 8px}
.pipe.compact{gap:8px 16px}.pipe.compact .step{padding:8px 10px}.pipe.compact .step .d{display:none}
.step{position:relative;border:1px solid #c4cfdc;border-radius:8px;padding:10px 12px;background:#EDF1F6;font-size:12px;cursor:pointer;min-height:44px}
.step .k,.step .d{display:block}
.step b{color:#24324a;font-weight:600}.step .k{font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.step .d{font-size:11px;color:#41526a;margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.step.model{background:#DCEBFA;border-color:#6C9BD2}.step.model .k{color:var(--blue)}
.step.human{background:#FDF1E1;border-color:#E0A458}.step.human .k{color:var(--amber)}
.step.st-ok{box-shadow:inset 4px 0 0 var(--blue)}
.step.st-flag{box-shadow:inset 4px 0 0 #D69E2E}
.step.st-escalate,.step.st-waiting,.step.st-hold{box-shadow:inset 4px 0 0 #DD8A2E}
.step.st-approve,.step.st-edit{box-shadow:inset 4px 0 0 var(--green)}
.step.st-error,.step.st-stop{box-shadow:inset 4px 0 0 var(--red)}
.step.st-pending{opacity:.42}.step.st-skipped{opacity:.6;border-style:dashed}
.step.sel{outline:2px solid var(--navy)}
.step.a-r::after{content:"→";position:absolute;right:-18px;top:50%;transform:translateY(-50%);color:#8795a8}
.step.a-l::after{content:"←";position:absolute;left:-18px;top:50%;transform:translateY(-50%);color:#8795a8}
.step.a-d::before{content:"↓";position:absolute;bottom:-17px;left:50%;transform:translateX(-50%);color:#8795a8}
.pipe.compact .step.a-d::before{bottom:-13px}
.verdict .btn{min-width:110px;font-weight:600}
.btn-pass{background:#E7F4EE;color:var(--green);border:1px solid #b9dcc9}.btn-pass:hover{background:var(--green);color:#fff}
.btn-fail{background:#FBEAE6;color:var(--red);border:1px solid #efc5bb}.btn-fail:hover{background:var(--red);color:#fff}
.saved{font-size:13px;font-weight:600}.saved.pass{color:var(--green)}.saved.fail{color:var(--red)}
kbd{background:#fff;border:1px solid var(--line);color:var(--navy);border-radius:4px;font-size:11px;padding:1px 5px;box-shadow:none}
.kv{font-size:13px}.kv dt{color:var(--muted);font-weight:500}.kv dd{margin-bottom:6px}
pre.prompt{white-space:pre-wrap;font-size:12px;background:#F6F9FC;border:1px solid var(--line);border-radius:6px;padding:10px;max-height:320px;overflow:auto}
.bslib-value-box .value-box-title{color:var(--muted)}
@media(max-width:767px){
  .navbar>.container-fluid{padding-left:16px;padding-right:16px}
  .navbar-brand{margin-right:8px}
  .pipe{grid-template-columns:1fr;gap:10px}
  .pipe .step{grid-row:auto!important;grid-column:1!important}
  .pipe .step::after,.pipe .step::before{display:none}
  .case-heading,.case-heading-chips{flex-wrap:wrap;gap:12px!important}
  .verdict{flex-wrap:wrap}
}
/* Reference-driven Review workspace. Other pages keep their full workflow diagram. */
:root{--blue:#2563eb;--navy:#162139;--line:#dce5f1;--muted:#647795}
body{font-family:Arial,sans-serif;font-size:14px;background:#f3f6fb;color:#17233b}
.navbar{min-height:56px}.navbar-brand{font-size:16px;letter-spacing:-.4px;margin-right:20px}
.navbar>.container-fluid{padding:0 20px}.navbar-brand>span{display:flex;align-items:center;gap:10px}
.app-monogram{display:inline-grid;place-items:center;width:28px;height:28px;background:#2563eb;color:#fff;border-radius:8px;font-size:18px}
#nav .nav-link{padding:14px 12px!important;font-size:14px;font-weight:500}
.nav-link .material-icon{width:15px;height:15px;margin-right:8px;color:#8095b3}
.nav-link.active .material-icon{color:#2563eb}
.profile-signature{display:flex;align-items:center;gap:8px;padding-left:16px;margin-left:12px;border-left:1px solid var(--line);font-size:12px;white-space:nowrap}
.profile-monogram{display:grid;place-items:center;border-radius:50%;width:32px;height:32px;background:#101a2c;color:white;font-size:12px}
#open_settings{font-size:12px;background:#f1f5fa;border:1px solid var(--line);border-radius:5px;padding:7px 10px;text-decoration:none;color:#34465f}
#export{font-size:12px;color:#34465f;border-color:#ccd8e8;background:white}
body:has(#tab-nav-0.active)>.container-fluid{padding-left:0;padding-right:0}
#tab-nav-0>.bslib-sidebar-layout{border:0;border-radius:0;margin:0;gap:0;background:#f3f6fb;--bslib-spacer:20px}
#tab-nav-0 .bslib-sidebar-layout>.main{padding:0 24px 24px;gap:20px}
#tab-nav-0 .sidebar{border-right:1px solid var(--line);border-radius:0}
#tab-nav-0 .sidebar-content{padding:14px 14px 12px;gap:10px}
#progress{font-size:12px}#progress .muted{font-size:11px}
#progress>div>div:first-child{display:flex;justify-content:space-between}
#show .shiny-options-group{display:flex;justify-content:space-between;gap:3px}
#show .radio-inline{margin:0;padding:0;font-size:11px}
#show input{position:absolute;opacity:0}
#show label{padding:6px 8px!important;border:1px solid transparent;border-radius:4px;color:#607492}
#show label:has(input:checked){border-color:#dce5f1;background:white;color:#2563eb}
#show label:has(input:focus-visible){outline:2px solid #2563eb}
#intent_filter{font-size:12px;min-height:32px;border:1px solid var(--line);border-radius:5px}
#case_list{margin:0 -14px}.caselist{max-height:calc(100vh - 255px);padding:0;margin:0}
.caseitem{display:block;padding:12px;border-bottom:1px solid #eef2f7;border-radius:0;font-size:12px;line-height:1.5;min-height:86px}
.caseitem.active{outline:0;border-left:3px solid #6393ff;padding-left:13px;background:#f3f7ff}
.case-row-title{display:flex;align-items:center;gap:6px;margin-bottom:5px}.caseitem .id{width:auto;font-family:monospace;color:#647795}
.caseitem.active .id{color:#214ca5}.caseitem .dot{width:8px;height:8px;margin:0}
.case-intent{margin-left:auto;font-size:10px;font-family:monospace;background:#f1f5f9;color:#566b86;border-radius:3px;padding:1px 6px}
.case-preview{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;color:#4c5f7a}
.caseitem.active .case-preview{color:#17233b}#run_missing{font-size:12px;border-radius:5px;min-height:34px}
.case-heading{min-height:56px;margin:0 -24px!important;padding:10px 24px;background:#fff;border-bottom:1px solid var(--line)}
.case-heading h4{font-size:20px;font-weight:700;font-family:monospace}
.case-heading-chips{gap:6px!important}.case-heading .btn{font-size:12px;background:white;border-color:#cbd7e7;color:#415571;border-radius:5px}
.chip{border-radius:3px;padding:2px 7px;font-size:12px;margin-bottom:5px;background:#f1f5f9;line-height:1.35}
.chip.big{font-size:12px;padding:2px 7px;font-weight:500}.chip.ok{color:#007958;background:#eafff5;border-color:#a6e9cd}.chip.bad{color:#d80039;background:#fff1f3;border-color:#ffc4ce}
#tab-nav-0 .card{border-radius:12px;background:white;gap:0;box-shadow:0 1px 2px #15243b05}
#tab-nav-0 .card-header{border:0;background:transparent;padding:18px 16px 0;font-size:13px}
#tab-nav-0 .card-header:after{content:"";display:block;border-bottom:1px solid #eef2f7;margin-top:14px}
#tab-nav-0 .card-body{padding:12px 16px 18px}
.customer-card,.expected-card{min-height:284px}.customer-card .card-header,.expected-card .card-header{text-transform:uppercase;letter-spacing:.6px;font-size:12px!important;color:#536986}
#email_card .email{font-size:14px;line-height:1.65;background:#f8fafc;border:1px solid #edf2f8;border-radius:8px;padding:14px;margin-top:8px!important}
.kv{margin-bottom:0;font-size:12px}.kv dt{font-size:10px;text-transform:uppercase;color:#8498b5;font-weight:600;margin-bottom:4px}.kv dd{margin-bottom:12px;line-height:1.5}.kv .muted{font-size:12px}
.routing-spec.safe{color:#007958;background:#effcf6;border-color:#a6e9cd}
.routing-spec{padding:6px 8px;background:#fff5f6;color:#d80039;border:1px solid #ffc7d0;border-radius:4px}
#tab-nav-0 .review-workflow{position:relative;border-radius:7px;min-height:104px}
#tab-nav-0 .review-workflow .card-header{width:38%;padding:14px 12px;font-size:12px;line-height:1.4;min-height:60px}
#tab-nav-0 .review-workflow .card-header:after{display:none}.review-workflow .muted{font-size:11px;color:#8498b5}
#tab-nav-0 .review-workflow .card-body{padding:0 12px 12px}.review-pipeline{position:absolute;top:12px;right:12px;width:59%;display:flex;gap:6px}
.summary-step{border:1px solid transparent;background:#f1f5f9;border-radius:4px;padding:5px 7px;flex:1;min-width:0;text-align:left;font:10px monospace;color:#455975}.summary-step span{display:block;margin-top:3px}.summary-step.model{border-color:#b4d1ff;color:#2563eb;background:#eff6ff}.summary-step.bad{border-color:#ffc3cf;color:#df0038;background:#fff1f3}.summary-step:focus-visible{outline:2px solid #2563eb}
.review-workflow #run_card>div{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.review-workflow #run_card .mt-3,.review-workflow #run_card .mt-2{margin-top:0!important}
.review-workflow #run_card .btn{font-size:11px;padding:4px 10px;background:#f1f5f9;color:#354963;border:0}.review-workflow #run_card #to_sim{background:transparent;color:#2563eb}
.draft-card,.verdict-card{min-height:435px}.draft-card .card-header,.verdict-card .card-header{font-size:14px!important;color:#111c30}
.draft-meta{float:right;color:#8498b5;font-size:11px;font-weight:400}.verdict-card #saved_badge{float:right;font-size:12px;font-weight:400;color:#8498b5}
#reply_card{height:100%;display:flex;flex-direction:column}#reply_card .reply{background:#f7f9fc;border-radius:8px;border-left:4px solid #4380ff;padding:16px;font-size:14px;line-height:1.7}
.reply-checkpoints{margin-top:auto;padding-top:16px;border-top:1px solid #eef2f7;font-size:11px;color:#607492}.reply-checkpoints>span:first-child{margin-right:6px}
#tab-nav-0 .verdict-card{border:2px solid #ccd8e8}.verdict{display:grid!important;grid-template-columns:1fr 1fr;gap:12px!important;margin-top:4px}
.verdict .btn{min-width:0;width:100%;min-height:70px;border-radius:8px;border-width:2px;font-size:16px;font-weight:600}.verdict .btn-pass{background:#fff;border-color:#00bd88;color:#007454}.verdict .btn-fail{background:#fff2f5;border-color:#ff3763;color:#c90036}
.verdict .btn small{display:block;font:10px monospace;margin-top:6px;font-weight:400;color:#6a809e}
.verdict-card label{font-size:12px;line-height:1.4}.verdict-card select{font-size:12px;border:1px solid #ffc0cd;border-radius:5px;min-height:34px}.verdict-card textarea{font:12px/1.6 monospace;border:1px solid #cbd7e7;border-radius:5px;min-height:82px;height:82px}
.review-shortcuts{padding-top:14px;border-top:1px solid #edf2f7;font:10px/1.8 monospace;margin-top:6px;color:#8196b5}
@media(max-width:1100px){.profile-signature{display:none}.navbar-brand{font-size:14px;margin-right:8px}#nav .nav-link{padding-left:9px!important;padding-right:9px!important}}
@media(max-width:767px){#tab-nav-0 .bslib-sidebar-layout>.main{padding:0 14px 14px}.case-heading{margin:0 -14px!important;padding:12px 14px}.review-pipeline{position:static;width:100%;flex-wrap:wrap}.summary-step{min-width:70px}#tab-nav-0 .review-workflow .card-header{width:100%;min-height:0}.draft-meta{float:none;display:block;margin-top:6px}.draft-card,.verdict-card{min-height:0}.reply-checkpoints{margin-top:24px}.caselist{max-height:360px}.profile-signature{display:none}}

/* Keep reference geometry stable against Bootstrap/Shiny defaults. */
.navbar{padding:0;min-height:56px}#nav{gap:2px;align-items:center}
#tab-nav-0{margin-top:0!important}
#tab-nav-0 .card-header{flex-wrap:wrap;align-items:center}
#tab-nav-0 .card-header:after{flex-basis:100%;width:100%;margin-top:10px}
#tab-nav-0 .draft-card .card-header>span:last-of-type,#tab-nav-0 .verdict-card .card-header>span:last-of-type{margin-left:auto}
#tab-nav-0 .verdict-card .card-body{gap:10px}
#tab-nav-0 .verdict-card .form-group{margin-bottom:0}
#tab-nav-0 .verdict-card .verdict{margin-bottom:6px!important}
#tab-nav-0 .review-workflow .card-header:after{display:none}
@media(min-width:1200px){#nav{flex-wrap:nowrap}.profile-signature{padding-left:10px;margin-left:6px;font-size:11px}#nav .nav-link{padding-left:10px!important;padding-right:10px!important}}
"""

JS = """
document.addEventListener('keydown', e => {
  const tag = (e.target.tagName || '').toUpperCase();
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
    // send what's typed now, so a fast save doesn't race Shiny's input debounce
    const box = document.getElementById('critique');
    if (box) Shiny.setInputValue('critique', box.value, {priority: 'event'});
    Shiny.setInputValue('kbd', 'save', {priority: 'event'});
    return;
  }
  if (e.target.closest('[role=tab], [contenteditable=true]')) return;
  if (['INPUT', 'TEXTAREA', 'SELECT'].includes(tag) || e.ctrlKey || e.metaKey || e.altKey) return;
  const map = {p: 'pass', f: 'fail', j: 'next', k: 'prev', ArrowRight: 'next', ArrowLeft: 'prev'};
  const k = map[e.key] || map[e.key.toLowerCase?.()];
  if (k) { e.preventDefault(); Shiny.setInputValue('kbd', k, {priority: 'event'}); }
});
document.addEventListener('click', e => {
  const c = e.target.closest('[data-case]');
  if (c) Shiny.setInputValue('pick_case', c.dataset.case, {priority: 'event'});
  const s = e.target.closest('[data-step]');
  if (s) Shiny.setInputValue(s.dataset.target, s.dataset.step, {priority: 'event'});
});
$(document).on('shiny:connected', () => {
  Shiny.addCustomMessageHandler('focus', id => setTimeout(() => document.getElementById(id)?.focus(), 50));
});
"""

# grid positions mirror the diagram: top row left→right, bottom row right→left, human under step 7
LAYOUT = {"1": (1, 1, "a-r"), "2": (1, 2, "a-r"), "3": (1, 3, "a-r"), "4": (1, 4, "a-r"), "5": (1, 5, "a-d"),
          "6": (2, 5, "a-l"), "7": (2, 4, "a-l a-d"), "8": (2, 3, "a-l"), "9": (2, 2, ""), "H": (3, 4, "")}


def pipeline(trace: list[dict], waiting: bool = False, selected: str | None = None, target: str = "step",
             compact: bool = False) -> str:
    last = {t["step"]: t for t in trace or []}
    cells = []
    for step in ["1", "2", "3", "4", "5", "6", "7", "H", "8", "9"]:
        row, col, arrows = LAYOUT[step]
        name, kind = STEPS[step]
        t = last.get(step)
        status = t["status"] if t else ("waiting" if step == "H" and waiting else "pending")
        detail = html.escape(t["detail"]) if t else ("Waiting for you" if status == "waiting" else "")
        kcls = "model" if kind == "model" else "human" if kind == "human" else ""
        label = f"{step} {name}" if step != "H" else name
        arrow = arrows.replace("a-d", "") if step == "7" and not (waiting or last.get("H")) else arrows
        cells.append(
            f'<button type="button" class="step {kcls} st-{status} {arrow} {"sel" if selected == step else ""}" '
            f'style="grid-row:{row};grid-column:{col}" data-step="{step}" data-target="{target}" title="{detail}">'
            f'<b>{html.escape(label)}</b><span class="k">{kind}{" · " + status if t or status == "waiting" else ""}</span>'
            f'<span class="d">{detail}</span></button>')
    return f'<div class="pipe {"compact" if compact else ""}">{"".join(cells)}</div>'


def highlight(text: str, good: list[str], bad: list[str]) -> str:
    esc = html.escape(text or "")
    terms = [(html.escape(t), "ok") for t in good if t] + [(html.escape(t), "bad") for t in bad if t]
    if not terms:
        return esc
    cls = {t.lower(): c for t, c in terms}
    pattern = re.compile("|".join(re.escape(t) for t, _ in sorted(terms, key=lambda x: -len(x[0]))), re.I)
    return pattern.sub(lambda m: f'<mark class="{cls.get(m.group(0).lower(), "ok")}">{m.group(0)}</mark>', esc)


def chip(text: str, kind: str = "", big: bool = False) -> str:
    return f'<span class="chip {kind} {"big" if big else ""}">{html.escape(str(text))}</span>'
