Feature: Critique-first review
  The expert writes what went wrong before choosing a category,
  so new kinds of failure aren't forced into the existing list.

  Scenario: In critique-first mode a fail needs only a critique
    Given critique-first review is on
    When the expert fails case "c07" with critique "Promises the fix by 6 pm" and no failure mode
    Then the verdict is saved
    And case "c07" is listed under "Not yet grouped"

  Scenario: The suggested mode is a hint, not a selection
    Given critique-first review is on
    And the step-6 check "time promise" fired on case "c07"
    When the expert opens case "c07"
    Then no failure mode is selected
    And "Promised fix time" is shown as a hint

  Scenario: A fail still needs a critique
    Given critique-first review is on
    When the expert fails case "c07" with no critique
    Then the verdict is refused with "write a short critique"

  Scenario: With critique-first off, today's rule stays
    Given critique-first review is off
    When the expert fails case "c07" with critique "Promises the fix by 6 pm" and no failure mode
    Then the verdict is refused with "pick a failure mode"
