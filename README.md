# Biological Data Visualization with Seaborn

[![CI](https://github.com/mbilal-OU/biology-data-viz-seaborn/actions/workflows/ci.yml/badge.svg)](https://github.com/mbilal-OU/biology-data-viz-seaborn/actions/workflows/ci.yml)
[![Docs](https://github.com/mbilal-OU/biology-data-viz-seaborn/actions/workflows/docs.yml/badge.svg)](https://github.com/mbilal-OU/biology-data-viz-seaborn/actions/workflows/docs.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-2E7D32)](LICENSE)

A tested portfolio of statistical visualization patterns for biology and
bioinformatics. The repository combines analysis-ready tables, reusable
Python functions, narrative notebooks, automated tests, and publication
exports. It emphasizes choosing a defensible representation, not merely
calling a plotting function.

All included datasets are seeded simulations with documented ground truth.
They support reproducible testing and do not represent experimental evidence.

## Flagship case studies

### Differential expression

![Differential-expression volcano and MA plots](figures/11_differential_expression_dashboard.png)

The volcano plot combines FDR with an explicit effect-size threshold. The MA
plot exposes abundance-dependent behavior that a volcano plot can hide. The
code accepts an analysis-ready results table and does not confuse visualization
with differential-expression inference.

### Pangenome population structure

![Pangenome frequency spectrum and PCA](figures/12_pangenome_structure.png)

Gene families are classified from measured prevalence, and PCA coordinates and
variance percentages are calculated directly from the binary presence-absence
matrix. A companion clustermap uses Jaccard distance, which is appropriate for
binary gene content.

### Compositional microbiome data

![CLR-transformed microbiome clustermap](figures/14_microbiome_clr_clustermap.png)

Relative abundances are zero-replaced, renormalized, and transformed to
centered-log-ratio coordinates. Clustering then uses Euclidean distance in CLR
space, equivalent to Aitchison distance, instead of treating percentages as
unconstrained measurements.

## Demonstrated capabilities

| Analytical question | Visualization and method | Biological example |
|---|---|---|
| Which features change and by how much? | Volcano, MA, box, violin, swarm | Differential expression |
| Do samples separate by gene content? | PCA, Jaccard clustermap | Bacterial pangenome |
| How are values distributed? | Histogram, ECDF, density | Variant allele frequencies |
| How does a response change over time? | Subject-aware time course, mean and SD | Cytokine kinetics |
| Are variables associated? | Scatter, regression, joint distribution | Docking and trait data |
| Is there multivariable structure? | Pairplot, correlation heatmap | Sequencing QC and metabolomics |
| How should compositions be compared? | CLR transform, Aitchison distance | Microbiome abundance |
| Can a mechanistic curve be estimated? | Nonlinear Michaelis-Menten fit | Enzyme inhibition |
| What do category counts show? | Annotated count heatmap | Pathway status table |

The package also demonstrates faceting, semantic mappings, accessible palettes,
annotation, legend control, vector export, reusable Axes-level functions, and
figure-level Seaborn objects.

## Quick start

```bash
git clone https://github.com/mbilal-OU/biology-data-viz-seaborn.git
cd biology-data-viz-seaborn
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
jupyter lab
```

Windows activation commands are documented in
[`docs/setup.md`](docs/setup.md).

Start with [`notebooks/omics_case_studies.ipynb`](notebooks/omics_case_studies.ipynb).
The original core-pattern notebook remains available as a detailed reference:
[`notebooks/seaborn_beginner_guide.ipynb`](notebooks/seaborn_beginner_guide.ipynb).

## Reusable API

```python
import pandas as pd
from bioviz import omics, theme

theme.set_theme()

de = pd.read_csv("data/differential_expression.csv")
fig, ax = omics.volcano_plot(
    de,
    fdr_threshold=0.05,
    effect_threshold=1.0,
)
theme.savefig(fig, "volcano.svg")
```

Pangenome PCA is similarly explicit:

```python
presence = pd.read_csv("data/pangenome_presence_absence.csv")
scores, explained_variance = omics.pangenome_pca(presence)
fig, ax, explained_variance = omics.pangenome_pca_plot(presence)
```

Invalid schemas, non-binary gene matrices, impossible thresholds, and negative
abundances raise clear errors instead of producing plausible but incorrect
figures.

## Scientific guardrails

- SD or confidence bands are descriptive unless tied to a stated inferential
  model. Their overlap is not used as a significance test.
- A pathway count table is not labeled as enrichment without a gene universe,
  statistical test, and multiple-testing correction.
- Clade-stratified trait plots do not claim to correct for shared ancestry.
- Microbiome compositions are transformed before distance-based clustering.
- PCA is used as an exploratory projection, not as evidence of discrete
  biological populations.
- Simulated docking scores are not interpreted as experimental affinity.

## Reproducibility and quality checks

```bash
python scripts/generate_datasets.py
python scripts/build_advanced_gallery.py
pytest -q
ruff check bioviz scripts tests
mkdocs build --strict
```

Continuous integration checks deterministic data generation, package linting,
semantic and rendering tests, notebook execution, package construction, code
coverage, and strict documentation links. PNG figures are written at 300 DPI;
SVG and PDF exports preserve vector text and geometry.

## Repository map

```text
bioviz/       reusable plotting and analysis helpers
data/         seeded datasets plus a complete data dictionary
figures/      rendered raster and vector gallery
notebooks/    narrative core and advanced case studies
scripts/      deterministic data and gallery builders
tests/        rendering, numerical, schema, and biological sanity checks
docs/         documentation site source
```

## Scope

This repository focuses on static statistical graphics with Seaborn and its
Matplotlib foundation. Custom phylogenomics layouts, genome tracks, synteny,
animation, and low-level figure engineering are covered in the companion
[biology-data-viz-matplotlib](https://github.com/mbilal-OU/biology-data-viz-matplotlib)
repository.

## Citation and license

Citation metadata are provided in [`CITATION.cff`](CITATION.cff). The code is
released under the [MIT License](LICENSE).
