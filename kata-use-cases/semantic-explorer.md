You should build a Business Ontology Explorer, not another generic RDF viewer. The tool should translate technical RDF/OWL constructs into business-friendly views such as Concept → Meaning → Rules → Evidence → Owner → Impact.

1. The showcase outcome

A business user selects Retention Offer and sees:

Retention Offer
│
├── Business meaning
│   └── 50% off for one month for an eligible customer
│
├── Eligibility
│   ├── Customer tenure: 13+ months
│   └── Not used in previous 12 months
│
├── Financial treatment
│   └── Does not count toward the ₹500 concession limit
│
├── Governed by
│   ├── Policy Rule 10
│   └── Policy Rule 13
│
├── Documented in
│   └── KB11
│
├── Business owner
│   └── Customer Retention & Lifecycle
│
└── Lifecycle
    └── Active


This information already exists across ontology.txt, but the application needs to organize it around a selected business concept rather than showing every triple simultaneously.

2. Recommended architecture

For a showcase-quality tool, use:

Layer	Technology	PurposeFront end	React + TypeScript	Business-facing interface
Graph	Cytoscape.js	Interactive concept and relationship graph
API	FastAPI	Parse ontology and expose business-oriented APIs
RDF engine	RDFLib	Load Turtle and run SPARQL
Reasoning	OWL-RL	Calculate inherited RDF/OWL relationships
Validation	pySHACL	Validate ontology and business constraints
Storage initially	In-memory RDFLib graph	Enough for your 450-line file
Deployment	Docker Compose	Consistent local and showcase setup

Cytoscape.js is an MIT-licensed graph visualization library with layouts, selectors, filtering, graph algorithms, touch support and JSON serialization. It is a library rather than a finished application, which makes it suitable for your custom business explorer.

RDFLib parses Turtle and provides RDF graphs, namespaces and SPARQL 1.1 querying. It can operate entirely in memory for an ontology of this size.

Architecture flow
                            Business browser
                                   │
              ┌────────────────────┴────────────────────┐
              │                                         │
        Business cards                         Cytoscape graph
              │                                         │
              └────────────────────┬────────────────────┘
                                   │
                              React UI
                                   │
                              REST/JSON
                                   │
                              FastAPI API
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
              RDFLib           OWL-RL           pySHACL
                 │
      ┌──────────┼───────────┬─────────────┐
      │          │           │             │
ontology.ttl  policy.md  business_rules  knowledge base
                            .json             .md


The current file explicitly separates ontology definitions from customer records and business-rule thresholds. The application should preserve that separation rather than merging all information into one uncontrolled graph.

3. Build the MVP in two iterations
Iteration 1: Ontology Explorer

Build these five screens:

Executive overview
Concept explorer
Rule explorer
Knowledge lineage
Governance and quality

Do not start with ontology editing. Keep the first version read-only.

Iteration 2: Rule and evidence integration

Later, ingest:

policy.md
business_rules.json
kb.md
optionally anonymized example customer scenarios

This produces the level-down view missing from WebVOWL.

4. Project structure
business-ontology-explorer/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── ontology.py
│   │   ├── services/
│   │   │   ├── concept_service.py
│   │   │   ├── rule_service.py
│   │   │   ├── lineage_service.py
│   │   │   └── validation_service.py
│   │   └── models/
│   │       └── api_models.py
│   ├── data/
│   │   ├── ontology.ttl
│   │   ├── policy.md
│   │   ├── business_rules.json
│   │   └── shapes.ttl
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ConceptGraph.tsx
│   │   │   ├── ConceptCard.tsx
│   │   │   ├── RulePanel.tsx
│   │   │   ├── EvidencePanel.tsx
│   │   │   └── GovernancePanel.tsx
│   │   ├── pages/
│   │   │   ├── Overview.tsx
│   │   │   ├── Explorer.tsx
│   │   │   ├── Rules.tsx
│   │   │   └── Quality.tsx
│   │   └── api.ts
│   └── package.json
├── docker-compose.yml
└── README.md

5. Bootstrap the project
Backend
mkdir business-ontology-explorer
cd business-ontology-explorer

mkdir -p backend/app/services backend/app/models backend/data backend/tests
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install fastapi uvicorn rdflib owlrl pyshacl pydantic python-multipart
pip freeze > requirements.txt


pySHACL validates RDF graphs against SHACL shapes and uses RDFLib and OWL-RL for RDF processing and inference.

Copy the file:

cp /path/to/ontology.txt data/ontology.ttl

Front end

From the project root:

npm create vite@latest frontend -- --template react-ts
cd frontend

npm install
npm install cytoscape
npm install -D @types/cytoscape

6. Load and index the ontology

Create backend/app/ontology.py:

from pathlib import Path

from rdflib import Graph, Namespace
from owlrl import DeductiveClosure, OWLRL_Semantics

ACME = Namespace("https://acme.example/ontology#")
DATA_PATH = Path(__file__).parent.parent / "data" / "ontology.ttl"


class OntologyStore:
    def __init__(self) -> None:
        self.asserted = Graph()
        self.asserted.parse(DATA_PATH, format="turtle")

        # Keep asserted and inferred graphs conceptually separate.
        self.inferred = Graph()

        for triple in self.asserted:
            self.inferred.add(triple)

        DeductiveClosure(OWLRL_Semantics).expand(self.inferred)


store = OntologyStore()


Keeping asserted and inferred facts distinguishable matters. A business user should be able to see:

countsTowardLimit = false
Source: directly declared on RetentionOffer


versus:

oncePerMonths = 12
Source: inherited from OnceOnlyOffer


Without this distinction, the presentation may suggest that inherited information was explicitly authored on the selected concept.

7. Create business-oriented API models

Your API should not expose raw RDF triples as its main output.

Return this shape:

{
  "id": "RetentionOffer",
  "label": "retention offer",
  "type": "BusinessConcept",
  "definition": "50% off for 1 month...",
  "parents": [
    {
      "id": "Discount",
      "label": "discount"
    },
    {
      "id": "OnceOnlyOffer",
      "label": "once-only offer"
    }
  ],
  "businessAttributes": [
    {
      "name": "Counts toward concession limit",
      "value": false,
      "source": "asserted"
    },
    {
      "name": "Offer frequency",
      "value": "Once every 12 months",
      "source": "inherited from OnceOnlyOffer"
    }
  ],
  "rules": [
    {
      "id": "PolicyRule10",
      "number": 10
    },
    {
      "id": "PolicyRule13",
      "number": 13
    }
  ],
  "evidence": [
    {
      "id": "KB11",
      "type": "KnowledgeArticle"
    }
  ],
  "owner": "Customer Retention & Lifecycle",
  "lifecycle": "active"
}


This is the most important transformation in the application:

RDF representation
        ↓
semantic interpretation
        ↓
business-oriented JSON
        ↓
business-readable interface

8. Implement the principal SPARQL queries
List classes
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?class ?label ?definition
WHERE {
    ?class a owl:Class .
    OPTIONAL { ?class skos:prefLabel ?label }
    OPTIONAL { ?class skos:definition ?definition }
}
ORDER BY ?label

Show parents and children
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?direction ?related ?label
WHERE {
    {
        BIND("parent" AS ?direction)
        <CONCEPT_IRI> rdfs:subClassOf ?related .
    }
    UNION
    {
        BIND("child" AS ?direction)
        ?related rdfs:subClassOf <CONCEPT_IRI> .
    }

    OPTIONAL { ?related skos:prefLabel ?label }
}

Find rules enforced by a concept
PREFIX acme: <https://acme.example/ontology#>

SELECT ?rule ?number
WHERE {
    <CONCEPT_IRI> acme:enforcesRule ?rule .
    OPTIONAL { ?rule acme:ruleNumber ?number }
}
ORDER BY ?number

Find concepts governed by a rule
PREFIX acme: <https://acme.example/ontology#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concept ?label ?definition
WHERE {
    ?concept acme:enforcesRule <RULE_IRI> .
    OPTIONAL { ?concept skos:prefLabel ?label }
    OPTIONAL { ?concept skos:definition ?definition }
}
ORDER BY ?label

Trace knowledge evidence
PREFIX acme: <https://acme.example/ontology#>

SELECT ?article ?articleId
WHERE {
    <CONCEPT_IRI> acme:documentedIn ?article .
    OPTIONAL { ?article acme:articleId ?articleId }
}
ORDER BY ?articleId

9. Implement FastAPI endpoints

Create backend/app/main.py:

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rdflib import RDF, RDFS, OWL, SKOS, URIRef

from .ontology import store, ACME

app = FastAPI(
    title="Business Ontology Explorer",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def local_name(value: URIRef) -> str:
    text = str(value)
    return text.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def first_value(graph, subject, predicate):
    return next(iter(graph.objects(subject, predicate)), None)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "assertedTriples": len(store.asserted),
        "inferredTriples": len(store.inferred),
    }


@app.get("/api/concepts")
def concepts():
    results = []

    for concept in store.asserted.subjects(RDF.type, OWL.Class):
        label = first_value(store.asserted, concept, SKOS.prefLabel)
        definition = first_value(store.asserted, concept, SKOS.definition)

        results.append({
            "id": local_name(concept),
            "iri": str(concept),
            "label": str(label) if label else local_name(concept),
            "definition": str(definition) if definition else None,
        })

    return sorted(results, key=lambda item: item["label"].lower())


@app.get("/api/concepts/{concept_id}")
def concept_detail(concept_id: str):
    concept = ACME[concept_id]

    if (concept, RDF.type, OWL.Class) not in store.asserted:
        raise HTTPException(status_code=404, detail="Concept not found")

    label = first_value(store.asserted, concept, SKOS.prefLabel)
    definition = first_value(store.asserted, concept, SKOS.definition)
    lifecycle = first_value(store.asserted, concept, ACME.lifecycleStatus)

    parents = []
    for parent in store.asserted.objects(concept, RDFS.subClassOf):
        parent_label = first_value(store.asserted, parent, SKOS.prefLabel)
        parents.append({
            "id": local_name(parent),
            "label": str(parent_label) if parent_label else local_name(parent),
        })

    children = []
    for child in store.asserted.subjects(RDFS.subClassOf, concept):
        child_label = first_value(store.asserted, child, SKOS.prefLabel)
        children.append({
            "id": local_name(child),
            "label": str(child_label) if child_label else local_name(child),
        })

    rules = []
    for rule in store.asserted.objects(concept, ACME.enforcesRule):
        number = first_value(store.asserted, rule, ACME.ruleNumber)
        rules.append({
            "id": local_name(rule),
            "number": int(number) if number else None,
        })

    articles = []
    for article in store.asserted.objects(concept, ACME.documentedIn):
        article_id = first_value(store.asserted, article, ACME.articleId)
        articles.append({
            "id": local_name(article),
            "articleId": str(article_id) if article_id else None,
        })

    owners = []
    for owner in store.asserted.objects(concept, ACME.ownedBy):
        owner_label = first_value(store.asserted, owner, SKOS.prefLabel)
        owners.append({
            "id": local_name(owner),
            "label": str(owner_label) if owner_label else local_name(owner),
        })

    return {
        "id": concept_id,
        "iri": str(concept),
        "label": str(label) if label else concept_id,
        "definition": str(definition) if definition else None,
        "lifecycle": str(lifecycle) if lifecycle else None,
        "parents": parents,
        "children": children,
        "rules": rules,
        "knowledgeArticles": articles,
        "owners": owners,
    }


Run it:

cd backend
source .venv/bin/activate

uvicorn app.main:app --reload --port 8000


Test:

http://localhost:8000/docs

10. Build a focused graph, not a graph of everything

The primary graph should display only:

selected concept
direct parents
direct children
associated rules
knowledge articles
owner
selected business attributes

Use colors that convey meaning:

Node	Color	ShapeSelected concept	Dark blue	Rounded rectangle
Parent class	Purple	Rectangle
Child concept	Light blue	Rectangle
Policy rule	Orange	Diamond
Knowledge article	Green	Document-like rectangle
Owner	Teal	Hexagon
Literal/business value	Grey	Pill

Avoid putting xsd:string, owl:Thing and every datatype property on the main business view. Put those behind a Technical details toggle.

The graph should have two modes:

Business view: meaning, rules, evidence, owner
Technical view: classes, properties, RDF/OWL axioms, IRIs

11. Cytoscape component

Create frontend/src/components/ConceptGraph.tsx:

import { useEffect, useRef } from "react";
import cytoscape, { ElementDefinition } from "cytoscape";

type Props = {
  elements: ElementDefinition[];
  onSelect: (id: string) => void;
};

export function ConceptGraph({ elements, onSelect }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const cy = cytoscape({
      container: containerRef.current,
      elements,
      layout: {
        name: "breadthfirst",
        directed: true,
        spacingFactor: 1.4,
      },
      style: [
        {
          selector: "node",
          style: {
            label: "data(label)",
            "font-size": 12,
            "text-wrap": "wrap",
            "text-max-width": 130,
            "background-color": "#4f6bed",
            color: "#ffffff",
            width: 70,
            height: 45,
            shape: "round-rectangle",
          },
        },
        {
          selector: 'node[type = "selected"]',
          style: {
            "background-color": "#0f3b5f",
            width: 95,
            height: 60,
            "font-weight": "bold",
          },
        },
        {
          selector: 'node[type = "rule"]',
          style: {
            "background-color": "#c55a11",
            shape: "diamond",
          },
        },
        {
          selector: 'node[type = "article"]',
          style: {
            "background-color": "#39825a",
          },
        },
        {
          selector: 'node[type = "owner"]',
          style: {
            "background-color": "#007f8b",
            shape: "hexagon",
          },
        },
        {
          selector: "edge",
          style: {
            label: "data(label)",
            "font-size": 10,
            width: 2,
            "line-color": "#a7a7a7",
            "target-arrow-color": "#a7a7a7",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
          },
        },
      ],
    });

    cy.on("tap", "node", event => {
      onSelect(event.target.id());
    });

    return () => cy.destroy();
  }, [elements, onSelect]);

  return <div ref={containerRef} style={{ width: "100%", height: "650px" }} />;
}


Cytoscape.js supports selectors, layouts, style mappings and interactive graph events, which fit this focused semantic-neighborhood approach.

12. Add the missing rule content

The current ontology only gives rule identifiers and numbers:

acme:PolicyRule10 a acme:PolicyRule ;
    acme:ruleNumber 10 .


It does not contain the complete Rule 10 statement. The detailed rules are expected in data/acme/policy.md.

Parse policy.md into a structure like:

{
  "10": {
    "title": "Once-only offer eligibility",
    "statement": "The offer is available only...",
    "conditions": [
      "Tenure must be at least 13 months",
      "Offer must not have been used in the last 12 months"
    ],
    "outcome": "Offer may be proposed",
    "source": "policy.md"
  }
}


Avoid claiming that this example wording is the real policy until it has been extracted from the actual file.

The UI then displays:

Rule 10

Purpose
Controls eligibility for once-only offers.

Applies to
• Late-fee waiver
• Retention offer
• Tenure
• Once-only offer

Evidence
• policy.md
• KB02
• KB11

13. Add SHACL validation

Create backend/data/shapes.ttl:

@prefix acme: <https://acme.example/ontology#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

acme:PolicyRuleShape
    a sh:NodeShape ;
    sh:targetClass acme:PolicyRule ;
    sh:property [
        sh:path acme:ruleNumber ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:integer ;
        sh:minInclusive 1 ;
    ] .

acme:PlanShape
    a sh:NodeShape ;
    sh:targetClass acme:Plan ;
    sh:property [
        sh:path acme:planCode ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
    ] ;
    sh:property [
        sh:path acme:monthlyPriceRupees ;
        sh:minCount 1 ;
        sh:datatype xsd:integer ;
        sh:minExclusive 0 ;
    ] .


Show the result in business language:

Ontology quality

✓ All policy rules have a numeric identifier
✓ All plans have a plan code
✓ All plan prices are positive integers
⚠ PolicyRule description says rules 1–11, but rules 12 and 13 exist


The final warning requires a custom lint rule because it compares narrative metadata with declared instances. In the current ontology, PolicyRule12 and PolicyRule13 exist even though the class and property definitions refer to rules 1 through 11.

14. Add explainability

Every business statement should have a Why am I seeing this? action.

For example:

Retention Offer does not count toward the ₹500 limit.

Why?

Direct assertion:
RetentionOffer → countsTowardLimit → false

Source:
ontology.ttl

Related policy:
Policy Rule 13

Related knowledge:
KB11


For inherited values:

Retention Offer may be used once every 12 months.

Why?

RetentionOffer → subclassOf → OnceOnlyOffer
OnceOnlyOffer → oncePerMonths → 12

Status:
Inferred through class inheritance


This provenance view will make the tool credible to architecture, governance and business stakeholders.

15. The business showcase script

Use a six-minute demonstration.

Minute 1: Business problem

“Policies, product definitions and support knowledge exist across different files. Business users cannot easily see how a policy affects a customer action or which source supports a decision.”

Minute 2: Executive overview

Show:

active concepts
policy rules
knowledge articles
owners
quality warnings
concepts without owners
rules without detailed text
Minutes 3–4: Retention-offer journey

Select:

Retention Offer


Demonstrate:

business definition
parent concepts
inherited 12-month cadence
13-month tenure dependency
Policy Rules 10 and 13
KB11 evidence
Customer Retention ownership
effect on the ₹500 concession limit
Minute 5: Impact analysis

Click Rule 10 and show all affected concepts:

Rule 10
├── Tenure
├── OnceOnlyOffer
├── LateFeeWaiver
└── RetentionOffer


Then say:

“Before changing Rule 10, the business can see every concept and customer outcome potentially affected.”

Minute 6: Governance

Show:

asserted versus inferred values
missing source or owner warnings
Rule 1–11 versus Rule 12/13 inconsistency
SHACL validation results

Finish with:

“This turns ontology from a technical RDF artifact into a traceable business decision map.”

16. Practical delivery plan
Period	DeliverableDays 1–2	RDFLib loader, namespace handling and APIs
Days 3–4	Concept page and focused Cytoscape graph
Day 5	Rule, article and owner panels
Days 6–7	Search, filters and impact analysis
Day 8	SHACL validation and custom lint warnings
Day 9	Business styling and sample journeys
Day 10	Docker packaging, testing and demo rehearsal
MVP acceptance criteria

The first showcase is ready when the tool can:

load a .ttl file without code changes
list ontology concepts
search by preferred or alternative label
show parents and children
display definitions in business language
show linked policy rules
show linked knowledge articles
show operational owners
distinguish asserted and inferred information
navigate from concept to rule and from rule to affected concepts
report ontology-quality findings
export a selected concept as PNG or PDF for presentations

The key design principle is: never make the audience interpret raw triples. Present a decision-oriented story and retain the RDF/OWL detail as drill-down evidence.
