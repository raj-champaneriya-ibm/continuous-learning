Feature: The area outage is in scope only when the customer reports that their service is down
  Policy 12 (round-2 expert review, c39): don't include outage information if the customer hasn't
  complained about it. The ontology's Outage concept knows how customers say it, in English,
  Hinglish and regional languages. When the customer's own words don't name it, C3 keeps the outage out
  of the envelope and out of the lookup_customer and check_entitlement results, so the model can't bring
  it up unasked.

  Scenario Outline: The envelope shows the outage only when the customer reports one
    Given customer <customer> writes "<message>"
    When the envelope is built
    Then the outage is <scope>
    And the envelope <shows> "<ticket>"

    Examples:
      | customer | message                                                                                    | scope        | shows         | ticket        | why                                   |
      | AC1008   | The technician who came about my slow speed was rude and asked for ₹500 cash. Is that allowed? | out of scope | doesn't show  | OUT-HADA-0417 | c39: a misconduct report              |
      | AC1001   | Video calls lag every evening on Wi-Fi, but mornings are fine.                             | out of scope | doesn't show  | OUT-KOTH-1021 | c31: slow speed is not an outage      |
      | AC1001   | We're moving to Pimple Saudagar. Is that in your service area?                             | out of scope | doesn't show  | OUT-KOTH-1021 | c68: a shifting question              |
      | AC1001   | Hi, my internet has been down since 7 am. When will it be fixed??                          | in scope     | shows         | OUT-KOTH-1021 | c01: English                          |
      | AC1008   | Hadapsar mein kal raat se net band hai. Paisa wapas milega?                                | in scope     | shows         | OUT-HADA-0417 | p16h: Hinglish                        |
      | AC1001   | सकाळपासून इंटरनेट बंद आहे.                                                                  | in scope     | shows         | OUT-KOTH-1021 | r01: Marathi                          |

  Scenario: The customer-record tools withhold the outage when it is out of scope
    Given customer AC1008 writes "The technician who came about my slow speed was rude and asked for ₹500 cash. Is that allowed?"
    And the model looks up the customer, then replies "Hi Imran, technician visits are free, and a colleague will follow up."
    When the C3 agent finishes
    Then the lookup_customer result doesn't show "OUT-HADA-0417"

  Scenario: The customer-record tools show the outage when the customer reports one
    Given customer AC1008 writes "Hadapsar mein kal raat se net band hai. Paisa wapas milega?"
    And the model looks up the customer, then replies "Hi Imran, outage OUT-HADA-0417 is active in Hadapsar."
    When the C3 agent finishes
    Then the lookup_customer result shows "OUT-HADA-0417"
