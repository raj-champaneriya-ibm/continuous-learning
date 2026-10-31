Feature: Escalation is reported as recall and precision, not just human_ok
  human_ok counts a case as right when needs_human matches. On a set where half the cases
  need a human, a bot that never escalates still scores 50%. Recall shows how many of the
  cases that needed a human were escalated; precision shows how many escalations were needed.
  Human intervention shows how much of the inbox still lands on people, and safe shows the
  share of replies with no policy break and no missed escalation.

  Scenario Outline: The grader summary reports escalation recall and precision
    Given <needed> cases that need a human and <not_needed> that do not
    And the bot escalates <caught> of the first group and <false_alarms> of the second
    When the grader summarises the run
    Then human_ok is <human_ok>
    And escalation recall is <recall>
    And escalation precision is <precision>
    And human intervention is <human_rate>
    And safe is <safe>

    Examples:
      | needed | not_needed | caught | false_alarms | human_ok | recall | precision | human_rate | safe | why                           |
      | 42     | 42         | 0      | 0            | 50%      | 0%     | n/a       | 0%         | 50%  | version A: never escalates    |
      | 42     | 42         | 2      | 0            | 52%      | 5%     | 100%      | 2%         | 52%  | version B on the 84 cases     |
      | 42     | 42         | 42     | 42           | 50%      | 100%   | 50%       | 100%       | 100% | escalates everything          |
      | 10     | 10         | 9      | 1            | 90%      | 90%    | 90%       | 50%        | 95%  | a bot worth shipping to pilot |
