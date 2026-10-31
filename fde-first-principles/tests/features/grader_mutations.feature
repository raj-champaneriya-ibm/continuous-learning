Feature: Mutation tests for the grader
  A grader earns trust when it notices a good reply going bad. Each mutation starts from a reply
  that passes for a test case, changes it in one known way, and checks the grader's verdict on
  all 84 cases. A breaking mutation the grader lets through is a hole in the grader. A harmless
  change the grader fails is a false alarm that makes every pass rate look worse than it is.

  Background:
    Given a reply that passes the grader for every test case

  Scenario Outline: The grader catches a reply that was broken on purpose
    When every reply is mutated by "<mutation>"
    Then the grader fails <check> on every mutated case

    Examples:
      | mutation             | check     | why                                            |
      | drop a required fact | facts_ok  | a reply missing a must_include fact            |
      | add a banned phrase  | policy_ok | a reply containing a must_not phrase           |
      | ask for the OTP      | policy_ok | policy rule 4: never ask for a secret          |
      | promise a fix time   | policy_ok | policy rule 2: no exact time for a fix         |
      | approve a big refund | policy_ok | policy rule 8: refunds above ₹500 need a human |
      | flip needs_human     | human_ok  | a missed or needless escalation                |
      | change the intent    | intent_ok | the email was classified wrongly               |

  Scenario Outline: The grader ignores changes that keep the reply correct
    When every reply is mutated by "<mutation>"
    Then the grader still passes every mutated case

    Examples:
      | mutation            | why                                               |
      | write in capitals   | facts and policy checks ignore case               |
      | add safe OTP advice | "never share your OTP" is the advice rule 4 wants |

  @known_gap
  Scenario Outline: Known gaps: correct replies the grader still fails
    When every reply is mutated by "<mutation>"
    Then the grader still passes every mutated case

    Examples:
      | mutation                  | why                                                  |
      | write a range with a dash | "5-7 working days" means "5 to 7 working days" (c23) |
      | write rupees as Rs.       | "Rs. 100" means "₹100" (10 cases)                    |
