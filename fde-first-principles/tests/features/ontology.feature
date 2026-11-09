Feature: The ontology gives every agent the same meaning for policy words
  data/acme/ontology.ttl holds the definitions behind policy rules 8 to 11. Prompts, tools and
  graders read the same file, so "credit" or "account holder" can't mean two different things.

  Scenario: Automatic money and the pre-approved retention offer don't count toward the ₹500 limit
    When the grader asks which kinds of money are excluded from the limit
    Then the answer is "double payment refund, outage credit, retention offer"

  Scenario Outline: A regional or informal word maps to the policy term
    When an agent looks up "<word>"
    Then it gets the definition of "<term>"

    Examples:
      | word          | term            | language            |
      | paisa wapas   | refund          | Hinglish            |
      | पैसा वापस      | refund          | Hindi               |
      | पैसे परत       | refund          | Marathi             |
      | सूट            | discount        | Marathi             |
      | ರಿಯಾಯಿತಿ        | discount        | Kannada             |
      | இழப்பீடு        | concession      | Tamil               |
      | late fee maaf | late-fee waiver | Hinglish            |
      | Account Holder | account holder | English, any case   |

  Scenario Outline: Every term the money and identity rules use is defined
    When an agent looks up "<term>"
    Then it gets the definition of "<term>"
    And the definition cites "<source>"

    Examples:
      | term             | source    |
      | concession limit | policy 8  |
      | concession       | policy 8  |
      | once-only offer  | policy 10 |
      | tenure           | policy 10 |
      | account holder   | policy 11 |
      | manipulation     | policy 9  |

  Scenario: An unknown word has no definition
    When an agent looks up "loyalty bonus"
    Then there is no definition

  Scenario: The glossary holds definitions, never customer records
    When a prompt asks for the glossary
    Then it contains "account holder"
    And it contains no customer id

  Scenario: The OWL reasoner inherits class properties and respects subclass overrides
    When the reasoner inspects the ontology
    Then "late-fee waiver" inherits oncePerMonths of 12 and countsTowardLimit true
    And "double payment refund" overrides countsTowardLimit to false
    And "cancellation" inherits requiresRole "account holder"

  Scenario: Operational governance validates stewardship and zero catalog drift
    When operations validates the ontology against live catalogs and business rules
    Then the operational health check passes with zero drift errors

  Scenario Outline: Entitlement computation joins ontology, decoupled rules and one customer record
    When the engine computes entitlements for customer "<customer_id>"
    Then the remaining 30-day headroom is <headroom> rupees
    And eligibility for "<offer>" is <eligible>

    Examples:
      | customer_id | headroom | offer                 | eligible | why                                            |
      | AC1020      | 500      | late-fee waiver       | false    | tenure 12 months is below 13-month threshold   |
      | AC1021      | 500      | late-fee waiver       | true     | tenure 13 months meets threshold, never used   |
      | AC1025      | 500      | late-fee waiver       | false    | used on 2026-05-14 (within 12-month cooldown)  |
      | AC1028      | 500      | late-fee waiver       | true     | used on 2025-07-01 (> 12 months ago)           |
      | AC1018      | 500      | retention offer       | false    | used on 2026-08-03 (within 12-month cooldown)  |
      | AC1023      | 500      | retention offer       | true     | used on 2025-07-15 (> 12 months ago)           |
      | AC1009      | 500      | double payment refund | true     | two ₹1,499 payments on record                  |
      | AC1012      | 500      | double payment refund | false    | payments [999, 2000] are different amounts     |
      | AC1014      | 50       | late-fee waiver       | true     | ₹450 used in last 30 days leaves ₹50 headroom  |
      | AC1032      | 300      | retention offer       | false    | ₹200 used leaves ₹300 headroom, tenure 9m      |

  Scenario: Business rules evolve commercially without changing the ontology
    When business operations raises the concession limit to 800 rupees and lowers minimum tenure to 6 months
    Then customer "AC1032" has 600 rupees of headroom and is eligible for "retention offer"
