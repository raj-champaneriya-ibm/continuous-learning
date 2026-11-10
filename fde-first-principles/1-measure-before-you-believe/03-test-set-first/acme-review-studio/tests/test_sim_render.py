"""Simulator rendering is accessible and treats all trace evidence as data."""
from html.parser import HTMLParser

from acme.sim.render import render_comparison, render_detail, render_result
from acme.sim.trace import Capabilities, RunResult, Span, Topology
from acme.sim.versions import Version


class Elements(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.elements = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def result():
    return RunResult(
        run_id="run", version_id="abcdef123456", state="completed", case_hash="same",
        output={"reply": "<script>alert(1)</script>", "decision": "send", "intent": "other"},
        spans=[
            Span(id="step-5", parent=None, kind="step", name="Draft <b>unsafe</b>", status="ok", ms=2,
                 attrs={"step": "5", "system_prompt": "<script>system</script>", "envelope": {"safe": "<b>"},
                        "recorded_response": {"secret": "not for display"}}),
            Span(id="turn", parent="step-5", kind="model_call", name="Turn 1", status="ok", ms=1),
            Span(id="tool", parent="turn", kind="tool_call", name="<img src=x>", status="error", ms=0,
                 attrs={"result": "<script>tool</script>"}),
        ],
    )


def version(version_id, name):
    return Version(id=version_id, content={"name": name, "implementation": "custom", "adapter": "offline",
                                           "config": {}, "pins": {}},
                   label="", status="candidate", created_at="")


def test_topology_buttons_and_nested_evidence_are_escaped_and_keyboard_accessible():
    run = result()
    topology = Topology(nodes=[{"id": "5", "name": "Draft"}], edges=[])
    markup = render_result(run, topology, "orchestrated", "step-5")
    markup += render_detail(run, "step-5", Capabilities(prompts=True, envelope=True, tool_calls=True))
    nodes = Elements(markup).elements
    buttons = [attrs for tag, attrs in nodes if tag == "button"]
    assert [button["data-step"] for button in buttons] == ["step-5", "turn", "tool"]
    assert all(button["type"] == "button" for button in buttons)
    assert "tool_call · error" in markup and "Nested evidence" in markup
    assert "&lt;script&gt;" in markup and "&lt;img" in markup
    assert not any(tag in {"script", "img"} for tag, _ in nodes)
    assert "not for display" not in markup


def test_capability_panels_and_unknown_implementations_use_span_tree():
    run = result()
    hidden = render_detail(run, "step-5", Capabilities())
    assert "System Prompt" not in hidden and "Envelope" not in hidden
    shown = render_detail(run, "step-5", Capabilities(prompts=True, envelope=True))
    assert "System Prompt" in shown and "Envelope" in shown
    fallback = render_result(run, Topology(), "unrecognized", None)
    assert "Run spans" in fallback and 'data-step="tool"' in fallback


def test_failure_without_a_step_remains_visible_in_the_topology():
    run = RunResult(run_id="failed", version_id="abcdef123456", state="failed",
                    spans=[Span(id="error", parent=None, kind="check", name="Run failed",
                                status="error", ms=0, attrs={"error": "Provider unavailable"})])
    markup = render_result(run, Topology(nodes=[{"id": "5", "name": "Draft"}]), "orchestrated", "error")
    assert 'data-step="error"' in markup and "check · error" in markup
    assert "Provider unavailable" in render_detail(run, "error", Capabilities())


def test_comparison_escapes_manifest_labels_and_reply_diff():
    left = result()
    right = RunResult(run_id="other", version_id="012345abcdef", state="completed", case_hash="same",
                      output={"reply": "<img src=x>", "decision": "escalate", "intent": "billing"})
    markup = render_comparison(left, right, version(left.version_id, "<script>name</script>"),
                               version(right.version_id, "Other"))
    assert "&lt;script&gt;name&lt;/script&gt;" in markup and "&lt;img" in markup
    assert "<ins>" in markup and "<del>" in markup
    assert not any(tag in {"script", "img"} for tag, _ in Elements(markup).elements)
