Feature: The lab's C3 agent writes the draft in step 5
  With the C3 provider the expert reviews the drafts of the agent the lab measures. C3 gets the case
  id, the customer id, the message and the earlier turns, and its result is mapped onto the draft the
  rest of the workflow already checks. A stand-in plays C3 here, so these scenarios need no model and
  no lab packages. The replies are the expert's preferred replies from round 2.

  Scenario Outline: C3's result comes back as a draft the workflow can check
    Given C3 replies "<reply>" after calling "<tools>" with escalation sources "<sources>"
    When case "<case>" runs through the workflow with C3
    Then C3 was given case "<case>" with its customer and message
    And the draft says "<reply>"
    And the draft's needs_human is <needs_human>
    And the draft's escalation reason is "<sources>"
    And the draft cites "<cited>"

    Examples:
      | case | reply                                                                                                                                                                                     | tools                                                   | sources                   | needs_human | cited           |
      | c38  | Hi Vikram, on your refund request of ₹3,000: customer representative will call you.                                                                                                       | lookup_customer, search_kb KB07 KB16                    | rule:money_above_headroom | true        | CRM, KB07, KB16 |
      | c39  | Dear Imran, what you describe is not allowed: technician visits are free and Acme never asks for cash. I have passed your report to a colleague who will follow up with you.            | lookup_customer, search_kb KB08                         | tool:escalate             | true        | CRM, KB08       |
      | c81  | Hi Kavya, we have noted the incident and will work with the respected authority to lodge a complaint. For anything about your account, use only the Acme app or our official channels. Sorry for the worry this caused. | define_term KB15, search_kb KB03 KB15 | model                     | true        | KB15, KB03      |
      | c44  | Hi Meera, cancellation needs 30 days of notice and the router is collected free of charge. If you'd like to stay, you're eligible for 50% off for one month.                              | lookup_customer, check_entitlement, search_kb KB10 KB11 | none                      | false       | CRM, KB10, KB11 |

  Scenario: C3's hand-off holds the reply for a person
    Given C3 replies "Hi Vikram, on your refund request of ₹3,000: customer representative will call you." after calling "lookup_customer" with escalation sources "rule:money_above_headroom"
    When case "c38" runs through the workflow with C3
    Then the escalation reasons include "model: rule:money_above_headroom"
    And the reply waits for a human

  Scenario: Earlier turns reach C3
    Given C3 replies "Hi Imran, outage OUT-HADA-0417 is still being worked on." after calling "lookup_customer" with escalation sources "none"
    And the customer wrote earlier "Hadapsar mein kal raat se net band hai."
    When customer "AC1008" writes "Still no internet. Any update?" and the email runs through the workflow with C3
    Then C3 was given the earlier turn "Hadapsar mein kal raat se net band hai."
    And the draft cites "CRM, OUTAGE"

  Scenario: A C3 failure is a model error in step 5, not a crash
    Given C3 fails with "API call limit reached (500 requests)"
    When case "c38" runs through the workflow with C3
    Then step 5 reports "model error: C3 failed: API call limit reached (500 requests)"
    And the reply waits for a human

  Scenario: The settings name picks the C3 agent
    When the studio makes the "c3" provider with no ACME_C3_MODEL set
    Then the provider is "C3 ontology agent" with model "anthropic:glm-5.3-flash"
