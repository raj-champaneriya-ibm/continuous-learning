Feature: The ontology gives every agent the same meaning for policy words
  data/acme/ontology.ttl holds the definitions behind policy rules 8 to 11. Prompts, tools and
  graders read the same file, so "credit" or "account holder" can't mean two different things.

  Scenario: Automatic money doesn't count toward the ₹500 limit
    When the grader asks which kinds of money are excluded from the limit
    Then the answer is "double payment refund, outage credit"

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
