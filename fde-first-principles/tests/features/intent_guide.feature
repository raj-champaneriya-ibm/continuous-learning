Feature: One written convention decides the intent label
  An email often touches several intents ("downgrade me and refund the difference or I'm leaving").
  lab.acme.INTENT_GUIDE writes down where each kind of email goes, with tie-breaks for the common
  mixes, and the C3 prompt uses it. The rows below are the edge cases, checked against the expert
  labels in the four case files. A label that disagrees with the guide is listed as a known gap until
  the domain expert rules on it: relabel the case, or change the guide and its row.

  Background:
    Given the labelled cases in the four case files

  Scenario: Every intent has a definition
    Then every intent has a definition in the guide

  Scenario Outline: The guide's edge cases match the expert labels
    Then case <case> is labelled "<intent>"

    Examples:
      | case | intent     | rule in the guide                                   |
      | c55  | upgrade    | a downgrade is a plan change                        |
      | c59  | upgrade    | a plan changed without consent                      |
      | c61  | upgrade    | the charge a plan change caused                     |
      | c60  | upgrade    | a plan change beats speed and money                 |
      | c50  | cancel     | cancelling beats a refund in the same email         |
      | p29a | cancel     | leaving over price                                  |
      | c04  | cancel     | cancelling because of a move                        |
      | c65  | relocation | moving the connection, even out of Pune             |
      | c71  | relocation | damage a shift caused                               |
      | c74  | relocation | a hazard a shift left behind                        |
      | c17  | outage     | compensation for the current outage                 |
      | c26  | billing    | refunding a past bill                               |
      | r25  | billing    | waiving a bill, even over an outage                 |
      | p01a | billing    | credit asked for slow speed                         |
      | c27  | billing    | an unauthorised payment                             |
      | c36  | speed      | a threat to leave doesn't change the intent         |
      | c16  | outage     | a legal threat doesn't change the intent            |
      | c29  | billing    | asking for a person doesn't change the intent       |
      | p37a | speed      | instructions to the assistant are ignored           |
      | m32  | other      | an account ownership transfer                       |
      | r39  | other      | staff misconduct                                    |
      | r41  | other      | a safety hazard no shift caused                     |
      | c84  | other      | a data-cap question                                 |
      | c77  | other      | a question about another customer                   |
      | c39  | other      | staff misconduct (expert, round 2)                  |
      | c70  | other      | an account ownership transfer (expert, round 2)     |

  @known_gap
  Scenario Outline: Labels that disagree with the guide (for the domain expert to rule on)
    Then case <case> is labelled "<guide>"

    Examples:
      | case | guide      | labelled   | why the guide disagrees                                      | same kind, labelled as the guide says |
      | c38  | billing    | speed      | the request is ₹3,000 back for slow speed                    | p01a to p06a, r05, r36, r42           |
      | p35a | other      | billing    | a question about another customer's bill                     | c77, m31, r24                         |
