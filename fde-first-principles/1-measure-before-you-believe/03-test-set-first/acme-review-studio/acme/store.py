"""Small JSON stores in runs/: the latest run + SME review per (round, case), and app settings."""
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
    def key(rnd: int, case_id: str) -> str:
        return f"{int(rnd)}:{case_id}"

    def get(self, rnd: int, case_id: str) -> dict:
        return dict(self._data.get(self.key(rnd, case_id), {}))

    def round(self, rnd: int) -> dict[str, dict]:
        return {v["case_id"]: dict(v) for v in self._data.values() if int(v["round"]) == int(rnd)}

    def rounds(self) -> list[int]:
        return sorted({int(v["round"]) for v in self._data.values()})

    def all(self) -> list[dict]:
        return [dict(v) for v in self._data.values()]

    def save_run(self, rnd: int, case_id: str, record: dict):
        """A new draft replaces the old one, and the old verdict no longer applies to it."""
        with self._lock:
            old = self._data.get(self.key(rnd, case_id), {})
            new = {"round": int(rnd), "case_id": case_id, **record}
            if old.get("verdict"):
                new["previous_verdict"] = {k: old.get(k) for k in REVIEW_FIELDS}
            self._data[self.key(rnd, case_id)] = new
            self._flush()

    def save_review(self, rnd: int, case_id: str, **review):
        with self._lock:
            entry = self._data.setdefault(self.key(rnd, case_id), {"round": int(rnd), "case_id": case_id})
            entry.update(review, reviewed_at=datetime.now().isoformat(timespec="seconds"))
            self._flush()

    def import_rows(self, rows: list[dict]):
        with self._lock:
            for r in rows:
                self._data.setdefault(self.key(r["round"], r["case_id"]), r)
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
        defaults = Settings()
        self.workflow = Settings(guards=raw.get("guards", defaults.guards),
                                 block_on_high_flags=raw.get("block_on_high_flags", True))

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({
            "provider": self.provider, "model": self.model, "round": self.round, "concurrency": self.concurrency,
            "critique_first": self.critique_first,
            **asdict(self.workflow)}, ensure_ascii=False, indent=1), "utf-8")
