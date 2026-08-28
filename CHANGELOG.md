# Changelog

All notable changes to this project are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [1.0.0]: 2026-08-28

### Added
- Full rebuild of the repository around a tested, importable `bioviz`
  package (`theme`, `relational`, `distributions`, `categorical`,
  `regression`, `matrix` modules).
- 10 simulated datasets in `data/`, each generated deterministically
  by `scripts/generate_datasets.py` with a documented biological and
  statistical rationale, plus `data/data_dictionary.md`.
- `tests/test_bioviz.py`: 20 tests covering both plot rendering and
  statistical sanity checks against known ground truth (e.g.
  Michaelis-Menten parameter recovery, correlation signs, distribution
  orderings).
- `notebooks/seaborn_beginner_guide.ipynb`: full tutorial covering 10
  Seaborn plot types, each with biological question → rationale →
  code → interpretation, executed end-to-end.
- `notebooks/matplotlib_practice.ipynb`: supplementary raw-Matplotlib
  warm-up notebook.
- `docs/`: gallery of every figure paired with its exact code, plus a
  documentation home page; `mkdocs.yml` for an optional docs site.
- `figures/workflow_diagram.svg`: repository pipeline diagram.
- Project scaffolding: `LICENSE` (MIT), `CITATION.cff`,
  `CONTRIBUTING.md`, `pyproject.toml`, `requirements.txt`,
  `environment.yml`, `.gitignore`.
- CI (`.github/workflows/ci.yml`): lint with ruff, regenerate datasets
  and diff for determinism, run pytest, execute both notebooks.
- Docs CI (`.github/workflows/docs.yml`): validate the mkdocs build.

## [0.1.0]: initial version

- Flat repository: README with inline code snippets, 10 example CSVs,
  a single tutorial notebook, and `seaborn_templates.py`.
