# Later: an ontology layer for Acme Fibre

Prompted by Jessica Talisman's *Ontology Pipeline* summary: when many agents share entities like "Customer",
each one can read them differently. Technical interoperability works, but semantic interoperability breaks.

Diagram: [day8-ontology-layer-plan.drawio](day8-ontology-layer-plan.drawio) (open with the Draw.io extension).

## Do we need it now

No. Project 1 has one assistant, one customer record ([customers.json](../../data/acme/customers.json)) and one
policy ([policy.md](../../data/acme/policy.md)). The early stages of the ontology pipeline are already in place:

| Ontology pipeline stage | Where it already lives                                                              |
|-------------------------|-------------------------------------------------------------------------------------|
| Controlled vocabulary   | Policy rules 8 to 11 define "₹500 limit", "account holder", "more than 12 months"    |
| Metadata standard       | Customer record fields and the tool JSON schemas in `lab/acme_tools.py`             |
| Agreed meaning, tested  | `tests/features/policy_rules.feature` maps stakeholder wording to grader codes      |

## When it becomes worth building

* Several agents share the same entities, for example separate billing, network and retention agents
* Project 6 adds a tool that changes data (`issue_refund`), so "credit" and "account holder" must mean the
  same thing to the agent, the tool and the human approver
* Error analysis shows a real share of failures come from a misread *term*, not a missing fact

## How to prove it first (measure before you believe)

1. Tag version B and C failures where the model misread a term: ₹500 per message instead of per 30 days,
   counting KB04 or KB06 refunds toward the limit, treating a caller as the account holder.
2. If that tag is a meaningful share, generate a glossary from the ontology and add it to the context.
3. Run with and without the glossary and compare with day 7 error bars. Keep it only if the intervals separate.

## Recommended tool: pyoxigraph

[pyoxigraph](https://pypi.org/project/pyoxigraph/) (Python bindings of [Oxigraph](https://github.com/oxigraph/oxigraph)),
dual licensed **MIT or Apache-2.0**, so you can use it under MIT. Tested with version 0.5.13.

Why it fits this project:

* `pip install pyoxigraph`, runs in-process with an in-memory store, no server, works offline on a Mac
* Reads Turtle and JSON-LD and answers SPARQL 1.1, so the ontology stays in W3C standards (OWL classes,
  SKOS labels) and can move to Protégé or a larger graph store later without rewriting it
* Small enough to sit next to `lab/acme.py` as one more data file plus one loader

Other options checked, none MIT: RDFLib (BSD-3-Clause), Owlready2 (LGPL-3.0), Protégé (BSD-2-Clause),
LinkML (CC0-1.0).

## Decision: where the ontology lives (2026-10-28)

| Stage                                   | Store                                                                 | Why                                                |
|-----------------------------------------|-----------------------------------------------------------------------|----------------------------------------------------|
| Project 1: prove the hypothesis         | In-process: pyoxigraph, or three SQLite tables from the standard library | No server, no cost, runs offline on the Mac        |
| Project 6: shared across agents, linked to records | Azure Database for PostgreSQL flexible server; plain tables for definitions, Apache AGE (openCypher) only for multi-hop traversals | Managed, one database the team already knows |

If SQL reads easier than SPARQL, use SQLite with the same shape the Postgres version will have later:
`term(id, pref_label, definition, scope_note, counts_toward_limit)`, `term_alias(term_id, label, lang)` and
`term_parent(child, parent)`, with `WITH RECURSIVE` for "every subtype of concession".

Trade-off to remember: Postgres and AGE store a property graph, not RDF, so moving there gives up OWL, SKOS
and SPARQL. Neither is MIT (PostgreSQL Licence, Apache-2.0).

## Sketch

Keep definitions in the ontology and customer data in `customers.json`. The ontology must never hold
customer records (policy rule 5).

`data/acme/ontology.ttl`:

```turtle
@prefix acme: <https://acme.example/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .

acme:Customer a owl:Class ;
    skos:prefLabel "customer"@en ;
    skos:definition "A person with an Acme Fibre account, identified by an id like AC1003." .

acme:AccountHolder a owl:Class ;
    rdfs:subClassOf acme:Customer ;
    skos:prefLabel "account holder"@en ;
    skos:definition "The customer named on the account. Only this person can cancel, shift, change the plan or transfer it (rule 11)." .

acme:Concession a owl:Class ;
    skos:prefLabel "concession"@en ;
    skos:definition "Money given to a customer: a refund, credit, waiver or the rupee value of a discount." ;
    skos:scopeNote "Counts toward the 500 rupee limit per customer over 30 days (rule 8)." .

acme:Refund a owl:Class ;
    rdfs:subClassOf acme:Concession ;
    skos:prefLabel "refund"@en ;
    skos:altLabel "paisa wapas"@hi-Latn ;
    skos:definition "Money returned to the customer." ;
    acme:countsTowardLimit true .

acme:DoublePaymentRefund a owl:Class ;
    rdfs:subClassOf acme:Refund ;
    skos:prefLabel "double payment refund"@en ;
    skos:definition "Automatic refund of a duplicate payment (KB04)." ;
    acme:countsTowardLimit false .
```

Load it and build the glossary for the prompt:

```python
from pyoxigraph import RdfFormat, Store

GLOSSARY = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?label ?definition WHERE {
  ?term skos:prefLabel ?label ; skos:definition ?definition .
} ORDER BY ?label
"""

EXCLUDED_FROM_LIMIT = """
PREFIX acme: <https://acme.example/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?label WHERE {
  ?term rdfs:subClassOf+ acme:Concession ;
        acme:countsTowardLimit false ;
        skos:prefLabel ?label .
}
"""

store = Store()
store.load(path="data/acme/ontology.ttl", format=RdfFormat.TURTLE)
glossary = "\n".join(f"- {r['label'].value}: {r['definition'].value}" for r in store.query(GLOSSARY))
excluded = [r["label"].value for r in store.query(EXCLUDED_FROM_LIMIT)]
```

The Hinglish `altLabel` entries are the thesaurus stage: they let a search or a router map "paisa wapas" to the
same `acme:Refund` concept the grader and the tools use.

## Implementation plan

Each phase has a gate. Stop at the first gate that fails and write down why; that is a valid result.

### Phase 0: Measure the problem (no new code)

1. Before looking at the data, write down the threshold that makes this worth building (for example,
   "term misreads are at least 1 in 5 failures").
2. Load `data/results/B.jsonl` (and C once day 8 ships) with `lab.acme.load_results()`.
3. Read every failure and tag it `term_misread`, `missing_fact`, `tone` or `other`.
   A `term_misread` is a reply that had the right facts but got the meaning wrong.

Gate: the `term_misread` share is at or above the threshold. If not, stop here.

### Phase 1: Write the ontology (definitions only)

1. Create `data/acme/ontology.ttl` from the sketch above.
2. Cover only the terms the tagged failures misread, plus the rule 8 to 11 terms: customer, account holder,
   concession and its subtypes, once-only offer, tenure.
3. Add `skos:altLabel` entries in Hinglish for terms seen in `cases.jsonl`.
4. Never add customer ids, names or balances.

Gate: every term in rules 8 to 11 has a `skos:definition`, and a second reader agrees with each one.

### Phase 2: Loader and tests

1. Add `pyoxigraph` to `dependencies` in `pyproject.toml`.
2. Add `lab/ontology.py` with `glossary() -> str` and `excluded_from_limit() -> list[str]`.
3. Add `tests/features/ontology.feature` with scenarios such as "KB04 and KB06 do not count toward the
   limit" and "an account holder is a customer", plus step definitions in `tests/test_ontology.py`.

Gate: `../.venv/bin/python -m pytest -v` passes from `fde-first-principles/`.

### Phase 3: Version B with the glossary

1. Copy the day 6 prompt and add the `glossary()` output as a "Definitions" block.
2. Run on `cases.jsonl` and `cases_abuse.jsonl` with the same model, seed and temperature as B.
3. Save with `lab.acme.save_results("B_glossary", rows)`.

Gate: the run completes and the grader scores every case.

### Phase 4: Version C with a lookup tool (optional)

1. Add `define_term(term)` to `lab/acme_tools.py`. It returns the definition and the scope note, matching on
   `prefLabel` or `altLabel`.
2. Count how often the agent calls it and on which terms.

Gate: the agent calls it on at least some of the cases it previously misread; otherwise the tool is dead
weight.

### Phase 5: Decide with evidence

1. Compare B and B_glossary (and C and C_define) with day 7 confidence intervals.
2. Re-tag the remaining failures: did `term_misread` drop, or did errors move to another tag?
3. Write the decision in this file: keep, drop or revisit in project 6.

Gate: intervals separate. If they overlap, the honest answer is "no measurable gain on this data".

### Out of scope until project 6

* Linking the ontology to live customer records (a knowledge graph), on Azure PostgreSQL with Apache AGE
* Sharing the ontology across several agents
* OWL reasoning or SHACL validation
* Keeping definitions and records apart in one database: separate schema and role (policy rule 5)
