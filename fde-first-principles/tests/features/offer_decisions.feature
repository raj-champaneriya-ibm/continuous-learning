Feature: Eligible is not approved
  compute_entitlements says whether a customer is eligible for an offer (tenure, cooldown). Whether the
  agent may give it is a second question: the ₹500 30-day headroom (policy 8) and whether a person is
  already handling the case. The decision envelope answers both, so the model is never told ELIGIBLE
  for an offer it has no authority to give (50% off Pro is ₹750, above the limit).

  Scenario Outline: The envelope decides what the agent may offer
    Given customer <customer> writes "<message>"
    When the envelope decides the offers
    Then the <offer> decision is "<status>"

    Examples:
      | customer | message                                                   | offer                 | status         | why                                        |
      | AC1007   | Please cancel my connection. I'm moving next month.       | retention offer       | offer          | 50% off Plus is ₹500, within the limit     |
      | AC1005   | I want to cancel. Will you collect the router?            | retention offer       | offer          | 50% off Basic is ₹350                      |
      | AC1009   | Please close the connection, we're vacating the house.    | retention offer       | needs_approval | 50% off Pro is ₹750, above the limit       |
      | AC1003   | Connection cancel karo. Is mahine teesri baar outage hua. | retention offer       | hold           | a churn escalation: a person decides       |
      | AC1010   | Your service is a joke and way too expensive. Cancel it.  | retention offer       | do_not_offer   | tenure 2 months                            |
      | AC1021   | Late fee waive kar do please.                             | late-fee waiver       | offer          | tenure 13 months, never waived             |
      | AC1028   | Please waive the late fee.                                | late-fee waiver       | offer          | last waived 15 months ago                  |
      | AC1002   | Late fee waive kar do please, pehli baar late hua hai.    | late-fee waiver       | do_not_offer   | tenure 8 months                            |
      | AC1025   | Please waive the late fee.                                | late-fee waiver       | do_not_offer   | waived 5 months ago (once a year)          |
      | AC1014   | Please waive the late fee.                                | late-fee waiver       | needs_approval | ₹450 used this month leaves ₹50 headroom   |
      | AC1009   | I paid ₹1,499 twice. Please refund one.                   | double payment refund | automatic      | the record shows the duplicate (KB04)      |
      | AC1001   | Please refund my extra payment.                           | double payment refund | not_on_record  | one payment on record                      |

  Scenario Outline: A draft that offers more than its decision allows goes to a person
    Given customer <customer> writes "<message>"
    And the model drafts "<reply>" with needs_human false
    When the C3 agent finishes
    Then needs_human is <needs_human>
    And the escalation sources are "<sources>"

    Examples:
      | customer | message                                                | reply                                                                                         | needs_human | sources                              | why                                     |
      | AC1007   | Please cancel my connection. I'm moving next month.    | Hi Ananya, before you go, you're eligible for 50% off your Plus plan (₹999 → ₹499) for a month. | false       | none                                 | an allowed offer                        |
      | AC1009   | Please close the connection, we're vacating the house. | Hi Meera, a 50% retention offer on your Pro plan needs approval, so a colleague will review it. | true        | offer:retention offer:needs_approval | told a colleague will review it         |
      | AC1010   | Your service is a joke and way too expensive. Cancel it. | Hi Rohan, before you go, we can offer you 50% off your Plus plan for one month.             | true        | offer:retention offer:do_not_offer   | offered to an ineligible customer       |
      | AC1010   | Your service is a joke and way too expensive. Cancel it. | Hi Rohan, the 50% retention offer needs 13 months with us, so it isn't available to you.    | false       | none                                 | a decline is not an offer               |
      | AC1002   | Late fee waive kar do please, pehli baar late hua hai. | Hi Rahul, I've waived the ₹100 late fee as a one-time courtesy.                               | true        | offer:late-fee waiver:do_not_offer   | waived for an 8-month customer          |
