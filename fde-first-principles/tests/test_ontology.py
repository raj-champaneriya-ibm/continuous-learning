"""Step definitions for features/ontology.feature and business graph engine tests."""
import re

import pytest
from pytest_bdd import parsers, scenarios, then, when

from lab.evals import policy_violations, score
from lab.ontology import (
    _store,
    compute_entitlements,
    customer_subgraph,
    define,
    domain_edges,
    excluded_from_limit,
    glossary,
    plans,
    pune_service_areas,
    terms,
    validate_ontology_ops,
)
from lab.version_c3 import (
    build_decision_envelope,
    check_entitlement,
    define_term,
    run_agent,
    search_kb_c3,
)

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


@when("the reasoner inspects the ontology")
def inspect_reasoned_ontology(world):
    world["terms"] = terms()


@when("operations validates the ontology against live catalogs and business rules")
def run_ops_validation(world):
    world["ops"] = validate_ontology_ops()


@when(parsers.parse('the engine computes entitlements for customer "{customer_id}"'))
def compute_for_customer(world, customer_id):
    world["entitlements"] = compute_entitlements(customer_id)


@when(parsers.parse(
    "business operations raises the concession limit to {limit:d} rupees and lowers minimum tenure to {min_tenure:d} months"
))
def apply_commercial_rule_override(world, limit, min_tenure):
    world["rules_override"] = {
        "concession_limit": {"max_rupees_30_days": limit},
        "offers": {
            "retention offer": {"min_tenure_months": min_tenure},
            "late-fee waiver": {"min_tenure_months": min_tenure},
        },
    }


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


@then(parsers.parse('"{term}" inherits oncePerMonths of {months:d} and countsTowardLimit true'))
def check_inherited_props(world, term, months):
    info = world["terms"][term]
    assert info["once_per_months"] == months
    assert info["counts_toward_limit"] is True


@then(parsers.parse('"{term}" overrides countsTowardLimit to false'))
def check_override_false(world, term):
    assert world["terms"][term]["counts_toward_limit"] is False


@then(parsers.parse('"{term}" inherits requiresRole "{role}"'))
def check_inherited_role(world, term, role):
    assert world["terms"][term]["requires_role"] == role


@then("the operational health check passes with zero drift errors")
def check_ops_clean(world):
    assert world["ops"]["ok"] is True, world["ops"]["drift_errors"]
    assert world["ops"]["stewardship_coverage"] == 1.0


@then(parsers.parse("the remaining 30-day headroom is {headroom:d} rupees"))
def check_headroom(world, headroom):
    assert world["entitlements"]["concession_headroom_rupees"] == headroom


@then(parsers.parse('eligibility for "{offer}" is {eligible}'))
def check_offer_eligibility(world, offer, eligible):
    expected = eligible.strip().lower() == "true"
    assert world["entitlements"]["offers"][offer]["eligible"] is expected


@then(parsers.parse('customer "{customer_id}" has {headroom:d} rupees of headroom and is eligible for "{offer}"'))
def check_overridden_entitlement(world, customer_id, headroom, offer):
    report = compute_entitlements(customer_id, rules=world["rules_override"])
    assert report["concession_headroom_rupees"] == headroom
    assert report["offers"][offer]["eligible"] is True


def test_domain_edges_and_ephemeral_subgraph_isolation():
    edges = domain_edges("retention offer")
    assert edges is not None
    assert "concession" in edges["superclasses"]
    assert "once-only offer" in edges["superclasses"]
    assert "KB11" in edges["kb_articles"]
    assert 10 in edges["policy_rules"]
    assert edges["owner_team"] == "Customer Retention & Lifecycle"
    assert plans()["Pro"]["price_rupees"] == 1499
    assert len(pune_service_areas()) == 8

    # Ephemeral customer subgraph must never leak into the shared TBox _store()
    base_size = len(_store())
    sub = customer_subgraph("AC1032")
    assert len(sub) > base_size
    assert len(_store()) == base_size


def test_evals_enforces_customer_headroom_and_plan_discounts():
    # AC1032 has ₹200 in credits_last_30_days, leaving ₹300 headroom
    assert "big_refund" in policy_violations(
        "Hi Varun, we have credited ₹400 to your account.", customer_id="AC1032"
    )
    assert "big_refund" not in policy_violations(
        "Hi Varun, we have credited ₹250 to your account.", customer_id="AC1032"
    )
    case = {
        "customer_id": "AC1032",
        "expected_intent": "billing",
        "must_include": ["Varun"],
        "must_not": [],
        "needs_human": True,
    }
    res = score(case, {"intent": "billing", "reply": "Hi Varun, we have credited ₹400 to your account.", "needs_human": True})
    assert "big_refund" in res["violations"]


def test_version_c3_tools_and_decision_envelope(monkeypatch):
    # Hinglish query resolves via ontology skos:altLabel -> acme:documentedIn -> KB04 / KB02
    kb_hits = search_kb_c3("paisa wapas", k=2)
    assert kb_hits[0]["id"] == "KB04"
    waiver_hits = search_kb_c3("late fee maaf", k=2)
    assert waiver_hits[0]["id"] == "KB02"

    term_info = define_term("सूट")
    assert term_info["term"] == "discount"
    ent_info = check_entitlement("AC1021", "late-fee waiver")
    assert ent_info["eligible"] is True

    case = {
        "id": "p18a",
        "customer_id": "AC1032",
        "message": "The Kothrud outage cost me a client meeting today. Please credit ₹400 to my account.",
        "expected_intent": "outage",
        "must_include": ["Varun", "OUT-KOTH-1021"],
        "must_not": [],
        "needs_human": True,
    }
    env = build_decision_envelope(case)
    assert env["concession_headroom_rupees"] == 300
    assert env["escalation_reasons"]  # ₹400 > ₹300 headroom

    # Verify version_c3 agent loop + post-draft policy guardrail
    def fake_chat(messages, **kwargs):
        return {
            "content": '{"intent": "outage", "reply": "Hi Varun, outage OUT-KOTH-1021 is active; your ₹400 credit request needs approval.", "needs_human": false}',
            "tool_calls": [],
            "message": {"role": "assistant", "content": "..."},
            "tokens_in": 100,
            "tokens_out": 30,
            "seconds": 0.1,
        }

    monkeypatch.setattr("lab.version_c3.chat", fake_chat)
    output, trace = run_agent(case)
    assert output["intent"] == "outage"
    # Even though fake_chat returned needs_human=false, the DecisionEnvelope escalation guardrail forces True
    assert output["needs_human"] is True
    assert len(trace) == 1
