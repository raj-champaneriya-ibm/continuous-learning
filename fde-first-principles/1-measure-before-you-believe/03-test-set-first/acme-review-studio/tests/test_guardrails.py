"""Step definitions for features/guardrails.feature. A scripted model stands in for Claude,
so these run in seconds and test only the code around the model."""
from pathlib import Path

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from pytest_bdd import given, parsers, scenarios, then, when

from acme.lab import load_lab
from acme.workflow import Deps, Workflow

XLSX = Path(__file__).parents[1] / "data" / "Acme_Fibre_Grounded_Draft_Eval.xlsx"
scenarios("features/guardrails.feature")


class ScriptedModel:
    name, model = "scripted", "script"

    def __init__(self):
        self.reply, self.calls = "", 0

    def status(self):
        return True, "scripted"

    def draft(self, system, user, ctx=None):
        self.calls += 1
        return {"output": {"intent": "other", "reply": self.reply, "needs_human": False, "escalation_reason": "",
                           "cited_sources": ["CRM"]}, "error": None, "latency_s": 0, "cost_usd": None, "raw": ""}


@pytest.fixture(scope="module")
def lab():
    return load_lab(XLSX)


@pytest.fixture
def world(lab):
    model = ScriptedModel()
    return {"lab": lab, "model": model, "wf": Workflow(Deps(lab=lab, provider=model), InMemorySaver())}


@given(parsers.parse('the model drafts "{reply}" for case "{case_id}"'))
def model_drafts(world, reply, case_id):
    case = world["lab"].case(case_id)
    world["model"].reply = reply
    world["email"] = {"customer_id": case["customer_id"], "message": case["message"], "case_id": case_id}


@given(parsers.parse('an email from customer "{customer_id}" saying "{message}"'))
def email_from(world, customer_id, message):
    world["email"] = {"customer_id": customer_id, "message": message, "case_id": "custom"}


@when("the email runs through the workflow")
def run(world):
    world["view"] = world["wf"].start(**world["email"])


@when(parsers.parse('the human chooses to "{action}"'))
def human_chooses(world, action):
    reply = "Hi Kavya, your area outage is OUT-KOTH-1021. Updates come in the Acme app." if action == "edit" else None
    world["view"] = world["wf"].resume(world["view"]["thread_id"], action, reply)


@then("the reply is sent automatically")
def sent(world):
    assert world["view"]["decision"] == "send", world["view"].get("reasons")
    assert world["view"]["outcome"] == "sent"


@then("the reply waits for a human")
def waits(world):
    assert world["view"]["decision"] == "escalate"
    assert world["view"]["waiting_for_human"]


@then(parsers.parse('step 6 flags "{check}"'))
def flags(world, check):
    assert check in [f["check"] for f in world["view"].get("flags", [])], world["view"].get("flags")


@then(parsers.parse('the escalation reasons include "{reason}"'))
def reason(world, reason):
    assert reason in world["view"]["reasons"]


@then("the model is not called")
def not_called(world):
    assert world["model"].calls == 0


@then(parsers.parse('the outcome is "{outcome}"'))
def outcome(world, outcome):
    assert world["view"]["outcome"] == outcome
