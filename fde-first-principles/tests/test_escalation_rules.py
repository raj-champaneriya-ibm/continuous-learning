"""Step definitions for features/escalation_rules.feature and features/offer_decisions.feature."""
import json

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from lab.acme import DATA, load_cases
from lab.version_c3 import build_decision_envelope, run_agent

scenarios("features/escalation_rules.feature", "features/offer_decisions.feature")

CASE_FILES = ["cases.jsonl", "cases_abuse.jsonl", "cases_multiturn.jsonl", "cases_regional.jsonl"]


@pytest.fixture
def world():
    return {"history": []}


@given(parsers.parse('customer {customer} writes "{message}"'))
def customer_writes(world, customer, message):
    world["case"] = {"id": "t1", "customer_id": customer, "message": message}


@given(parsers.parse('customer {customer} earlier wrote "{text}"'))
def customer_earlier_wrote(world, customer, text):
    world["customer_id"] = customer
    world["history"].append({"role": "customer", "text": text})


@given(parsers.parse('the agent replied "{text}"'))
def agent_replied(world, text):
    world["history"].append({"role": "assistant", "text": text})


@given(parsers.parse('the customer now writes "{message}"'))
def customer_now_writes(world, message):
    world["case"] = {"id": "t1", "customer_id": world["customer_id"], "history": world["history"],
                     "message": message}


@given("every labelled case in the four case files")
def every_labelled_case(world):
    world["cases"] = [case for name in CASE_FILES for case in load_cases(DATA / name)]


@given(parsers.parse('the model drafts "{reply}" with needs_human {model_says}'))
def model_drafts(world, monkeypatch, reply, model_says):
    answer = json.dumps({"intent": "other", "reply": reply, "needs_human": model_says == "true"})

    def fake_chat(messages, **kwargs):
        return {"content": answer, "tool_calls": [], "message": {"role": "assistant", "content": answer},
                "tokens_in": 0, "tokens_out": 0, "seconds": 0.0}

    monkeypatch.setattr("lab.version_c3.chat", fake_chat)


@when("the escalation rules read it")
def rules_read_it(world):
    world["fired"] = [t["rule"] for t in build_decision_envelope(world["case"])["escalation_triggers"]]


@when("the escalation rules read each one")
def rules_read_each(world):
    world["false_triggers"] = {
        case["id"]: [t["rule"] for t in build_decision_envelope(case)["escalation_triggers"]]
        for case in world["cases"] if not case["needs_human"]
    }


@when("the envelope decides the offers")
def envelope_decides(world):
    world["decisions"] = build_decision_envelope(world["case"])["offer_decisions"]


@when("the C3 agent finishes")
def agent_finishes(world):
    world["output"], _ = run_agent(world["case"])


@then(parsers.parse('the rule "{rule}" fires'))
def rule_fires(world, rule):
    assert rule in world["fired"], world["fired"]


@then("no rule fires")
def no_rule_fires(world):
    assert world["fired"] == [], world["fired"]


@then("no rule fires on a case labelled needs_human false")
def no_false_triggers(world):
    fired = {case_id: rules for case_id, rules in world["false_triggers"].items() if rules}
    assert world["false_triggers"], "no cases labelled needs_human false were read"
    assert not fired, f"rules fired on {len(fired)} cases that need no human: {fired}"


@then(parsers.parse('the {offer} decision is "{status}"'))
def offer_decision_is(world, offer, status):
    assert world["decisions"][offer]["status"] == status, world["decisions"][offer]


@then(parsers.parse("needs_human is {expected}"))
def needs_human_is(world, expected):
    assert world["output"]["needs_human"] is (expected == "true"), world["output"]


@then(parsers.parse('the escalation sources are "{sources}"'))
def escalation_sources_are(world, sources):
    expected = [] if sources == "none" else [s.strip() for s in sources.split(",")]
    assert world["output"]["escalation_sources"] == expected, world["output"]["escalation_sources"]
