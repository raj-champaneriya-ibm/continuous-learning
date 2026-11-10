"""SQLite persistence for immutable version content and simulator runs."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from .privacy import redact
from .trace import RunInput, RunResult


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RunStore:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS versions (
                    id TEXT PRIMARY KEY, content TEXT NOT NULL, label TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL, created_at TEXT NOT NULL, signed_off_by TEXT
                );
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY, version_id TEXT NOT NULL REFERENCES versions(id),
                    case_id TEXT NOT NULL, state TEXT NOT NULL, input TEXT NOT NULL,
                    result TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS runs_version_case ON runs(version_id, case_id, created_at);
            """)

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.path, timeout=30)
        try:
            db.row_factory = sqlite3.Row
            db.execute("PRAGMA foreign_keys = ON")
            db.execute("PRAGMA busy_timeout = 30000")
            with db:
                yield db
        finally:
            db.close()

    def put_version(self, version_id: str, content: dict[str, Any], *, label: str = "",
                    status: str = "snapshot") -> None:
        serialized = _json(content)
        with self._connect() as db:
            existing = db.execute("SELECT content FROM versions WHERE id = ?", (version_id,)).fetchone()
            if existing and existing["content"] != serialized:
                raise ValueError(f"Version id collision for {version_id}")
            if not existing:
                db.execute("INSERT INTO versions(id, content, label, status, created_at) VALUES (?, ?, ?, ?, ?)",
                           (version_id, serialized, label, status, _now()))
            elif label:
                db.execute("UPDATE versions SET label = CASE WHEN label = '' THEN ? ELSE label END, "
                           "status = CASE WHEN status = 'snapshot' THEN ? ELSE status END WHERE id = ?",
                           (label, status, version_id))

    def version(self, version_id: str) -> dict[str, Any]:
        with self._connect() as db:
            row = db.execute("SELECT * FROM versions WHERE id = ?", (version_id,)).fetchone()
        if row is None:
            raise KeyError(f"Unknown version {version_id!r}")
        return {**dict(row), "content": json.loads(row["content"])}

    def versions(self, *, include_components: bool = False) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute("SELECT * FROM versions ORDER BY (label = ''), created_at DESC").fetchall()
        result = [{**dict(row), "content": json.loads(row["content"])} for row in rows]
        return result if include_components else [row for row in result if row["status"] != "component"]

    def set_version_status(self, version_id: str, status: str, *, label: str | None = None,
                           signed_off_by: str | None = None) -> None:
        transitions = {"snapshot": {"candidate"}, "candidate": {"released", "retired"},
                       "released": {"retired"}, "retired": set(), "component": set()}
        with self._connect() as db:
            row = db.execute("SELECT status, label FROM versions WHERE id = ?", (version_id,)).fetchone()
            if row is None:
                raise KeyError(f"Unknown version {version_id!r}")
            if status not in transitions[row["status"]]:
                raise ValueError(f"Cannot change version from {row['status']} to {status}")
            new_label = label if label is not None else row["label"]
            if status == "candidate" and not new_label.strip():
                raise ValueError("A candidate needs a label")
            if status == "released" and not (signed_off_by or "").strip():
                raise ValueError("A release needs a reviewer sign-off")
            db.execute("UPDATE versions SET status = ?, label = ?, signed_off_by = ? WHERE id = ?",
                       (status, new_label, signed_off_by, version_id))

    def save(self, result: RunResult, run_input: RunInput, *, secrets: tuple[str, ...] = ()) -> RunResult:
        safe_result = redact(result.as_dict(), secrets=secrets)
        safe_input = redact(run_input.__dict__, secrets=secrets)
        now = _now()
        with self._connect() as db:
            existing = db.execute("SELECT version_id FROM runs WHERE id = ?", (result.run_id,)).fetchone()
            if existing and existing["version_id"] != result.version_id:
                raise ValueError("A run cannot change versions")
            db.execute("""
                INSERT INTO runs(id, version_id, case_id, state, input, result, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET state = excluded.state, input = excluded.input,
                    result = excluded.result, updated_at = excluded.updated_at
            """, (result.run_id, result.version_id, run_input.case_id, result.state,
                  _json(safe_input), _json(safe_result), now, now))
        return RunResult.from_dict(safe_result)

    def get(self, run_id: str) -> tuple[RunResult, RunInput]:
        with self._connect() as db:
            row = db.execute("SELECT result, input FROM runs WHERE id = ?", (run_id,)).fetchone()
        if row is None:
            raise KeyError(f"Unknown run {run_id!r}")
        return RunResult.from_dict(json.loads(row["result"])), RunInput(**json.loads(row["input"]))

    def list(self, *, version_id: str | None = None, case_id: str | None = None,
             limit: int = 100) -> list[RunResult]:
        clauses, args = [], []
        if version_id is not None:
            clauses.append("version_id = ?")
            args.append(version_id)
        if case_id is not None:
            clauses.append("case_id = ?")
            args.append(case_id)
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        with self._connect() as db:
            rows = db.execute("SELECT result FROM runs" + where + " ORDER BY created_at DESC LIMIT ?",
                              (*args, limit)).fetchall()
        return [RunResult.from_dict(json.loads(row["result"])) for row in rows]

    def purge_older_than(self, days: int, *, checkpoints: Path | None = None) -> int:
        if days < 1:
            raise ValueError("Retention must be at least one day")
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        with self._connect() as db:
            attached = checkpoints is not None and checkpoints.is_file()
            if attached:
                db.execute("ATTACH DATABASE ? AS checkpoint_store", (str(checkpoints),))
            db.execute("BEGIN IMMEDIATE")
            rows = db.execute("SELECT id, version_id FROM runs WHERE updated_at < ? AND state NOT IN "
                              "('queued', 'running', 'waiting_for_human')", (cutoff,)).fetchall()
            if attached:
                tables = {row["name"] for row in db.execute(
                    "SELECT name FROM checkpoint_store.sqlite_master WHERE type = 'table'")}
                threads = [(f"{row['version_id']}:{row['id']}",) for row in rows]
                for table in ("writes", "checkpoints"):
                    if table in tables:
                        db.executemany(f"DELETE FROM checkpoint_store.{table} WHERE thread_id = ?", threads)
            cursor = db.execute("DELETE FROM runs WHERE updated_at < ? AND state NOT IN "
                                "('queued', 'running', 'waiting_for_human')", (cutoff,))
            return cursor.rowcount

    def collect_unreferenced_snapshots(self, review_versions: Iterable[str] = ()) -> list[str]:
        protected = set(review_versions)
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            rows = db.execute("SELECT id FROM versions WHERE status = 'snapshot' AND NOT EXISTS "
                              "(SELECT 1 FROM runs WHERE runs.version_id = versions.id)").fetchall()
            removed = [row["id"] for row in rows if row["id"] not in protected]
            db.executemany("DELETE FROM versions WHERE id = ?", ((version_id,) for version_id in removed))
            return removed
