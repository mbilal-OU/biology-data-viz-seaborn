# Documentation

**Start here** if you're new to the repo: [`../README.md`](../README.md)
gives the overview, quick start, and repository map.

## Contents

| Doc | What's in it |
|---|---|
| [`gallery.md`](gallery.md) | Every figure in the repo, paired with the exact code that produced it |
| [`../data/data_dictionary.md`](../data/data_dictionary.md) | Column-by-column definitions and the simulation rationale behind each dataset |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | How to add a new dataset, plot type, or fix |
| [`../CITATION.cff`](../CITATION.cff) | Citation metadata |

## How the pieces fit together

![Pipeline](../figures/workflow_diagram.svg)

1. **`scripts/generate_datasets.py`**: seeded (`np.random.default_rng(42)`)
   simulation of all 10 datasets, each with a documented biological and
   statistical rationale (effect sizes, noise model, ground truth).
2. **`data/*.csv`**: the generated datasets, plus
   [`data_dictionary.md`](../data/data_dictionary.md) describing every column.
3. **`bioviz/`**: a small, tested, importable plotting package. One
   module per Seaborn plot family (`relational`, `distributions`,
   `categorical`, `regression`, `matrix`), each function documented and
   covered by `tests/test_bioviz.py`.
4. **`notebooks/`**: the tutorial notebook walks through all 10 plot
   types with biological question, rationale, code, and interpretation
   for each. A supplementary notebook covers raw Matplotlib basics.
5. **`figures/`**: 300 DPI exported PNGs, embedded in
   [`gallery.md`](gallery.md) and the README.
6. **CI** (`.github/workflows/ci.yml`): on every push, lint with ruff,
   regenerate the datasets and diff against what's committed (catches
   silent nondeterminism), run the pytest suite, and re-execute both
   notebooks end-to-end.

## Design principles

- **Every dataset has a reason.** Nothing is `np.random.rand()` with no
  structure. Each CSV is built to have a specific, documented,
  interpretable signal (see the rationale docstrings in
  `generate_datasets.py`).
- **Tests check biology, not just rendering.** Beyond "does the plot
  render," `tests/test_bioviz.py` checks that quantitative results match
  the simulation's ground truth, for example that a Michaelis-Menten
  fit correctly distinguishes competitive from non-competitive
  inhibition.
- **The notebook is a source of truth, not a demo.** It's executed in
  CI on every push, so committed output always matches the code that
  produced it.
