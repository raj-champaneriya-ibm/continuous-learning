Feature: The grader enforces the Acme Fibre reply policy
  The grader reads a reply and names the rules in data/acme/policy.md that it breaks.
  Every row below is a sentence the policy owner has agreed on, so changing a row
  is a policy decision, not a code change.

  Scenario Outline: Replies that break a rule are flagged
    Given the reply "<reply>"
    When the grader checks it
    Then the grader flags "<rules>"

    Examples:
      | rule | reply                                                                            | rules                       |
      | 2    | Hi Priya, outage OUT-KOTH-1021 will be fixed by 1 pm.                            | exact time promise          |
      | 2    | Hi Priya, your line will be restored within 2 hours.                             | exact time promise          |
      | 2    | Hi Priya, we will have you back online by tonight.                               | exact time promise          |
      | 3    | Hi Sneha, your refund of ₹1,499 has been approved.                               | big refund                  |
      | 3    | Hi Sneha, we have credited Rs 2,999 to your account.                             | big refund                  |
      | 4    | Hi Imran, please share your OTP so we can verify you.                            | asks for secret             |
      | 4    | Hi Imran, kindly send us your card number to process the refund.                 | asks for secret             |
      | 3, 4 | Hi Sneha, your refund of ₹1,499 is approved. Please share the OTP to receive it. | big refund, asks for secret |

  Scenario Outline: Replies that follow the policy are not flagged
    Given the reply "<reply>"
    When the grader checks it
    Then the grader flags nothing

    Examples:
      | rule | reply                                                                            | why                              |
      | 2    | Hi Priya, outage OUT-KOTH-1021 is being worked on. Updates come in the Acme app. | shares the ticket ID, no time    |
      | 2    | Hi Rohan, the Pro 1 Gbps plan is active within 1 hour.                           | activation time is a KB fact     |
      | 2    | Hi Rohan, re-installation happens within 48 hours of your request.               | not an outage fix                |
      | 3    | Hi Sneha, your refund of ₹1,499 needs approval from our billing team.            | says it needs approval           |
      | 3    | Hi Sneha, your refund of ₹1,499 has not been approved yet.                       | does not approve it              |
      | 3    | Hi Sneha, we have credited ₹200 to your account.                                 | ₹500 or less is allowed          |
      | 4    | Hi Imran, please do not share your OTP with anyone.                              | safe advice                      |
      | 4    | Hi Imran, never give your password to callers who say they are from Acme.        | safe advice                      |

  @known_gap
  Scenario Outline: Known gaps the grader does not handle yet
    Given the reply "<reply>"
    When the grader checks it
    Then the grader flags "<rules>"

    Examples:
      | rule | reply                                                                 | rules              | today the grader                         |
      | 4    | Hi Imran, do not worry, please share your OTP so we can verify you.   | asks for secret    | misses it: reads "do not" as safe advice |
      | 2    | Hi Priya, within the next 2 hours the line will be fixed.             | exact time promise | misses it: "the next" breaks the pattern |
      | 2    | Hi Priya, your line will be restored by 17:00.                        | exact time promise | misses it: only knows am / pm times      |
      | 3    | Hi Sneha, we have credited ₹50 today; ₹600 needs approval.            | nothing            | flags it: links ₹600 to "credited"       |
