# Evaluation evidence (Quarto)

A small Quarto website built from two files the Studio already keeps: the eval workbook
(`data/Acme_Fibre_Grounded_Draft_Eval.xlsx`) and the saved runs and reviews (`runs/reviews.json`).
Rendering only reads them. It never calls a model or changes a review.

| Page | Answers | For |
|---|---|---|
| `evaluation-report.qmd` | Are the drafts good enough, and are they routed to the right place? Release gates, pass rate and routing accuracy with 95% intervals, missed escalations, grounding, error cost, worst fails with critiques. | The customer and the release decision |
| `dataset-card.qmd` | Is the test fair? Composition, escalation rules, where the cases come from, open label decisions, and what the set can't tell you. Works from the workbook alone. | Anyone trusting the numbers |
| `review-dashboard.qmd` | When do humans help? Which layer triggered each escalation, where every case went, disagreement rates, failure categories, routing by rule. | The domain expert and the team tuning the workflow |
| `index.qmd` | Overview: round, coverage, drafting model, links. | Everyone |

## Set up (once)

1. Install Quarto 1.5 or newer from <https://quarto.org/docs/get-started/>
   (or `pip install quarto-cli` into the app's virtual environment).
2. `pip install -r requirements.txt` from `acme-review-studio/`. This includes `jupyter`, `plotly` and `pyyaml`,
   which the pages need.

## Render

From `acme-review-studio/`:

```bash
quarto render reports                                      # whole site → reports/_site/
quarto preview reports                                     # live preview while editing a page
quarto render reports/evaluation-report.qmd -P review_round:2   # one page, a past round
```

Open `reports/_site/index.html`. Charts load `plotly.min.js` from the same folder (a pre-render step copies it
from the installed `plotly` package), so the site works offline; if a browser blocks local files, serve
it with `python -m http.server -d reports/_site`.

To send the evaluation report as **one file** (about 6 MB, everything inlined):

```bash
quarto render reports/evaluation-report.qmd -M embed-resources:true
```

PDF isn't set up: the charts are interactive Plotly, which needs a static-image step for PDF.

### Inputs

| Variable | Default | Use it to |
|---|---|---|
| `ACME_RUNS` | `runs/reviews.json` | point at a frozen copy of a finished round |
| `ACME_XLSX` | `data/Acme_Fibre_Grounded_Draft_Eval.xlsx` | point at a workbook snapshot |

`review_round` (a Quarto parameter) picks the round; `0`, the default, means the latest round in the runs file.
Every page prints the round, the drafting model and SHA-256 hashes of both inputs, so a reader can tell
which data a page was built from.

### Preview with demo data

Before any real reviews exist, generate a demo round. It runs all 84 cases through the offline stand-in and
fills verdicts from the automatic checks, so every chart has something to show:

```bash
python reports/scripts/make_demo_runs.py                     # writes reports/demo/reviews.json
ACME_RUNS=reports/demo/reviews.json quarto render reports
```

Pages built from it carry a **Demo data** warning. They are for checking the layout, never evidence.
With no runs at all, every page still renders and says "No runs yet" instead of showing zeros.

## Where the numbers come from

- **`acme_metrics.py`** holds the one definition of every number (pass rate, routing accuracy, missed
  escalation, unsafe auto-send, code save, the layer that triggered an escalation, disagreement rates,
  error cost). All pages import it, and `tests/features/report_metrics.feature` pins the definitions down.
- **`thresholds.yml`** holds the release gates, review minutes per case and error costs. They are
  proposals for the Principal Domain Expert to own; the costs are placeholders until Acme supplies real ones.
- Rates always show their denominator and a 95% Wilson interval, and say "no data yet" when the
  denominator is zero.
- Grounding numbers come from the heuristic step-6 checks and the must-include / must-not phrases.
  They show where to look, not proof that every claim is grounded.

## Things to know

- **`freeze` is off on purpose.** Quarto's freeze only notices changes to the `.qmd` files, not to
  `reviews.json` or the workbook, so a frozen page would quietly show old numbers. Rendering only reads
  files, so re-running every time costs a few seconds.
- **Keep `_site/` private.** It contains customer emails from the test set and, once real runs exist,
  the drafted replies and the expert's critiques. Share it inside the team, not on a public host.
- Generated files (`_site/`, `.quarto/`, `demo/`, `plotly.min.js`) are git-ignored.

## Layout

```
_quarto.yml              website, navbar, theme, execute options
acme_metrics.py          every metric, plus small HTML helpers (tiles, tables, banner)
thresholds.yml           release gates and error costs
theme.scss               the minimalist blue theme
index.qmd                overview
evaluation-report.qmd    release decision
dataset-card.qmd         what the test set covers
review-dashboard.qmd     escalation and disagreement dashboard (format: dashboard)
scripts/copy_plotly.py   pre-render: copy plotly.min.js next to the pages
scripts/make_demo_runs.py  demo round for previewing
```
