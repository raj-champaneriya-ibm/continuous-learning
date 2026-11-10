"""Resolve immutable versions, run adapters, grade, and persist their evidence."""
from __future__ import annotations

import copy
import difflib
import json
import logging
import math
import os
import queue
import threading
import uuid
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from acme.checks import eval_checks
from acme.lab import Lab
from acme.providers import C3_DEFAULT_MODEL
from acme.store import AppSettings
from acme.workflow import _LOG_LOCK

from .adapters import ADAPTERS
from .adapters.common import validate_draft
from .privacy import redact, secret_values
from .runs import RunStore
from .trace import RunInput, RunResult, Span
from .versions import Version, VersionRegistry, case_hash, label_hash

LOG = logging.getLogger(__name__)


def review_record(result: RunResult) -> dict[str, Any]:
    output = result.output or {}
    trace = [{"step": span.attrs["step"], "name": span.name, "kind": span.kind, "status": span.status,
              "detail": span.attrs.get("detail", ""), "ms": span.ms}
             for span in result.spans if "step" in span.attrs]
    return {
        "version_id": result.version_id, "run_id": result.run_id, "state": result.state,
        "pins": result.pins, "case_hash": result.case_hash, "label_hash": result.label_hash,
        "grade": result.grade, "drift": result.drift, "audit": result.audit,
        "thread_id": output.get("thread_id"), "provider": output.get("provider"), "model": output.get("model"),
        "latency_s": result.usage.get("latency_s"), "cost_usd": result.usage.get("cost_usd"),
        "error": next((span.attrs.get("error") for span in result.spans if span.status == "error"), None),
        "model_intent": output.get("intent") if output.get("has_draft") else None,
        "model_needs_human": output.get("needs_human") if output.get("has_draft") else None,
        "escalation_reason": output.get("escalation_reason"), "reply": output.get("reply"),
        "cited_sources": output.get("cited_sources", []), "flags": output.get("flags", []),
        "guard_hits": output.get("guard_hits", []), "decision": output.get("decision"),
        "reasons": output.get("reasons", []), "outcome": output.get("outcome"),
        "final_reply": output.get("final_reply"), "waiting_for_human": result.state == "waiting_for_human",
        "model_called": output.get("model_called", False), "trace": trace,
    }


class SimulationService:
    def __init__(self, studio_root: Path, lab: Lab, settings: AppSettings, *, runs_dir: Path | None = None):
        self.root, self.lab, self.settings = Path(studio_root).resolve(), lab, settings
        self.runs_dir = Path(runs_dir or self.root / "runs")
        self.store = RunStore(self.runs_dir / "simulator.sqlite")
        self.registry = VersionRegistry(self.root, self.store)
        self._adapters: dict[str, Any] = {}
        self._adapter_lock = threading.Lock()
        self._run_locks: dict[str, threading.Lock] = {}
        self._run_locks_lock = threading.Lock()

    @staticmethod
    def _working_model(settings: AppSettings) -> str:
        if settings.provider == "c3":
            return os.environ.get("ACME_C3_MODEL") or C3_DEFAULT_MODEL
        return "rules" if settings.provider == "offline" else settings.model

    def freeze_working(self) -> Version:
        settings, lab = copy.deepcopy(self.settings), copy.deepcopy(self.lab)
        provider = settings.provider
        model = self._working_model(settings)
        manifest: dict[str, Any] = {
            "name": "working-copy", "implementation": "orchestrated", "adapter": "studio-langgraph",
            "inputs": ["customer_id", "message", "portal", "history"],
            "config": {"provider": provider, "model": model, "temperature": 0.0, "max_steps": 6,
                       "timeout_s": 180},
            "knowledge": {"workbook": str(lab.path)},
        }
        if provider == "c3":
            manifest["slots"] = {"draft": {"implementation": "agent_loop", "adapter": "lab-c3",
                                             "model": {"id": model, "temperature": 0.0, "max_steps": 6}}}
        return self.registry.freeze(manifest, lab=lab, settings=settings.workflow)

    def seed_manifests(self) -> list[Version]:
        existing = {(version.name, version.label) for version in self.registry.list()}
        created = []
        for path in sorted((self.root / "workflows").glob("*.yaml")):
            manifest = self.registry.load_manifest(path)
            identity = (manifest.get("name"), str(manifest.get("label") or ""))
            if identity not in existing:
                lab = self.lab if not (manifest.get("knowledge") or {}).get("workbook") else None
                version = self.registry.freeze(manifest, lab=lab)
                existing.add((version.name, version.label))
                created.append(version)
        return created

    def adapter(self, version: Version):
        with self._adapter_lock:
            if version.id not in self._adapters:
                cls = ADAPTERS.get(version.adapter)
                if cls is None:
                    raise ValueError(f"No adapter registered for {version.adapter!r}")
                if cls.implementation != version.implementation:
                    raise ValueError("Adapter does not match the implementation model")
                self._adapters[version.id] = cls(self.registry, self.runs_dir / "checkpoints.sqlite",
                                                 self.runs_dir / "runs.jsonl")
            return self._adapters[version.id]

    def drift(self, version: Version) -> list[str]:
        changed = self.registry.drift(version, current_lab=self.lab)
        if version.name == "working-copy":
            config = version.content["config"]
            if (config["provider"], config["model"]) != (self.settings.provider, self._working_model(self.settings)):
                changed.append("working-copy model")
            if (config["guards"], config["block_on_high_flags"]) != (
                    self.settings.workflow.guards, self.settings.workflow.block_on_high_flags):
                changed.append("working-copy guards")
        return changed

    def status(self, version_id: str, *, audit: bool = False, recorded: bool = False) -> tuple[bool, str]:
        version = self.registry.get(version_id)
        if version.status == "legacy":
            return False, "This legacy round has unknown pins and is available for review only."
        if version.status == "retired" and not audit:
            return False, "This version is retired; it can only run as an audit."
        drift = self.drift(version)
        if version.status == "released" and drift and not audit:
            return False, "Released version has drifted. Run as audit to proceed: " + ", ".join(drift)
        try:
            adapter = self.adapter(version)
            if recorded:
                return (True, "Recorded replay available.") if adapter.capabilities(version).recorded_replay else (
                    False, "This adapter does not support recorded replay.")
            return adapter.status(version)
        except (ValueError, OSError) as exc:
            return False, str(exc)

    def _secrets(self, version: Version) -> tuple[str, ...]:
        names = ["LLM_API_KEY", "LLM_ANTHROPIC_KEY"]
        auth = version.content["config"].get("auth")
        if auth:
            names.append(auth.removeprefix("env:"))
        return secret_values(*names)

    @staticmethod
    def _check_input(run_input: RunInput) -> None:
        if not isinstance(run_input.customer_id, str) or not run_input.customer_id.strip():
            raise ValueError("Customer id is required")
        if not isinstance(run_input.message, str) or not run_input.message.strip():
            raise ValueError("A customer message is required")
        if not isinstance(run_input.history, list) or not all(
                isinstance(turn, dict) and turn.get("role") in {"customer", "assistant"}
                and isinstance(turn.get("text"), str) for turn in run_input.history):
            raise ValueError("History must contain customer or assistant text turns")

    @staticmethod
    def _validate(result: RunResult, version_id: str, run_id: str) -> None:
        if result.version_id != version_id or result.run_id != run_id:
            raise ValueError("Adapter returned a different run or version id")
        if result.state not in {"completed", "waiting_for_human", "failed"}:
            raise ValueError("Adapter returned an invalid state")
        ids = {span.id for span in result.spans}
        if len(ids) != len(result.spans) or any(span.parent and span.parent not in ids for span in result.spans):
            raise ValueError("Adapter returned duplicate spans or missing parents")
        parents = {span.id: span.parent for span in result.spans}
        for span in result.spans:
            visited = {span.id}
            parent = span.parent
            while parent:
                if parent in visited:
                    raise ValueError("Adapter returned a cyclic span tree")
                visited.add(parent)
                parent = parents[parent]
        if result.state != "failed":
            validate_draft(result.output)
            if result.output.get("decision") not in {"send", "escalate"}:
                raise ValueError("Adapter returned an invalid routing decision")

    def _grade(self, result: RunResult, run_input: RunInput, version: Version) -> None:
        if result.state != "completed" or not result.output:
            return
        record = review_record(result)
        if run_input.case:
            result.grade = {"eval": eval_checks(run_input.case, record), "eval_status": "graded"}
        else:
            result.grade = {"eval": None, "eval_status": "no label for free-form input"}
        try:
            from lab.acme import customer_text, use_data_root
            from lab.evals import policy_violations
        except ModuleNotFoundError as exc:
            result.grade.update(policy=None, policy_status=f"lab unavailable: {exc}")
            return
        case = run_input.case or {"message": run_input.message, "history": run_input.history}
        with use_data_root(self.registry.lab_data(version)):
            result.grade.update(policy=policy_violations(result.output.get("reply") or "",
                                                         customer_id=run_input.customer_id,
                                                         asked=customer_text(case)),
                                policy_status="graded")

    @staticmethod
    def _failure(run_id: str, version_id: str, exc: Exception) -> RunResult:
        message = f"{type(exc).__name__}: {exc}"
        return RunResult(run_id=run_id, version_id=version_id, state="failed",
                         spans=[Span(id="error", parent=None, kind="check", name="Run failed",
                                     status="error", ms=0, attrs={"error": message})])

    def _execute(self, version: Version, run_id: str, fn) -> RunResult:
        results: queue.Queue[tuple[RunResult | None, Exception | None]] = queue.Queue(maxsize=1)
        cancelled = threading.Event()

        def worker():
            try:
                results.put((fn(cancelled), None))
            except Exception as exc:  # adapter errors are persisted as failed runs
                LOG.warning("Simulator run %s failed: %s", run_id, type(exc).__name__)
                results.put((None, exc))

        threading.Thread(target=worker, daemon=True, name=f"sim-{run_id[:8]}").start()
        try:
            result, error = results.get(timeout=version.content["config"]["timeout_s"])
        except queue.Empty:
            cancelled.set()
            return self._failure(run_id, version.id,
                                 TimeoutError(f"Run exceeded {version.content['config']['timeout_s']} seconds"))
        if error is not None:
            return self._failure(run_id, version.id, error)
        if result is None:
            return self._failure(run_id, version.id, RuntimeError("Adapter returned no result"))
        try:
            self._validate(result, version.id, run_id)
        except Exception as exc:  # malformed adapter results are persisted as failed runs
            return self._failure(run_id, version.id, exc)
        return result

    def run(self, version_id: str, run_input: RunInput, *, audit: bool = False, sample: int = 0,
            batch_id: str | None = None, replay_of: str | None = None) -> RunResult:
        self._check_input(run_input)
        version = self.registry.get(version_id)
        ready, message = self.status(version_id, audit=audit, recorded=bool(replay_of))
        if not ready:
            raise ValueError(message)
        adapter = self.adapter(version)
        fingerprint = case_hash(asdict(run_input))
        recorded = None
        if replay_of:
            previous, _ = self.store.get(replay_of)
            if previous.version_id != version_id or previous.case_hash != fingerprint:
                raise ValueError("Recorded replay needs the same version and input")
            recorded = next((span.attrs["recorded_response"] for span in previous.spans
                             if "recorded_response" in span.attrs), None)
            if recorded is None:
                raise ValueError("The selected run has no recorded model response")
        drift = self.drift(version)
        run_id = uuid.uuid4().hex
        pending = RunResult(run_id=run_id, version_id=version_id, state="queued", pins=version.pins,
                            case_hash=fingerprint, label_hash=label_hash(run_input.case), drift=drift,
                            sample=sample, batch_id=batch_id, replay_of=replay_of, audit=audit)
        self.store.save(pending, run_input, secrets=self._secrets(version))
        pending.state = "running"
        self.store.save(pending, run_input, secrets=self._secrets(version))
        result = self._execute(version, run_id,
                               lambda cancelled: adapter.start(version, run_input, run_id, sample=sample,
                                                               recorded=recorded, cancelled=cancelled))
        result.pins, result.case_hash, result.label_hash, result.drift = (
            version.pins, fingerprint, pending.label_hash, drift)
        result.sample, result.batch_id, result.replay_of, result.audit = sample, batch_id, replay_of, audit
        try:
            self._grade(result, run_input, version)
        except Exception as exc:  # grading failures must be visible, not reported as passing evidence
            LOG.warning("Grading simulator run %s failed: %s", run_id, type(exc).__name__)
            failed = self._failure(run_id, version_id, exc)
            failed.output, failed.spans = result.output, result.spans + failed.spans
            failed.pins, failed.case_hash, failed.label_hash, failed.drift = (
                version.pins, fingerprint, pending.label_hash, drift)
            failed.sample, failed.batch_id, failed.replay_of, failed.audit = sample, batch_id, replay_of, audit
            result = failed
        return self.store.save(result, run_input, secrets=self._secrets(version))

    def run_samples(self, version_id: str, run_input: RunInput, count: int, *, audit: bool = False) -> list[RunResult]:
        if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= 100:
            raise ValueError("Samples must be an integer between 1 and 100")
        batch_id = uuid.uuid4().hex
        return [self.run(version_id, run_input, audit=audit, sample=sample, batch_id=batch_id)
                for sample in range(count)]

    def apply_retention(self, days: int) -> tuple[int, int]:
        if days < 1:
            raise ValueError("Retention must be at least one day")
        removed = self.store.purge_older_than(days, checkpoints=self.runs_dir / "checkpoints.sqlite")
        log_path = self.runs_dir / "runs.jsonl"
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        log_removed = 0
        with _LOG_LOCK:
            if log_path.exists():
                kept = []
                for number, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), 1):
                    if not line.strip():
                        continue
                    try:
                        stamp = datetime.fromisoformat(json.loads(line)["at"]).astimezone(timezone.utc)
                    except (ValueError, KeyError, TypeError) as exc:
                        raise ValueError(f"Cannot apply retention: invalid log timestamp on line {number}") from exc
                    if stamp < cutoff:
                        log_removed += 1
                    else:
                        kept.append(line)
                temp = log_path.with_name(f".{log_path.name}.{uuid.uuid4().hex}.tmp")
                try:
                    temp.write_text("".join(line + "\n" for line in kept), encoding="utf-8")
                    os.replace(temp, log_path)
                finally:
                    temp.unlink(missing_ok=True)
        return removed, log_removed

    def resume(self, run_id: str, decision: dict[str, Any]) -> RunResult:
        with self._run_locks_lock:
            lock = self._run_locks.setdefault(run_id, threading.Lock())
        with lock:
            previous, run_input = self.store.get(run_id)
            if previous.state != "waiting_for_human":
                raise ValueError("Only a held run can be resumed")
            version = self.registry.get(previous.version_id)
            if version.status == "retired":
                raise ValueError("This run remains held because its version was retired")
            ready, message = self.status(version.id, audit=previous.audit)
            if not ready:
                raise ValueError(f"This run remains held: {message}")
            adapter = self.adapter(version)
            result = self._execute(version, run_id, lambda cancelled: adapter.resume(
                version, run_id, decision, cancelled=cancelled))
            result.pins, result.case_hash, result.label_hash = previous.pins, previous.case_hash, previous.label_hash
            result.drift = self.drift(version)
            result.sample, result.batch_id, result.replay_of, result.audit = (
                previous.sample, previous.batch_id, previous.replay_of, previous.audit)
            try:
                self._grade(result, run_input, version)
            except Exception as exc:
                failed = self._failure(run_id, version.id, exc)
                failed.output, failed.spans = result.output, result.spans + failed.spans
                failed.pins, failed.case_hash, failed.label_hash = previous.pins, previous.case_hash, previous.label_hash
                failed.drift, failed.audit = result.drift, previous.audit
                result = failed
            return self.store.save(result, run_input, secrets=self._secrets(version))


def sample_spread(results: list[RunResult]) -> dict[str, Any]:
    checks = [r.grade.get("eval") for r in results if r.grade.get("eval") is not None]
    passed = sum(1 for item in checks if item.get("routing_ok") is True and item.get("intent_ok") is True
                 and not item.get("missing") and not item.get("banned"))
    n = len(checks)
    if not n:
        return {"passed": 0, "graded": 0, "total": len(results), "rate": None, "interval": None}
    p, z = passed / n, 1.96
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return {"passed": passed, "graded": n, "total": len(results), "rate": p,
            "interval": (max(0.0, center - half), min(1.0, center + half))}


def compare_reviews(cases: list[dict], current: dict[str, dict], baseline: dict[str, dict]) -> list[dict[str, Any]]:
    """Compare saved evidence, with newly missed escalations and regressions first."""
    def verdict(record: dict) -> str:
        if record.get("verdict") in {"Pass", "Fail"}:
            return record["verdict"]
        checks = (record.get("grade") or {}).get("eval")
        if not checks:
            return "—"
        failed = (checks.get("intent_ok") is False or checks.get("routing_ok") is False
                  or checks.get("missing") or checks.get("banned"))
        return "Fail (auto)" if failed else "Pass (auto)"

    rows = []
    for case in cases:
        old, new = baseline.get(case["id"], {}), current.get(case["id"], {})
        if not old and not new:
            continue
        old_verdict, new_verdict = verdict(old), verdict(new)
        missed = bool(case["needs_human"] and new.get("decision") == "send"
                      and old.get("decision") in {"send", "escalate"} and old["decision"] != "send")
        regressed = old_verdict.startswith("Pass") and new_verdict.startswith("Fail")
        improved = old_verdict.startswith("Fail") and new_verdict.startswith("Pass")
        rows.append({"case_id": case["id"], "baseline": old_verdict, "current": new_verdict,
                     "baseline_decision": old.get("decision") or "—", "decision": new.get("decision") or "—",
                     "change": "Missed escalation" if missed else "Regression" if regressed else
                               "Improvement" if improved else "No regression",
                     "priority": 0 if missed else 1 if regressed else 2 if improved else 3})
    return sorted(rows, key=lambda row: (row["priority"], row["case_id"]))


def compare_results(left: RunResult, right: RunResult) -> dict[str, Any]:
    if left.case_hash != right.case_hash:
        raise ValueError("Only runs of the same input can be compared")
    a, b = left.output or {}, right.output or {}
    fields = ("decision", "reasons", "intent", "reply")
    differences = {field: {"left": a.get(field), "right": b.get(field)}
                   for field in fields if a.get(field) != b.get(field)}
    differences["grade"] = {"left": left.grade, "right": right.grade}
    differences["usage"] = {"left": left.usage, "right": right.usage}
    differences["reply_diff"] = list(difflib.ndiff((a.get("reply") or "").split(), (b.get("reply") or "").split()))
    return differences


def manifest_diff(left: Version, right: Version) -> list[dict[str, Any]]:
    changes = []
    for key in ("implementation", "adapter"):
        if left.content.get(key) != right.content.get(key):
            changes.append({"field": key, "left": left.content.get(key), "right": right.content.get(key)})
    for key in ("provider", "model", "temperature", "max_steps", "guards", "block_on_high_flags"):
        a, b = left.content["config"].get(key), right.content["config"].get(key)
        if a != b:
            changes.append({"field": key, "left": a, "right": b})
    for key in ("topology", "prompt:system", "workbook", "lab_files", "code", "slot:draft"):
        a, b = left.pins.get(key), right.pins.get(key)
        if a != b:
            changes.append({"field": key, "left": a, "right": b})
    return redact(changes)
