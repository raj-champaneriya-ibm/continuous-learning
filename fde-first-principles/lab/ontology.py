"""The Acme ontology & business graph engine (data/acme/ontology.ttl + data/acme/business_rules.json).

Definitions and domain structure live in ontology.ttl (TBox).
Commercial thresholds and cooldown parameters live in business_rules.json.
Customer records stay in customers.json (policy rule 5) and are joined only in ephemeral
single-customer subgraphs at request time.

    from lab.ontology import (
        glossary, excluded_from_limit, define, plans, pune_service_areas,
        reason_owl_rl, compute_entitlements, validate_ontology_ops,
    )
    glossary()                    # "- account holder: The customer named on the account. ..." for a prompt
    excluded_from_limit()         # ['double payment refund', 'outage credit']
    define("paisa wapas")         # {'term': 'refund', 'definition': ..., 'source': 'KB04', ...}
    compute_entitlements("AC1009")
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pyoxigraph import Literal, NamedNode, Quad, RdfFormat, Store

from .acme import DATA, RECORD_DATE, kb_by_id, load_customers, load_outages, outage_for
from .business_rules import (
    duplicate_payment_amount,
    load_business_rules,
    months_since,
    outage_exceeds_hours,
)

ONTOLOGY = DATA / "ontology.ttl"
ACME_NS = "https://acme.example/ontology#"
REQ_NS = "https://acme.example/request#"

PREFIXES = """
PREFIX acme: <https://acme.example/ontology#>
PREFIX acme_req: <https://acme.example/request#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
"""

# OWL 2 RL + Defeasible Class-Property Inheritance rules (SPARQL 1.1 Update)
_DIRECT_INHERIT_PROPS = (
    "acme:countsTowardLimit",
    "acme:oncePerMonths",
    "acme:ownedBy",
    "acme:requiresRole",
)

_OWL_RL_UPDATES = [
    # 1. Defeasible inheritance along direct rdfs:subClassOf hops (before transitive closure)
    *[
        PREFIXES + f"""
        INSERT {{ ?sub {prop} ?val }}
        WHERE {{
          ?sub rdfs:subClassOf ?sup .
          ?sup {prop} ?val .
          FILTER NOT EXISTS {{
            ?sub rdfs:subClassOf ?mid .
            ?mid rdfs:subClassOf ?sup .
            FILTER(?mid != ?sub && ?mid != ?sup)
          }}
          FILTER NOT EXISTS {{ ?sub {prop} ?existing }}
        }}
        """
        for prop in _DIRECT_INHERIT_PROPS
    ],
    # 2. Additive rule-enforcement propagation down subclass hierarchy
    PREFIXES + """
    INSERT { ?sub acme:enforcesRule ?rule }
    WHERE {
      ?sub rdfs:subClassOf ?sup .
      ?sup acme:enforcesRule ?rule .
    }
    """,
    # 3. prp-inv1 / prp-inv2: owl:inverseOf bidirectional materialization
    PREFIXES + """
    INSERT { ?y ?q ?x }
    WHERE {
      { ?p owl:inverseOf ?q } UNION { ?q owl:inverseOf ?p }
      ?x ?p ?y .
      FILTER(isIRI(?y))
    }
    """,
    # 4. prp-spo1: rdfs:subPropertyOf
    PREFIXES + """
    INSERT { ?x ?q ?y }
    WHERE {
      ?p rdfs:subPropertyOf ?q .
      ?x ?p ?y .
    }
    """,
    # 5. prp-trp: owl:TransitiveProperty
    PREFIXES + """
    INSERT { ?x ?p ?z }
    WHERE {
      ?p a owl:TransitiveProperty .
      ?x ?p ?y .
      ?y ?p ?z .
    }
    """,
    # 6. prp-symp: owl:SymmetricProperty
    PREFIXES + """
    INSERT { ?y ?p ?x }
    WHERE {
      ?p a owl:SymmetricProperty .
      ?x ?p ?y .
      FILTER(isIRI(?y))
    }
    """,
    # 7. cax-sco: instance typing across rdfs:subClassOf
    PREFIXES + """
    INSERT { ?inst a ?sup }
    WHERE {
      ?inst a ?cls .
      ?cls rdfs:subClassOf ?sup .
      FILTER(?inst != ?cls)
    }
    """,
    # 8. prp-dom / prp-rng: domain and range inference on non-class individuals
    PREFIXES + """
    INSERT { ?x a ?c }
    WHERE {
      ?p rdfs:domain ?c .
      ?x ?p ?y .
      FILTER NOT EXISTS { ?x a owl:Class }
    }
    """,
    PREFIXES + """
    INSERT { ?y a ?c }
    WHERE {
      ?p rdfs:range ?c .
      ?x ?p ?y .
      FILTER(isIRI(?y))
      FILTER NOT EXISTS { ?y a owl:Class }
    }
    """,
]

_SCM_SCO_UPDATE = PREFIXES + """
INSERT { ?c1 rdfs:subClassOf ?c3 }
WHERE {
  ?c1 rdfs:subClassOf ?c2 .
  ?c2 rdfs:subClassOf ?c3 .
  FILTER(?c1 != ?c3)
}
"""

TERMS = PREFIXES + """
SELECT ?term ?label ?definition ?note ?source ?counts ?once WHERE {
  ?term a owl:Class ; skos:prefLabel ?label ; skos:definition ?definition .
  FILTER(LANG(?label) = "en" || LANG(?label) = "")
  OPTIONAL { ?term skos:scopeNote ?note }
  OPTIONAL { ?term acme:source ?source }
  OPTIONAL { ?term acme:countsTowardLimit ?counts }
  OPTIONAL { ?term acme:oncePerMonths ?once }
} ORDER BY ?label
"""

LABELS = PREFIXES + """
SELECT ?label ?name WHERE {
  ?term a owl:Class ; skos:prefLabel ?label .
  FILTER(LANG(?label) = "en" || LANG(?label) = "")
  { ?term skos:prefLabel ?name } UNION { ?term skos:altLabel ?name }
}
"""

EXCLUDED_FROM_LIMIT = PREFIXES + """
SELECT DISTINCT ?label WHERE {
  ?term rdfs:subClassOf+ acme:Concession ; acme:countsTowardLimit false ; skos:prefLabel ?label .
  FILTER(LANG(?label) = "en" || LANG(?label) = "")
} ORDER BY ?label
"""

PLANS_QUERY = PREFIXES + """
SELECT ?code ?price ?speed ?kbId WHERE {
  ?plan a acme:Plan ;
        acme:planCode ?code ;
        acme:monthlyPriceRupees ?price ;
        acme:speedMbps ?speed .
  OPTIONAL {
    ?plan acme:documentedIn ?kb .
    ?kb acme:articleId ?kbId .
  }
} ORDER BY ?price
"""

AREAS_QUERY = PREFIXES + """
SELECT DISTINCT ?name WHERE {
  ?area a acme:PuneServiceArea ;
        acme:areaName ?name .
} ORDER BY ?name
"""

EDGES_QUERY = PREFIXES + """
SELECT ?label ?kbId ?ruleNum ?ownerLabel ?roleLabel WHERE {
  ?term a owl:Class ; skos:prefLabel ?label .
  FILTER(LANG(?label) = "en" || LANG(?label) = "")
  OPTIONAL { ?term acme:documentedIn ?kb . ?kb acme:articleId ?kbId }
  OPTIONAL { ?term acme:enforcesRule ?r . ?r acme:ruleNumber ?ruleNum }
  OPTIONAL { ?term acme:ownedBy ?o . ?o skos:prefLabel ?ownerLabel }
  OPTIONAL { ?term acme:requiresRole ?role . ?role skos:prefLabel ?roleLabel }
}
"""


def reason_owl_rl(store: Store, max_iterations: int = 10) -> int:
    """Materialize OWL 2 RL and defeasible class-property entailments to a fixed point.

    Returns the number of inferred quads added to `store`.
    """
    initial_count = len(store)
    for _ in range(max_iterations):
        before = len(store)
        for update_query in _OWL_RL_UPDATES:
            store.update(update_query)
        if len(store) == before:
            break
    # Finally materialize transitive rdfs:subClassOf closure (scm-sco) and instance typing
    for _ in range(max_iterations):
        before = len(store)
        store.update(_SCM_SCO_UPDATE)
        store.update(_OWL_RL_UPDATES[6])  # cax-sco
        if len(store) == before:
            break
    return len(store) - initial_count


@lru_cache(maxsize=1)
def _store() -> Store:
    store = Store()
    store.load(path=str(ONTOLOGY), format=RdfFormat.TURTLE)
    reason_owl_rl(store)
    return store


def _value(term) -> Optional[str]:
    return term.value if term is not None else None


def _bool_value(term) -> Optional[bool]:
    if term is None:
        return None
    return term.value.lower() == "true"


def _int_value(term) -> Optional[int]:
    if term is None:
        return None
    return int(term.value)


@lru_cache(maxsize=1)
def _edge_metadata() -> Dict[str, Dict[str, Any]]:
    meta: Dict[str, Dict[str, Any]] = {}
    for row in _store().query(EDGES_QUERY):
        label = row["label"].value
        entry = meta.setdefault(
            label,
            {"kb_articles": [], "policy_rules": [], "owner_team": None, "requires_role": None},
        )
        kb_id = _value(row["kbId"])
        if kb_id and kb_id not in entry["kb_articles"]:
            entry["kb_articles"].append(kb_id)
        rule_num = _int_value(row["ruleNum"])
        if rule_num is not None and rule_num not in entry["policy_rules"]:
            entry["policy_rules"].append(rule_num)
        owner = _value(row["ownerLabel"])
        if owner:
            entry["owner_team"] = owner
        role = _value(row["roleLabel"])
        if role:
            entry["requires_role"] = role
    for entry in meta.values():
        entry["kb_articles"].sort()
        entry["policy_rules"].sort()
    return meta


@lru_cache(maxsize=1)
def terms() -> Dict[str, Dict[str, Any]]:
    """Every defined class term by its canonical English label, enriched with reasoned edges."""
    edges = _edge_metadata()
    out: Dict[str, Dict[str, Any]] = {}
    for row in _store().query(TERMS):
        label = row["label"].value
        e = edges.get(label, {})
        out[label] = {
            "term": label,
            "iri": row["term"].value,
            "definition": row["definition"].value,
            "note": _value(row["note"]),
            "source": _value(row["source"]),
            "counts_toward_limit": _bool_value(row["counts"]),
            "once_per_months": _int_value(row["once"]),
            "kb_articles": list(e.get("kb_articles", [])),
            "policy_rules": list(e.get("policy_rules", [])),
            "owner_team": e.get("owner_team"),
            "requires_role": e.get("requires_role"),
        }
    return out


@lru_cache(maxsize=1)
def _alias_index() -> Dict[str, str]:
    """O(1) casefolded lookup from any English or regional label to its canonical English term."""
    return {row["name"].value.strip().casefold(): row["label"].value for row in _store().query(LABELS)}


def glossary(only_terms: Optional[List[str]] = None) -> str:
    """One line per term, ready to paste into a prompt as a 'Definitions' block."""
    all_terms = terms()
    selected = [all_terms[k] for k in only_terms if k in all_terms] if only_terms else list(all_terms.values())
    return "\n".join(
        f"- {t['term']}: {t['definition']}" + (f" {t['note']}" if t["note"] else "")
        for t in selected
    )


def excluded_from_limit() -> List[str]:
    """Kinds of money that don't count toward the ₹500 limit (automatic ones)."""
    return [row["label"].value for row in _store().query(EXCLUDED_FROM_LIMIT)]


def define(word: str) -> Optional[Dict[str, Any]]:
    """The definition behind an English or regional word ('paisa wapas', 'सूट'), or None."""
    if not word:
        return None
    canonical = _alias_index().get(word.strip().casefold())
    return terms().get(canonical) if canonical else None


@lru_cache(maxsize=1)
def plans() -> Dict[str, Dict[str, Any]]:
    """Broadband plan catalog queried from the ontology (`Basic`, `Plus`, `Pro`)."""
    out: Dict[str, Dict[str, Any]] = {}
    for row in _store().query(PLANS_QUERY):
        code = row["code"].value
        out[code] = {
            "code": code,
            "price_rupees": int(row["price"].value),
            "speed_mbps": int(row["speed"].value),
            "kb_article": _value(row["kbId"]) or "KB09",
        }
    return out


@lru_cache(maxsize=1)
def pune_service_areas() -> List[str]:
    """The eight Pune neighbourhoods served by Acme Fibre (queried from `acme:PuneServiceArea`)."""
    return [row["name"].value for row in _store().query(AREAS_QUERY)]


def domain_edges(word_or_term: str) -> Optional[Dict[str, Any]]:
    """Return a concept's reasoned taxonomic and operational edges (KB articles, rules, owner, role)."""
    info = define(word_or_term)
    if not info:
        return None
    iri = info["iri"]
    parents_q = PREFIXES + f"""
    SELECT DISTINCT ?parentLabel WHERE {{
      <{iri}> rdfs:subClassOf+ ?parent .
      ?parent skos:prefLabel ?parentLabel .
      FILTER(LANG(?parentLabel) = "en" || LANG(?parentLabel) = "")
    }} ORDER BY ?parentLabel
    """
    children_q = PREFIXES + f"""
    SELECT DISTINCT ?childLabel WHERE {{
      ?child rdfs:subClassOf+ <{iri}> ;
             skos:prefLabel ?childLabel .
      FILTER(LANG(?childLabel) = "en" || LANG(?childLabel) = "")
    }} ORDER BY ?childLabel
    """
    store = _store()
    return {
        **info,
        "superclasses": [r["parentLabel"].value for r in store.query(parents_q)],
        "subclasses": [r["childLabel"].value for r in store.query(children_q)],
    }


def extract_concepts(text: str) -> List[Dict[str, Any]]:
    """Scan English, Hinglish or regional text and return matched ontology concepts."""
    if not text:
        return []
    lowered = text.casefold()
    matched_terms: List[str] = []
    # Match longer phrases first so "double payment refund" matches before "refund"
    for alias, canonical in sorted(_alias_index().items(), key=lambda kv: -len(kv[0])):
        if len(alias) < 3:
            continue
        if alias.isascii():
            if not re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", lowered):
                continue
        elif alias not in lowered:
            continue
        if canonical not in matched_terms:
            matched_terms.append(canonical)
    all_terms = terms()
    return [all_terms[c] for c in matched_terms if c in all_terms]


OUTAGE_TERMS = ("outage", "outage credit")


def customer_reported_outage(text: str) -> bool:
    """Policy 12: does the customer's own text report that their service is down?

    True when the text names an Outage or OutageCredit concept in any language the ontology labels
    ("no internet", "net band", "इंटरनेट बंद", ...). A slow-speed or billing email is not an outage report."""
    return any(c["term"] in OUTAGE_TERMS for c in extract_concepts(text))


def customer_subgraph(customer: Union[str, Dict[str, Any]],
                      outage: Optional[Dict[str, Any]] = None) -> Store:
    """Create an isolated per-request Store containing the reasoned TBox + ONE customer's ABox triples.

    Policy rule 5 guardrail: the shared `_store()` is never mutated, and only one customer's
    record is ever materialized in the ephemeral store.
    """
    if isinstance(customer, str):
        record = load_customers().get(customer.strip().upper())
        if record is None:
            raise KeyError(f"Unknown customer_id {customer!r}")
    else:
        record = customer
    if outage is None and record.get("area"):
        outage = outage_for(record)

    ephemeral = Store()
    for quad in _store():
        ephemeral.add(quad)

    cid = str(record.get("id") or "TEMP").strip().upper()
    subj = NamedNode(f"{REQ_NS}Customer_{cid}")
    rdf_type = NamedNode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
    xsd_int = NamedNode("http://www.w3.org/2001/XMLSchema#integer")
    xsd_bool = NamedNode("http://www.w3.org/2001/XMLSchema#boolean")

    ephemeral.add(Quad(subj, rdf_type, NamedNode(f"{ACME_NS}Customer")))
    plan_code = str(record.get("plan") or "")
    if plan_code in plans():
        ephemeral.add(Quad(subj, NamedNode(f"{ACME_NS}subscribedTo"), NamedNode(f"{ACME_NS}Plan_{plan_code}")))

    area_name = str(record.get("area") or "")
    area_slug = area_name.replace(" ", "")
    if area_name in pune_service_areas():
        ephemeral.add(Quad(subj, NamedNode(f"{ACME_NS}locatedIn"), NamedNode(f"{ACME_NS}Area_{area_slug}")))

    tenure = int(record.get("tenure_months") or 0)
    credits_30d = int(record.get("credits_last_30_days") or 0)
    dup_amt = duplicate_payment_amount(record.get("payments_this_cycle") or [])

    ephemeral.add(Quad(subj, NamedNode(f"{ACME_NS}tenureMonths"), Literal(str(tenure), datatype=xsd_int)))
    ephemeral.add(Quad(subj, NamedNode(f"{ACME_NS}creditsLast30Days"), Literal(str(credits_30d), datatype=xsd_int)))
    ephemeral.add(
        Quad(
            subj,
            NamedNode(f"{ACME_NS}hasDuplicatePayment"),
            Literal("true" if dup_amt is not None else "false", datatype=xsd_bool),
        )
    )
    if outage:
        out_node = NamedNode(f"{REQ_NS}Outage_{outage['ticket']}")
        ephemeral.add(Quad(out_node, rdf_type, NamedNode(f"{ACME_NS}Outage")))
        ephemeral.add(Quad(subj, NamedNode(f"{ACME_NS}affectedByOutage"), out_node))
    return ephemeral


def price_discount_rupees(percent: Union[int, float], plan_name: str) -> Optional[int]:
    """Compute the rupee value of a percentage discount on a named plan using ontology plan prices."""
    if not plan_name:
        return None
    wanted = plan_name.strip().casefold()
    for code, info in plans().items():
        if code.casefold() == wanted or f"{code.casefold()} plan" == wanted:
            return int(round((float(percent) / 100.0) * info["price_rupees"]))
    return None


def compute_entitlements(customer: Union[str, Dict[str, Any]],
                         *,
                         rules: Optional[Dict[str, Any]] = None,
                         as_of: str = RECORD_DATE) -> Dict[str, Any]:
    """Compute deterministic concession headroom and offer eligibility for one customer.

    Combines:
    1) Ontology meaning & catalog (`plans()`, `excluded_from_limit()`, `terms()`),
    2) Decoupled business rules (`data/acme/business_rules.json` or custom `rules` overrides),
    3) Single-customer operational state (`customers.json` + `outages.json`).
    """
    if isinstance(customer, str):
        record = load_customers().get(customer.strip().upper())
        if record is None:
            raise KeyError(f"Unknown customer_id {customer!r}")
    else:
        record = customer

    active_rules = load_business_rules(overrides=rules) if rules else load_business_rules()
    all_plans = plans()
    all_terms = terms()
    excluded = set(excluded_from_limit())

    plan_code = str(record.get("plan") or "Basic")
    plan_info = all_plans.get(plan_code, {"code": plan_code, "price_rupees": 699, "speed_mbps": 100})
    plan_price = int(plan_info["price_rupees"])
    tenure = int(record.get("tenure_months") or 0)
    balance_due = int(record.get("balance_due") or 0)

    limit_cfg = active_rules["concession_limit"]
    limit_rupees = int(limit_cfg["max_rupees_30_days"])
    ledger_field = str(limit_cfg.get("customer_ledger_field") or "credits_last_30_days")
    used_30d = int(record.get(ledger_field) or 0)
    headroom_rupees = max(0, limit_rupees - used_30d)

    # 1. Late-fee waiver (KB02, Policy 10)
    lfw_cfg = active_rules["offers"]["late-fee waiver"]
    lfw_amount = int(lfw_cfg["fixed_amount_rupees"])
    lfw_min_tenure = int(lfw_cfg["min_tenure_months"])
    lfw_cooldown = int(
        lfw_cfg.get("cooldown_months")
        or all_terms.get("late-fee waiver", {}).get("once_per_months")
        or 12
    )
    lfw_used_on = record.get(lfw_cfg["cooldown_field"])
    lfw_months_ago = months_since(lfw_used_on, as_of=as_of)
    lfw_tenure_ok = tenure >= lfw_min_tenure
    lfw_cooldown_ok = lfw_months_ago is None or lfw_months_ago >= lfw_cooldown
    lfw_counts = "late-fee waiver" not in excluded
    lfw_within_limit = (not lfw_counts) or (lfw_amount <= headroom_rupees)
    lfw_eligible = lfw_tenure_ok and lfw_cooldown_ok
    if not lfw_tenure_ok:
        lfw_reason = f"Ineligible: tenure {tenure} months is below {lfw_min_tenure}-month minimum (KB02, policy 10)."
    elif not lfw_cooldown_ok:
        lfw_reason = f"Ineligible: late-fee waiver already used on {lfw_used_on} ({lfw_months_ago}m ago < {lfw_cooldown}m cooldown)."
    elif not lfw_within_limit:
        lfw_reason = f"Needs human approval: ₹{lfw_amount} exceeds remaining 30-day headroom of ₹{headroom_rupees}."
    else:
        lfw_reason = f"Eligible: tenure {tenure}m >= {lfw_min_tenure}m, cooldown clear, ₹{lfw_amount} within ₹{headroom_rupees} headroom."

    # 2. Retention offer (KB11, Policy 8 & 10)
    ro_cfg = active_rules["offers"]["retention offer"]
    ro_pct = int(ro_cfg["discount_percent"])
    ro_amount = int(round((ro_pct / 100.0) * plan_price))
    ro_min_tenure = int(ro_cfg["min_tenure_months"])
    ro_cooldown = int(
        ro_cfg.get("cooldown_months")
        or all_terms.get("retention offer", {}).get("once_per_months")
        or 12
    )
    ro_used_on = record.get(ro_cfg["cooldown_field"])
    ro_months_ago = months_since(ro_used_on, as_of=as_of)
    ro_tenure_ok = tenure >= ro_min_tenure
    ro_cooldown_ok = ro_months_ago is None or ro_months_ago >= ro_cooldown
    ro_counts = "retention offer" not in excluded
    ro_within_limit = (not ro_counts) or (ro_amount <= headroom_rupees)
    ro_eligible = ro_tenure_ok and ro_cooldown_ok
    if not ro_tenure_ok:
        ro_reason = f"Ineligible: tenure {tenure} months is below {ro_min_tenure}-month minimum (KB11, policy 10)."
    elif not ro_cooldown_ok:
        ro_reason = f"Ineligible: retention offer already used on {ro_used_on} ({ro_months_ago}m ago < {ro_cooldown}m cooldown)."
    else:
        ro_reason = (
            f"Eligible under KB11: {ro_pct}% off {plan_code} (₹{plan_price}) = ₹{ro_amount} "
            f"(tenure {tenure}m >= {ro_min_tenure}m, cooldown clear)."
        )

    # 3. Double payment refund (KB04, Policy 8)
    dpr_cfg = active_rules["offers"]["double payment refund"]
    dup_amt = duplicate_payment_amount(record.get(dpr_cfg["requires_duplicate_payment_in_field"]) or [])
    dpr_counts = "double payment refund" not in excluded
    dpr_eligible = dup_amt is not None
    dpr_reason = (
        f"Eligible: duplicate payment of ₹{dup_amt} on record; automatic refund in {dpr_cfg['sla_working_days']} working days (excluded from ₹{limit_rupees} limit)."
        if dpr_eligible
        else "Ineligible: customer record does not show a duplicate payment in this billing cycle (policy 9)."
    )

    # 4. Outage credit (KB06, Policy 8)
    oc_cfg = active_rules["offers"]["outage credit"]
    active_outage = outage_for(record) if record.get("area") else None
    oc_min_hours = int(oc_cfg["min_outage_hours"])
    oc_eligible = outage_exceeds_hours(active_outage, min_hours=oc_min_hours)
    oc_counts = "outage credit" not in excluded
    if active_outage and oc_eligible:
        oc_reason = f"Eligible: outage {active_outage['ticket']} exceeds {oc_min_hours}h; credit added automatically (KB06)."
    elif active_outage:
        oc_reason = (
            f"Not yet triggered: outage {active_outage['ticket']} (since {active_outage['since']}) has not exceeded "
            f"{oc_min_hours} hours; automatic credit applies only after {oc_min_hours} hours (KB06)."
        )
    else:
        oc_reason = f"Ineligible: no active outage on record in {record.get('area')}."

    return {
        "customer_id": record.get("id"),
        "customer_name": record.get("name"),
        "area": record.get("area"),
        "is_pune_service_area": record.get("area") in pune_service_areas(),
        "plan": plan_code,
        "plan_price_rupees": plan_price,
        "tenure_months": tenure,
        "balance_due_rupees": balance_due,
        "complaints_last_30_days": int(record.get("complaints_last_30_days") or 0),
        "concession_limit_rupees": limit_rupees,
        "credits_used_last_30_days_rupees": used_30d,
        "concession_headroom_rupees": headroom_rupees,
        "excluded_from_limit": sorted(excluded),
        "offers": {
            "late-fee waiver": {
                "eligible": lfw_eligible,
                "auto_approvable": lfw_eligible and lfw_within_limit,
                "needs_human": lfw_eligible and not lfw_within_limit,
                "amount_rupees": lfw_amount,
                "counts_toward_limit": lfw_counts,
                "tenure_ok": lfw_tenure_ok,
                "cooldown_ok": lfw_cooldown_ok,
                "last_used_on": lfw_used_on,
                "kb_article": lfw_cfg["kb_article"],
                "reason": lfw_reason,
            },
            "retention offer": {
                "eligible": ro_eligible,
                "auto_approvable": ro_eligible and ro_within_limit,
                "exceeds_500_limit": ro_amount > headroom_rupees,
                "discount_percent": ro_pct,
                "amount_rupees": ro_amount,
                "counts_toward_limit": ro_counts,
                "tenure_ok": ro_tenure_ok,
                "cooldown_ok": ro_cooldown_ok,
                "last_used_on": ro_used_on,
                "kb_article": ro_cfg["kb_article"],
                "reason": ro_reason,
            },
            "double payment refund": {
                "eligible": dpr_eligible,
                "auto_approvable": dpr_eligible,
                "needs_human": False,
                "amount_rupees": dup_amt or 0,
                "counts_toward_limit": dpr_counts,
                "sla_working_days": dpr_cfg["sla_working_days"],
                "kb_article": dpr_cfg["kb_article"],
                "reason": dpr_reason,
            },
            "outage credit": {
                "eligible": oc_eligible,
                "auto_approvable": oc_eligible,
                "needs_human": False,
                "counts_toward_limit": oc_counts,
                "active_outage_ticket": active_outage["ticket"] if active_outage else None,
                "kb_article": oc_cfg["kb_article"],
                "reason": oc_reason,
            },
        },
    }


def validate_ontology_ops(rules_path: Optional[Path] = None) -> Dict[str, Any]:
    """Operational governance check: verify zero schema drift across ontology.ttl,
    business_rules.json, customers.json, outages.json, and kb.md.
    """
    all_terms = terms()
    ont_plans = plans()
    ont_areas = set(pune_service_areas())
    kb_ids = set(kb_by_id().keys())
    rules = load_business_rules(path=rules_path)
    drift_errors: List[str] = []

    # 1. Stewardship & lifecycle check on all OWL classes
    unowned = [t["term"] for t in all_terms.values() if t["term"] != "operational owner" and not t.get("owner_team")]
    if unowned:
        drift_errors.append(f"Classes missing operational owner (acme:ownedBy): {unowned}")

    # 2. KB reference integrity
    for t in all_terms.values():
        for kb_id in t.get("kb_articles", []):
            if kb_id not in kb_ids:
                drift_errors.append(f"Concept {t['term']!r} links to missing article {kb_id!r}")

    # 3. Customer & outage catalog sync
    for cid, cust in load_customers().items():
        if cust["plan"] not in ont_plans:
            drift_errors.append(f"Customer {cid} has plan {cust['plan']!r} not in ontology acme:Plan")
        if cust["area"] not in ont_areas:
            drift_errors.append(f"Customer {cid} has area {cust['area']!r} not in ontology acme:PuneServiceArea")
    for area, out in load_outages().items():
        if area not in ont_areas:
            drift_errors.append(f"Outage {out['ticket']} area {area!r} not in ontology acme:PuneServiceArea")

    # 4. Business rules -> Ontology concept binding integrity
    limit_concept = rules.get("concession_limit", {}).get("concept")
    if limit_concept not in all_terms:
        drift_errors.append(f"business_rules.json concession_limit concept {limit_concept!r} missing from ontology")
    for offer_key, offer_cfg in rules.get("offers", {}).items():
        concept = offer_cfg.get("concept")
        if concept not in all_terms:
            drift_errors.append(f"business_rules.json offer {offer_key!r} concept {concept!r} missing from ontology")

    # 5. Policy rule 5 PII guardrail
    glossary_text = glossary()
    if re.search(r"\bAC\d{4}\b", glossary_text):
        drift_errors.append("Policy rule 5 violation: customer ID found in static ontology glossary")

    return {
        "ok": len(drift_errors) == 0,
        "class_count": len(all_terms),
        "plan_count": len(ont_plans),
        "service_area_count": len(ont_areas),
        "stewardship_coverage": round(
            (len(all_terms) - len(unowned)) / max(1, len(all_terms)), 3
        ),
        "drift_errors": drift_errors,
    }
