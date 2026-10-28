# Later: an ontology layer for Acme Fibre

Prompted by Jessica Talisman's *Ontology Pipeline* summary: when many agents share entities like "Customer",
each one can read them differently. Technical interoperability works, but semantic interoperability breaks.

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
