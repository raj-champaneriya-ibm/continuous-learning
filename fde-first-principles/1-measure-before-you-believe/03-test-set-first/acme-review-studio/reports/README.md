# Quarto starter

Install Quarto separately from https://quarto.org/docs/get-started/ and install
`jupyter` and `papermill` into the app's Python environment. Activate that environment.
From the app root:

```sh
quarto render reports/round-review.qmd -P review_round:1
```

HTML is written beside the source. No model calls. Run the app first to create
`runs/reviews.json`; with no saved records the report correctly shows zero coverage.
The report uses the bundled workbook. If using ACME_XLSX, change the workbook path
in the report to the matching snapshot before rendering.

For reproducible releases, copy the workbook and reviews together after editing stops,
record source revision, provider/model, guard configuration and dependency lock, then
render against that snapshot. Hashes detect changing inputs but do not preserve them.

Validation: Python computation cells executed successfully against local validation
results. Quarto CLI was unavailable, so full HTML rendering was not verified.
