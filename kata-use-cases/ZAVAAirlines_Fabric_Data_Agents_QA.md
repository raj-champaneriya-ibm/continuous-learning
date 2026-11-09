# ZAVAAirlines Fabric Data Agents - Q&A

📋 ZAVAAirlines Fabric IQ Ontology
Read carefully before answering
Customer Background

ZAVAAirlines operates global flight operations across multiple regions. Business units—including operations, maintenance, and finance—use independent systems with inconsistent definitions for key concepts such as delay, incident, and cost impact.

As a result: reports across departments are inconsistent, AI-generated insights vary depending on the data source, and cross-domain decision-making is unreliable.

Technology Background

ZAVA has implemented Microsoft Fabric with: Power BI semantic models across domains, OneLake as a unified storage layer, Fabric Graph enabled for relationship analysis, and early Fabric Data Agents for conversational analytics. The organization is evaluating Fabric IQ Ontology to unify business meaning across domains without disrupting existing systems.

Challenges

After initial implementation, ZAVA observes: conflicting responses between different Fabric Data Agents, increased latency in multi-hop analytical queries, difficulty governing Ontology extensions across teams, confusion between semantic reasoning (Ontology) and query execution (engine/Graph), and a requirement to combine real-time + historical data without duplication.

## 1. Improve Query Generation Accuracy
**Question:** Most critical configuration element?

**Answer:** Defining detailed Data Agent instructions and data source descriptions.

## 2. Incorrect Source Selection at Runtime
**Answer:** Data source descriptions are not clearly defined, leading to incorrect source selection at runtime.

## 3. Data Agent Query Processing Flow
**Select all that apply:**
- Combine user query with schema, instructions, and example queries.
- Select and invoke the appropriate tool for query execution.
- Validate and format the response before returning to the user.

## 4. Production Preparation Lifecycle
**Correct sequence:**
Add data sources → Configure instructions and data source descriptions → Add execution tools → Perform structured evaluation → Publish.

## 5. Match Lifecycle Steps
- Publish → Make the agent available to consumers.
- Configure Instructions → Define how the agent should behave and respond.
- Add Tools → Enable query execution mechanisms.
- Add Data Source → Select relevant tables and data inputs.

## 6. Evaluation Prompt Placeholders
**Statement:** Custom evaluation prompts can omit required placeholders.

**Answer:** False.

## 7. Evaluation SDK Functions
- evaluate_data_agent → Compares responses with expected answers.
- get_evaluation_summary → Provides overall performance summary.
- get_evaluation_details → Returns breakdown of responses.

## 8. Scalable Evaluation Strategy
**Answer:** Define standardized evaluation datasets and automated validation workflows.

## 9. Structured Evaluation Requirements
**Select all that apply:**
- Install and import the Fabric Data Agent SDK.
- Create a dataset of questions and expected answers.
- Use evaluate_data_agent to compare results.

## 10. Unstructured Data Support
**Statement:** Fabric Data Agents can leverage unstructured data using Azure AI Search integration.

**Answer:** True.

## 11. Consistent Responses Across Teams, Excel, and Copilot Studio
**Answer:** Provide explicit instructions in the Fabric Data Agent publishing description.

## 12. Fabric Data Agent as Knowledge Source
**Select all that apply:**
- Foundry determines whether the Data Agent should be invoked.
- The Data Agent can inherit governance policies enforced through underlying Fabric security controls.
- The agent uses the end user's identity when querying Fabric data.

## 13. Direct OneLake Access vs Data Agents
**Statement:** Direct access to OneLake data can provide equivalent governance and contextual reasoning as Fabric Data Agents if RBAC is configured.

**Answer:** False.

## 14. Architecture Responsibilities
- Fabric Data Agent → Provide governed, semantic access to enterprise data.
- Microsoft Foundry Agent Service → Orchestrate agents and determine which capability to invoke.
- Microsoft 365 Copilot → Provide end-user conversational experience and reasoning layer.
- MCP Tools → Enable integration with external systems and actions.

## 15. External AI Access Pattern
**Answer:** Configure Fabric Data Agent as an MCP Server.

## 16. Fabric Data Agents vs Power BI Copilot
**Select all that apply:**
- When queries require integration with external APIs or tools.
- When users need conversational insights across multiple heterogeneous data sources.
