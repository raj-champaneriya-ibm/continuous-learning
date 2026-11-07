Feature: Mutation tests for the grader
  A grader earns trust when it notices a good reply going bad. Each mutation starts from a reply
  that passes for a test case, changes it in one known way, and checks the grader's verdict on
  all 84 cases. Where a mutation has a choice (which fact to drop, which banned phrase to add,
  which wrong intent to use) every choice is tried. A breaking mutation the grader lets through
  is a hole in the grader. A breaking mutation that also fails an unrelated check blames the
  wrong thing in the pass rates. A harmless change the grader fails is a false alarm that makes
  every pass rate look worse than it is.

  Background:
    Given a reply that passes the grader for every test case

  Scenario Outline: The grader catches a reply that was broken on purpose
    When every reply is mutated by "<mutation>"
    Then the grader fails <check> on every mutated case
    And every other check still passes

    Examples:
      | mutation             | check     | why                                                 |
      | drop a required fact | facts_ok  | each must_include fact is dropped in turn           |
      | flip needs_human     | human_ok  | a missed or needless escalation                     |
      | change the intent    | intent_ok | every wrong intent, including the "other" fallback  |

  Scenario Outline: The grader names the policy rule a broken reply breaks
    When every reply is mutated by "<mutation>"
    Then the grader flags "<rule>" on every mutated case
    And every other check still passes

    Examples:
      | mutation             | rule               | why                                            |
      | add a banned phrase  | must not           | each must_not phrase is added in turn          |
      | ask for the OTP      | asks for secret    | policy rule 4: never ask for a secret          |
      | promise a fix time   | exact time promise | policy rule 2: no exact time for a fix         |
      | approve a big refund | big refund         | policy rule 8: refunds above ₹500 need a human |

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
