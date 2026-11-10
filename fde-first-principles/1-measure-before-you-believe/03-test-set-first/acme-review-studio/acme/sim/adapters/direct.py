"""Adapters for the C3 agent loop and the offline callable."""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import requests

from acme.providers import C3Provider, OfflineProvider

from ..trace import Capabilities, RunInput, RunResult, Span, Topology
from ..versions import Version, VersionRegistry
from .common import direct_output


class DirectAdapter:
    implementation = "custom"

    def __init__(self, registry: VersionRegistry, checkpoints: Path, log_path: Path):
        self.registry = registry

    def _provider(self, version: Version):
        return OfflineProvider()

    def capabilities(self, version: Version) -> Capabilities:
        return Capabilities()

    def status(self, version: Version) -> tuple[bool, str]:
        try:
            return self._provider(version).status()
        except (ValueError, OSError) as exc:
            return False, str(exc)

    def input_schema(self, version: Version) -> dict[str, Any]:
        props = {"customer_id": {"type": "string"}, "message": {"type": "string"},
                 "portal": {"type": "string"}, "history": {"type": "array"}}
        return {"type": "object", "properties": {key: props[key] for key in version.content["inputs"]},
                "required": ["customer_id", "message"]}

    def topology(self, version: Version) -> Topology:
        return Topology(nodes=[{"id": "draft", "name": version.name}], edges=[])

    def start(self, version: Version, run_input: RunInput, run_id: str, sample: int = 0,
              recorded: dict[str, Any] | None = None,
              cancelled: threading.Event | None = None) -> RunResult:
        if recorded is not None:
            raise ValueError("This adapter does not support recorded replay")
        lab, config = self.registry.load_lab(version), version.content["config"]
        provider = self._provider(version)
        customer = lab.customers.get(run_input.customer_id)
        if not customer:
            output = direct_output(lab, config, run_input, None, provider=provider.name,
                                   model=getattr(provider, "model", ""))
            return RunResult(run_id=run_id, version_id=version.id, state="completed", output=output,
                             spans=[Span(id="verify", parent=None, kind="guard", name="Verify account",
                                         status="stop", ms=0, attrs={"reason": output["reasons"][0]})])
        result = provider.draft("", "", {"message": run_input.message, "customer": customer,
                                         "outage": lab.outage_for(customer), "case_id": run_input.case_id,
                                         "customer_id": run_input.customer_id, "history": run_input.history,
                                         "sample": sample})
        if result["error"]:
            raise RuntimeError(result["error"])
        output = direct_output(lab, config, run_input, result["output"], provider=provider.name,
                               model=getattr(provider, "model", ""))
        raw = result.get("raw") or {}
        if isinstance(raw, str):
            try:
                raw = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                raw = {"text": raw}
        raw = raw if isinstance(raw, dict) else {}
        spans = self._spans(raw, result)
        usage = {"latency_s": result.get("latency_s"), "cost_usd": result.get("cost_usd"),
                 "tokens_in": raw.get("tokens_in"), "tokens_out": raw.get("tokens_out")}
        return RunResult(run_id=run_id, version_id=version.id, state="completed",
                         output=output, spans=spans, usage=usage)

    def _spans(self, raw: dict[str, Any], result: dict[str, Any]) -> list[Span]:
        return [Span(id="draft", parent=None, kind="step", name="Offline draft", status="ok",
                     ms=int(float(result.get("latency_s") or 0) * 1000))]

    def resume(self, version: Version, run_id: str, decision: dict[str, Any],
               cancelled: threading.Event | None = None) -> RunResult:
        raise ValueError("This adapter cannot pause for a human")


class AgentLoopAdapter(DirectAdapter):
    implementation = "agent_loop"

    def _provider(self, version: Version):
        config = version.content["config"]
        return C3Provider(model=config["model"], lab_root=self.registry.lab_root,
                          data_root=self.registry.lab_data(version), temperature=config["temperature"],
                          max_steps=config["max_steps"], timeout=config["timeout_s"], persist_cache=False)

    def capabilities(self, version: Version) -> Capabilities:
        return Capabilities(prompts=True, tool_calls=True, envelope=True)

    def _spans(self, raw: dict[str, Any], result: dict[str, Any]) -> list[Span]:
        spans = [Span(id="agent", parent=None, kind="agent", name="C3 agent loop", status="ok",
                      ms=int(float(result.get("latency_s") or 0) * 1000),
                      attrs={"envelope": raw.get("envelope")})]
        for index, turn in enumerate(raw.get("turns") or []):
            turn_id = f"turn-{index}"
            attrs = {key: turn[key] for key in ("tokens_in", "tokens_out", "stop_reason",
                                                "system_prompt", "user_prompt") if turn.get(key) is not None}
            spans.append(Span(id=turn_id, parent="agent", kind="model_call", name=f"Turn {index + 1}",
                              status="ok", ms=int(float(turn.get("seconds") or 0) * 1000), attrs=attrs))
            for number, call in enumerate(turn.get("tool_calls") or []):
                name, args, value = call
                spans.append(Span(id=f"{turn_id}:tool-{number}", parent=turn_id, kind="tool_call", name=str(name),
                                  status="error" if isinstance(value, dict) and value.get("error") else "ok",
                                  ms=0, attrs={"arguments": args, "result": value}))
        for number, source in enumerate(raw.get("escalation_sources") or []):
            spans.append(Span(id=f"guard-{number}", parent="agent", kind="guard", name=str(source),
                              status="escalate", ms=0))
        return spans


class VersionBAdapter(DirectAdapter):
    """Run the lab's single-call, oracle-context Version B on frozen lab data."""

    def capabilities(self, version: Version) -> Capabilities:
        return Capabilities(prompts=True)

    def status(self, version: Version) -> tuple[bool, str]:
        try:
            from lab import llm, version_b
        except ModuleNotFoundError as exc:
            return False, f"Version B needs the lab package and {exc.name}."
        model = version.content["config"]["model"]
        if model.startswith("anthropic:"):
            return False, "Version B needs a model endpoint that supports its JSON schema."
        if model.startswith("api:"):
            base = llm._env("LLM_BASE_URL")
            if not base:
                return False, "Set LLM_BASE_URL for the Version B model."
            if urlsplit(base).hostname not in {"localhost", "127.0.0.1", "::1"} and not llm._env("LLM_API_KEY"):
                return False, "Set LLM_API_KEY for the Version B model."
            return True, f"Version B model: {model}."
        try:
            with requests.Session() as session:
                session.trust_env = False
                response = session.get(f"{llm.OLLAMA}/api/tags", timeout=1)
                response.raise_for_status()
                models = {item.get("name") for item in response.json().get("models", [])}
        except (requests.RequestException, ValueError) as exc:
            return False, f"Ollama is unavailable: {exc}"
        if model not in models:
            return False, f"Install or select Ollama model {model!r}."
        return True, f"Version B model: {model}."

    def start(self, version: Version, run_input: RunInput, run_id: str, sample: int = 0,
              recorded: dict[str, Any] | None = None,
              cancelled: threading.Event | None = None) -> RunResult:
        if recorded is not None:
            raise ValueError("This adapter does not support recorded replay")
        from lab.acme import INTENT_KB, use_data_root
        from lab import version_b

        lab, config = self.registry.load_lab(version), version.content["config"]
        if run_input.customer_id not in lab.customers:
            output = direct_output(lab, config, run_input, None, provider="version-b", model=config["model"])
            return RunResult(run_id=run_id, version_id=version.id, state="completed", output=output,
                             spans=[Span(id="verify", parent=None, kind="guard", name="Verify account",
                                         status="stop", ms=0, attrs={"reason": output["reasons"][0]})])
        case = dict(run_input.case or {})
        case.update(id=run_input.case_id, customer_id=run_input.customer_id,
                    message=run_input.message, history=run_input.history)
        if not case.get("expected_intent"):
            message = run_input.message.lower()
            scores = {intent: sum(word in message for word in words)
                      for intent, words in OfflineProvider.KEYWORDS.items()}
            case["expected_intent"] = max(scores, key=scores.get) if max(scores.values()) else "other"
            context_source = "Keyword estimate for free-form input"
        else:
            context_source = "Dataset label (oracle context)"
        with use_data_root(self.registry.lab_data(version)):
            system, user = version_b.system_prompt(), version_b.user_message(case)
            started = time.monotonic()
            result = version_b.version_b(case, temperature=config["temperature"], run=sample,
                                         model=config["model"], timeout=config["timeout_s"], persist_cache=False)
        if result.get("parse_error"):
            raise ValueError("Version B returned invalid JSON.")
        if not isinstance(result.get("needs_human"), bool):
            raise ValueError("Version B returned an invalid needs_human value.")
        cited = ["CRM", *INTENT_KB[case["expected_intent"]]]
        outage = lab.outage_for(lab.customers[run_input.customer_id])
        if outage and outage.get("ticket") and outage["ticket"] in (result.get("reply") or ""):
            cited.append("OUTAGE")
        draft = {"intent": result.get("intent"), "reply": result.get("reply"),
                 "needs_human": result["needs_human"],
                 "escalation_reason": "Model requested review" if result["needs_human"] else "",
                 "cited_sources": cited}
        output = direct_output(lab, config, run_input, draft, provider="version-b", model=config["model"])
        latency = float(result.get("seconds") or time.monotonic() - started)
        span = Span(id="draft", parent=None, kind="model_call", name="Version B draft", status="ok",
                    ms=int(latency * 1000), attrs={"system_prompt": system, "user_prompt": user,
                                                   "context_source": context_source,
                                                   "tokens_in": result.get("tokens_in"),
                                                   "tokens_out": result.get("tokens_out")})
        return RunResult(run_id=run_id, version_id=version.id, state="completed", output=output,
                         spans=[span], usage={"latency_s": latency, "cost_usd": None,
                                              "tokens_in": result.get("tokens_in"),
                                              "tokens_out": result.get("tokens_out")})
