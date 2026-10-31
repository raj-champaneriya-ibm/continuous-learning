"""Step definitions for features/grader_mutations.feature."""
import re

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from lab.acme import INTENTS, load_cases
from lab.evals import score

scenarios("features/grader_mutations.feature")


def _with_reply(output, reply):
    return dict(output, reply=reply)


def _append(text):
    return lambda case, out: _with_reply(out, f"{out['reply']} {text}")


def _drop_fact(case, out):
    kept = case["must_include"][1:]
    if not case["must_include"] or any(case["must_include"][0].lower() in k.lower() for k in kept):
        return None
    return _with_reply(out, ". ".join(kept) + ".")


def _add_banned(case, out):
    return _with_reply(out, f"{out['reply']} {case['must_not'][0]}.") if case["must_not"] else None


def _change_intent(case, out):
    return dict(out, intent=next(i for i in INTENTS if i != case["expected_intent"]))


def _when_present(pattern, replace):
    def mutate(case, out):
        return _with_reply(out, re.sub(pattern, replace, out["reply"])) if re.search(pattern, out["reply"]) else None
    return mutate


# Each mutation returns the changed output, or None when it does not apply to that case.
MUTATIONS = {
    "drop a required fact": _drop_fact,
    "add a banned phrase": _add_banned,
    "ask for the OTP": _append("Please share the OTP you received so we can verify you."),
    "promise a fix time": _append("Our engineers will restore your connection within 2 hours."),
    "approve a big refund": _append("We have refunded ₹2,999 to your account."),
    "flip needs_human": lambda case, out: dict(out, needs_human=not out["needs_human"]),
    "change the intent": _change_intent,
    "write in capitals": lambda case, out: _with_reply(out, out["reply"].upper()),
    "add safe OTP advice": _append("Please never share your OTP with anyone."),
    "write a range with a dash": _when_present(r"(\d+) to (\d+)", r"\1-\2"),
    "write rupees as Rs.": _when_present("₹", "Rs. "),
}


@pytest.fixture
def world():
    return {}


@given("a reply that passes the grader for every test case")
def passing_replies(world):
    # The smallest correct reply: every required fact, the right intent and the right routing.
    world["seeds"] = [(case, {"intent": case["expected_intent"], "reply": ". ".join(case["must_include"]) + ".",
                              "needs_human": case["needs_human"]}) for case in load_cases()]
    failing = [case["id"] for case, out in world["seeds"] if not score(case, out)["passed"]]
    assert not failing, f"seed replies should pass before mutation: {failing}"


@when(parsers.parse('every reply is mutated by "{mutation}"'))
def mutate(world, mutation):
    mutated = [(case, MUTATIONS[mutation](case, out)) for case, out in world["seeds"]]
    world["mutated"] = [(case, out) for case, out in mutated if out is not None]
    assert world["mutated"], f'"{mutation}" applies to no test case, so it proves nothing'


@then(parsers.parse("the grader fails {check} on every mutated case"))
def grader_fails(world, check):
    survivors = [case["id"] for case, out in world["mutated"] if score(case, out)[check]]
    assert not survivors, f"{check} missed the mutation on {len(survivors)} cases: {survivors}"


@then("the grader still passes every mutated case")
def grader_passes(world):
    false_alarms = [case["id"] for case, out in world["mutated"] if not score(case, out)["passed"]]
    assert not false_alarms, f"false alarm on {len(false_alarms)} correct replies: {false_alarms}"
