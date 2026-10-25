Feature: Escalation is reported as recall and precision, not just human_ok
  human_ok counts a case as right when needs_human matches. On a set where half the cases
  need a human, a bot that never escalates still scores 50%. Recall shows how many of the
  cases that needed a human were escalated; precision shows how many escalations were needed.

  Scenario Outline: The grader summary reports escalation recall and precision
    Given <needed> cases that need a human and <not_needed> that do not
    And the bot escalates <caught> of the first group and <false_alarms> of the second
    When the grader summarises the run
    Then human_ok is <human_ok>
    And escalation recall is <recall>
    And escalation precision is <precision>

    Examples:
      | needed | not_needed | caught | false_alarms | human_ok | recall | precision | why                          |
      | 42     | 42         | 0      | 0            | 50%      | 0%     | n/a       | version A: never escalates   |
      | 42     | 42         | 2      | 0            | 52%      | 5%     | 100%      | version B on the 84 cases    |
      | 42     | 42         | 42     | 42           | 50%      | 100%   | 50%       | escalates everything         |
      | 10     | 10         | 9      | 1            | 90%      | 90%    | 90%       | a bot worth shipping to pilot |
