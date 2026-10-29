"""Data contract for the Acme test cases: mechanical checks an SME shouldn't have to do by eye."""
import re
from collections import Counter

import pytest

from lab.acme import DATA, INTENTS, kb_by_id, load_cases, load_customers, load_outages

CASE_FILES = ["cases.jsonl", "cases_abuse.jsonl", "cases_multiturn.jsonl", "cases_regional.jsonl"]
EXPECTED_TOTAL = 256
RULE = re.compile(r"^(E[1-9]|N[1-7])$")
SCRIPTS = {
    "Devanagari": "\u0900-\u097F", "Gujarati": "\u0A80-\u0AFF", "Gurmukhi": "\u0A00-\u0A7F",
    "Tamil": "\u0B80-\u0BFF", "Telugu": "\u0C00-\u0C7F", "Kannada": "\u0C80-\u0CFF", "Malayalam": "\u0D00-\u0D7F",
}
LANGUAGE_SCRIPT = {
    "Hindi (Devanagari)": "Devanagari", "Marathi (Devanagari)": "Devanagari", "Gujarati": "Gujarati",
    "Punjabi (Gurmukhi)": "Gurmukhi", "Tamil": "Tamil", "Telugu": "Telugu", "Kannada": "Kannada",
    "Malayalam": "Malayalam",
}


@pytest.fixture(scope="module")
def cases():
    return [(name, case) for name in CASE_FILES for case in load_cases(DATA / name)]


def _problems(cases, check):
    return [f"{case['id']}: {msg}" for _, case in cases for msg in check(case)]


def test_total_and_unique_ids(cases):
    ids = Counter(case["id"] for _, case in cases)
    assert len(cases) == EXPECTED_TOTAL
    assert not [i for i, n in ids.items() if n > 1], "duplicate ids"


def test_labels_are_valid(cases):
    kb = set(kb_by_id())

    def check(case):
        if case["expected_intent"] not in INTENTS:
            yield f"unknown intent {case['expected_intent']}"
        if not RULE.match(case["escalation_rule"]):
            yield f"unknown rule {case['escalation_rule']}"
        elif case["needs_human"] != case["escalation_rule"].startswith("E"):
            yield f"needs_human={case['needs_human']} contradicts {case['escalation_rule']}"
        for source in case["kb_sources"]:
            if source not in kb and source != "-" and not re.match(r"^P\d+$", source):
                yield f"unknown source {source}"
        overlap = {m.lower() for m in case["must_include"]} & {m.lower() for m in case["must_not"]}
        if overlap:
            yield f"in both must_include and must_not: {overlap}"

    assert not _problems(cases, check)


def test_cases_match_the_customer_record(cases):
    customers, outages = load_customers(), load_outages()

    def check(case):
        customer = customers.get(case["customer_id"])
        if customer is None:
            yield f"unknown customer {case['customer_id']}"
            return
        first = customer["name"].split()[0]
        if case["must_include"] and first not in case["must_include"] and "third-party" not in case["tags"]:
            yield f"must_include lacks the first name {first}"
        outage = outages.get(customer["area"])
        for ticket in (m for m in case["must_include"] if m.startswith("OUT-")):
            if not outage or outage["ticket"] != ticket:
                yield f"{ticket} is not the outage in {customer['area']}"

    assert not _problems(cases, check)


def test_regional_cases_carry_an_english_gloss(cases):
    def check(case):
        if not case.get("message_en"):
            yield "message_en missing"
        for turn in case.get("history", []):
            if turn["role"] == "customer" and re.search(r"[^\x00-\x7F₹]", turn["text"]) and not turn.get("text_en"):
                yield "customer turn without text_en"

    assert not _problems([c for c in cases if c[0] == "cases_regional.jsonl"], check)


def test_language_label_matches_the_script(cases):
    def check(case):
        script = LANGUAGE_SCRIPT.get(case["language"])
        if script and not re.search(f"[{SCRIPTS[script]}]", case["message"]):
            yield f"labelled {case['language']} but the message has no {script} text"

    assert not _problems(cases, check)


def test_references_point_to_real_cases(cases):
    ids = {case["id"] for _, case in cases}
    pairs = {}
    for _, case in cases:
        if case.get("pair_id"):
            pairs.setdefault(case["pair_id"], []).append(case["twin"])
    assert all(sorted(t) == ["abuse", "honest"] for t in pairs.values())
    assert not [c["id"] for _, c in cases if c.get("twin_of") and c["twin_of"] not in ids]
