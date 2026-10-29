"""Step definitions for features/ontology.feature."""
import re

import pytest
from pytest_bdd import parsers, scenarios, then, when

from lab.ontology import define, excluded_from_limit, glossary

scenarios("features/ontology.feature")


@pytest.fixture
def world():
    return {}


@when("the grader asks which kinds of money are excluded from the limit")
def ask_excluded(world):
    world["answer"] = ", ".join(excluded_from_limit())


@when(parsers.parse('an agent looks up "{word}"'))
def look_up(world, word):
    world["definition"] = define(word)


@when("a prompt asks for the glossary")
def ask_glossary(world):
    world["glossary"] = glossary()


@then(parsers.parse('the answer is "{expected}"'))
def answer_is(world, expected):
    assert world["answer"] == expected


@then(parsers.parse('it gets the definition of "{term}"'))
def gets_definition(world, term):
    assert world["definition"] is not None and world["definition"]["term"] == term


@then(parsers.parse('the definition cites "{source}"'))
def cites(world, source):
    assert source in (world["definition"]["source"] or "")


@then("there is no definition")
def no_definition(world):
    assert world["definition"] is None


@then(parsers.parse('it contains "{text}"'))
def contains(world, text):
    assert text in world["glossary"]


@then("it contains no customer id")
def no_customer_id(world):
    assert not re.search(r"\bAC\d{4}\b", world["glossary"])
