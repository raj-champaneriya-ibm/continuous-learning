"""Step definitions for features/outage_scope.feature."""
import json

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from lab.version_c3 import _envelope_brief, build_decision_envelope, version_c3

scenarios("features/outage_scope.feature")


@pytest.fixture
def world():
    return {}


@given(parsers.parse('customer {customer} writes "{message}"'))
def customer_writes(world, customer, message):
    world["case"] = {"id": "t1", "customer_id": customer, "message": message}


@given(parsers.parse('the model looks up the customer, then replies "{reply}"'))
def model_looks_up_then_replies(world, monkeypatch, reply):
    answer = json.dumps({"intent": "other", "reply": reply, "needs_human": False})
    lookup = {"function": {"name": "lookup_customer", "arguments": {"customer_id": world["case"]["customer_id"]}}}
    turns = iter([
        {"content": "", "tool_calls": [lookup], "message": {"role": "assistant", "content": "", "tool_calls": [lookup]}},
        {"content": answer, "tool_calls": [], "message": {"role": "assistant", "content": answer}},
    ])

    def fake_chat(messages, **kwargs):
        return {**next(turns), "tokens_in": 0, "tokens_out": 0, "seconds": 0.0}

    monkeypatch.setattr("lab.version_c3.chat", fake_chat)


@when("the envelope is built")
def envelope_is_built(world):
    world["envelope"] = build_decision_envelope(world["case"])
    world["brief"] = _envelope_brief(world["envelope"])


@when("the C3 agent finishes")
def agent_finishes(world):
    world["output"] = version_c3(world["case"])


@then(parsers.parse("the outage is {scope}"))
def outage_scope_is(world, scope):
    assert world["envelope"]["outage_in_scope"] is (scope == "in scope")


@then(parsers.parse('the envelope {shows} "{ticket}"'))
def envelope_shows(world, shows, ticket):
    assert (ticket in world["brief"]) is (shows == "shows"), world["brief"]


@then(parsers.parse('the lookup_customer result {shows} "{ticket}"'))
def lookup_result_shows(world, shows, ticket):
    results = [json.dumps(t["result"], ensure_ascii=False) for t in world["output"]["tool_calls"]
               if t["name"] == "lookup_customer"]
    assert results, world["output"]["tool_calls"]
    assert (ticket in results[0]) is (shows == "shows"), results[0]
