"""HTTP adapter allowlisting, redirects, schema checks and redaction."""
import json
import threading
import time
from pathlib import Path

import pytest

from acme.lab import load_lab
from acme.sim.adapters.http import _endpoint
from acme.sim.service import SimulationService
from acme.sim.trace import RunInput
from acme.store import AppSettings

ROOT = Path(__file__).parents[1]


class Response:
    def __init__(self, status=200, *, data=None, location=None, chunks=None):
        self.status_code = status
        self.headers = {"Location": location} if location else {}
        self.chunks = chunks if chunks is not None else [json.dumps(data).encode()]
        self.closed = False

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def iter_content(self, chunk_size):
        yield from self.chunks

    def close(self):
        self.closed = True


class Session:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []
        self.trust_env = True

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.responses.pop(0)

    def close(self):
        pass


@pytest.fixture
def world(tmp_path, monkeypatch):
    lab = load_lab(ROOT / "data" / "Acme_Fibre_Grounded_Draft_Eval.xlsx")
    service = SimulationService(ROOT, lab, AppSettings(tmp_path / "settings.json"), runs_dir=tmp_path / "runs")
    monkeypatch.setenv("ACME_SIM_ALLOWED_HOSTS", "agent.example.com,other.example.com,localhost")
    monkeypatch.setenv("ACME_REMOTE_AGENT_TOKEN", "synthetic-remote-key")
    return {"service": service, "lab": lab}


def version(world, **config):
    manifest = world["service"].registry.load_manifest(ROOT / "workflows" / "remote-agent.yaml")
    manifest["config"].update(config)
    return world["service"].registry.freeze(manifest)


def run(world, frozen):
    case = world["lab"].case("c02")
    return world["service"].run(frozen.id, RunInput.from_case(case))


@pytest.mark.parametrize("url", [
    "https://not-allowed.example/path",
    "http://agent.example.com/path",
    "https://user@agent.example.com/path",
    "https://@agent.example.com/path",
    "https://agent.example.com/path?token=abc",
    "https://agent.example.com/path#fragment",
])
def test_endpoints_reject_untrusted_urls(monkeypatch, url):
    monkeypatch.setenv("ACME_SIM_ALLOWED_HOSTS", "agent.example.com")
    with pytest.raises(ValueError):
        _endpoint(url)


def test_loopback_http_is_allowed_only_when_explicitly_allowlisted(monkeypatch):
    monkeypatch.setenv("ACME_SIM_ALLOWED_HOSTS", "localhost")
    assert _endpoint("http://localhost:9000/draft") == ("http", "localhost", 9000)
    with pytest.raises(ValueError, match="not in ACME_SIM_ALLOWED_HOSTS"):
        _endpoint("http://127.0.0.1:9000/draft")


@pytest.mark.parametrize("endpoint", [
    "https://agent.example.com/draft?token=synthetic-secret",
    "https://user:synthetic-secret@agent.example.com/draft",
    "https://agent.example.com/draft#synthetic-secret",
])
def test_secret_bearing_endpoints_are_rejected_before_freezing(world, endpoint):
    with pytest.raises(ValueError):
        version(world, endpoint=endpoint)
    assert b"synthetic-secret" not in world["service"].store.path.read_bytes()


def test_http_sends_auth_without_persisting_secrets(world, monkeypatch):
    secret = "synthetic-remote-key"
    payload = {"output": {"intent": "billing", "reply": f"Hi Rahul, we will check. OTP is 938271. {secret}",
                          "needs_human": False, "escalation_reason": "", "cited_sources": ["CRM"]},
               "spans": [{"id": "tool", "kind": "tool_call", "name": "lookup", "status": "ok",
                          "attrs": {"api_key": secret}}]}
    session = Session([Response(data=payload)])
    monkeypatch.setattr("acme.sim.adapters.http.requests.Session", lambda: session)
    result = run(world, version(world))
    assert result.state == "completed"
    _, kwargs = session.calls[0]
    assert kwargs["headers"]["Authorization"].endswith(secret)
    assert set(kwargs["json"]) == {"customer_id", "message", "history"}
    assert not session.trust_env
    persisted = json.dumps(result.as_dict())
    assert secret not in persisted and "938271" not in persisted
    assert next(span for span in result.spans if span.id == "remote:tool").attrs["api_key"] == "[REDACTED]"


def test_redirect_cannot_send_auth_to_a_different_allowlisted_origin(world, monkeypatch):
    session = Session([Response(status=307, location="https://other.example.com/steal")])
    monkeypatch.setattr("acme.sim.adapters.http.requests.Session", lambda: session)
    result = run(world, version(world))
    assert result.state == "failed"
    assert "original allowlisted origin" in result.spans[-1].attrs["error"]
    assert len(session.calls) == 1


@pytest.mark.parametrize("payload,cap,error", [
    ({"output": {"reply": "x" * 300}}, 80, "size limit"),
    ({"output": {"intent": "billing", "reply": "hello", "needs_human": "false"}}, 10000, "boolean"),
])
def test_http_rejects_oversized_and_invalid_drafts(world, monkeypatch, payload, cap, error):
    session = Session([Response(data=payload)])
    monkeypatch.setattr("acme.sim.adapters.http.requests.Session", lambda: session)
    result = run(world, version(world, max_response_bytes=cap))
    assert result.state == "failed"
    assert error in result.spans[-1].attrs["error"]
    assert world["service"].store.get(result.run_id)[0].state == "failed"


def test_http_stream_stops_after_timeout(world, monkeypatch):
    closed = threading.Event()

    class SlowResponse(Response):
        def iter_content(self, chunk_size):
            time.sleep(0.15)
            yield b"{}"

        def close(self):
            closed.set()

    session = Session([SlowResponse()])
    monkeypatch.setattr("acme.sim.adapters.http.requests.Session", lambda: session)
    result = run(world, version(world, timeout_s=0.05))
    assert result.state == "failed" and "TimeoutError" in result.spans[-1].attrs["error"]
    assert closed.wait(timeout=2)
