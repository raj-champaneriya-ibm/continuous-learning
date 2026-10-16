Feature: Guardrails around the grounded draft
  The model writes the reply. Code checks every claim and decides whether a person must see it
  first, so a confident but wrong draft never reaches the customer on its own.

  Scenario: A grounded reply is sent without a human
    Given the model drafts "Hi Rohan, the Pro 1 Gbps plan costs ₹1,499 per month and is active within 1 hour." for case "c05"
    When the email runs through the workflow
    Then the reply is sent automatically

  Scenario Outline: Step 6 holds back unsupported or unsafe claims
    Given the model drafts "<reply>" for case "<case>"
    When the email runs through the workflow
    Then step 6 flags "<check>"
    And the reply waits for a human

    Examples:
      | case | check                 | reply                                                           |
      | c01  | time promise          | Hi Priya, outage OUT-KOTH-1021 will be fixed by 1 pm.           |
      | c13  | unsupported ticket    | Hi Meera, there is an outage in Kharadi, ticket OUT-KHAR-0001.  |
      | c26  | financial promise     | Hi Sneha, your refund of ₹1,499 has been approved.              |
      | c80  | other customer's data | Hi Vikram, AC1001 belongs to Priya Kulkarni.                    |
      | c09  | asks for a secret     | Hi Imran, please share your OTP so we can verify you.           |

  Scenario: A legal threat goes to a human even when the model says it is safe
    Given the model drafts "Hi Kavya, outage OUT-KOTH-1021 is being worked on." for case "c16"
    When the email runs through the workflow
    Then the escalation reasons include "guard: legal threat"
    And the reply waits for a human

  Scenario: An unknown customer never reaches the model
    Given an email from customer "AC9999" saying "Please refund my last bill"
    When the email runs through the workflow
    Then the model is not called
    And the reply waits for a human

  Scenario Outline: The human decides what happens to a held reply
    Given the model drafts "Hi Kavya, outage OUT-KOTH-1021 is being worked on." for case "c16"
    When the email runs through the workflow
    And the human chooses to "<action>"
    Then the outcome is "<outcome>"

    Examples:
      | action  | outcome           |
      | approve | sent_after_review |
      | edit    | sent_after_review |
      | hold    | held              |
