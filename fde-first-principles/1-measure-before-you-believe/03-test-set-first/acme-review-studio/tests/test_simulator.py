"""Version, execution and adapter contract tests, all offline."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from acme.lab import load_lab
from acme.providers import ClaudeCodeProvider
from acme.sim.service import SimulationService, compare_results, review_record
from acme.sim.trace import RunInput
from acme.store import AppSettings

ROOT = Path(__file__).parents[1]


@pytest.fixture
def service(tmp_path):
    lab = load_lab(ROOT / "data" / "Acme_Fibre_Grounded_Draft_Eval.xlsx")
    settings = AppSettings(tmp_path / "settings.json")
    return SimulationService(ROOT, lab, settings, runs_dir=tmp_path / "runs")


def test_working_versions_are_stable_and_pin_unsaved_edits(service):
    first = service.freeze_working()
    same = service.freeze_working()
    assert first.id == same.id
    old = service.registry.load_lab(first).kb["KB01"]["text"]
    service.lab.kb["KB01"]["text"] += " A changed article."
    newer = service.freeze_working()
    assert newer.id != first.id
    assert service.registry.load_lab(first).kb["KB01"]["text"] == old
    assert "sheet:Policy_KB" in service.registry.drift(first, current_lab=service.lab)
    assert newer.pins["workbook"] and newer.pins["lab_files"]["policy.md"]


def test_batch_and_resume_keep_the_original_provider(service):
    version = service.freeze_working()
    customer = next(iter(service.lab.customers))
    inputs = [RunInput(customer_id=customer, message="I am sending a legal notice."),
              RunInput(customer_id=customer, message="What is my bill?")]
    first = service.run(version.id, inputs[0])
    assert first.state == "waiting_for_human"
    service.settings.provider = "c3"
    second = service.run(version.id, inputs[1])
    resumed = service.resume(first.run_id, {"action": "hold"})
    assert first.version_id == second.version_id == resumed.version_id == version.id
    assert resumed.state == "completed"
    assert resumed.output["provider"] == second.output["provider"] == "offline"
    assert resumed.output["outcome"] == "held"
    assert resumed.grade["policy_status"] == "graded"


def test_recorded_replay_and_comparison_use_the_same_input(service):
    version = service.freeze_working()
    case = service.lab.cases[0]
    run_input = RunInput.from_case(case)
    original = service.run(version.id, run_input)
    replay = service.run(version.id, run_input, replay_of=original.run_id)
    assert replay.replay_of == original.run_id
    assert replay.output["reply"] == original.output["reply"]
    assert replay.output["decision"] == original.output["decision"]
    assert [(span.id, span.parent, span.kind, span.status) for span in replay.spans] == [
        (span.id, span.parent, span.kind, span.status) for span in original.spans]
    assert compare_results(original, replay)["grade"]["left"] == original.grade
    with pytest.raises(ValueError, match="same version and input"):
        service.run(version.id, RunInput(customer_id=case["customer_id"], message="Different"), replay_of=original.run_id)


def test_recorded_replay_does_not_require_the_original_provider(service, monkeypatch):
    manifest = {"name": "scripted-claude", "implementation": "orchestrated", "adapter": "studio-langgraph",
                "config": {"provider": "claude-code", "model": "sonnet"}}
    version = service.registry.freeze(manifest, lab=service.lab, settings=service.settings.workflow)
    monkeypatch.setattr(ClaudeCodeProvider, "status", lambda self: (True, "Scripted"))
    monkeypatch.setattr(ClaudeCodeProvider, "draft", lambda self, system, user, ctx=None: {
        "output": {"intent": "billing", "reply": "Thank you. The team will check.", "needs_human": False,
                   "escalation_reason": "", "cited_sources": ["CRM"]},
        "error": None, "latency_s": 0.1, "cost_usd": 0, "raw": {},
    })
    run_input = RunInput.from_case(service.lab.case("c02"))
    original = service.run(version.id, run_input)
    monkeypatch.setattr(ClaudeCodeProvider, "status", lambda self: (False, "Provider is offline"))

    def unexpected_call(*args, **kwargs):
        raise AssertionError("Recorded replay must not call the provider")

    monkeypatch.setattr(ClaudeCodeProvider, "draft", unexpected_call)
    assert not service.status(version.id)[0]
    assert service.status(version.id, recorded=True)[0]
    replay = service.run(version.id, run_input, replay_of=original.run_id)
    assert replay.state == original.state
    assert replay.output["reply"] == original.output["reply"]
    assert replay.output["decision"] == original.output["decision"]


def test_candidate_drift_warns_and_released_drift_requires_audit(service):
    version = service.registry.freeze({
        "name": "candidate", "label": "1.0", "implementation": "orchestrated",
        "adapter": "studio-langgraph", "config": {"provider": "offline"},
    }, lab=service.lab, settings=service.settings.workflow)
    service.lab.kb["KB01"]["text"] += " Changed."
    run_input = RunInput(customer_id=next(iter(service.lab.customers)), message="What is my bill?")
    candidate = service.run(version.id, run_input)
    assert "sheet:Policy_KB" in candidate.drift
    service.store.set_version_status(version.id, "released", signed_off_by="reviewer")
    with pytest.raises(ValueError, match="Run as audit"):
        service.run(version.id, run_input)
    audited = service.run(version.id, run_input, audit=True)
    assert audited.audit and "sheet:Policy_KB" in audited.drift


def test_working_copy_settings_are_drifted_without_changing_the_frozen_drafter(service):
    version = service.registry.name(service.freeze_working().id, "reviewed-copy")
    service.settings.workflow.guards[0]["enabled"] = not service.settings.workflow.guards[0]["enabled"]
    service.settings.provider = "c3"
    run_input = RunInput(customer_id=next(iter(service.lab.customers)), message="What is my bill?")
    candidate = service.run(version.id, run_input)
    assert candidate.output["provider"] == "offline"
    assert {"working-copy guards", "working-copy model"} <= set(candidate.drift)
    service.store.set_version_status(version.id, "released", signed_off_by="reviewer")
    assert not service.status(version.id)[0]
    audited = service.run(version.id, run_input, audit=True)
    assert audited.audit and "working-copy guards" in audited.drift


@pytest.mark.parametrize("filename", ["studio-declarative.yaml", "offline-direct.yaml"])
def test_offline_adapter_contract(service, filename):
    manifest = service.registry.load_manifest(ROOT / "workflows" / filename)
    version = service.registry.freeze(manifest)
    result = service.run(version.id, RunInput.from_case(service.lab.cases[0]))
    assert result.state in {"completed", "waiting_for_human"}
    assert result.version_id == version.id
    assert result.output["intent"] in {"outage", "billing", "speed", "cancel", "upgrade", "relocation", "other"}
    assert all(span.status and span.kind for span in result.spans)
    assert review_record(result)["version_id"] == version.id


def test_c3_nested_turns_and_no_unused_studio_prompt(service, monkeypatch):
    monkeypatch.setenv("LLM_ANTHROPIC_KEY", "not-a-real-key")
    calls = []

    def fake_chat(messages, **kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            tool = {"function": {"name": "lookup_customer", "arguments": {"customer_id": "AC1001"}}}
            return {"content": "", "tool_calls": [tool],
                    "message": {"role": "assistant", "content": "", "tool_calls": [tool]},
                    "tokens_in": 10, "tokens_out": 4, "seconds": 0.1}
        content = json.dumps({"intent": "other", "reply": "Thank you. The team will check.",
                              "needs_human": False})
        return {"content": content, "tool_calls": [], "message": {"role": "assistant", "content": content},
                "tokens_in": 12, "tokens_out": 5, "seconds": 0.1}

    monkeypatch.setattr("lab.version_c3.chat", fake_chat)
    manifest = service.registry.load_manifest(ROOT / "workflows" / "studio-c3.yaml")
    version = service.registry.freeze(manifest)
    customer = next(iter(service.lab.customers))
    result = service.run(version.id, RunInput(customer_id=customer, message="Please check my account."))
    assert result.state in {"completed", "waiting_for_human"}
    assert calls[0]["model"] == "anthropic:glm-5.3-flash"
    assert any(span.kind == "tool_call" and span.parent.startswith("step-5:turn-") for span in result.spans)
    fetch = next(span for span in result.spans if span.id == "step-4")
    assert "user_prompt" not in fetch.attrs
    assert next(span for span in result.spans if span.id == "step-5").attrs["envelope"]
