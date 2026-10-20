"""Step definitions for features/review_flow.feature.

The steps play the part of the Review page: they call the same acme.review functions app.py calls
on open and on save, so the rules are pinned without a browser.
"""
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from acme.review import initial_mode, suggest_mode, validate_verdict

scenarios("features/review_flow.feature")

CASE = {"id": "c07", "expected_intent": "outage", "needs_human": False, "must_include": [], "must_not": []}


@pytest.fixture
def ctx():
    return {"case": dict(CASE), "rec": {"reply": "Hi Priya, it will be fixed by 6 pm.", "decision": "send"},
            "critique_first": True, "records": {}, "refusal": None}


@given("critique-first review is on")
def on(ctx):
    ctx["critique_first"] = True


@given("critique-first review is off")
def off(ctx):
    ctx["critique_first"] = False


@given(parsers.parse('the step-6 check "{check}" fired on case "{case_id}"'))
def check_fired(ctx, check, case_id):
    ctx["rec"]["flags"] = [{"check": check, "severity": "high", "detail": ""}]


def try_save(ctx, verdict, mode, critique):
    refusal = validate_verdict(verdict, mode, critique, ctx["critique_first"])
    if refusal:
        ctx["refusal"] = refusal
    else:
        ctx["records"][ctx["case"]["id"]] = {"verdict": verdict, "failure_mode": mode, "critique": critique}


@when(parsers.parse('the expert fails case "{case_id}" with critique "{critique}" and no failure mode'))
def fail_no_mode(ctx, case_id, critique):
    try_save(ctx, "Fail", "", critique)


@when(parsers.parse('the expert fails case "{case_id}" with no critique'))
def fail_no_critique(ctx, case_id):
    try_save(ctx, "Fail", "Promised fix time", "")


@when(parsers.parse('the expert opens case "{case_id}"'))
def open_case(ctx, case_id):
    ctx["selected"] = initial_mode(ctx["case"], ctx["rec"], ctx["critique_first"])


@then("the verdict is saved")
def saved(ctx):
    assert ctx["records"]["c07"]["verdict"] == "Fail"


@then('case "c07" is listed under "Not yet grouped"')
def not_yet_grouped(ctx):
    ungrouped = [cid for cid, r in ctx["records"].items() if r["verdict"] == "Fail" and not r["failure_mode"]]
    assert "c07" in ungrouped


@then("no failure mode is selected")
def none_selected(ctx):
    assert ctx["selected"] == ""


@then(parsers.parse('"{mode}" is shown as a hint'))
def hint(ctx, mode):
    assert suggest_mode(ctx["case"], ctx["rec"]) == mode


@then(parsers.parse('the verdict is refused with "{message}"'))
def refused(ctx, message):
    assert ctx["refusal"] == message
    assert not ctx["records"]
