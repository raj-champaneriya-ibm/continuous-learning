# Agent 365

## Identity

Agent Identity Blueprint Principal is the credential-bearing principal that stores authentication material and obtains tokens for agent identities.
Agent Identity represents the actual deployed agent instance and is the identity referenced in governance and auditing scenarios.
Agent's User Account provides user-based tokens containing the idtyp=user claim, which is required by legacy APIs expecting a user identity.
Agent Identity Blueprint is the template from which agent identities are created, and its identifier is used for identity-related auditing and correlation.

## Governance

Shared controls → Controls defining a joint implementation duty for both infrastructure and configuration.
Microsoft managed controls → Controls where the customer gets visibility into Microsoft's implementation and audit results.
Improvement actions → Workflow elements used to centralize evidence and assign tasks to users.
Your (Customer) controls → Controls for which the customer handles system configuration and people.

# observability

AlertInfo contains the alert metadata, severity, status, category, and other details about security alerts.
CloudAppEvents records activity events such as tool usage, resource access, and application actions.
AgentsInfo provides inventory and configuration information about AI agents, helping identify misconfigured agents.
AlertEvidence contains the entities, URLs, resources, files, and other evidence linked to an alert, useful for investigating jailbreak attempts.