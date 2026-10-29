"""The Acme ontology: shared definitions for the words policy.md relies on (data/acme/ontology.ttl).

Definitions only. Customer records stay in customers.json (policy rule 5).

    from lab.ontology import glossary, excluded_from_limit, define
    glossary()                    # "- account holder: The customer named on the account. ..." for a prompt
    excluded_from_limit()         # ['double payment refund', 'outage credit']
    define("paisa wapas")         # {'term': 'refund', 'definition': ..., 'source': 'KB04', ...}
"""
from __future__ import annotations

from functools import lru_cache
from typing import Dict, List, Optional

from pyoxigraph import RdfFormat, Store

from .acme import DATA

ONTOLOGY = DATA / "ontology.ttl"
PREFIXES = """
PREFIX acme: <https://acme.example/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
"""
TERMS = PREFIXES + """
SELECT ?term ?label ?definition ?note ?source WHERE {
  ?term skos:prefLabel ?label ; skos:definition ?definition .
  OPTIONAL { ?term skos:scopeNote ?note }
  OPTIONAL { ?term acme:source ?source }
} ORDER BY ?label
"""
LABELS = PREFIXES + """
SELECT ?label ?name WHERE {
  ?term skos:prefLabel ?label .
  { ?term skos:prefLabel ?name } UNION { ?term skos:altLabel ?name }
}
"""
EXCLUDED_FROM_LIMIT = PREFIXES + """
SELECT ?label WHERE {
  ?term rdfs:subClassOf+ acme:Concession ; acme:countsTowardLimit false ; skos:prefLabel ?label .
} ORDER BY ?label
"""


@lru_cache(maxsize=1)
def _store() -> Store:
    store = Store()
    store.load(path=str(ONTOLOGY), format=RdfFormat.TURTLE)
    return store


def _value(term) -> Optional[str]:
    return term.value if term is not None else None


@lru_cache(maxsize=1)
def terms() -> Dict[str, Dict[str, Optional[str]]]:
    """Every defined term by its English label."""
    return {row["label"].value: {"term": row["label"].value, "definition": row["definition"].value,
                                 "note": _value(row["note"]), "source": _value(row["source"])}
            for row in _store().query(TERMS)}


def glossary() -> str:
    """One line per term, ready to paste into a prompt as a 'Definitions' block."""
    return "\n".join(f"- {t['term']}: {t['definition']}" + (f" {t['note']}" if t["note"] else "")
                     for t in terms().values())


def excluded_from_limit() -> List[str]:
    """Kinds of money that don't count toward the ₹500 limit (automatic ones)."""
    return [row["label"].value for row in _store().query(EXCLUDED_FROM_LIMIT)]


def define(word: str) -> Optional[Dict[str, Optional[str]]]:
    """The definition behind an English or regional word ('paisa wapas', 'सूट'), or None."""
    wanted = word.strip().casefold()
    for row in _store().query(LABELS):
        if row["name"].value.casefold() == wanted:
            return terms()[row["label"].value]
    return None
