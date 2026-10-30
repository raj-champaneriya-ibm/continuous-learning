# Day 10 · Read the failures, not the averages

<!-- learn:status -->
**Status:** ⏳ open · morning 1 of 2 · dropped 2026-10-30 · ship by Sun 1 Nov, 05:00 · project 1, step 10
<!-- /learn:status -->

> **First-principles question:** Why does it fail, and which fix matters most?

**Why it matters for an FDE:** Averages tell you that something is wrong. Only reading failures tells you what to change. This is the most valuable hour in any AI project.

**Time:** about 105 minutes, over 2 mornings

### 1 · Learn (about 30 minutes)
- [A Field Guide to Rapidly Improving AI Products (Hamel Husain)](https://hamel.dev/blog/posts/field-guide/) · 20 min. Read 'The Most Common Mistake: Skipping Error Analysis' and 'A Simple Data Viewer'. Stop there.

### 2 · Build (about 50 minutes)
1. The notebook writes every failed case (A, B, C) into failures.csv.
2. Read at least 20 failures one by one in the viewer. Write a short note for each in failures.csv (this is called open coding).
3. Group the notes into 4 to 7 categories (wrong intent, missing fact, broke a rule, invented a fact, wrong tool, bad JSON…). Write the category next to each note.
4. Reload: count failures per category per version and draw the chart.

Your starter notebook is `notebook.ipynb` in this folder: fill in the **TODO** cells and run the ✅ self-check at the end.

### Done when
- [ ] At least 20 failures have a note and a category.
- [ ] A table: category × version.
- [ ] The top 3 categories, each with one example case id.

### 3 · Record (5 minutes or less)
- Show the category table.
- Read one failure aloud and explain its category.
- Say which single fix would remove the most failures.
- Two takes at most, then upload to YouTube as Unlisted and paste the link.

_Tempted to do more? Park it in `later.md`: Build a tiny HTML page to browse traces._

<sub>Project 1 · Measure before you believe: Build one customer-support assistant three ways (rules, one model call, an agent loop), measure all three, and recommend one with evidence.</sub>

## In my words
<!-- Fill these in before you ship (plain, simple English is perfect). Claude can help you turn what you said
     in your video into text, but keep your own words. -->
**For a beginner:** …

**For an engineer:** …

**For a customer:** …

## What surprised me
…

## How I used AI
…

## Video
<!-- learn:video -->
_Added when you ship._
<!-- /learn:video -->
