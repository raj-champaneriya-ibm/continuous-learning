"""Adapters for the studio graph and its allowlisted declarative form."""
from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Any

from langgraph.checkpoint.sqlite import SqliteSaver

from acme.providers import C3Provider, ClaudeCodeProvider, OfflineProvider
from acme.workflow import Deps, Settings, Workflow

from ..trace import Capabilities, RunInput, RunResult, Span, Topology
from ..privacy import RedactingSerializer
from ..versions import Version, VersionRegistry
from .common import no_draft, validate_draft

_NODE_STEPS = {"receive": "1", "route": "2", "verify": "3", "fetch": "4", "draft": "5",
               "check": "6", "decide": "7", "human": "H", "send": "8", "log": "9"}
_STATUS = {"approve": "ok", "edit": "ok", "hold": "skipped"}


class RecordedProvider:
    def __init__(self, provider: str, model: str, response: dict[str, Any]):
        self.name, self.model, self.response = provider, model, response

    def status(self) -> tuple[bool, str]:
        return True, "Reusing the recorded response."

    def draft(self, system: str, user: str, ctx: dict | None = None) -> dict[str, Any]:
        return dict(self.response)


class OrchestratedAdapter:
    implementation = "orchestrated"

    def __init__(self, registry: VersionRegistry, checkpoints: Path, log_path: Path):
        self.registry, self.log_path = registry, log_path
        checkpoints.parent.mkdir(parents=True, exist_ok=True)
        self.checkpointer = SqliteSaver(sqlite3.connect(checkpoints, check_same_thread=False),
                                       serde=RedactingSerializer())

    def capabilities(self, version: Version) -> Capabilities:
        provider = version.content["config"]["provider"]
        return Capabilities(interrupt=True, prompts=provider != "offline", tool_calls=provider == "c3",
                            envelope=provider == "c3", recorded_replay=True)

    def _provider(self, version: Version, recorded: dict[str, Any] | None = None):
        config = version.content["config"]
        name, model = config["provider"], config["model"]
        if recorded is not None:
            return RecordedProvider(name, model, recorded)
        if name == "offline":
            return OfflineProvider()
        if name == "claude-code":
            return ClaudeCodeProvider(model=model, timeout=config["timeout_s"])
        if name == "c3":
            return C3Provider(model=model, lab_root=self.registry.lab_root, data_root=self.registry.lab_data(version),
                              temperature=config["temperature"], max_steps=config["max_steps"],
                              timeout=config["timeout_s"], persist_cache=False)
        raise ValueError(f"Unknown drafting provider {name!r}")

    def status(self, version: Version) -> tuple[bool, str]:
        try:
            if self.implementation == "declarative":
                Workflow._validate_spec(version.content.get("spec"))
            return self._provider(version).status()
        except (ValueError, OSError) as exc:
            return False, str(exc)

    def input_schema(self, version: Version) -> dict[str, Any]:
        props = {"customer_id": {"type": "string"}, "message": {"type": "string"},
                 "portal": {"type": "string"}, "history": {"type": "array"}}
        return {"type": "object", "properties": {key: props[key] for key in version.content["inputs"]},
                "required": ["customer_id", "message"]}

    def _workflow(self, version: Version, *, recorded: dict[str, Any] | None = None,
                  cancelled: threading.Event | None = None) -> Workflow:
        config = version.content["config"]
        deps = Deps(lab=self.registry.load_lab(version), provider=self._provider(version, recorded),
                    settings=Settings(guards=config["guards"], block_on_high_flags=config["block_on_high_flags"]),
                    log_path=self.log_path, version_id=version.id, cancelled=cancelled)
        return Workflow(deps, self.checkpointer, spec=version.content.get("spec")
                        if self.implementation == "declarative" else None)

    def topology(self, version: Version) -> Topology:
        graph = self._workflow(version).graph.get_graph()
        nodes = [{"id": _NODE_STEPS.get(key, key), "name": key.replace("_", " ").title()}
                 for key in graph.nodes if key in _NODE_STEPS]
        edges = [{"source": _NODE_STEPS.get(edge.source, edge.source),
                  "target": _NODE_STEPS.get(edge.target, edge.target), "conditional": bool(edge.conditional)}
                 for edge in graph.edges if edge.source in _NODE_STEPS and edge.target in _NODE_STEPS]
        return Topology(nodes=nodes, edges=edges)

    def start(self, version: Version, run_input: RunInput, run_id: str, sample: int = 0,
              recorded: dict[str, Any] | None = None,
              cancelled: threading.Event | None = None) -> RunResult:
        view = self._workflow(version, recorded=recorded, cancelled=cancelled).start(
            customer_id=run_input.customer_id, message=run_input.message, portal=run_input.portal,
            case_id=run_input.case_id, history=run_input.history, run_id=run_id, sample=sample)
        return self._result(version, run_id, view)

    def resume(self, version: Version, run_id: str, decision: dict[str, Any],
               cancelled: threading.Event | None = None) -> RunResult:
        action = decision.get("action")
        if action not in {"approve", "edit", "hold"}:
            raise ValueError("Human decision must be approve, edit or hold")
        if action == "edit" and not str(decision.get("reply") or "").strip():
            raise ValueError("An edited reply cannot be empty")
        view = self._workflow(version, cancelled=cancelled).resume(
            f"{version.id}:{run_id}", action, decision.get("reply"))
        return self._result(version, run_id, view)

    def _result(self, version: Version, run_id: str, view: dict[str, Any]) -> RunResult:
        llm = view.get("llm") or {}
        raw = llm.get("raw")
        if isinstance(raw, str):
            try:
                raw = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                raw = {"text": raw}
        raw = raw if isinstance(raw, dict) else {}
        provider = llm.get("provider") or version.content["config"]["provider"]
        spans = []
        for item in view.get("trace", []):
            step = item["step"]
            attrs: dict[str, Any] = {"step": step, "detail": item["detail"]}
            if step == "4" and provider not in {"c3", "offline"} and view.get("user_prompt"):
                attrs["user_prompt"] = view["user_prompt"]
            if step == "5" and raw.get("envelope"):
                attrs["envelope"] = raw["envelope"]
            spans.append(Span(id=f"step-{step}", parent=None, kind="human" if step == "H" else "step",
                              name=item["name"], status=_STATUS.get(item["status"], item["status"]),
                              ms=item["ms"], attrs=attrs))
        if view.get("waiting_for_human") and not any(span.id == "step-H" for span in spans):
            spans.append(Span(id="step-H", parent=None, kind="human", name="Human decision",
                              status="waiting", ms=0, attrs={"step": "H", "reasons": view.get("reasons", [])}))
        draft = view.get("draft")
        if view.get("model_called"):
            turns = raw.get("turns") or ([{"step": 0, "tool_calls": [
                (call.get("name"), call.get("args"), call.get("result")) for call in raw.get("tool_calls", [])]}]
                if raw.get("tool_calls") else [{}])
            for index, turn in enumerate(turns):
                turn_id = f"step-5:turn-{index}"
                attrs = {key: turn[key] for key in ("tokens_in", "tokens_out", "stop_reason",
                                                    "system_prompt", "user_prompt") if turn.get(key) is not None}
                if index == 0:
                    if provider not in {"c3", "offline"}:
                        attrs.update(system_prompt=view.get("system_prompt"), user_prompt=view.get("user_prompt"))
                    attrs["recorded_response"] = {"output": draft, "error": llm.get("error"),
                                                  "latency_s": llm.get("latency_s", 0),
                                                  "cost_usd": llm.get("cost_usd"), "raw": raw}
                spans.append(Span(id=turn_id, parent="step-5", kind="model_call",
                                  name=f"Turn {index + 1}" if provider == "c3" else "Draft",
                                  status="error" if llm.get("error") else "ok",
                                  ms=int(float(turn.get("seconds") or 0) * 1000), attrs=attrs))
                for number, call in enumerate(turn.get("tool_calls") or []):
                    name, args, result = call
                    spans.append(Span(id=f"{turn_id}:tool-{number}", parent=turn_id, kind="tool_call",
                                      name=str(name), status="error" if isinstance(result, dict) and result.get("error")
                                      else "ok", ms=0, attrs={"arguments": args, "result": result}))
            for number, source in enumerate(raw.get("escalation_sources") or []):
                spans.append(Span(id=f"step-5:guard-{number}", parent="step-5", kind="guard",
                                  name=str(source), status="escalate", ms=0))
        if llm.get("error"):
            spans.append(Span(id="adapter-error", parent="step-5" if view.get("model_called") else None,
                              kind="check", name="Draft failed", status="error", ms=0,
                              attrs={"error": llm["error"]}))
        output = validate_draft(draft) if draft else no_draft("; ".join(view.get("reasons") or ["No draft"]))
        output = {**output, "has_draft": bool(draft), "model_called": bool(view.get("model_called")),
                  "provider": provider, "model": llm.get("model"), "thread_id": view.get("thread_id"),
                  "decision": view.get("decision"), "reasons": view.get("reasons", []),
                  "flags": view.get("flags", []), "guard_hits": view.get("guard_hits", []),
                  "outcome": view.get("outcome"), "final_reply": view.get("final_reply"),
                  "waiting_for_human": view.get("waiting_for_human", False)}
        usage = {"latency_s": llm.get("latency_s"), "cost_usd": llm.get("cost_usd"),
                 "tokens_in": raw.get("tokens_in"), "tokens_out": raw.get("tokens_out")}
        state = "failed" if llm.get("error") else "waiting_for_human" if view.get("waiting_for_human") else "completed"
        return RunResult(run_id=run_id, version_id=version.id, state=state, output=output, spans=spans, usage=usage)


class DeclarativeAdapter(OrchestratedAdapter):
    implementation = "declarative"
