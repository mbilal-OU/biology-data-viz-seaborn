# biology-data-viz-seaborn

[![CI](https://github.com/mbilal-OU/biology-data-viz-seaborn/actions/workflows/ci.yml/badge.svg)](https://github.com/mbilal-OU/biology-data-viz-seaborn/actions/workflows/ci.yml)
[![Docs](https://github.com/mbilal-OU/biology-data-viz-seaborn/actions/workflows/docs.yml/badge.svg)](https://github.com/mbilal-OU/biology-data-viz-seaborn/actions/workflows/docs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)
[![Seaborn](https://img.shields.io/badge/seaborn-%E2%89%A50.13-informational)](https://seaborn.pydata.org)

**biology-data-viz-seaborn** is a tested Seaborn tutorial and reusable
plotting toolkit, built entirely on biologically realistic simulated
datasets.
> **From a seeded simulation, to a tested plotting package, to a narrative notebook, to publication-ready figures, all checked in CI.**

![Pipeline](figures/workflow_diagram.svg)

**Jump to:** [Full tutorial (every plot, explained)](#full-tutorial-every-plot-explained) · [Quick start](#quick-start) · [Repository structure](#repository-structure) · [Reproducibility](#reproducibility)

---

## At a glance

This repo is the learning layer for biology and bioinformatics
visualization with Seaborn. It provides simulated data with real
statistical structure, a small tested package to plot it, and, below,
a full walkthrough of all 10 plot types where each one gets its own
explanation, biological question, code, result, and instructions for
using it on your own data.

| You provide | This repo returns |
|---|---|
| nothing, just clone it | 10 simulated datasets with documented biological rationale |
| `python scripts/generate_datasets.py` | byte-identical, reproducible CSVs (seeded) |
| a dataset from `data/` | a tested `bioviz` function that plots it correctly-styled |
| the tutorial below (or the notebook) | biological question, why this plot, code, interpretation, and how to reuse it, for 10 plot types |
| `pytest tests/` | rendering checks and statistical sanity checks against known ground truth |

It deliberately stays a **teaching and reference toolkit**. It doesn't
try to be a general-purpose visualization library or handle your own
raw data ingestion. Each tutorial section below tells you exactly what
column structure you need to point it at your own DataFrame.

---

## Quick start

```bash
git clone https://github.com/mbilal-OU/biology-data-viz-seaborn.git
cd biology-data-viz-seaborn

python -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt
pip install -e .
```

```bash
jupyter notebook notebooks/seaborn_beginner_guide.ipynb
```

Conda users: `conda env create -f environment.yml && conda activate bioviz-seaborn`.

---

## Full Tutorial: Every Plot, Explained

For each plot below: what the plot type is for, the biological question it answers here, the exact code that produces it, an interpretation of the actual result, and what you'd need to use it on your own data. This mirrors `notebooks/seaborn_beginner_guide.ipynb` exactly. Every snippet below is executed end-to-end in CI on every push.

```python
import pandas as pd
from bioviz import theme, relational, distributions, categorical, regression, matrix

theme.set_theme()
```

---

### 1. Scatter Plot: Docking Landscape

**Plot type:** Scatter plot

**What this plot type is for:** A scatter plot maps two continuous variables to x/y position. It's the right choice when you want to see the *shape* of a relationship (linear, non-linear, clustered) rather than just a summary statistic. Here, point size and color add two more variables (`ring_count`, `target`) without needing a third axis.

**Biological question:** Across three drug targets, how does ligand lipophilicity (logP) relate to predicted binding affinity (Vina score)? Are the best-scoring ligands clustered in a particular logP range?

**Dataset:** `data/docking_scores.csv`. 360 rows. Simulated virtual-screening results against 3 protein targets.

**Create this figure:**

```python
df = pd.read_csv("data/docking_scores.csv")
fig, ax = relational.docking_scatter(df)
```

![Scatter Plot: Docking Landscape](figures/01_docking_scatter.png)

**Interpretation:** Binding score is **not** monotonic in logP: each target shows a clear inverted-U pattern, worsening at both very low and very high lipophilicity. This matches known medicinal-chemistry behavior: overly hydrophilic ligands bind poorly to a typically hydrophobic pocket, while overly hydrophobic ligands lose entropic favorability and solubility. `GPCR_C` shows the best (most negative) scores overall.

**Requirements to use this on your own data:**

- one continuous x variable (a numeric column)
- one continuous y variable (a numeric column)
- optionally: a categorical column for `hue`, a numeric column for `size`

**Adapted code for your own DataFrame:**

```python
import seaborn as sns

sns.scatterplot(
    data=my_df, x="your_x_column", y="your_y_column",
    hue="your_group_column", size="your_size_column",
)
```

---

### 2. Line Plot: Cytokine Time Course

**Plot type:** Line plot

**What this plot type is for:** A line plot connects ordered observations, and with `errorbar="sd"` it also draws a shaded band showing spread at each point. Use it whenever the x-axis is naturally ordered (time, dose, distance) and you have repeated measurements at each x value; a scatter plot alone would hide the trend and the variability together.

**Biological question:** Does an anti-IL-6R antibody blunt the IL-6 response to an inflammatory (LPS) challenge, and at which time points does the effect become visible?

**Dataset:** `data/timecourse_cytokines.csv`. 140 rows. IL-6 concentration over 24h, vehicle vs. antibody, 10 subjects/arm.

**Create this figure:**

```python
df = pd.read_csv("data/timecourse_cytokines.csv")
fig, ax = relational.cytokine_timecourse(df)
```

![Line Plot: Cytokine Time Course](figures/02_cytokine_timecourse.png)

**Interpretation:** Both arms show the expected acute-phase shape: rapid rise, peak around 4h, slow decay. The antibody-treated arm's peak is visibly damped to roughly half the vehicle peak, and the SD bands don't overlap near the peak, suggestive of a real effect, though a formal mixed-effects model would be needed to confirm significance.

**Requirements to use this on your own data:**

- one ordered x variable (time, dose, etc.)
- one continuous y variable
- a categorical `hue` column to compare groups/arms
- multiple observations per x value per group, so `errorbar` has something to summarize

**Adapted code for your own DataFrame:**

```python
sns.lineplot(
    data=my_df, x="time_column", y="measurement_column",
    hue="group_column", errorbar="sd", marker="o",
)
```

---

### 3. Histogram & ECDF: Variant Allele Frequency

**Plot type:** Histogram / ECDF

**What this plot type is for:** A histogram (or KDE) shows the shape of a single distribution. An ECDF (empirical cumulative distribution function) shows the same information without binning artifacts, and makes it trivial to read off "what fraction of the data is below X", which is often the more useful question when comparing distributions across groups.

**Biological question:** Do missense variants show a different allele-frequency distribution than synonymous or common/benign variants, consistent with stronger purifying selection?

**Dataset:** `data/variants.csv`. 2000 rows. Simulated variant calls with functional consequence and allele frequency.

**Create this figure:**

```python
df = pd.read_csv("data/variants.csv")
fig, ax = distributions.variant_af_histogram(df)

# same data, cumulative view:
fig, ax = distributions.variant_af_ecdf(df)
```

![Histogram & ECDF: Variant Allele Frequency](figures/03_variant_af_histogram.png)

![Histogram & ECDF: Variant Allele Frequency (2)](figures/03b_variant_af_ecdf.png)

**Interpretation:** Missense variants have the lowest median allele frequency, synonymous variants sit in between, and the common/benign class is shifted markedly toward intermediate-to-high frequency. The ECDF makes the rightward shift of the common/benign curve especially easy to see: a larger fraction of those variants sit at higher frequency at every point along the curve.

**Requirements to use this on your own data:**

- one continuous numeric column to plot the distribution of
- optionally: a categorical `hue` column to compare distributions across groups

**Adapted code for your own DataFrame:**

```python
sns.histplot(data=my_df, x="value_column", hue="group_column", element="step", stat="density")
sns.ecdfplot(data=my_df, x="value_column", hue="group_column")
```

---

### 4. Box / Violin / Swarm: Differential Gene Expression

**Plot type:** Box / Violin / Swarm

**What this plot type is for:** Boxplots summarize a group comparison compactly (median, IQR, outliers), good for scanning many groups at once. Violin + swarm goes further, showing the full distribution shape plus every individual data point, which catches bimodality or outlier-driven effects a boxplot alone would hide.

**Biological question:** Which genes change expression under treatment, in which direction, and how consistent is that change across replicates?

**Dataset:** `data/gene_expression.csv`. 180 rows. Log2 expression for 6 genes, control vs. treatment, 15 replicates each.

**Create this figure:**

```python
df = pd.read_csv("data/gene_expression.csv")
fig, ax = categorical.expression_boxplot(df)

# distribution shape + every replicate:
fig, ax = categorical.expression_violin_swarm(df)
```

![Box / Violin / Swarm: Differential Gene Expression](figures/04_expression_boxplot.png)

![Box / Violin / Swarm: Differential Gene Expression (2)](figures/04b_expression_violin_swarm.png)

**Interpretation:** `MYC` and `IL6` shift up under treatment, `TP53` and `CDKN1A` shift down, while the housekeeping genes `GAPDH` and `ACTB` show negligible change, as expected of genes that shouldn't respond to this treatment. The swarm overlay confirms these shifts hold across replicates rather than being driven by one or two outliers.

**Requirements to use this on your own data:**

- one categorical x column (the groups being compared, e.g. gene or condition)
- one continuous y column (the measurement)
- optionally: a second categorical `hue` column for a grouped/split comparison

**Adapted code for your own DataFrame:**

```python
sns.boxplot(data=my_df, x="group_column", y="value_column", hue="condition_column")
sns.violinplot(data=my_df, x="group_column", y="value_column", hue="condition_column", split=True)
```

---

### 5. Regression & Nonlinear Curve Fitting: Enzyme Kinetics

**Plot type:** Regression (lmplot) + SciPy curve_fit

**What this plot type is for:** `lmplot` visualizes a trend with uncertainty across groups. useful for a first look. But some biological questions need an actual mechanistic model, not just a trend line: here we also fit the real Michaelis-Menten equation with nonlinear least squares (`scipy.optimize.curve_fit`) and compare the fitted parameters directly, since visual inspection alone can't reliably distinguish inhibition mechanisms.

**Biological question:** Does a candidate inhibitor act competitively (raises apparent Km, Vmax unchanged) or non-competitively (lowers Vmax, Km unchanged)?

**Dataset:** `data/enzyme_kinetics.csv`. 96 rows. Michaelis-Menten kinetics under no inhibitor / competitive / non-competitive inhibitor, 4 replicates each.

**Create this figure:**

```python
df = pd.read_csv("data/enzyme_kinetics.csv")
g = regression.enzyme_kinetics_lmplot(df)

fit = regression.fit_michaelis_menten(df)
print(fit)
```

```text
        inhibitor        vmax        km
0     competitive  103.29675  27.482396
1  noncompetitive   54.27754   8.127880
2            none  102.54479   8.591107
```

![Regression & Nonlinear Curve Fitting: Enzyme Kinetics](figures/05_enzyme_lmplot.png)

**Interpretation:** The fitted parameters make the mechanism unambiguous: `competitive` raises Km roughly 3x with Vmax essentially unchanged; `noncompetitive` halves Vmax with Km unchanged, textbook signatures of each inhibition type, correctly recovered from noisy simulated data. `tests/test_bioviz.py` checks this holds within 15–20% of ground truth on every CI run, so a future bug in the fitting code would fail the build, not just look slightly off in a plot.

**Requirements to use this on your own data:**

- one x column representing a dose/concentration/independent variable
- one y column representing the response
- optionally: a categorical `hue` column for the lmplot comparison
- for a real curve fit: choose (or write) a model function matching your system's known kinetics, don't default to a linear fit if the underlying process is nonlinear

**Adapted code for your own DataFrame:**

```python
from scipy.optimize import curve_fit

def my_model(x, param1, param2):
    return ...  # your mechanistic equation

popt, pcov = curve_fit(my_model, my_df["x_column"], my_df["y_column"])
```

---

### 6. Heatmap: Metabolite Correlation

**Plot type:** Annotated correlation heatmap

**What this plot type is for:** A heatmap color-codes a matrix of values, most commonly a correlation matrix. With `annot=True` it also prints the numeric value in each cell, so a reader can verify a pattern directly instead of trusting color intensity alone. It's the fastest way to scan many pairwise relationships at once.

**Biological question:** Which metabolites co-vary across samples, and do those correlations reflect known pathway membership (glycolysis, TCA cycle, amino-acid pool)?

**Dataset:** `data/metabolites.csv`. 60 rows. Targeted metabolomics panel, 9 metabolites drawn from 3 correlated latent pathway factors.

**Create this figure:**

```python
df = pd.read_csv("data/metabolites.csv")
fig, ax = matrix.metabolite_corr_heatmap(df)
```

![Heatmap: Metabolite Correlation](figures/06_metabolite_heatmap.png)

**Interpretation:** Three clear correlation blocks emerge: glycolysis (glucose/pyruvate/lactate), TCA cycle (citrate/α-ketoglutarate/succinate), and the amino-acid pool (glutamine/alanine/serine), matching the three latent pathway factors used to simulate the data. Serine shows weaker cross-correlation with the glycolytic block, reflecting its partial biosynthetic link via 3-phosphoglycerate.

**Requirements to use this on your own data:**

- a wide-format table: one row per sample, one column per numeric variable
- drop or exclude any ID columns before calling `.corr()`

**Adapted code for your own DataFrame:**

```python
numeric = my_df.drop(columns=["sample_id"])
sns.heatmap(numeric.corr(), cmap="vlag", center=0, annot=True, fmt=".2f")
```

---

### 7. Clustermap: Microbiome Composition

**Plot type:** Clustermap

**What this plot type is for:** A clustermap is a heatmap with hierarchical clustering applied to both rows and columns, so similar samples and similar variables are grouped together automatically, revealing structure (like a natural split into subgroups) without you having to specify it in advance.

**Biological question:** Do gut and skin microbiome samples cluster separately based on species composition, and which taxa drive that separation?

**Dataset:** `data/microbiome_abundance.csv`. 288 rows in long format: 12 species x 24 samples (12 gut, 12 skin), relative abundance.

**Create this figure:**

```python
df = pd.read_csv("data/microbiome_abundance.csv")
g = matrix.microbiome_clustermap(df)
```

![Clustermap: Microbiome Composition](figures/07_microbiome_clustermap.png)

**Interpretation:** Samples cluster into two clean groups that correspond exactly to body site, and the species dendrogram separates gut-dominant taxa (*Bacteroides*, *Faecalibacterium*, *Prevotella*) from skin-dominant taxa (*Staphylococcus*, *Cutibacterium*, *Corynebacterium*), recovering the known ecological distinction between these two niches from composition data alone.

**Requirements to use this on your own data:**

- long-format data with a sample column, a variable/feature column, and a value column
- pivot to wide format first (`pivot_table`): rows = features, columns = samples

**Adapted code for your own DataFrame:**

```python
piv = my_df.pivot_table(
    index="feature_column", columns="sample_column",
    values="value_column", fill_value=0,
)
sns.clustermap(piv, cmap="mako", z_score=0)
```

---

### 8. Pairplot: Sequencing QC Metrics

**Plot type:** Pairplot

**What this plot type is for:** A pairplot draws every pairwise scatter plot between a set of numeric columns, plus each column's marginal distribution on the diagonal, the fastest way to screen a QC table for artifacts or outliers across many metrics at once.

**Biological question:** Are there systematic relationships between QC metrics, for instance, do low-coverage samples also show more PCR duplication, and do any batches look like outliers?

**Dataset:** `data/qc_metrics.csv`. 96 rows. Per-sample sequencing QC for a 96-sample batch across 3 sub-batches.

**Create this figure:**

```python
df = pd.read_csv("data/qc_metrics.csv")
g = matrix.qc_pairplot(df)
```

![Pairplot: Sequencing QC Metrics](figures/08_qc_pairplot.png)

**Interpretation:** `coverage_mean` and `duplicates_pct` are clearly negatively correlated: samples with lower coverage tend to show higher PCR duplication, a common artifact of low-input library preparation. `q30_pct` tracks the same latent "input quality" factor. No batch stands out as a systematic outlier.

**Requirements to use this on your own data:**

- several numeric columns to compare pairwise (3–6 is usually the readable range)
- optionally: a categorical `hue` column to color points by group

**Adapted code for your own DataFrame:**

```python
sns.pairplot(
    my_df, vars=["metric_1", "metric_2", "metric_3"],
    hue="group_column", diag_kind="kde",
)
```

---

### 9. Jointplot: Trait Relationships by Clade

**Plot type:** Jointplot (KDE)

**What this plot type is for:** A jointplot combines a bivariate relationship with each variable's marginal distribution. With `kind="kde"` and `hue`, it compares both the *shape/slope* of a relationship and the *location* of each group's distribution simultaneously, useful for spotting Simpson's-paradox-style situations where a pooled trend would misrepresent every individual group.

**Biological question:** Is the relationship between two morphological traits consistent across clades, or does it depend on which clade a sample belongs to?

**Dataset:** `data/phylo_traits.csv`. 120 rows. Two continuous traits across 3 clades, each with its own allometric slope.

**Create this figure:**

```python
df = pd.read_csv("data/phylo_traits.csv")
g = matrix.phylo_traits_jointplot(df)
```

![Jointplot: Trait Relationships by Clade](figures/09_phylo_jointplot.png)

**Interpretation:** `Clade_B` is fully separated in trait-space with a shallow slope. `Clade_A` and `Clade_C` share a similar trait-1 range but visibly different slopes. `Clade_C` rises more steeply per unit of trait 1 than `Clade_A` does. Pooling all three clades into a single regression would blur both distinctions: it would average away Clade_B's separate location and Clade_A/C's different slopes, misrepresenting every individual clade's true relationship.

**Requirements to use this on your own data:**

- two continuous columns (x and y)
- optionally: a categorical `hue` column to compare across groups
- if the legend overlaps your data, move it: `sns.move_legend(g.ax_joint, "upper left", bbox_to_anchor=(1.15, 1.2))`

**Adapted code for your own DataFrame:**

```python
g = sns.jointplot(data=my_df, x="trait_x", y="trait_y", hue="group_column", kind="kde", fill=True)
sns.move_legend(g.ax_joint, "upper left", bbox_to_anchor=(1.15, 1.2))
```

---

### 10. Annotated Heatmap: Pathway Enrichment

**Plot type:** Annotated integer heatmap

**What this plot type is for:** The same annotated-heatmap technique as #6, applied to count data instead of correlations, useful whenever you have a small contingency-style table and want the reader to be able to verify the pattern from the printed numbers, not just color.

**Biological question:** Which biological pathways show a significant excess of up- or down-regulated genes, meaning which pathways are enriched in a differential expression result?

**Dataset:** `data/pathway_status_table.csv`. 6 rows. Gene counts per pathway × functional status, from a mock enrichment analysis.

**Create this figure:**

```python
df = pd.read_csv("data/pathway_status_table.csv")
fig, ax = matrix.pathway_status_heatmap(df)
```

![Annotated Heatmap: Pathway Enrichment](figures/10_pathway_heatmap.png)

**Interpretation:** `Apoptosis` shows a clear excess of upregulated genes and `Cell_Cycle` a clear excess of downregulated genes relative to the other categories, consistent with a treatment that triggers programmed cell death while halting proliferation (e.g. a genotoxic or cell-cycle-arresting agent). `Immune_Response` also shows mild upregulation enrichment.

**Requirements to use this on your own data:**

- a table already shaped as rows × categories (a contingency table), with an index column to set as row labels

**Adapted code for your own DataFrame:**

```python
indexed = my_df.set_index("row_label_column")
sns.heatmap(indexed, annot=True, fmt="d", cmap="crest")
```

---

### Bonus. Raw Matplotlib: Annotated QC Scatter

**Plot type:** Matplotlib Figure/Axes API

**What this plot type is for:** Every Seaborn function returns real Matplotlib `Figure`/`Axes` objects. This bonus example (from `notebooks/matplotlib_practice.ipynb`) shows the raw API underneath, useful when you need custom annotations, flagged points, or manual multi-panel layouts that Seaborn doesn't expose directly.

**Biological question:** Which specific samples fail a QC coverage threshold, and can they be flagged directly on the plot for a lab notebook or report?

**Dataset:** `data/qc_metrics.csv`. Same QC dataset as #8, viewed through raw Matplotlib instead of Seaborn.

**Create this figure:**

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.scatter(df["coverage_mean"], df["duplicates_pct"], alpha=0.5, color="gray")

low_cov = df[df["coverage_mean"] < 30]
ax.scatter(low_cov["coverage_mean"], low_cov["duplicates_pct"], color="crimson", label="coverage < 30x")
ax.axvline(30, color="crimson", linestyle="--", linewidth=1)
ax.legend()
```

![Raw Matplotlib: Annotated QC Scatter](figures/practice_annotated_qc.png)

**Interpretation:** A handful of samples fall below the 30x coverage threshold and are flagged in red directly on the plot. This pattern (compute a subset, plot it again in a different color on the same Axes) is the general recipe for highlighting outliers or QC failures in any Matplotlib/Seaborn figure.

**Requirements to use this on your own data:**

- any DataFrame; this technique layers on top of any scatter/line plot
- a boolean filter defining the subset you want to highlight

**Adapted code for your own DataFrame:**

```python
fig, ax = plt.subplots()
ax.scatter(my_df["x"], my_df["y"], alpha=0.5, color="gray")
flagged = my_df[my_df["x"] < threshold]
ax.scatter(flagged["x"], flagged["y"], color="crimson", label="flagged")
ax.legend()
```

---


## Using `bioviz` on your own data: general pattern

Every example above follows the same shape: read your CSV, call one
`bioviz` function, get back a styled `Figure`/`Axes`. To adapt any of
them:

```python
import pandas as pd
from bioviz import theme, matrix   # or relational / distributions / categorical / regression

theme.set_theme()

my_df = pd.read_csv("your_data.csv")
fig, ax = matrix.metabolite_corr_heatmap(my_df)   # works on any wide numeric table
fig.savefig("my_figure.png", dpi=300, bbox_inches="tight")
```

If your columns don't match the exact names `bioviz` expects, either
rename them (`my_df.rename(columns={...})`) before calling the
function, or use the "adapted code" snippet under each plot above,
which shows the raw Seaborn call with placeholder column names you can
swap in directly.

---

## Repository structure

```
biology-data-viz-seaborn/
├── bioviz/                      # Reusable, tested plotting package
│   ├── theme.py                 #   consistent styling
│   ├── relational.py            #   scatter, line
│   ├── distributions.py         #   histogram, KDE, ECDF
│   ├── categorical.py           #   box, violin, swarm
│   ├── regression.py            #   lmplot + Michaelis-Menten curve fitting
│   └── matrix.py                #   heatmap, clustermap, pairplot, jointplot
├── data/
│   ├── *.csv                    # 10 simulated datasets
│   └── data_dictionary.md       # column definitions and simulation rationale
├── scripts/
│   ├── generate_datasets.py         # deterministic (seeded) data generation, with rationale docstrings
│   └── _build_readme_gallery.py     # generates the tutorial section of this README
├── notebooks/
│   ├── seaborn_beginner_guide.py    # tutorial, authored as a Jupytext script
│   ├── seaborn_beginner_guide.ipynb # executed notebook (source of truth for output)
│   └── matplotlib_practice.ipynb    # supplementary raw-Matplotlib warm-up
├── figures/                     # publication-quality exported figures (300 DPI) and workflow_diagram.svg
├── docs/
│   ├── index.md                 # docs home
│   └── gallery.md               # mirror of the tutorial below, as a standalone page
├── tests/
│   └── test_bioviz.py           # rendering smoke tests and statistical sanity checks
├── seaborn_templates.py         # minimal copy-paste reference (no bioviz dependency)
├── .github/workflows/
│   ├── ci.yml                   # lint, determinism check, tests, notebook execution
│   └── docs.yml                 # mkdocs build check
├── requirements.txt / environment.yml / pyproject.toml / mkdocs.yml
├── CHANGELOG.md / CONTRIBUTING.md / CITATION.cff / LICENSE (MIT)
```

---

## Scope and guardrails

**This repo does:**
- simulate every dataset deterministically, with a documented
  biological and statistical rationale, not arbitrary numbers;
- ship plotting code as a tested, importable package rather than
  copy-paste notebook cells;
- verify quantitative claims against the data's actual ground truth
  (for example, a curve fit that correctly distinguishes inhibition
  mechanisms), not just that a plot renders;
- re-execute the tutorial notebooks in CI on every push, so committed
  output always matches the code;
- tell you exactly what column structure each plot needs so you can
  point it at your own data.

**This repo does not:**
- ingest or validate real experimental data on your behalf. Data
  cleaning is out of scope; bring your own tidy DataFrame;
- attempt to be a general-purpose visualization library. `bioviz`
  functions are intentionally specific to the tutorial's biological
  scenarios, meant as a template to adapt, not a black box;
- cover 3D visualization, interactive/Plotly-based dashboards, or
  genome-browser-style tracks. This is a Seaborn/Matplotlib-focused
  static-figure tutorial.

---

## Reproducibility

- All data is generated deterministically (`np.random.default_rng(42)`);
  `python scripts/generate_datasets.py` regenerates byte-identical CSVs.
- CI regenerates the datasets on every push and diffs them against
  what's committed, so a silent nondeterminism bug fails the build.
- `pytest tests/ -v` runs 20 tests: rendering smoke tests for every
  plot function, plus statistical sanity checks (fitted parameters
  recover simulation ground truth, correlation signs match the
  simulated structure, distribution orderings hold).
- Both notebooks are executed end-to-end in CI (`ExecutePreprocessor`,
  180s timeout), so a broken cell fails the build, not just a local run.

```bash
pytest tests/ -v
```

---

## 8-week self-study roadmap

| Week | Focus |
|---|---|
| 1 | Scatter and line plots (relational) |
| 2 | Histograms, KDE, ECDF (distributions) |
| 3 | Box, violin, swarm (categorical) |
| 4 | Regression and nonlinear curve fitting |
| 5 | Heatmaps |
| 6 | Clustermaps |
| 7 | Pairplots and jointplots |
| 8 | Combine plots into a multi-panel figure; add a new dataset (see `CONTRIBUTING.md`) |

---

## Documentation

- [Documentation home](docs/index.md)
- [Plot gallery (standalone page)](docs/gallery.md)
- [Data dictionary](data/data_dictionary.md)
- [Changelog](CHANGELOG.md)

## Contributing

New datasets, plot types, and clearer explanations are welcome. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for dataset-generation conventions,
test requirements, and how to re-execute the notebooks before a PR.

## Citation

Citation metadata is in [`CITATION.cff`](CITATION.cff). GitHub renders
a "Cite this repository" button automatically.

## License

[MIT](LICENSE)

## Tags

`seaborn` · `python` · `bioinformatics` · `biology` · `data-visualization` · `matplotlib` · `omics` · `tutorial` · `reproducible-research`
