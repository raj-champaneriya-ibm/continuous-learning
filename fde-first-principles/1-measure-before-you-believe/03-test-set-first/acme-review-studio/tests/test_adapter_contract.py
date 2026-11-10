"""Contract scenarios exercise every registered adapter without a live model or network."""
import json
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from acme.lab import INTENTS, load_lab
from acme.providers import DRAFT_SCHEMA
from acme.sim.adapters import ADAPTERS
from acme.sim.adapters.direct import VersionBAdapter
from acme.sim.service import SimulationService
from acme.sim.trace import SPAN_KINDS, SPAN_STATUSES, RunInput
from acme.store import AppSettings

ROOT = Path(__file__).parents[1]
MANIFESTS = {
    "studio-langgraph": "studio-offline.yaml",
    "spec-langgraph": "studio-declarative.yaml",
    "lab-c3": "c3-agent.yaml",
    "lab-version-b": "version-b.yaml",
    "offline": "offline-direct.yaml",
    "http-json": "remote-agent.yaml",
}
scenarios("features/adapter_contract.feature")


class ScriptedResponse:
    status_code = 200
    headers = {}

    def __init__(self):
        self.body = json.dumps({
            "output": {"intent": "billing", "reply": "Hi Vikram, the team will check.",
                       "needs_human": False, "escalation_reason": "", "cited_sources": ["CRM"]}
        }).encode()

    def raise_for_status(self):
        pass

    def iter_content(self, chunk_size):
        yield self.body

    def close(self):
        pass


class ScriptedSession:
    trust_env = False

    def post(self, url, **kwargs):
        return ScriptedResponse()

    def close(self):
        pass


@pytest.fixture
def world(tmp_path, monkeypatch):
    lab = load_lab(ROOT / "data" / "Acme_Fibre_Grounded_Draft_Eval.xlsx")
    service = SimulationService(ROOT, lab, AppSettings(tmp_path / "settings.json"), runs_dir=tmp_path / "runs")
    from lab import version_b, version_c3

    def chat(messages, **kwargs):
        content = json.dumps({"intent": "billing", "reply": "Hi Vikram, the team will check.",
                              "needs_human": False})
        return {"content": content, "message": {"role": "assistant", "content": content},
                "tool_calls": [], "tokens_in": 12, "tokens_out": 4, "seconds": 0.01}

    monkeypatch.setattr(version_b, "chat", chat)
    monkeypatch.setattr(version_c3, "chat", chat)
    monkeypatch.setattr(VersionBAdapter, "status", lambda self, version: (True, "Scripted"))
    monkeypatch.setattr("acme.sim.adapters.http.requests.Session", ScriptedSession)
    monkeypatch.setenv("LLM_ANTHROPIC_KEY", "scripted-key")
    monkeypatch.setenv("ACME_SIM_ALLOWED_HOSTS", "agent.example.com")
    monkeypatch.setenv("ACME_REMOTE_AGENT_TOKEN", "scripted-token")
    return {"service": service, "lab": lab}


@given(parsers.parse('adapter "{adapter}" has a scripted model'))
def scripted_adapter(world, adapter):
    manifest = world["service"].registry.load_manifest(ROOT / "workflows" / MANIFESTS[adapter])
    world["version"] = world["service"].registry.freeze(manifest)


@when(parsers.parse('the adapter runs dataset case "{case_id}"'))
def run_case(world, case_id):
    world["result"] = world["service"].run(world["version"].id, RunInput.from_case(world["lab"].case(case_id)))


@then("its run has the common draft schema and valid spans")
def valid_contract(world):
    result = world["result"]
    assert result.state in {"completed", "waiting_for_human"}
    assert set(DRAFT_SCHEMA["required"]) <= result.output.keys()
    assert result.output["intent"] in INTENTS
    assert isinstance(result.output["needs_human"], bool)
    assert result.output["decision"] in {"send", "escalate"}
    assert result.spans and all(span.kind in SPAN_KINDS and span.status in SPAN_STATUSES for span in result.spans)


@then("its run retains the frozen version and pins")
def pinned(world):
    assert world["result"].version_id == world["version"].id
    assert world["result"].pins == world["version"].pins
    assert world["service"].store.get(world["result"].run_id)[0].version_id == world["version"].id


def test_contract_outline_covers_every_registered_adapter():
    assert set(MANIFESTS) == set(ADAPTERS)
