"""Step definitions for features/report_metrics.feature.

Each scenario writes a small runs file like the one Review Studio saves, points the report module at
it and reads it back through reports/acme_metrics.load(), the same call every Quarto page makes.
"""
import json
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

sys.path.insert(0, str(Path(__file__).parents[1] / "reports"))
import acme_metrics as m  # noqa: E402

scenarios("features/report_metrics.feature")

REVIEWABLE = ["c02", "c03", "c04", "c05"]          # don't-escalate cases, used for verdict scenarios


@pytest.fixture
def runs(tmp_path, monkeypatch):
    path = tmp_path / "reviews.json"
    monkeypatch.setattr(m, "RUNS", path)
    return {"path": path, "records": {}}


def save(runs, case_id, rnd=1, **fields):
    record = {"round": rnd, "case_id": case_id, "provider": "scripted", "model": "script", "reply": "",
              "reasons": [], "flags": [], "model_needs_human": None, **fields}
    runs["records"][f"{rnd}:{case_id}"] = {**runs["records"].get(f"{rnd}:{case_id}", {}), **record}
    runs["path"].write_text(json.dumps(runs["records"], ensure_ascii=False), encoding="utf-8")


# ------------------------------------------------------------------ given
@given(parsers.parse('case "{case_id}" was sent automatically'))
def sent(runs, case_id):
    save(runs, case_id, decision="send", model_needs_human=False)


@given(parsers.parse('case "{case_id}" was sent automatically saying "{reply}"'))
def sent_saying(runs, case_id, reply):
    save(runs, case_id, decision="send", model_needs_human=False, reply=reply)


@given(parsers.parse('case "{case_id}" was escalated because "{reason}"'))
def escalated(runs, case_id, reason):
    save(runs, case_id, decision="escalate", reasons=[reason], model_needs_human=reason.startswith("model:"))


@given(parsers.parse('case "{case_id}" was escalated because "{reason}" although the model said no human was needed'))
def escalated_by_code(runs, case_id, reason):
    save(runs, case_id, decision="escalate", reasons=[reason], model_needs_human=False)


@given(parsers.re(r"the expert passed (?P<passed>\d+) repl(?:y|ies) and failed (?P<failed>\d+)"))
def verdicts(runs, passed, failed):
    marks = ["Pass"] * int(passed) + ["Fail"] * int(failed)
    for case_id, verdict in zip(REVIEWABLE, marks):
        save(runs, case_id, decision="send", model_needs_human=False, verdict=verdict,
             failure_mode="" if verdict == "Pass" else "Missing fact")


@given("those verdicts came from the demo script")
def demo(runs):
    for key in runs["records"]:
        runs["records"][key]["verdict_source"] = "demo-auto"
    runs["path"].write_text(json.dumps(runs["records"]), encoding="utf-8")


@given(parsers.parse("round {a:d} and round {b:d} are both saved"))
def two_rounds(runs, a, b):
    save(runs, "c05", rnd=a, decision="send")
    save(runs, "c05", rnd=b, decision="send")


@given("no case has been run")
def nothing(runs):
    assert not runs["path"].exists()


# ------------------------------------------------------------------ when
@when("the reports read the saved runs", target_fixture="ev")
def read(runs):
    return m.load()


@when(parsers.parse("the reports read round {rnd:d}"), target_fixture="ev")
def read_round(runs, rnd):
    return m.load(rnd)


# ------------------------------------------------------------------ then
@then(parsers.re(r"(?P<n>\d+) missed escalations? (?:is|are) reported"))
def missed(ev, n):
    assert len(ev.missed()) == int(n), ev.missed()[["id", "decision", "expected_human"]]


@then(parsers.re(r"(?P<n>\d+) code saves? (?:is|are) reported"))
def code_saves(ev, n):
    assert len(ev.code_saves()) == int(n)


@then(parsers.re(r"(?P<n>\d+) unsafe auto-sends? (?:is|are) reported"))
def unsafe(ev, n):
    assert len(ev.unsafe_sends()) == int(n)


@then(parsers.parse('routing accuracy reads "{text}"'))
def routing(ev, text):
    assert ev.routing_accuracy().text == text


@then(parsers.parse('the pass rate reads "{text}"'))
def pass_rate(ev, text):
    assert ev.pass_rate().text == text


@then(parsers.parse("{n:d} cases count as run"))
def cases_run(ev, n):
    assert len(ev.run) == n


@then(parsers.parse('the "{layer}" layer fired on {n:d} escalation'))
def layer_fired(ev, layer, n):
    lay = ev.layers().set_index("layer")
    assert lay.loc[layer, "fired"] == n
    assert lay.drop(layer).fired.sum() == 0, "a reason was credited to more than one layer"


@then(parsers.parse("the reports show round {rnd:d}"))
def shows_round(ev, rnd):
    assert ev.round == rnd and ev.rounds == [1, 2]


@then(parsers.parse('the page banner warns "{title}"'))
def banner(ev, title):
    assert f"## {title}" in m.banner(ev)


@then("no release gate is met")
def no_gate(ev):
    gates = ev.gates()
    assert not gates.met.any()
    assert (gates.set_index("gate").loc["Expert pass rate (lower end of 95% CI)", "actual"]) == "—"
