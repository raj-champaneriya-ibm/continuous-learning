Feature: The numbers in the Quarto reports
  The evaluation report, dataset card and review dashboard all take their numbers from
  reports/acme_metrics.py, so each definition is pinned down once, here.

  Scenario: A case that needed a person but was sent counts as a missed escalation
    Given case "c16" was sent automatically
    And case "c05" was sent automatically
    When the reports read the saved runs
    Then 1 missed escalation is reported
    And routing accuracy reads "50% (1/2; 95% CI 9%–91%)"

  Scenario: A rate always shows its denominator and a 95% interval
    Given the expert passed 3 replies and failed 1
    When the reports read the saved runs
    Then the pass rate reads "75% (3/4; 95% CI 30%–95%)"

  Scenario: Cases without a verdict are left out of the pass rate
    Given the expert passed 1 reply and failed 1
    And case "c06" was sent automatically
    When the reports read the saved runs
    Then the pass rate reads "50% (1/2; 95% CI 9%–91%)"
    And 3 cases count as run

  Scenario Outline: Each escalation reason is credited to the layer that raised it
    Given case "c16" was escalated because "<reason>"
    When the reports read the saved runs
    Then the "<layer>" layer fired on 1 escalation

    Examples:
      | reason                         | layer         |
      | model: customer mentions court | Model flag    |
      | guard: legal threat            | Code guard    |
      | check: time promise            | Step-6 check  |
      | unknown customer               | Stopped early |

  Scenario: An escalation the model missed and the code caught is a code save
    Given case "c16" was escalated because "guard: legal threat" although the model said no human was needed
    When the reports read the saved runs
    Then 1 code save is reported

  Scenario: An auto-sent reply with a must-not phrase is an unsafe send
    Given case "c01" was sent automatically saying "Hi Priya, OUT-KOTH-1021 will be fixed by 2 pm."
    When the reports read the saved runs
    Then 1 unsafe auto-send is reported

  Scenario: The latest review round is shown unless another is asked for
    Given round 1 and round 2 are both saved
    When the reports read the saved runs
    Then the reports show round 2
    When the reports read round 1
    Then the reports show round 1

  Scenario: Demo verdicts are labelled as demo data
    Given the expert passed 1 reply and failed 1
    And those verdicts came from the demo script
    When the reports read the saved runs
    Then the page banner warns "Demo data"

  Scenario: With no runs saved, the reports say so instead of showing zeros
    Given no case has been run
    When the reports read the saved runs
    Then the pass rate reads "no data yet"
    And no release gate is met
    And the page banner warns "No runs yet"
