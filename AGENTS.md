---
title: Agent guide
description: Environment setup, test execution, and debugging for the continuous-learning repository
---

## Repository layout

* `fde-first-principles/` holds the Python project: the shared grader in `lab/`, data in `data/`, and daily notebooks
* `fde-first-principles/tests/` holds the BDD tests for the grader (`features/*.feature` plus `test_*.py` step definitions)
* `fde-first-principles/1-measure-before-you-believe/03-test-set-first/acme-review-studio/` is a separate app with its own `requirements.txt` and `pytest.ini`
* `dsa/` and `boosted tree/` are standalone study notes

## Environment setup

Use the virtual environment at the repository root (`.venv`, Python 3.11). VS Code selects it through `.vscode/settings.json`.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install --group fde-first-principles/pyproject.toml:dev
```

`--group` needs pip 25.1 or later. The `dev` group in `fde-first-principles/pyproject.toml` installs `pytest` and `pytest-bdd`.

## Running the tests

Always run pytest from `fde-first-principles/`. The pytest settings (`pythonpath`, `testpaths`) live in its `pyproject.toml`, so running from the repository root fails with import errors and also collects the `acme-review-studio` tests.

```bash
cd fde-first-principles
../.venv/bin/python -m pytest -v
```

Expected result: all scenarios pass, and scenarios tagged `@known_gap` report as `xfail`.

| Goal                                          | Command (from `fde-first-principles/`)                       |
|-----------------------------------------------|--------------------------------------------------------------|
| Run one group of scenarios                    | `../.venv/bin/python -m pytest -v -k follow_the_policy`      |
| Run scenarios mentioning a word               | `../.venv/bin/python -m pytest -v -k OTP`                    |
| Show the real assertion behind each known gap | `../.venv/bin/python -m pytest -v --runxfail -k known_gaps`  |

## How the BDD tests work

* `tests/features/policy_rules.feature` is the source of truth that stakeholders read; each `Examples` row is one agreed policy decision
* `tests/test_policy_rules.py` maps the Gherkin steps to `lab.evals.policy_violations()`
* Rule names in the feature use spaces (`big refund`) and map to grader codes (`big_refund`)
* `tests/conftest.py` turns the `@known_gap` tag into a strict `xfail`

When a grader fix makes a known gap pass, the strict `xfail` fails the run. Move that row from the known-gaps table into the table it now belongs to.

To add a case, add a row to the matching `Examples` table. New step wording needs a matching step definition in `tests/test_policy_rules.py`.

## Debugging in VS Code

Install the recommended extensions from `.vscode/extensions.json`:

* Python (`ms-python.python`) for the Test Explorer
* Python Debugger (`ms-python.debugpy`) for breakpoints
* Pylance (`ms-python.vscode-pylance`) for navigation and type checks
* Cucumber (`CucumberOpen.cucumber-official`) for Gherkin highlighting, formatting, and outline

Breakpoints do not bind in `.feature` files. Set them in the step functions in `tests/test_policy_rules.py` or inside `lab/evals.py`.

Use the Test Explorer for single scenarios. It lists one test per `Examples` row under `test_policy_rules.py`, and its Debug Test action uses the `Python: debug test (Test Explorer)` launch configuration.

Use Run and Debug (F5) for groups:

| Launch configuration                      | Use it to                                                          |
|-------------------------------------------|--------------------------------------------------------------------|
| `BDD: debug all policy scenarios`         | Step through every scenario                                        |
| `BDD: debug scenarios matching a keyword` | Enter a `-k` expression such as `OTP` or `known_gaps`              |
| `BDD: debug known gaps as real failures`  | Stop on the actual assertion while fixing a gap (uses `--runxfail`) |

> [!NOTE]
> The Cucumber extension recognises plain-string steps such as `the grader checks it`. Steps wrapped in `parsers.parse(...)` may show as undefined in the editor even though pytest-bdd runs them correctly.
