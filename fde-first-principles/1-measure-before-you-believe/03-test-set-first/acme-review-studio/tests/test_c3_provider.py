"""Step definitions for features/c3_provider.feature. A stand-in plays lab.version_c3.version_c3, so these
run without the lab's packages or a model and test only the provider and the workflow around it."""
import re
from pathlib import Path

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from pytest_bdd import given, parsers, scenarios, then, when

from acme.lab import load_lab
from acme.providers import C3Provider, make_provider
from acme.workflow import Deps, Workflow

XLSX = Path(__file__).parents[1] / "data" / "Acme_Fibre_Grounded_Draft_Eval.xlsx"
scenarios("features/c3_provider.feature")


class StandInC3:
    """Records the case it was given and returns a version_c3-style result row (or raises)."""

    def __init__(self):
        self.row, self.error, self.cases = None, None, []

    def __call__(self, case):
        self.cases.append(case)
        if self.error:
            raise RuntimeError(self.error)
        return dict(self.row)


def _tool_calls(tools):
    """'lookup_customer, search_kb KB07 KB16' -> version_c3 tool_calls with results shaped like the lab's."""
    calls = []
    for part in [p.strip() for p in tools.split(",") if p.strip()]:
        name, *ids = part.split()
        result = {"lookup_customer": {"name": "customer record"},
                  "search_kb": [{"id": i, "title": "", "text": ""} for i in ids],
                  "get_article": {"id": ids[0]} if ids else {},
                  "define_term": {"term": "", "kb_articles": ids},
                  }.get(name, {})
        calls.append({"step": 0, "name": name, "args": {}, "result": result})
    return calls


@pytest.fixture(scope="module")
def lab():
    return load_lab(XLSX)


@pytest.fixture
def world(lab):
    c3 = StandInC3()
    return {"lab": lab, "c3": c3, "history": [],
            "wf": Workflow(Deps(lab=lab, provider=C3Provider(runner=c3)), InMemorySaver())}


@given(parsers.parse('C3 replies "{reply}" after calling "{tools}" with escalation sources "{sources}"'))
def c3_replies(world, reply, tools, sources):
    sources = [] if sources == "none" else [s.strip() for s in sources.split(",")]
    world["c3"].row = {"intent": "other", "reply": reply, "needs_human": bool(sources),
                       "escalation_sources": sources, "tool_calls": _tool_calls(tools)}


@given(parsers.parse('C3 fails with "{error}"'))
def c3_fails(world, error):
    world["c3"].error = error


@given(parsers.parse('the customer wrote earlier "{text}"'))
def earlier_turn(world, text):
    world["history"].append({"role": "customer", "text": text})


@when(parsers.parse('case "{case_id}" runs through the workflow with C3'))
def run_case(world, case_id):
    case = world["lab"].case(case_id)
    world["case"] = case
    world["view"] = world["wf"].start(customer_id=case["customer_id"], message=case["message"], case_id=case_id,
                                      history=case.get("history"))


@when(parsers.parse('customer "{customer_id}" writes "{message}" and the email runs through the workflow with C3'))
def run_email(world, customer_id, message):
    world["view"] = world["wf"].start(customer_id=customer_id, message=message, history=world["history"])


@when(parsers.parse('the studio makes the "{name}" provider with no ACME_C3_MODEL set'))
def make_c3(world, name, monkeypatch):
    monkeypatch.delenv("ACME_C3_MODEL", raising=False)
    world["provider"] = make_provider(name, "sonnet")


@then(parsers.parse('C3 was given case "{case_id}" with its customer and message'))
def c3_given_case(world, case_id):
    (given,) = world["c3"].cases
    message = re.sub(r"[ \t]+", " ", world["case"]["message"].replace("\r\n", "\n")).strip()
    assert (given["id"], given["customer_id"], given["message"]) == (case_id, world["case"]["customer_id"], message)


@then(parsers.parse('C3 was given the earlier turn "{text}"'))
def c3_given_history(world, text):
    (given,) = world["c3"].cases
    assert {"role": "customer", "text": text} in given["history"], given["history"]


@then(parsers.parse('the draft says "{reply}"'))
def draft_says(world, reply):
    assert world["view"]["draft"]["reply"] == reply


@then(parsers.parse("the draft's needs_human is {flag}"))
def draft_needs_human(world, flag):
    assert world["view"]["draft"]["needs_human"] is (flag == "true")


@then(parsers.parse("the draft's escalation reason is \"{sources}\""))
def draft_reason(world, sources):
    assert world["view"]["draft"]["escalation_reason"] == ("" if sources == "none" else sources)


@then(parsers.parse('the draft cites "{cited}"'))
def draft_cites(world, cited):
    assert world["view"]["draft"]["cited_sources"] == [c.strip() for c in cited.split(",")]


@then(parsers.parse('the escalation reasons include "{reason}"'))
def reasons_include(world, reason):
    assert reason in world["view"]["reasons"], world["view"]["reasons"]


@then("the reply waits for a human")
def waits(world):
    assert world["view"]["decision"] == "escalate"
    assert world["view"]["waiting_for_human"]


@then(parsers.parse('step 5 reports "{issue}"'))
def step5_reports(world, issue):
    assert issue in world["view"]["issues"], world["view"]["issues"]
    assert world["view"]["llm"]["provider"] == "c3"


@then(parsers.parse('the provider is "{label}" with model "{model}"'))
def provider_is(world, label, model):
    assert (world["provider"].label, world["provider"].model) == (label, model)
