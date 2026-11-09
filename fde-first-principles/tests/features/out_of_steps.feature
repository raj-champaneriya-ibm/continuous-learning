Feature: C3 always ends with a reply, even when it runs out of steps
  In v2, v3 and v4, c84 ("Does Acme have a data cap?") spent all six steps searching the help articles
  for something they don't mention and returned nothing, so the guard sent an empty draft to a person.
  Now C3 gets one more turn once the steps run out, and that turn has to answer from what it has. A
  model that still calls a tool on that turn has given up, as before. A scripted model plays C3 here,
  so these scenarios need no model.

  Background:
    Given customer AC1003 writes "Does Acme have a data cap? My neighbour says you slow people down after 3.3 TB."

  Scenario: Out of steps, C3 still writes a reply
    Given the model searches the help articles on every step, then replies "Hi Sneha, our help articles don't say anything about data caps, so I can't confirm either way."
    When the C3 agent finishes
    Then the reply is "Hi Sneha, our help articles don't say anything about data caps, so I can't confirm either way."
    And the model got one more turn after the step limit, telling it to answer now
    And the result is marked out of steps
    And the escalation sources don't include "fallback:gave_up"

  Scenario: A model that keeps calling tools on the extra turn has given up
    Given the model searches the help articles on every step and on the extra turn too
    When the C3 agent finishes
    Then the reply is empty
    And the escalation sources include "fallback:gave_up"
    And the escalation sources include "guard:empty_reply"
    And a person gets the email

  Scenario: A model that answers within its steps gets no extra turn
    Given the model searches the help articles once, then replies "Hi Sneha, our help articles don't say anything about data caps."
    When the C3 agent finishes
    Then the reply is "Hi Sneha, our help articles don't say anything about data caps."
    And the model was called 2 times
    And the result is not marked out of steps
