# Conversation Summary

## Question 1
**Michael Carter, Data Architect at ZAVAAirlines, is building a multi-agent analytics system that must answer:**

“Which delays this week were caused by aircraft rotation constraints rather than weather, and what downstream financial impact did they trigger?”

The system must:
- Combine real-time and historical data
- Avoid duplicating data across systems
- Ensure consistent interpretation of “delay cause”
- Support relationship traversal across entities

### Correct Answers
- ✅ OneLake as a unified storage layer
- ✅ Fabric Graph for multi-hop traversal
- ✅ Ontology entity types and relationships

### Explanation
- OneLake combines real-time and historical data while avoiding duplication.
- Fabric Graph enables multi-hop relationship traversal across entities.
- Ontology provides consistent business definitions and relationships.
- Power BI dashboards and separate semantic models do not meet the core architectural requirements.

---

## Question 2
**Match each component with its primary responsibility.**

| Component | Primary Responsibility |
|------------|------------------------|
| Fabric Data Agent | Conversational analytics over governed data |
| Operations Agent | Continuous monitoring and action recommendations |
| Work IQ | Personalized work context from Microsoft 365 |
| Fabric IQ | Enterprise semantic grounding across all data |

### Correct Mapping
- Fabric Data Agent → Conversational analytics over governed data
- Operations Agent → Continuous monitoring and action recommendations
- Work IQ → Personalized work context from Microsoft 365
- Fabric IQ → Enterprise semantic grounding across all data
