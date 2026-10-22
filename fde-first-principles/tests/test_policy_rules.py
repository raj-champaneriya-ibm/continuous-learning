"""Step definitions for features/policy_rules.feature."""
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from lab.evals import policy_violations

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


@then(parsers.parse('the grader flags "{rules}"'))
def flags(world, rules):
    expected = set() if rules == "nothing" else {r.strip().replace(" ", "_") for r in rules.split(",")}
    assert set(world["found"]) == expected, world["found"]


@then("the grader flags nothing")
def flags_nothing(world):
    assert world["found"] == [], world["found"]
