# Biological Statistics Visualization with Seaborn

[![CI](https://github.com/mbilal-OU/seaborn-biological-statistics/actions/workflows/ci.yml/badge.svg)](https://github.com/mbilal-OU/seaborn-biological-statistics/actions/workflows/ci.yml)
[![Docs](https://github.com/mbilal-OU/seaborn-biological-statistics/actions/workflows/docs.yml/badge.svg)](https://github.com/mbilal-OU/seaborn-biological-statistics/actions/workflows/docs.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-2E7D32)](LICENSE)

A tested portfolio for exploring biological distributions, relationships, and
group structure with Seaborn. Its distinctive role is high-level statistical
graphics from tidy data: semantic mappings, distribution-aware displays,
faceted comparisons, and matrix exploration, backed by reusable functions and
input validation.

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

### Why Seaborn has its own repository

Seaborn is used here for rapid, statistically informed exploration of tidy
biological tables. Matplotlib handles custom geometry, Plotly handles direct
interaction, ggplot2 demonstrates declarative layered graphics, ggtree and
ComplexHeatmap align evolutionary and matrix data, Shiny builds reactive
applications, and Gnuplot supports headless command-line rendering.

## Visual tutorial gallery

These are rendered outputs from the repository, not decorative screenshots.
Click any title or figure to open its tutorial, including the input contract,
exact code, own-data example, interpretation, and scientific limits.

### Relationships, trends, and uncertainty

| Tutorial example | Tutorial example |
|---|---|
| [**Docking-score relationship**](docs/figure-tutorials.md#01-docking-score-relationship)<br>[![Docking scatter plot](figures/01_docking_scatter.png)](docs/figure-tutorials.md#01-docking-score-relationship)<br>Scatter semantics, group encoding, trend estimation, and cautious association language. | [**Cytokine time course**](docs/figure-tutorials.md#02-cytokine-time-course)<br>[![Cytokine time-course plot](figures/02_cytokine_timecourse.png)](docs/figure-tutorials.md#02-cytokine-time-course)<br>Repeated measurements, individual trajectories, summary curves, and explicit variability. |
| [**Enzyme-response regression**](docs/figure-tutorials.md#05-enzyme-response-regression)<br>[![Enzyme regression facets](figures/05_enzyme_lmplot.png)](docs/figure-tutorials.md#05-enzyme-response-regression)<br>Faceted regression for comparing conditions without hiding between-group structure. | [**Trait association with marginals**](docs/figure-tutorials.md#09-trait-association-with-marginals)<br>[![Joint distribution plot](figures/09_phylo_jointplot.png)](docs/figure-tutorials.md#09-trait-association-with-marginals)<br>A joint view of association and marginal distributions, without claiming phylogenetic correction. |

### Distributions and group comparisons

| Tutorial example | Tutorial example |
|---|---|
| [**Variant-frequency histogram**](docs/figure-tutorials.md#03-variant-frequency-histogram)<br>[![Variant allele-frequency histogram](figures/03_variant_af_histogram.png)](docs/figure-tutorials.md#03-variant-frequency-histogram)<br>Binning choices and distribution shape for bounded biological measurements. | [**Variant-frequency ECDF**](docs/figure-tutorials.md#03b-variant-frequency-ecdf)<br>[![Variant allele-frequency ECDF](figures/03b_variant_af_ecdf.png)](docs/figure-tutorials.md#03b-variant-frequency-ecdf)<br>A bin-free companion view that makes thresholds and tail probabilities easy to read. |
| [**Expression box plot**](docs/figure-tutorials.md#04-expression-box-plot)<br>[![Gene-expression box plot](figures/04_expression_boxplot.png)](docs/figure-tutorials.md#04-expression-box-plot)<br>Robust group summaries with medians, quartiles, and outlier visibility. | [**Expression violin and swarm**](docs/figure-tutorials.md#04b-expression-violin-and-swarm)<br>[![Gene-expression violin and swarm plot](figures/04b_expression_violin_swarm.png)](docs/figure-tutorials.md#04b-expression-violin-and-swarm)<br>Distribution shape plus the observed samples, avoiding a summary-only story. |

### Multivariable structure and matrices

| Tutorial example | Tutorial example |
|---|---|
| [**Metabolite heatmap**](docs/figure-tutorials.md#06-metabolite-correlation-heatmap)<br>[![Metabolite heatmap](figures/06_metabolite_heatmap.png)](docs/figure-tutorials.md#06-metabolite-correlation-heatmap)<br>Matrix encoding, centered color scales, annotation, and readable feature comparison. | [**Microbiome clustermap**](docs/figure-tutorials.md#07-microbiome-clustermap)<br>[![Microbiome clustermap](figures/07_microbiome_clustermap.png)](docs/figure-tutorials.md#07-microbiome-clustermap)<br>Exploratory hierarchical structure and the motivation for composition-aware preprocessing. |
| [**Sequencing-QC pairplot**](docs/figure-tutorials.md#08-sequencing-qc-pairplot)<br>[![Sequencing quality-control pairplot](figures/08_qc_pairplot.png)](docs/figure-tutorials.md#08-sequencing-qc-pairplot)<br>Pairwise distributions and correlations for fast multivariable quality control. | [**Pathway count heatmap**](docs/figure-tutorials.md#10-pathway-count-heatmap)<br>[![Pathway count heatmap](figures/10_pathway_heatmap.png)](docs/figure-tutorials.md#10-pathway-count-heatmap)<br>Annotated categorical counts, clearly separated from statistical enrichment claims. |

### Advanced omics case studies

| Tutorial example | Tutorial example |
|---|---|
| [**Differential-expression dashboard**](docs/figure-tutorials.md#11-differential-expression-dashboard)<br>[![Volcano and MA plots](figures/11_differential_expression_dashboard.png)](docs/figure-tutorials.md#11-differential-expression-dashboard)<br>Volcano and MA views with FDR and effect-size thresholds computed from the data. | [**Pangenome population structure**](docs/figure-tutorials.md#12-pangenome-population-structure)<br>[![Pangenome frequency spectrum and PCA](figures/12_pangenome_structure.png)](docs/figure-tutorials.md#12-pangenome-population-structure)<br>Gene-frequency classes and PCA derived from a binary presence-absence matrix. |
| [**Pangenome Jaccard clustermap**](docs/figure-tutorials.md#13-pangenome-jaccard-clustermap)<br>[![Pangenome Jaccard clustermap](figures/13_pangenome_clustermap.png)](docs/figure-tutorials.md#13-pangenome-jaccard-clustermap)<br>Binary gene-content clustering with a distance metric appropriate for presence-absence data. | [**CLR microbiome clustermap**](docs/figure-tutorials.md#14-clr-microbiome-clustermap)<br>[![CLR microbiome clustermap](figures/14_microbiome_clr_clustermap.png)](docs/figure-tutorials.md#14-clr-microbiome-clustermap)<br>Zero replacement, centered-log-ratio transformation, and Euclidean distance in CLR space. |

### Guided practice

| Tutorial example | Tutorial example |
|---|---|
| [**Annotated QC exercise**](docs/figure-tutorials.md#practice-annotated-qc)<br>[![Annotated sequencing QC practice figure](figures/practice_annotated_qc.png)](docs/figure-tutorials.md#practice-annotated-qc)<br>A worked practice output for annotation, thresholds, and communicating actionable QC findings. |  |

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
git clone https://github.com/mbilal-OU/seaborn-biological-statistics.git
cd seaborn-biological-statistics
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
[matplotlib-genomic-figures](https://github.com/mbilal-OU/matplotlib-genomic-figures)
repository.

## Portfolio series

- **Seaborn** · [Matplotlib](https://github.com/mbilal-OU/matplotlib-genomic-figures) · [Plotly](https://github.com/mbilal-OU/plotly-interactive-omics)
- [ggplot2](https://github.com/mbilal-OU/ggplot2-omics-grammar) · [ggtree + ComplexHeatmap](https://github.com/mbilal-OU/ggtree-complexheatmap-phylogenomics) · [Shiny](https://github.com/mbilal-OU/shiny-omics-explorer) · [Gnuplot](https://github.com/mbilal-OU/gnuplot-bioinformatics-cli)

## Citation and license

Citation metadata are provided in [`CITATION.cff`](CITATION.cff). The code is
released under the [MIT License](LICENSE).
