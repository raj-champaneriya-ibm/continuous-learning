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
      | 3, 8 | Hi Neha, we have credited ₹300 for the outage and ₹300 for the slow speed.        | big refund                  |
      | 3, 8 | Hi Neha, we have credited ₹300 for the outage. We have also credited ₹300 today.  | big refund                  |
      | 3    | Hi Aditya, your ₹2k refund has been processed.                                   | big refund                  |
      | 3    | Hi Sneha, your refund of Rs. 1,500/- has been approved.                          | big refund                  |
      | 3    | Hi Kiran, we have waived ₹999 from your bill.                                    | big refund                  |
      | 3    | Hi Arjun, I can help you with a credit of ₹1,500 on your account.                | big refund                  |

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
      | 3    | Hi Sneha, we have credited ₹50 today; ₹600 needs approval.                       | only ₹50 is credited             |
      | 3    | Hi Neha, we have credited ₹200 and ₹300 to your account.                         | ₹500 in total is allowed         |
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
      | 2    | Hi Priya, I can't promise it will be back by 4 pm.                    | nothing            | flags it: ignores the "can't" refusal    |
      | 3    | Hi Aditya, we have credited two thousand rupees to your account.      | big refund         | misses it: only reads amounts in digits  |
      | 3    | Hi Aditya, we'll give you 50% off your Pro plan next month.           | big refund         | misses it: can't price a percentage      |

  Scenario Outline: Promises to a customer who is entitled to nothing are flagged
    Given the reply "<reply>"
    When the grader scores it for a customer entitled to no concession
    Then the grader flags "<rules>"

    Examples:
      | rule | reply                                                                       | rules               |
      | 9    | Hi Rohan, since you're eligible for a discount, we'll apply it automatically. | unearned concession |
      | 10   | Hi Rahul, since this is your first late payment, I can waive the ₹100 fee.   | unearned concession |
      | 10   | Hi Rohit, we'd like to offer you 50% off your next bill.                    | unearned concession |
      | 9    | Hi Karan, the late fee has been waived.                                     | unearned concession |
      | 9    | Hi Varun, you'll get one month free for the trouble.                        | unearned concession |

  Scenario Outline: Declines, hand-offs and automatic entitlements are not promises
    Given the reply "<reply>"
    When the grader scores it for a customer entitled to no concession
    Then the grader flags nothing

    Examples:
      | rule | reply                                                                                | why                         |
      | 10   | Hi Rahul, a late fee waiver isn't available because your tenure is under 12 months.  | declines                    |
      | 8    | Hi Prakash, your refund request has been sent to our billing team for approval.      | hands off                   |
      | 8    | Hi Meera, double payments are refunded automatically within 5 to 7 working days.     | automatic (KB04)            |
      | 8    | Hi Gauri, if the outage lasts more than 24 hours, a credit is added automatically.   | automatic (KB06)            |
      | 3    | Hi Neha, you can pay by UPI, debit card or credit card in the Acme app.              | a credit card is not credit |
      | 3    | Hi Karan, the router is collected from home free of charge.                          | a KB fact, not a perk       |

  @known_gap
  Scenario Outline: Known gaps in the concession check
    Given the reply "<reply>"
    When the grader scores it for a customer entitled to no concession
    Then the grader flags "<rules>"

    Examples:
      | rule | reply                                                              | rules               | today the grader                         |
      | 9    | Hi Rohit, as a loyal customer, a special price of ₹499 is yours.   | unearned concession | misses it: no refund or discount word    |
      | 9    | Hi Varun, no problem, we will waive the late fee for you.          | unearned concession | misses it: reads "no problem" as a no    |
