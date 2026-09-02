# Contributing

Contributions are welcome: new plot types, new datasets, clearer
explanations, or bug fixes.

## Setup

```bash
git clone https://github.com/mbilal-OU/seaborn-biological-statistics.git
cd seaborn-biological-statistics
pip install -r requirements.txt
pip install -e .
```

## Repository conventions

- **Datasets** are generated, not hand-written. If you add or change a
  dataset, do it in `scripts/generate_datasets.py`, with a docstring
  explaining the biological scenario and the statistical rationale
  behind the simulation (distribution choices, effect sizes, noise
  model). Regenerate with `python scripts/generate_datasets.py` and
  update `data/data_dictionary.md` to match.
- **Plotting code** lives in `bioviz/`, organized by Seaborn plot
  family (`relational.py`, `distributions.py`, `categorical.py`,
  `regression.py`, `matrix.py`). Every public function needs a
  docstring describing its parameters and what it returns.
- **Tests**: add both a rendering smoke test and, where the data has
  a known ground truth, a statistical sanity check to
  `tests/test_bioviz.py`. Run tests with:

  ```bash
  pytest tests/ -v
  ```

- **Notebook**: the tutorial notebook is authored as a Jupytext
  "percent" script at `notebooks/seaborn_beginner_guide.py` and
  converted to `.ipynb`. To edit it:

  ```bash
  jupytext --to notebook notebooks/seaborn_beginner_guide.py -o notebooks/seaborn_beginner_guide.ipynb
  jupyter nbconvert --to notebook --execute --inplace notebooks/seaborn_beginner_guide.ipynb
  ```

  Please re-execute the notebook before committing so committed output
  matches the code (CI checks this, see `.github/workflows/ci.yml`).

## Adding a new plot type

1. Add or extend a dataset generator in `scripts/generate_datasets.py`
   with a clear rationale docstring.
2. Add a plotting function to the appropriate `bioviz/*.py` module.
3. Add a rendering test (and a statistical sanity check if applicable)
   to `tests/test_bioviz.py`.
4. Add a section to the tutorial notebook following the existing
   structure: biological question → why this plot → code →
   interpretation.
5. Update the summary table at the end of the notebook and the plot
   list in `README.md`.

## Pull requests

- Keep PRs focused on one change.
- Make sure `pytest tests/ -v` passes locally before opening a PR.
- Describe the biological motivation for any new dataset or plot in
  the PR description.
