"""Version lifecycle, migration, privacy and isolation regressions."""
import copy
import json
import shutil
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from acme.lab import export_to_excel, load_lab, read_review_log
from acme.providers import OfflineProvider
from acme.sim.service import SimulationService, compare_reviews
from acme.sim.trace import RunInput
from acme.store import AppSettings, ReviewStore

ROOT = Path(__file__).parents[1]
WORKBOOK = ROOT / "data" / "Acme_Fibre_Grounded_Draft_Eval.xlsx"


@pytest.fixture
def service(tmp_path):
    lab = load_lab(WORKBOOK)
    return SimulationService(ROOT, lab, AppSettings(tmp_path / "settings.json"), runs_dir=tmp_path / "runs")


def test_legacy_reviews_migrate_and_round_trip_through_excel(tmp_path):
    path = tmp_path / "reviews.json"
    path.write_text(json.dumps({
        "1:c07": {"round": 1, "case_id": "c07", "reply": "Legacy draft", "verdict": "Pass"},
        "2:c01": {"round": 2, "case_id": "c01", "reply": "Second draft"},
    }), encoding="utf-8")
    store = ReviewStore(path)
    assert store.get("legacy-round-1", "c07")["reply"] == "Legacy draft"
    store.save_review(1, "c07", verdict="Fail", critique="Needs review")
    store.save_run("abcdef123456", "c07", {"reply": "Versioned draft", "decision": "escalate"})
    stored = json.loads(path.read_text(encoding="utf-8"))
    assert "1:c07" not in stored
    assert stored["legacy-round-1:c07"]["verdict"] == "Fail"
    assert stored["abcdef123456:c07"]["round"] == 3

    workbook = tmp_path / "copy.xlsx"
    shutil.copy2(WORKBOOK, workbook)
    export_to_excel(load_lab(workbook), store.all(), workbook)
    rows = read_review_log(workbook)
    legacy = [row for row in rows if row["case_id"] == "c07" and row["version_id"] == "legacy-round-1"]
    versioned = [row for row in rows if row["case_id"] == "c07" and row["version_id"] == "abcdef123456"]
    assert len(legacy) == len(versioned) == 1
    assert (legacy[0]["verdict"], legacy[0]["critique"]) == ("Fail", "Needs review")
    assert versioned[0]["reply"] == "Versioned draft"


def test_snapshot_collection_preserves_runs_and_reviews(service, tmp_path):
    in_run = service.freeze_working()
    run = service.run(in_run.id, RunInput(customer_id=next(iter(service.lab.customers)), message="What is my bill?"))
    service.lab.kb["KB01"]["text"] += " Reviewed snapshot."
    in_review = service.freeze_working()
    service.registry.lab_data(in_review)
    reviews = ReviewStore(tmp_path / "reviews.json")
    reviews.save_review(in_review.id, "c01", verdict="Pass")
    service.lab.kb["KB01"]["text"] += " Unused snapshot."
    unused = service.freeze_working()
    unused_path = service.registry.lab_data(unused).parent

    assert service.registry.collect_unreferenced_snapshots(reviews.versions()) == 1
    assert service.store.get(run.run_id)[0].version_id == in_run.id
    assert service.registry.get(in_review.id).id == in_review.id
    with pytest.raises(KeyError):
        service.registry.get(unused.id)
    assert not unused_path.exists()


def test_retention_removes_expired_runs_and_checkpoints_but_keeps_held_runs(service):
    version = service.freeze_working()
    customer = next(iter(service.lab.customers))
    complete = service.run(version.id, RunInput(customer_id=customer, message="What is my bill?"))
    held = service.run(version.id, RunInput(customer_id=customer, message="I am sending a legal notice."))
    assert complete.state == "completed" and held.state == "waiting_for_human"
    with sqlite3.connect(service.store.path) as db:
        db.execute("UPDATE runs SET updated_at = '2000-01-01T00:00:00+00:00'")
    log = service.runs_dir / "runs.jsonl"
    with log.open("a", encoding="utf-8") as file:
        file.write(json.dumps({"at": "2000-01-01T00:00:00", "case_id": "old"}) + "\n")

    removed, logs = service.apply_retention(1)
    assert (removed, logs) == (1, 1)
    with pytest.raises(KeyError):
        service.store.get(complete.run_id)
    assert service.store.get(held.run_id)[0].state == "waiting_for_human"
    with sqlite3.connect(service.runs_dir / "checkpoints.sqlite") as db:
        threads = {row[0] for row in db.execute("SELECT DISTINCT thread_id FROM checkpoints")}
    assert f"{version.id}:{complete.run_id}" not in threads
    assert f"{version.id}:{held.run_id}" in threads
    assert all(json.loads(line)["case_id"] != "old" for line in log.read_text().splitlines())


def test_release_requires_current_graded_cases_and_retired_resume_stays_held(service):
    case = service.lab.case("c07")
    version = service.registry.name(service.freeze_working().id, "candidate-1")
    with pytest.raises(ValueError, match="sign-off"):
        service.registry.release(version.id, [case], "")
    with pytest.raises(ValueError, match="missing or stale"):
        service.registry.release(version.id, [case], "Reviewer")
    result = service.run(version.id, RunInput.from_case(case))
    if result.state == "waiting_for_human":
        result = service.resume(result.run_id, {"action": "hold"})
    changed = copy.deepcopy(case)
    changed["expected_intent"] = "other"
    with pytest.raises(ValueError, match="missing or stale"):
        service.registry.release(version.id, [changed], "Reviewer")
    released = service.registry.release(version.id, [case], "Reviewer")
    assert released.status == "released" and released.signed_off_by == "Reviewer"
    held = service.run(version.id, RunInput.from_case(case))
    assert held.state == "waiting_for_human"
    service.registry.retire(version.id)
    with pytest.raises(ValueError, match="retired"):
        service.resume(held.run_id, {"action": "approve"})
    assert service.store.get(held.run_id)[0].state == "waiting_for_human"
    assert not service.status(version.id)[0]
    assert service.status(version.id, audit=True)[0]


def test_adapter_errors_and_timeouts_are_saved(service, monkeypatch):
    manifest = {"name": "timeout", "implementation": "orchestrated", "adapter": "studio-langgraph",
                "config": {"provider": "offline", "timeout_s": 0.05}}
    version = service.registry.freeze(manifest, lab=service.lab, settings=service.settings.workflow)
    adapter = service.adapter(version)
    done = threading.Event()

    def slow(*args, cancelled, **kwargs):
        cancelled.wait(timeout=2)
        done.set()
        return None

    monkeypatch.setattr(adapter, "start", slow)
    run_input = RunInput(customer_id=next(iter(service.lab.customers)), message="What is my bill?")
    timed_out = service.run(version.id, run_input)
    assert timed_out.state == "failed"
    assert "TimeoutError" in timed_out.spans[-1].attrs["error"]
    assert service.store.get(timed_out.run_id)[0].state == "failed"
    assert done.wait(timeout=2)

    monkeypatch.setattr(adapter, "start", lambda *args, **kwargs: {"not": "a RunResult"})
    invalid = service.run(version.id, run_input)
    assert invalid.state == "failed" and invalid.spans[-1].status == "error"
    assert service.store.get(invalid.run_id)[0].state == "failed"


def test_secrets_are_redacted_from_runs_checkpoints_and_logs(service, monkeypatch):
    secret, otp = "synthetic-private-key-xyz", "938271"
    monkeypatch.setenv("LLM_API_KEY", secret)

    def draft(self, system, user, ctx=None):
        return {"output": {"intent": "other", "reply": f"OTP is {otp}; {secret}", "needs_human": True,
                           "escalation_reason": secret, "cited_sources": []},
                "error": None, "latency_s": 0.01, "cost_usd": None, "raw": {"password": secret}}

    monkeypatch.setattr(OfflineProvider, "draft", draft)
    version = service.freeze_working()
    result = service.run(version.id, RunInput(customer_id=next(iter(service.lab.customers)),
                                               message=f"My OTP is {otp}. Please check."))
    assert result.state == "waiting_for_human"
    resumed = service.resume(result.run_id, {"action": "hold"})
    assert resumed.state == "completed"
    for path in (service.store.path, service.runs_dir / "checkpoints.sqlite", service.runs_dir / "runs.jsonl"):
        data = path.read_bytes()
        assert secret.encode() not in data and otp.encode() not in data
    assert "[REDACTED]" in json.dumps(resumed.as_dict())


def test_c3_concurrent_versions_read_their_own_lab_snapshots(service, tmp_path, monkeypatch):
    source = service.registry.lab_root / "data" / "acme"
    data = tmp_path / "lab-data"
    shutil.copytree(source, data)
    manifest = service.registry.load_manifest(ROOT / "workflows" / "c3-agent.yaml")
    manifest["knowledge"] = {"lab_data": str(data)}
    before = service.registry.freeze(manifest, lab=service.lab)
    kb = data / "kb.md"
    text = kb.read_text(encoding="utf-8")
    heading, rest = text.split("\n", 1)
    kb.write_text(heading + "\nSnapshot two marker.\n" + rest, encoding="utf-8")
    after = service.registry.freeze(manifest, lab=service.lab)
    monkeypatch.setenv("LLM_ANTHROPIC_KEY", "scripted-key")

    def chat(messages, **kwargs):
        if not any(item.get("role") == "tool" for item in messages):
            tool = {"function": {"name": "get_article", "arguments": {"article_id": "KB01"}}}
            return {"content": "", "tool_calls": [tool],
                    "message": {"role": "assistant", "content": "", "tool_calls": [tool]},
                    "tokens_in": 1, "tokens_out": 1, "seconds": 0.01}
        content = json.dumps({"intent": "billing", "reply": "The team will check.", "needs_human": False})
        return {"content": content, "tool_calls": [], "message": {"role": "assistant", "content": content},
                "tokens_in": 1, "tokens_out": 1, "seconds": 0.01}

    monkeypatch.setattr("lab.version_c3.chat", chat)
    run_input = RunInput(customer_id=next(iter(service.lab.customers)), message="What is my bill?")
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda version: service.run(version.id, run_input), (before, after)))
    tool_text = [next(span.attrs["result"]["text"] for span in result.spans
                      if span.kind == "tool_call" and span.name == "get_article") for result in results]
    assert "Snapshot two marker." not in tool_text[0]
    assert "Snapshot two marker." in tool_text[1]
    assert "lab:kb.md" in results[0].drift


def test_review_comparison_puts_new_missed_escalations_first():
    cases = [{"id": "c1", "needs_human": True}, {"id": "c2", "needs_human": False}]
    baseline = {"c1": {"decision": "escalate", "verdict": "Pass"},
                "c2": {"decision": "send", "verdict": "Pass"}}
    current = {"c1": {"decision": "send", "verdict": "Fail"},
               "c2": {"decision": "send", "verdict": "Fail"}}
    rows = compare_reviews(cases, current, baseline)
    assert [(row["case_id"], row["change"]) for row in rows] == [
        ("c1", "Missed escalation"), ("c2", "Regression")]
