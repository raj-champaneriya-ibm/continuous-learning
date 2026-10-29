# Acme Fibre: the project brief (fictional)

**Acme Fibre** is a made-up broadband company in Pune. It has about 40,000 home customers. Its
support team of 25 people answers around 1,200 customer emails a day. Many emails are in English,
many in Hinglish (Hindi written in English letters).

The head of support says:

> "We want an AI agent to answer customer emails. Our competitors are doing it."

Your job in project 1 is to find out what they really need, build it three ways
(rules, one model call, an agent), measure all three, and recommend one with evidence.

## The files

| File | What it is |
|---|---|
| `customers.json` | 40 sample customers: area, plan, tenure, balance, plus history (credits in the last 30 days, last late-fee waiver, last retention offer, payments this cycle) |
| `outages.json` | Outages happening right now, by area |
| `kb.md` | 16 short help articles the support team uses |
| `policy.md` | Rules every reply must follow |
| `cases.jsonl` | Test cases: an email plus what a correct reply must contain (from day 3) |
| `cases_abuse.jsonl` | 40 contrast pairs (80 cases): the same request from a customer trying to milk a loophole and from one who is entitled, told apart by the customer record. Drafted, not yet expert-reviewed |
| `cases_multiturn.jsonl` | 40 conversations graded on the next reply: earlier turns are in `history` (render them with `lab.acme.conversation()`). Drafted, not yet expert-reviewed |
| `cases_regional.jsonl` | 52 emails and threads in Marathi, Hindi, Gujarati, Tamil, Telugu, Kannada, Malayalam, Punjabi, Hinglish and mixed languages. `message_en` and `text_en` hold English glosses for reviewers; `twin_of` points to the same scenario in another file. Drafted, not yet expert- or native-speaker-reviewed |
| `queries.jsonl` | Search tests: a question plus the right help article (from project 2) |

Plans: **Basic** 100 Mbps ₹699/month · **Plus** 300 Mbps ₹999/month · **Pro** 1 Gbps ₹1,499/month.

All names, numbers and policies here are invented for learning. Real customer data never goes
into this public repository.
