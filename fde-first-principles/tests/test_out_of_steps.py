"""Step definitions for features/out_of_steps.feature. A scripted model replaces lab.version_c3.chat."""
import json

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from lab.version_c3 import MAX_STEPS, OUT_OF_STEPS, version_c3

scenarios("features/out_of_steps.feature")

SEARCH = {"function": {"name": "search_kb", "arguments": {"query": "data cap"}}}


def _search_turn():
    return {"content": "", "tool_calls": [SEARCH], "message": {"role": "assistant", "content": "", "tool_calls": [SEARCH]}}


def _reply_turn(reply):
    answer = json.dumps({"intent": "other", "reply": reply, "needs_human": False})
    return {"content": answer, "tool_calls": [], "message": {"role": "assistant", "content": answer}}


def _script(world, monkeypatch, turns):
    """Replace the model with these turns, and record what each call was sent."""
    turns, world["calls"] = iter(turns), []

    def fake_chat(messages, **kwargs):
        world["calls"].append([dict(m) for m in messages])
        return {**next(turns), "tokens_in": 0, "tokens_out": 0, "seconds": 0.0}

    monkeypatch.setattr("lab.version_c3.chat", fake_chat)


@pytest.fixture
def world():
    return {}


@given(parsers.parse('customer {customer} writes "{message}"'))
def customer_writes(world, customer, message):
    world["case"] = {"id": "t1", "customer_id": customer, "message": message}


@given(parsers.parse('the model searches the help articles on every step, then replies "{reply}"'))
def searches_every_step_then_replies(world, monkeypatch, reply):
    _script(world, monkeypatch, [_search_turn() for _ in range(MAX_STEPS)] + [_reply_turn(reply)])


@given("the model searches the help articles on every step and on the extra turn too")
def searches_every_step_and_after(world, monkeypatch):
    _script(world, monkeypatch, [_search_turn() for _ in range(MAX_STEPS + 1)])


@given(parsers.parse('the model searches the help articles once, then replies "{reply}"'))
def searches_once_then_replies(world, monkeypatch, reply):
    _script(world, monkeypatch, [_search_turn(), _reply_turn(reply)])


@when("the C3 agent finishes")
def agent_finishes(world):
    world["output"] = version_c3(world["case"])


@then(parsers.parse('the reply is "{reply}"'))
def reply_is(world, reply):
    assert world["output"]["reply"] == reply


@then("the reply is empty")
def reply_is_empty(world):
    assert world["output"]["reply"] == ""


@then("the model got one more turn after the step limit, telling it to answer now")
def one_more_turn(world):
    assert len(world["calls"]) == MAX_STEPS + 1
    assert world["calls"][-1][-1] == {"role": "user", "content": OUT_OF_STEPS}


@then(parsers.parse("the model was called {n:d} times"))
def model_called(world, n):
    assert len(world["calls"]) == n


@then("the result is marked out of steps")
def marked_out_of_steps(world):
    assert world["output"].get("out_of_steps") is True


@then("the result is not marked out of steps")
def not_marked_out_of_steps(world):
    assert not world["output"].get("out_of_steps")


@then(parsers.parse('the escalation sources include "{source}"'))
def sources_include(world, source):
    assert source in world["output"]["escalation_sources"], world["output"]["escalation_sources"]


@then(parsers.parse('the escalation sources don\'t include "{source}"'))
def sources_exclude(world, source):
    assert source not in world["output"]["escalation_sources"], world["output"]["escalation_sources"]


@then("a person gets the email")
def person_gets_it(world):
    assert world["output"]["needs_human"] is True
