# Later: grader ideas parked on day 5

Day 5 uses only code-based checks. These ideas come from the Anthropic eval guide, matched to Acme policy rules.

## Graders to add

| Grader                        | Method                                            | Acme rule it checks                                  |
|-------------------------------|---------------------------------------------------|------------------------------------------------------|
| Consistency                   | Cosine similarity of replies to paraphrased input | Same question, same answer (c22 vs c21, c79 vs c09)  |
| Tone and style                | LLM judge, Likert 1-5                             | P7: simple, polite English, also for angry input     |
| Sentiment                     | Sentiment model on the reply                      | Reply stays calm when the customer is angry          |
| Relevance and coherence       | ROUGE-L against a reference reply                 | Needs reference replies per case first               |
| Privacy preservation          | LLM judge, binary                                 | P5: no other customer's data (c77, c80)              |
| Context utilisation           | LLM judge, ordinal 0-3                            | Uses the KB article and outage record it was given   |
| Grader agreement              | Compare LLM judge vs a human-labelled sample      | Test the grader itself before trusting it            |

Structure every judge prompt so the output is machine-gradable: ask for reasoning first, then a single label (`yes`/`no` or `1`-`5`) in a fixed tag.

## Test cases to add

* Empty or one-word message ("hi", "?")
* Message that is not about Acme at all
* Very long message (more than 300 words, several issues at once)
* Abusive or toxic message that still contains a real issue
* More cases where experts disagree, with a second labeller to measure agreement

## Grader false positives still open

* "We're fixing it and will update you in 2 hours" is flagged as a time promise
* c23: KB04 auto-refund of ₹1,499 conflicts with the ₹500 rule; an expert must decide which rule wins
