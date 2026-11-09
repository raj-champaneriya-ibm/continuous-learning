# Conversation Summary

📋 ZAVAAirlines Fabric Data Agents
Read carefully before answering
Customer Background

ZAVAAirlines operations teams monitor flight delays, crew assignments, aircraft maintenance events, and real-time disruption signals across several regions. Business users depend on analysts for SQL, DAX, and KQL queries, which slows decision-making during operational incidents.

Technology Background

ZAVA is implementing Fabric Data Agents connected to Lakehouse tables, Power BI semantic models, Eventhouse, and Azure AI Search. The Data Agents are configured with data source descriptions, instructions, tools, example queries, and evaluation datasets.

Challenges

The solution must improve query accuracy, select the correct data source at runtime, enforce user permissions, support structured and unstructured data, and validate agent quality before production rollout.

For ZAVAAirlines, the recommended Fabric Data Agents design should map each challenge to the appropriate Fabric capability.

Challenge	Fabric Data Agent Capability	Implementation
Improve query accuracy	Instructions, example queries, and evaluation datasets	Provide domain-specific instructions for flight delays, crew scheduling, maintenance, and disruption management. Include representative SQL, DAX, and KQL examples and validate outputs using evaluation datasets before deployment.
Select the correct data source at runtime	Data source descriptions and intelligent source selection	Clearly describe each source: Lakehouse for operational history, Power BI semantic models for business metrics, Eventhouse for real-time telemetry and disruption signals, and Azure AI Search for unstructured documents. The agent uses these descriptions to choose the most appropriate source.
Enforce user permissions	Microsoft Fabric security and source-level authorization	Data Agents honor existing permissions from Lakehouse, semantic models, Eventhouse, and other connected sources, ensuring users only see data they are authorized to access.
Support structured and unstructured data	Multiple connected data sources	Combine structured sources (Lakehouse, semantic models, Eventhouse) with unstructured content indexed through Azure AI Search, enabling answers that combine operational data and documentation.
Validate quality before production rollout	Evaluation datasets and agent testing	Use evaluation sets containing expected airline operational questions and answers to measure accuracy, grounding, source selection, and response quality before publishing the agent.
Recommended Architecture

Lakehouse

Flight history
Crew assignments
Maintenance records

Power BI Semantic Models

Delay KPIs
Operational performance metrics
Executive reporting measures

Eventhouse

Real-time disruption events
Aircraft telemetry
Streaming operational signals

Azure AI Search

Operations manuals
Maintenance procedures
Incident documentation

Fabric Data Agent

Uses instructions and examples
Chooses the appropriate source dynamically
Respects security permissions
Validated through evaluation datasets
Key Best Practice

The most important factor for accurate source selection is maintaining high-quality data source descriptions and instructions, while evaluation datasets are used to continuously verify that the agent selects the correct source and returns accurate, grounded responses.

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
