"""Step definitions for features/expert_review.feature."""
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from lab.acme import load_cases
from lab.evals import CHECKS, score

scenarios("features/expert_review.feature")


def _names(text):
    """'reveals limit, must_not: ₹500' -> {'reveals_limit', 'must_not: ₹500'}; 'nothing' -> set()."""
    if text == "nothing":
        return set()
    return {part.strip() if ":" in part else part.strip().replace(" ", "_") for part in text.split(",")}


@pytest.fixture
def world():
    return {}


@given(parsers.parse("test case {case_id}"))
def given_test_case(world, case_id):
    world["case"] = next(case for case in load_cases() if case["id"] == case_id)


@given(parsers.parse('a draft that says "{reply}" and hands the email to a person'))
def a_draft(world, reply):
    # The verdicts are about what the reply says, so the intent and the hand-off match the label.
    case = world["case"]
    assert case["needs_human"], f"{case['id']} is not a hand-off case; this step doesn't fit it"
    world["draft"] = {"intent": case["expected_intent"], "reply": reply, "needs_human": True}


@when("the grader scores the draft")
def grader_scores(world):
    world["result"] = score(world["case"], world["draft"])


@then(parsers.parse('the checks that fail are "{fails}"'))
def checks_that_fail(world, fails):
    failed = {check for check in CHECKS if not world["result"][check]}
    assert failed == _names(fails), world["result"]


@then(parsers.parse('the grader flags "{flags}"'))
def grader_flags(world, flags):
    assert set(world["result"]["violations"]) == _names(flags), world["result"]["violations"]
