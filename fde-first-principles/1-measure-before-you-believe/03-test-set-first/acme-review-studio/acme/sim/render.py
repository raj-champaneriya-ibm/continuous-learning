"""Escaped HTML renderers for simulator topologies and evidence."""
from __future__ import annotations

import html
import json
from collections import defaultdict
from typing import Any

from .service import compare_results, manifest_diff
from .trace import Capabilities, RunResult, Span, Topology
from .versions import Version


def _text(value: Any) -> str:
    if isinstance(value, (dict, list, tuple)):
        value = json.dumps(value, ensure_ascii=False, indent=2, default=str)
    return html.escape(str(value if value is not None else "—"), quote=True)


def _button(span: Span, selected: str | None, target: str) -> str:
    return (f'<button type="button" class="sim-span st-{_text(span.status)} '
            f'{"selected" if span.id == selected else ""}" data-step="{_text(span.id)}" '
            f'data-target="{_text(target)}"><b>{_text(span.name)}</b>'
            f'<span>{_text(span.kind)} · {_text(span.status)} · {span.ms} ms</span></button>')


def _tree(spans: list[Span], selected: str | None, target: str, parent: str | None = None) -> str:
    children: dict[str | None, list[Span]] = defaultdict(list)
    for span in spans:
        children[span.parent].append(span)

    def branch(node: str | None) -> str:
        items = []
        for span in children.get(node, []):
            items.append("<li>" + _button(span, selected, target) + branch(span.id) + "</li>")
        return "<ul>" + "".join(items) + "</ul>" if items else ""

    return '<div class="sim-tree">' + branch(parent) + "</div>"


def _topology(result: RunResult, topology: Topology, selected: str | None, target: str) -> str:
    spans = {span.attrs.get("step"): span for span in result.spans if span.attrs.get("step")}
    buttons = []
    for node in topology.nodes:
        step = str(node["id"])
        span = spans.get(step) or Span(id=f"step-{step}", parent=None, kind="step",
                                      name=str(node["name"]), status="skipped", ms=0,
                                      attrs={"step": step, "detail": "Not run"})
        buttons.append(_button(span, selected, target))
    edges = " · ".join(f'{_text(edge["source"])} → {_text(edge["target"])}'
                       for edge in topology.edges)
    roots = {span.id for span in result.spans if span.parent is None and not span.attrs.get("step")}
    extra = ([span for span in result.spans if span.parent is not None or span.id in roots]
             if roots else [])
    return ('<div class="sim-topology" aria-label="Workflow steps">' + "".join(buttons) + "</div>"
            + (f'<div class="muted mt-2">Connections: {edges}</div>' if edges else "")
            + ('<h4>Other run evidence</h4>' + _tree(extra, selected, target) if extra else ""))


def render_result(result: RunResult, topology: Topology, implementation: str,
                  selected: str | None, target: str = "sim_step_click") -> str:
    if implementation in {"orchestrated", "declarative"} and topology.nodes:
        return _topology(result, topology, selected, target)
    if implementation == "agent_loop":
        return '<h4>Agent turn timeline</h4>' + _tree(result.spans, selected, target)
    if implementation == "api":
        return '<h4>HTTP exchange</h4>' + _tree(result.spans, selected, target)
    if implementation == "multi_agent":
        return '<h4>Agent handoffs</h4>' + _tree(result.spans, selected, target)
    return '<h4>Run spans</h4>' + _tree(result.spans, selected, target)


def render_detail(result: RunResult, selected: str | None, capabilities: Capabilities,
                  target: str = "sim_step_click") -> str:
    span = next((item for item in result.spans if item.id == selected), None)
    if span is None:
        return '<div class="muted">Select a span to inspect its evidence.</div>'
    output = [f'<div><b>{_text(span.name)}</b> · {_text(span.status)} · {span.ms} ms</div>']
    attrs = {key: value for key, value in span.attrs.items()
             if key not in {"step", "recorded_response"} and value is not None
             and (capabilities.prompts or key not in {"system_prompt", "user_prompt"})
             and (capabilities.envelope or key != "envelope")}
    for key, value in attrs.items():
        output.append(f'<details open><summary>{_text(key.replace("_", " ").title())}</summary>'
                      f'<pre class="prompt">{_text(value)}</pre></details>')
    children = [item for item in result.spans if item.parent == span.id]
    if children:
        output.append('<div class="mt-2"><b>Nested evidence</b></div>')
        output.append(_tree(result.spans, selected, target, parent=span.id))
        for child in children:
            if child.kind == "model_call":
                tool_calls = [item for item in result.spans if item.parent == child.id and item.kind == "tool_call"]
                for tool in tool_calls:
                    output.append(f'<details><summary>Tool: {_text(tool.name)} · {_text(tool.status)}</summary>'
                                  f'<pre class="prompt">{_text(tool.attrs)}</pre></details>')
    return "".join(output)


def render_comparison(left: RunResult, right: RunResult, left_version: Version, right_version: Version) -> str:
    diff = compare_results(left, right)
    changes = manifest_diff(left_version, right_version)
    lines = []
    for key in ("decision", "reasons", "intent", "grade", "usage"):
        if key in diff:
            lines.append(f'<tr><th scope="row">{_text(key.title())}</th>'
                         f'<td><pre>{_text(diff[key]["left"])}</pre></td>'
                         f'<td><pre>{_text(diff[key]["right"])}</pre></td></tr>')
    words = []
    for word in diff["reply_diff"]:
        text = _text(word[2:])
        if word.startswith("+ "):
            words.append(f"<ins>{text}</ins>")
        elif word.startswith("- "):
            words.append(f"<del>{text}</del>")
        elif word.startswith("  "):
            words.append(text)
    manifest = "".join(f'<li><b>{_text(item["field"])}</b>: {_text(item["left"])} → {_text(item["right"])}</li>'
                       for item in changes) or "<li>No manifest differences.</li>"
    return (f'<details><summary>Manifest differences</summary><ul>{manifest}</ul></details>'
            '<div class="table-responsive"><table class="table table-sm sim-compare"><thead><tr>'
            f'<th>Field</th><th>{_text(left_version.name)} · {_text(left.version_id)}</th>'
            f'<th>{_text(right_version.name)} · {_text(right.version_id)}</th></tr></thead>'
            f'<tbody>{"".join(lines)}</tbody></table></div>'
            f'<div><b>Reply diff:</b> {" ".join(words) or "No reply."}</div>')
