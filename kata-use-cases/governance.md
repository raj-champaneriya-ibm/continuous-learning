# Agent Identity

Agent Identity Blueprint Principal is the credential-bearing principal that stores authentication material and obtains tokens for agent identities.
Agent Identity represents the actual deployed agent instance and is the identity referenced in governance and auditing scenarios.
Agent's User Account provides user-based tokens containing the idtyp=user claim, which is required by legacy APIs expecting a user identity.
Agent Identity Blueprint is the template from which agent identities are created, and its identifier is used for identity-related auditing and correlation.


