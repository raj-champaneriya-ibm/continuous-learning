"""Content-addressed workflow versions, snapshots and drift detection."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml
from langgraph.checkpoint.memory import InMemorySaver

from acme.lab import Lab, load_lab
from acme.providers import OfflineProvider
from acme.workflow import PORTALS, Deps, Settings, Workflow, system_prompt

from .privacy import redact
from .network import endpoint_origin
from .runs import RunStore
from .trace import RunInput

_IMPLEMENTATIONS = {"orchestrated", "declarative", "agent_loop", "multi_agent", "api", "custom"}
_INPUTS = {"customer_id", "message", "portal", "history"}
_DATA_SUFFIXES = {".json", ".jsonl", ".md", ".ttl"}
_ENV_REFERENCE = re.compile(r"^env:[A-Za-z_][A-Za-z0-9_]*$")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str).encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def case_hash(case: Any) -> str:
    return digest(canonical(case))


def label_hash(case: dict[str, Any] | None) -> str:
    if not case:
        return ""
    return case_hash({key: case.get(key) for key in ("expected_intent", "needs_human", "must_include", "must_not")})


def lab_snapshot(lab: Lab) -> dict[str, Any]:
    return {"cases": lab.cases, "customers": lab.customers, "outages": lab.outages,
            "kb": lab.kb, "failure_modes": lab.failure_modes}


def _sheet_hashes(lab: Lab) -> dict[str, str]:
    return {f"sheet:{name}": case_hash(content) for name, content in (
        ("Dataset", lab.cases), ("Customers", lab.customers), ("Outages", lab.outages),
        ("Policy_KB", lab.kb), ("Failure_Modes", lab.failure_modes))}


@dataclass(frozen=True)
class Version:
    id: str
    content: dict[str, Any]
    label: str
    status: str
    created_at: str
    signed_off_by: str | None = None

    @property
    def name(self) -> str:
        return self.content["name"]

    @property
    def implementation(self) -> str:
        return self.content["implementation"]

    @property
    def adapter(self) -> str:
        return self.content["adapter"]

    @property
    def pins(self) -> dict[str, Any]:
        return self.content["pins"]


class VersionRegistry:
    def __init__(self, studio_root: Path, store: RunStore, *, lab_root: Path | None = None):
        self.root = Path(studio_root).resolve()
        self.lab_root = Path(lab_root or self.root.parents[2]).resolve()
        if str(self.lab_root) not in sys.path:
            sys.path.append(str(self.lab_root))
        self.repo_root = Path(subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "--show-toplevel"],
            check=True, capture_output=True, text=True
        ).stdout.strip()).resolve()
        self.store = store
        self.artifacts = store.path.parent / "artifacts" / "sha256"
        self.snapshots = store.path.parent / "snapshots"

    def _path_text(self, path: Path) -> str:
        resolved = path.resolve()
        return resolved.relative_to(self.repo_root).as_posix() if resolved.is_relative_to(self.repo_root) else str(resolved)

    def _path(self, value: str, *, base: Path | None = None) -> Path:
        path = Path(value)
        return (path if path.is_absolute() else (base or self.repo_root) / path).resolve()

    def _put_artifact(self, data: bytes) -> str:
        sha = digest(data)
        path = self.artifacts / sha[:2] / sha
        if path.exists():
            if digest(path.read_bytes()) != sha:
                raise ValueError(f"Corrupt artifact {sha}")
            return sha
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(f".{sha}.{uuid.uuid4().hex}.tmp")
        try:
            tmp.write_bytes(data)
            os.chmod(tmp, 0o444)
            os.replace(tmp, path)
        finally:
            tmp.unlink(missing_ok=True)
        return sha

    def _artifact(self, sha: str) -> bytes:
        if not re.fullmatch(r"[a-f0-9]{64}", sha):
            raise ValueError("Invalid artifact hash")
        data = (self.artifacts / sha[:2] / sha).read_bytes()
        if digest(data) != sha:
            raise ValueError(f"Corrupt artifact {sha}")
        return data

    def _git_pin(self) -> dict[str, Any]:
        def git(*args: str) -> bytes:
            return subprocess.run(["git", "-C", str(self.repo_root), *args], check=True,
                                  capture_output=True).stdout

        commit = git("rev-parse", "HEAD").decode().strip()
        status = git("status", "--porcelain=v1", "-z", "--untracked-files=all")
        dirty = bool(status)
        if not dirty:
            return {"commit": commit, "dirty": False, "diff_sha256": None}
        parts = [git("diff", "--binary", "HEAD"), status]
        for item in status.split(b"\0"):
            if item.startswith(b"?? "):
                path = (self.repo_root / os.fsdecode(item[3:])).resolve()
                if path.is_relative_to(self.repo_root) and path.is_file():
                    parts.extend([item[3:], hashlib.sha256(path.read_bytes()).digest()])
        return {"commit": commit, "dirty": True, "diff_sha256": digest(b"\0".join(parts))}

    def _code_files(self) -> list[Path]:
        files = [self.root / "app.py", self.root / "requirements.txt"]
        files.extend((self.root / "acme").rglob("*.py"))
        files.extend((self.lab_root / "lab").glob("*.py"))
        return sorted((p for p in files if p.is_file()), key=str)

    def load_manifest(self, path: Path) -> dict[str, Any]:
        path = Path(path).resolve()
        if not path.is_relative_to(self.root / "workflows"):
            raise ValueError("Manifests must be in the studio's workflows directory")
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Manifest {path.name} must contain a mapping")
        return data

    def _validate(self, manifest: dict[str, Any]) -> None:
        if not isinstance(manifest.get("name"), str) or not manifest["name"].strip():
            raise ValueError("A version needs a name")
        if manifest.get("implementation") not in _IMPLEMENTATIONS:
            raise ValueError("Unknown implementation model")
        if not isinstance(manifest.get("adapter"), str) or not manifest["adapter"]:
            raise ValueError("A version needs a registered adapter")
        inputs = manifest.get("inputs", ["customer_id", "message", "portal", "history"])
        if not isinstance(inputs, list) or not {"customer_id", "message"} <= set(inputs) or set(inputs) - _INPUTS:
            raise ValueError("Inputs must include customer_id and message and use supported field names")
        config = manifest.get("config") or {}
        if not isinstance(config, dict):
            raise ValueError("Version config must be a mapping")
        timeout = config.get("timeout_s", 180)
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not 0 < timeout <= 3600:
            raise ValueError("timeout_s must be between 0 and 3600 seconds")
        auth = config.get("auth")
        if auth is not None and (not isinstance(auth, str) or not _ENV_REFERENCE.fullmatch(auth)):
            raise ValueError("Authentication must reference an environment variable, not a secret")
        if manifest["implementation"] == "api":
            endpoint_origin(config.get("endpoint") or "")
        if redact(manifest) != manifest:
            raise ValueError("Manifests must not contain credentials or customer secrets")

    def freeze(self, manifest: dict[str, Any], *, lab: Lab | None = None, settings: Settings | None = None,
               label: str | None = None) -> Version:
        manifest = json.loads(canonical(manifest))
        self._validate(manifest)
        if manifest["implementation"] == "declarative":
            Workflow._validate_spec(manifest.get("spec"))
        knowledge = manifest.get("knowledge") or {}
        workbook = Path(knowledge.get("workbook") or (lab.path if lab else self.root / "data" /
                        "Acme_Fibre_Grounded_Draft_Eval.xlsx"))
        if not workbook.is_absolute():
            workbook = self.root / workbook
        workbook = workbook.resolve()
        if workbook.suffix.lower() != ".xlsx" or not workbook.is_file():
            raise ValueError(f"Workbook is not an existing .xlsx file: {workbook}")
        lab = lab or load_lab(workbook)
        data_root = Path(knowledge.get("lab_data") or self.lab_root / "data" / "acme")
        if not data_root.is_absolute():
            data_root = self.root / data_root
        data_root = data_root.resolve()
        if not data_root.is_dir():
            raise ValueError(f"Lab data directory does not exist: {data_root}")

        config = dict(manifest.get("config") or {})
        config.setdefault("timeout_s", 180)
        config.setdefault("temperature", 0.0)
        config.setdefault("max_steps", 6)
        if settings is not None:
            config.update(asdict(settings))
        else:
            guards = config.get("guards")
            if isinstance(guards, str):
                guard_path = (self.root / guards).resolve()
                if not guard_path.is_relative_to(self.root) or guard_path.suffix not in {".yaml", ".yml"}:
                    raise ValueError("Guard files must be YAML inside the studio")
                guards = yaml.safe_load(guard_path.read_text(encoding="utf-8"))
            config["guards"] = guards if guards is not None else Settings().guards
            config.setdefault("block_on_high_flags", True)
        if not isinstance(config["guards"], list):
            raise ValueError("guards must be a list")
        if not isinstance(config["block_on_high_flags"], bool):
            raise ValueError("block_on_high_flags must be a boolean")

        slot = (manifest.get("slots") or {}).get("draft") or {}
        slot_model = slot.get("model") or {}
        if slot.get("adapter") == "lab-c3":
            config["provider"] = "c3"
            config["model"] = slot_model.get("id") or config.get("model") or "anthropic:glm-5.3-flash"
            config["temperature"] = slot_model.get("temperature", config["temperature"])
            config["max_steps"] = slot_model.get("max_steps", config["max_steps"])
        config.setdefault("provider", "offline")
        config.setdefault("model", "rules" if config["provider"] == "offline" else "sonnet")
        if not isinstance(config["temperature"], (int, float)) or not 0 <= config["temperature"] <= 2:
            raise ValueError("temperature must be between 0 and 2")
        if isinstance(config["max_steps"], bool) or not isinstance(config["max_steps"], int) or not 1 <= config["max_steps"] <= 100:
            raise ValueError("max_steps must be an integer between 1 and 100")

        code = {self._path_text(path): digest(path.read_bytes()) for path in self._code_files()}
        data_files = {
            path.relative_to(data_root).as_posix(): self._put_artifact(path.read_bytes())
            for path in sorted(data_root.rglob("*"))
            if path.is_file() and path.suffix.lower() in _DATA_SUFFIXES
            and not any(part.startswith(".") for part in path.relative_to(data_root).parts)
        }
        if not data_files:
            raise ValueError(f"No supported lab data files in {data_root}")
        artifacts = {"studio_lab": self._put_artifact(canonical(lab_snapshot(lab))),
                     "workbook": self._put_artifact(workbook.read_bytes()), "lab_files": data_files}
        graph = Workflow(Deps(lab=lab, provider=OfflineProvider()), InMemorySaver()).graph.get_graph()
        topology = {"nodes": sorted(graph.nodes),
                    "edges": sorted((e.source, e.target, bool(e.conditional)) for e in graph.edges)}
        if manifest["implementation"] == "declarative":
            topology = manifest.get("spec") or {}
        if manifest["adapter"] == "lab-version-b":
            from lab.acme import use_data_root
            from lab.version_b import system_prompt as b_system_prompt
            with use_data_root(data_root):
                prompts = {"version-b": b_system_prompt()}
        elif config["provider"] == "c3" or manifest["implementation"] == "agent_loop":
            if str(self.lab_root) not in sys.path:
                sys.path.append(str(self.lab_root))
            from lab.acme import use_data_root
            from lab.version_c3 import system_prompt as c3_system_prompt
            with use_data_root(data_root):
                prompts = {"c3": c3_system_prompt()}
        else:
            prompts = {portal: system_prompt(lab, style) for portal, style in PORTALS.items()}
        pins: dict[str, Any] = {
            "code": self._git_pin(), "code_files": code, "topology": case_hash(topology),
            "model": {key: config[key] for key in ("provider", "model", "temperature", "max_steps")},
            "prompt:system": case_hash(prompts), "guards": case_hash(config["guards"]),
            "block_on_high_flags": config["block_on_high_flags"],
            **_sheet_hashes(lab), "workbook": artifacts["workbook"],
            "lab_files": dict(data_files),
        }
        component = None
        if slot:
            component_content = {"name": manifest["name"] + ":draft", "implementation": slot.get("implementation"),
                                 "adapter": slot.get("adapter"), "model": pins["model"],
                                 "code": pins["code"], "code_files": code, "lab_files": data_files}
            component = digest(canonical(component_content))[:12]
            self.store.put_version(component, component_content, status="component")
            pins["slot:draft"] = component
        resolved = {
            "schema": 1, "name": manifest["name"], "implementation": manifest["implementation"],
            "adapter": manifest["adapter"], "inputs": manifest.get("inputs", sorted(_INPUTS)),
            "config": config, "slots": {**(manifest.get("slots") or {}),
                                         **({"draft_version": component} if component else {})},
            "spec": manifest.get("spec"), "knowledge": {
                "workbook": self._path_text(workbook), "lab_data": self._path_text(data_root)},
            "pins": pins, "artifacts": artifacts,
        }
        version_id = digest(canonical(resolved))[:12]
        display = label if label is not None else str(manifest.get("label") or "")
        self.store.put_version(version_id, resolved, label=display, status="candidate" if display else "snapshot")
        return self.get(version_id)

    def get(self, version_id: str) -> Version:
        row = self.store.version(version_id)
        if row["status"] != "legacy" and digest(canonical(row["content"]))[:12] != version_id:
            raise ValueError(f"Version {version_id} failed its content hash")
        return Version(id=row["id"], content=row["content"], label=row["label"], status=row["status"],
                       created_at=row["created_at"], signed_off_by=row["signed_off_by"])

    def list(self) -> list[Version]:
        return [self.get(row["id"]) for row in self.store.versions()]

    def import_legacy_rounds(self, rounds: list[int]) -> None:
        for rnd in rounds:
            version_id = f"legacy-round-{int(rnd)}"
            content = {"schema": 0, "name": version_id, "implementation": "custom", "adapter": "legacy",
                       "inputs": [], "config": {}, "pins": {"provenance": "unknown"}, "artifacts": {}}
            self.store.put_version(version_id, content, label=version_id, status="legacy")

    def load_lab(self, version: Version) -> Lab:
        data = json.loads(self._artifact(version.content["artifacts"]["studio_lab"]))
        return Lab(path=self._path(version.content["knowledge"]["workbook"]), **data)

    def lab_data(self, version: Version) -> Path:
        target = self.snapshots / version.id / "lab"
        for name, sha in version.content["artifacts"]["lab_files"].items():
            part = Path(name)
            if part.is_absolute() or ".." in part.parts:
                raise ValueError(f"Invalid snapshot path {name!r}")
            source = self.artifacts / sha[:2] / sha
            self._artifact(sha)
            destination = target / part
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                if digest(destination.read_bytes()) != sha:
                    raise ValueError(f"Corrupt snapshot file {name}")
            else:
                try:
                    os.link(source, destination)
                except FileExistsError:
                    if digest(destination.read_bytes()) != sha:
                        raise ValueError(f"Corrupt snapshot file {name}")
        return target

    def drift(self, version: Version, *, current_lab: Lab | None = None) -> list[str]:
        pins, knowledge = version.pins, version.content["knowledge"]
        changed = []
        if self._git_pin() != pins["code"]:
            changed.append("code (commit or working-tree diff)")
        for path, sha in pins["code_files"].items():
            source = self._path(path)
            if not source.is_file() or digest(source.read_bytes()) != sha:
                changed.append(path)
        workbook = self._path(knowledge["workbook"])
        if not workbook.is_file() or digest(workbook.read_bytes()) != pins["workbook"]:
            changed.append(knowledge["workbook"])
        if current_lab is not None and current_lab.path.resolve() == workbook:
            for name, sha in _sheet_hashes(current_lab).items():
                if pins[name] != sha:
                    changed.append(name)
        data_root = self._path(knowledge["lab_data"])
        expected = pins["lab_files"]
        current = {
            p.relative_to(data_root).as_posix(): digest(p.read_bytes())
            for p in data_root.rglob("*")
            if p.is_file() and p.suffix.lower() in _DATA_SUFFIXES
            and not any(part.startswith(".") for part in p.relative_to(data_root).parts)
        } if data_root.is_dir() else {}
        for name in sorted(set(expected) | set(current)):
            if expected.get(name) != current.get(name):
                changed.append(f"lab:{name}")
        return list(dict.fromkeys(changed))

    def name(self, version_id: str, label: str) -> Version:
        self.store.set_version_status(version_id, "candidate", label=label)
        return self.get(version_id)

    def retire(self, version_id: str) -> Version:
        self.store.set_version_status(version_id, "retired")
        return self.get(version_id)

    def release(self, version_id: str, cases: list[dict[str, Any]], signoff: str) -> Version:
        if not signoff.strip():
            raise ValueError("A reviewer sign-off is required")
        if not cases:
            raise ValueError("Release requires a non-empty dataset")
        latest = {}
        for result in self.store.list(version_id=version_id, limit=100000):
            _, run_input = self.store.get(result.run_id)
            latest.setdefault(run_input.case_id, (result, run_input))
        missing = []
        for case in cases:
            evidence = latest.get(case["id"])
            if evidence is None:
                missing.append(case["id"])
                continue
            result, run_input = evidence
            expected_hash = case_hash(asdict(RunInput.from_case(case, run_input.portal)))
            if (result.state != "completed" or result.grade.get("eval_status") != "graded"
                    or not result.grade.get("eval") or result.case_hash != expected_hash
                    or result.label_hash != label_hash(case)):
                missing.append(case["id"])
        if missing:
            raise ValueError(f"Release requires a completed, graded run of the current dataset for every case; "
                             f"missing or stale: {', '.join(missing)}")
        self.store.set_version_status(version_id, "released", signed_off_by=signoff.strip())
        return self.get(version_id)

    def collect_unreferenced_snapshots(self, review_versions: list[str]) -> int:
        removed = self.store.collect_unreferenced_snapshots(review_versions)
        for version_id in removed:
            if not re.fullmatch(r"[a-f0-9]{12}", version_id):
                raise ValueError(f"Invalid snapshot id {version_id!r}")
            path = self.snapshots / version_id
            if path.is_symlink():
                raise ValueError(f"Snapshot directory must not be a symlink: {path}")
            if path.exists():
                shutil.rmtree(path)
        return len(removed)
