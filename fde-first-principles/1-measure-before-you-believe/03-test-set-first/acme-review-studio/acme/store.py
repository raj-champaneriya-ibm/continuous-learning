"""Small JSON stores in runs/: the latest run + SME review per (version, case), and app settings."""
from __future__ import annotations

import json
import threading
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .workflow import Settings

REVIEW_FIELDS = ("verdict", "failure_mode", "critique", "reviewed_at", "judge_verdict")


class ReviewStore:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._lock = threading.Lock()
        self._data: dict[str, dict] = json.loads(self.path.read_text("utf-8")) if self.path.exists() else {}

    @staticmethod
    def version_id(version: int | str) -> str:
        value = str(version)
        return f"legacy-round-{int(value)}" if value.isdigit() else value

    @classmethod
    def key(cls, version: int | str, case_id: str) -> str:
        return f"{cls.version_id(version)}:{case_id}"

    @staticmethod
    def _record_version(key: str, record: dict) -> str:
        return record.get("version_id") or ReviewStore.version_id(key.split(":", 1)[0])

    def get(self, version: int | str, case_id: str) -> dict:
        version_id = self.version_id(version)
        record = self._data.get(self.key(version_id, case_id))
        if record is None and version_id.startswith("legacy-round-"):
            record = self._data.get(f"{version_id.removeprefix('legacy-round-')}:{case_id}")
        return {**record, "version_id": version_id} if record else {}

    def version(self, version: int | str) -> dict[str, dict]:
        version_id = self.version_id(version)
        return {record["case_id"]: {**record, "version_id": version_id}
                for key, record in self._data.items() if self._record_version(key, record) == version_id}

    def versions(self) -> list[str]:
        return sorted({self._record_version(key, record) for key, record in self._data.items()})

    def round(self, rnd: int) -> dict[str, dict]:
        return {v["case_id"]: dict(v) for v in self.all() if int(v.get("round") or 0) == int(rnd)}

    def rounds(self) -> list[int]:
        return sorted({int(v["round"]) for v in self._data.values() if v.get("round")})

    def all(self) -> list[dict]:
        return [{**record, "version_id": self._record_version(key, record)} for key, record in self._data.items()]

    def _round_for(self, version: int | str) -> int:
        version_id = self.version_id(version)
        if version_id.startswith("legacy-round-") and version_id.removeprefix("legacy-round-").isdigit():
            return int(version_id.removeprefix("legacy-round-"))
        for key, record in self._data.items():
            if self._record_version(key, record) == version_id and record.get("round"):
                return int(record["round"])
        return max(self.rounds(), default=0) + 1

    def _move_legacy(self, version_id: str, case_id: str) -> None:
        if version_id.startswith("legacy-round-"):
            old_key = f"{version_id.removeprefix('legacy-round-')}:{case_id}"
            self._data.pop(old_key, None)

    def save_run(self, version: int | str, case_id: str, record: dict):
        """A new draft replaces the old one, and the old verdict no longer applies to it."""
        with self._lock:
            version_id = self.version_id(version)
            old = self.get(version_id, case_id)
            new = {**record, "round": self._round_for(version_id), "case_id": case_id, "version_id": version_id}
            if old.get("verdict"):
                new["previous_verdict"] = {k: old.get(k) for k in REVIEW_FIELDS}
            self._move_legacy(version_id, case_id)
            self._data[self.key(version_id, case_id)] = new
            self._flush()

    def save_review(self, version: int | str, case_id: str, **review):
        with self._lock:
            version_id = self.version_id(version)
            entry = self.get(version_id, case_id) or {"round": self._round_for(version_id), "case_id": case_id,
                                                       "version_id": version_id}
            entry.update(review, reviewed_at=datetime.now().isoformat(timespec="seconds"))
            self._move_legacy(version_id, case_id)
            self._data[self.key(version_id, case_id)] = entry
            self._flush()

    def import_rows(self, rows: list[dict]):
        with self._lock:
            for r in rows:
                version_id = r.get("version_id") or self.version_id(r["round"])
                self._data.setdefault(self.key(version_id, r["case_id"]), {**r, "version_id": version_id})
            self._flush()

    def _flush(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._data, ensure_ascii=False, indent=1), "utf-8")
        tmp.replace(self.path)


class AppSettings:
    """Provider, model, round and guardrails, kept between app restarts."""

    def __init__(self, path: Path):
        self.path = Path(path)
        raw = json.loads(self.path.read_text("utf-8")) if self.path.exists() else {}
        self.provider = raw.get("provider", "offline")
        self.model = raw.get("model", "sonnet")
        self.round = int(raw.get("round", 1))
        self.concurrency = int(raw.get("concurrency", 3))
        self.critique_first = bool(raw.get("critique_first", True))
        self.run_retention_days = int(raw.get("run_retention_days", 0))
        defaults = Settings()
        self.workflow = Settings(guards=raw.get("guards", defaults.guards),
                                 block_on_high_flags=raw.get("block_on_high_flags", True))

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({
            "provider": self.provider, "model": self.model, "round": self.round, "concurrency": self.concurrency,
            "critique_first": self.critique_first, "run_retention_days": self.run_retention_days,
            **asdict(self.workflow)}, ensure_ascii=False, indent=1), "utf-8")
