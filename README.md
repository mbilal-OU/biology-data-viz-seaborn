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

## Start here: the visualization learning path

This is a **public, tutorial-first portfolio repository**. The README is designed
to let a learner scan the figures first, understand the analytical question,
open the matching notebook, and then reuse the tested plotting functions.

| Goal | Best starting point |
|---|---|
| Learn the visual grammar from worked examples | Browse the visual tutorial gallery below |
| Reproduce every figure | Run the notebooks from top to bottom |
| Reuse tested plotting code | Import the functions in the reusable API section |
| Understand scientific limitations | Read the scientific guardrails before interpreting a plot |
| Build a publication figure | Export PNG for review and SVG/PDF for final editing |

### A growing visualization series

The two current repositories establish a reusable pattern for a broader public
learning series:

- **Seaborn**: statistical graphics, tidy data, semantic mappings, distributions,
  uncertainty, and omics exploration.
- **Matplotlib**: low-level figure engineering, custom geometry, dashboards,
  animation, phylogenomics, genome tracks, and publication layout.
- **Future Python and R modules** can follow the same structure for interactive
  graphics and specialist ecosystems such as Plotly, Altair, ggplot2, ggtree,
  ComplexHeatmap, and Shiny.

Each module should remain independently runnable, visual from the first screen,
scientifically careful, and strong enough to serve as both a tutorial and a
portfolio artifact.

## Visual tutorial gallery

These are rendered outputs from the repository, not decorative screenshots.
Click any figure to open the full-resolution version. The numbered filenames
match the progression in
[the beginner notebook](notebooks/seaborn_beginner_guide.ipynb), while the
advanced omics panels are developed in
[the case-study notebook](notebooks/omics_case_studies.ipynb).

### Relationships, trends, and uncertainty

| Tutorial example | Tutorial example |
|---|---|
| **Docking-score relationship**<br>[![Docking scatter plot](figures/01_docking_scatter.png)](figures/01_docking_scatter.png)<br>Scatter semantics, group encoding, trend estimation, and cautious association language. | **Cytokine time course**<br>[![Cytokine time-course plot](figures/02_cytokine_timecourse.png)](figures/02_cytokine_timecourse.png)<br>Repeated measurements, individual trajectories, summary curves, and explicit variability. |
| **Enzyme-response regression**<br>[![Enzyme regression facets](figures/05_enzyme_lmplot.png)](figures/05_enzyme_lmplot.png)<br>Faceted regression for comparing conditions without hiding between-group structure. | **Trait association with marginals**<br>[![Joint distribution plot](figures/09_phylo_jointplot.png)](figures/09_phylo_jointplot.png)<br>A joint view of association and marginal distributions, without claiming phylogenetic correction. |

### Distributions and group comparisons

| Tutorial example | Tutorial example |
|---|---|
| **Variant-frequency histogram**<br>[![Variant allele-frequency histogram](figures/03_variant_af_histogram.png)](figures/03_variant_af_histogram.png)<br>Binning choices and distribution shape for bounded biological measurements. | **Variant-frequency ECDF**<br>[![Variant allele-frequency ECDF](figures/03b_variant_af_ecdf.png)](figures/03b_variant_af_ecdf.png)<br>A bin-free companion view that makes thresholds and tail probabilities easy to read. |
| **Expression box plot**<br>[![Gene-expression box plot](figures/04_expression_boxplot.png)](figures/04_expression_boxplot.png)<br>Robust group summaries with medians, quartiles, and outlier visibility. | **Expression violin and swarm**<br>[![Gene-expression violin and swarm plot](figures/04b_expression_violin_swarm.png)](figures/04b_expression_violin_swarm.png)<br>Distribution shape plus the observed samples, avoiding a summary-only story. |

### Multivariable structure and matrices

| Tutorial example | Tutorial example |
|---|---|
| **Metabolite heatmap**<br>[![Metabolite heatmap](figures/06_metabolite_heatmap.png)](figures/06_metabolite_heatmap.png)<br>Matrix encoding, centered color scales, annotation, and readable feature comparison. | **Microbiome clustermap**<br>[![Microbiome clustermap](figures/07_microbiome_clustermap.png)](figures/07_microbiome_clustermap.png)<br>Exploratory hierarchical structure and the motivation for composition-aware preprocessing. |
| **Sequencing-QC pairplot**<br>[![Sequencing quality-control pairplot](figures/08_qc_pairplot.png)](figures/08_qc_pairplot.png)<br>Pairwise distributions and correlations for fast multivariable quality control. | **Pathway count heatmap**<br>[![Pathway count heatmap](figures/10_pathway_heatmap.png)](figures/10_pathway_heatmap.png)<br>Annotated categorical counts, clearly separated from statistical enrichment claims. |

### Advanced omics case studies

| Tutorial example | Tutorial example |
|---|---|
| **Differential-expression dashboard**<br>[![Volcano and MA plots](figures/11_differential_expression_dashboard.png)](figures/11_differential_expression_dashboard.png)<br>Volcano and MA views with FDR and effect-size thresholds computed from the data. | **Pangenome population structure**<br>[![Pangenome frequency spectrum and PCA](figures/12_pangenome_structure.png)](figures/12_pangenome_structure.png)<br>Gene-frequency classes and PCA derived from a binary presence–absence matrix. |
| **Pangenome Jaccard clustermap**<br>[![Pangenome Jaccard clustermap](figures/13_pangenome_clustermap.png)](figures/13_pangenome_clustermap.png)<br>Binary gene-content clustering with a distance metric appropriate for presence–absence data. | **CLR microbiome clustermap**<br>[![CLR microbiome clustermap](figures/14_microbiome_clr_clustermap.png)](figures/14_microbiome_clr_clustermap.png)<br>Zero replacement, centered-log-ratio transformation, and Euclidean distance in CLR space. |

### Guided practice

| Tutorial example | Tutorial example |
|---|---|
| **Annotated QC exercise**<br>[![Annotated sequencing QC practice figure](figures/practice_annotated_qc.png)](figures/practice_annotated_qc.png)<br>A worked practice output for annotation, thresholds, and communicating actionable QC findings. |  |

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

![Reproducible visualization workflow](figures/workflow_diagram.svg)

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

## Portfolio series

- **Seaborn** · [Matplotlib](https://github.com/mbilal-OU/biology-data-viz-matplotlib) · [Plotly](https://github.com/mbilal-OU/Biology-data-viz-plotly)
- [ggplot2](https://github.com/mbilal-OU/Biology-data-viz-ggplot2) · [ggtree + ComplexHeatmap](https://github.com/mbilal-OU/Biology-data-viz-ggtree-complexheatmap) · [Shiny](https://github.com/mbilal-OU/Biology-data-viz-shiny) · [Gnuplot](https://github.com/mbilal-OU/biology-data-viz-gnuplot)

## Citation and license

Citation metadata are provided in [`CITATION.cff`](CITATION.cff). The code is
released under the [MIT License](LICENSE).
