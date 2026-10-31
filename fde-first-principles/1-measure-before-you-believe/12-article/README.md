# Day 12 · Article: measure before you believe

<!-- learn:status -->
**Status:** not dropped yet · project 1, step 12
<!-- /learn:status -->

> **First-principles question:** Can you tell the project 1 story so that a stranger trusts your numbers?

**Why it matters for an FDE:** An FDE's write-up travels further than any meeting. A public article with real error bars is proof that you measure before you believe, and writing it shows you what you really understood.

**Time:** about 235 minutes, over 3 mornings

### Set up
- Open your rajc.work Hugo site locally (`hugo server`) so you can preview the post before it goes live.

### Before you start
- Ship day 11 first. The article ends with your ADR's decision and its "what would change my mind".
- Your numbers live in two places: the day 9 table (`09-success-cost-latency/notebook.ipynb`) and the evidence table in `11-recommendation-first-draft/notebook.ipynb`. Check every number in the article against one of them.
- For the diagram, export your day 11 design as PNG and put it next to the post in your Hugo site.

### 1 · Learn (about 40 minutes)
- [What to blog about (Simon Willison): 'Write about your projects'](https://simonwillison.net/2022/Nov/6/what-to-blog-about/) · 5 min. Why a project write-up is worth more than the project. Note what he says to include.
- [Technical Writing One (Google): Short sentences](https://developers.google.com/tech-writing/one/short-sentences) · 20 min. One idea per sentence. Try the exercises on a paragraph of your ADR.

### 2 · Write and publish (about 185 minutes)
1. Close every notebook. In the README's 'Without notes' section, write about 300 words from memory: what you built, what you measured, what surprised you. No notes, no AI. Whatever you can't write is what to revisit.
2. Now open the notebooks and check every number. Turn the 300 words into article.md: the setup / question / inside block at the top, then the story.
3. Grow it to 800–1,200 words: what Acme asked for, the three versions, your table (pass rate ± 2 se, p95 seconds, ₹ per 1,000 emails), two failures that taught you something and your ADR's decision. Add your design diagram.
4. Edit for a reader: read it aloud, cut what does not help, one idea per sentence. AI may fix grammar only: note it under 'How I used AI'.
5. Publish it on rajc.work (draft: false, build, push). Open the live page, then ship with `fde-coach learn done --article <link>`.

Your starter is `article.md` in this folder: Hugo front matter plus a skeleton. Copy it into your site when it is ready.

### Done when
- [ ] 'Without notes' in README.md has about 300 words, written before you opened the notebooks.
- [ ] article.md has 800–1,200 words, a table of your real numbers and one diagram.
- [ ] Every number in the article matches a notebook.
- [ ] The article is live on rajc.work.

### 3 · Record (optional for an article)
- Optional: a 3-minute video reading the setup / question / inside block aloud, ending with the one thing you would tell a customer.
- Share the link wherever you like: the article is the proof.

_Tempted to do more? Park it in `later.md`: Run the same three-way test privately on your own communication agent (a private repo, never this one)._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

## Without notes
<!-- Step 1, before you open any notebook: about 300 words from memory. What you built, what you measured,
     what surprised you. No notes, no AI. Whatever you can't write is what to revisit. -->
…

## How I used AI
…

## The article
<!-- learn:article -->
_Added when you ship._
<!-- /learn:article -->

## Video
<!-- learn:video -->
_Optional for an article._
<!-- /learn:video -->
