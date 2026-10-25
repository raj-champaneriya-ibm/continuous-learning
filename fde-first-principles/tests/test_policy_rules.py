"""Step definitions for features/policy_rules.feature."""
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from lab.evals import policy_violations, score

scenarios("features/policy_rules.feature")


@pytest.fixture
def world():
    return {}


@given(parsers.parse('the reply "{reply}"'))
def the_reply(world, reply):
    world["reply"] = reply


@when("the grader checks it")
def grader_checks(world):
    world["found"] = policy_violations(world["reply"])


@when("the grader scores it for a customer entitled to no concession")
def grader_scores_no_concession(world):
    case = {"expected_intent": "other", "must_include": [], "must_not": [], "needs_human": False,
            "concession_allowed": False}
    world["found"] = score(case, {"intent": "other", "reply": world["reply"]})["violations"]


@then(parsers.parse('the grader flags "{rules}"'))
def flags(world, rules):
    expected = set() if rules == "nothing" else {r.strip().replace(" ", "_") for r in rules.split(",")}
    assert set(world["found"]) == expected, world["found"]


@then("the grader flags nothing")
def flags_nothing(world):
    assert world["found"] == [], world["found"]
