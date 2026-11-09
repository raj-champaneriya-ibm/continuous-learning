"""Step definitions for features/intent_guide.feature."""
import pytest
from pytest_bdd import given, parsers, scenarios, then

from lab.acme import DATA, INTENT_GUIDE, INTENTS, load_cases

scenarios("features/intent_guide.feature")

CASE_FILES = ["cases.jsonl", "cases_abuse.jsonl", "cases_multiturn.jsonl", "cases_regional.jsonl"]


@pytest.fixture
def world():
    return {}


@given("the labelled cases in the four case files")
def labelled_cases(world):
    world["labels"] = {case["id"]: case["expected_intent"] for name in CASE_FILES for case in load_cases(DATA / name)}


@then("every intent has a definition in the guide")
def every_intent_defined():
    assert list(INTENT_GUIDE) == INTENTS, sorted(set(INTENTS) ^ set(INTENT_GUIDE))


@then(parsers.parse('case {case} is labelled "{intent}"'))
def case_is_labelled(world, case, intent):
    assert world["labels"][case] == intent, f"{case} is labelled {world['labels'][case]!r}"
