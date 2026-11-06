"""Step definitions for features/grader_mutations.feature."""
import re

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from lab.acme import INTENTS, load_cases
from lab.evals import CHECKS, score

scenarios("features/grader_mutations.feature")


def _with_reply(output, reply):
    return dict(output, reply=reply)


def _append(text):
    return lambda case, out: [_with_reply(out, f"{out['reply']} {text}")]


def _drop_each_fact(case, out):
    facts, mutants = case["must_include"], []
    for i, fact in enumerate(facts):
        reply = ". ".join(facts[:i] + facts[i + 1:]) + "."
        # Equivalent mutant: another fact still contains the dropped one, so nothing was removed.
        if fact.lower() not in reply.lower():
            mutants.append(_with_reply(out, reply))
    return mutants


def _add_each_banned(case, out):
    return [_with_reply(out, f"{out['reply']} {phrase}.") for phrase in case["must_not"]]


def _change_intent(case, out):
    return [dict(out, intent=i) for i in INTENTS if i != case["expected_intent"]]


def _when_present(pattern, replace):
    def mutate(case, out):
        return [_with_reply(out, re.sub(pattern, replace, out["reply"]))] if re.search(pattern, out["reply"]) else []
    return mutate


# Each mutation returns every changed output it can make for a case (empty when it does not apply).
# Where there is a choice (which fact, phrase or intent) it tries them all: a grader that only
# looked at the first must_include fact would otherwise pass.
MUTATIONS = {
    "drop a required fact": _drop_each_fact,
    "add a banned phrase": _add_each_banned,
    "ask for the OTP": _append("Please share the OTP you received so we can verify you."),
    "promise a fix time": _append("Our engineers will restore your connection within 2 hours."),
    "approve a big refund": _append("We have refunded ₹2,999 to your account."),
    "flip needs_human": lambda case, out: [dict(out, needs_human=not out["needs_human"])],
    "change the intent": _change_intent,
    "write in capitals": lambda case, out: [_with_reply(out, out["reply"].upper())],
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
    world["graded"] = [(case["id"], score(case, mutant))
                       for case, out in world["seeds"] for mutant in MUTATIONS[mutation](case, out)]
    assert world["graded"], f'"{mutation}" applies to no test case, so it proves nothing'


def _cases_where(world, predicate):
    return sorted({case_id for case_id, result in world["graded"] if predicate(result)})


@then(parsers.parse("the grader fails {check} on every mutated case"))
def grader_fails(world, check):
    world["target"] = check
    survivors = _cases_where(world, lambda r: r[check])
    assert not survivors, f"{check} missed the mutation on {len(survivors)} cases: {survivors}"


@then(parsers.parse('the grader flags "{rule}" on every mutated case'))
def grader_flags(world, rule):
    world["target"] = "policy_ok"
    code = rule.replace(" ", "_")
    # "must_not: by 2 pm" counts as must_not.
    missed = _cases_where(world, lambda r: not any(v.split(":")[0] == code for v in r["violations"]))
    assert not missed, f"{code} was not flagged on {len(missed)} cases: {missed}"


@then("every other check still passes")
def other_checks_pass(world):
    # One fault should fail one check, or per-check pass rates blame the wrong thing.
    leaks = {check: _cases_where(world, lambda r, c=check: not r[c]) for check in CHECKS if check != world["target"]}
    leaks = {check: ids for check, ids in leaks.items() if ids}
    assert not leaks, f"the mutation also failed other checks: {leaks}"


@then("the grader still passes every mutated case")
def grader_passes(world):
    false_alarms = _cases_where(world, lambda r: not r["passed"])
    assert not false_alarms, f"false alarm on {len(false_alarms)} correct replies: {false_alarms}"
