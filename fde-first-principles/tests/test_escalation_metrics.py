"""Step definitions for features/escalation_metrics.feature."""
import math

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from lab.evals import score, summary

scenarios("features/escalation_metrics.feature")


def _graded(expected: bool, flagged: bool) -> dict:
    case = {"expected_intent": "other", "must_include": [], "must_not": [], "needs_human": expected}
    return score(case, {"intent": "other", "reply": "", "needs_human": flagged})


def _percent(value: float) -> str:
    return "n/a" if math.isnan(value) else f"{value:.0%}"


@pytest.fixture
def world():
    return {}


@given(parsers.parse("{needed:d} cases that need a human and {not_needed:d} that do not"))
def cases(world, needed, not_needed):
    world["needed"], world["not_needed"] = needed, not_needed


@given(parsers.parse("the bot escalates {caught:d} of the first group and {false_alarms:d} of the second"))
def bot_escalates(world, caught, false_alarms):
    needed, not_needed = world["needed"], world["not_needed"]
    world["scores"] = (
        [_graded(True, i < caught) for i in range(needed)]
        + [_graded(False, i < false_alarms) for i in range(not_needed)]
    )


@when("the grader summarises the run")
def summarise(world):
    world["summary"] = summary(world["scores"])


@then(parsers.parse("human_ok is {expected}"))
def human_ok_is(world, expected):
    assert _percent(world["summary"]["human_ok"]) == expected


@then(parsers.parse("escalation recall is {expected}"))
def recall_is(world, expected):
    assert _percent(world["summary"]["escalation_recall"]) == expected


@then(parsers.parse("escalation precision is {expected}"))
def precision_is(world, expected):
    assert _percent(world["summary"]["escalation_precision"]) == expected
