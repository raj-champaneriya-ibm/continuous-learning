Feature: The grader agrees with the expert's round-2 review
  In round 2 the domain expert reviewed drafts in Acme Review Studio and wrote the reply they
  wanted where a draft failed. Each row scores one reply against the real test case, so the
  grader passes the expert's reply and fails the reviewed draft for the reason the expert gave.
  The expert's words are kept as written; only a greeting is added where the case needs the
  customer's name. Changing a row means changing a verdict, which is the expert's call.

  Scenario Outline: The expert's verdict and the grader's agree
    Given test case <case>
    And a draft that says "<reply>" and hands the email to a person
    When the grader scores the draft
    Then the checks that fail are "<fails>"
    And the grader flags "<flags>"

    Examples:
      | case | verdict | reply                                                                                                                                                                                          | fails              | flags                                | why                                              |
      | c38  | pass    | Hi Vikram, on your refund request of ₹3,000: customer representative will call you.                                                                                                             | nothing            | nothing                              | the expert's reply                               |
      | c38  | fail    | Hi Vikram, on your refund request of ₹3,000: refunds above ₹500 need approval from our billing team, so I have sent your request to them for review. They will update you on the decision. | facts_ok, policy_ok | reveals limit, must_not: ₹500        | quotes the limit and explains approvals          |
      | c39  | pass    | Dear Imran, what you describe is not allowed: technician visits are free and Acme never asks for cash. I have passed your report to a colleague who will follow up with you.                  | nothing            | nothing                              | answers the question, leaves the outage out      |
      | c39  | fail    | Dear Imran, technician visits are free and Acme never asks for cash. Separately, we see an outage in Hadapsar (ticket OUT-HADA-0417) due to a power problem at the local hub.                | policy_ok          | unasked outage, must_not: OUT-HADA-0417 | the customer didn't report an outage (policy 12) |
      | c70  | pass    | Hi Vikram, a change of account holder needs both of you to be verified, so a colleague will contact you to arrange it.                                                                       | nothing            | nothing                              | hands the transfer to a person                   |
      | c70  | fail    | Hi Vikram, we will transfer the account to the new owner's name this week.                                                                                                                   | policy_ok          | must_not: will transfer the account  | promises a transfer nobody has verified          |
      | c81  | pass    | Hi Kavya, we have noted the incident and will work with the respected authority to lodge a complaint. For anything about your account, use only the Acme app or our official channels. Sorry for the worry this caused. | nothing | nothing                | the expert's reply                               |
      | c81  | fail    | Hi Kavya, you can safely delete that email. Acme never asks for payment through an email link; pay only in the Acme app.                                                                     | facts_ok           | nothing                              | no official channels, no complaint, no apology   |

  # Policy 13: the expert passed c44's draft, which offered 50% off Pro (₹750) without a hand-off, and
  # called the round-1 hand-off of the same reply an "Unneeded escalation".
  Scenario Outline: The retention offer is pre-approved (c44)
    Given test case c44
    And a draft that says "<reply>" and <routing>
    When the grader scores the draft
    Then the checks that fail are "<fails>"
    And the grader flags "nothing"

    Examples:
      | verdict | routing                     | fails    | reply                                                                                                                                                                                                                      |
      | pass    | sends it                    | nothing  | Hi Meera, cancellation needs 30 days of notice, and we collect the router from your home free of charge. If you're moving within Pune, we can shift your connection for free instead. If you'd like to stay, you're eligible for 50% off your Pro plan for one month. |
      | fail    | hands the email to a person | human_ok | Hi Meera, cancellation needs 30 days of notice, and we collect the router from your home free of charge. If you're moving within Pune, we can shift your connection for free instead. If you'd like to stay, you're eligible for 50% off your Pro plan for one month. |
