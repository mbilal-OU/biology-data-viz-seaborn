# Plot Gallery

Every figure in this repository, shown next to the exact `bioviz` call
that produced it. All code below is copy-pasteable, and it matches
[`notebooks/seaborn_beginner_guide.ipynb`](../notebooks/seaborn_beginner_guide.ipynb)
exactly, which is executed end-to-end in CI, so these snippets are
guaranteed to run.

```python
import pandas as pd
from bioviz import theme, relational, distributions, categorical, regression, matrix

theme.set_theme()
DATA = "data"
```

---

## 1 · Scatter: Docking Landscape

**Question:** How does ligand lipophilicity (logP) relate to docking
score, per target?

```python
df = pd.read_csv(f"{DATA}/docking_scores.csv")
fig, ax = relational.docking_scatter(df)
```

![Docking scatter](../figures/01_docking_scatter.png)

Each target shows an inverted-U relationship: binding worsens at both
very low and very high lipophilicity, not just one direction.

---

## 2 · Line: Cytokine Time Course

**Question:** Does an anti-IL-6R antibody blunt the IL-6 response to
an LPS challenge?

```python
df = pd.read_csv(f"{DATA}/timecourse_cytokines.csv")
fig, ax = relational.cytokine_timecourse(df)
```

![Cytokine time course](../figures/02_cytokine_timecourse.png)

The antibody-treated arm's peak is damped to roughly half the vehicle
peak, with non-overlapping SD bands near the 4h peak.

---

## 3 · Histogram / ECDF: Variant Allele Frequency

**Question:** Do missense variants show stronger purifying selection
than synonymous or common/benign variants?

```python
df = pd.read_csv(f"{DATA}/variants.csv")
fig, ax = distributions.variant_af_histogram(df)
```

![Variant AF histogram](../figures/03_variant_af_histogram.png)

```python
fig, ax = distributions.variant_af_ecdf(df)
```

![Variant AF ECDF](../figures/03b_variant_af_ecdf.png)

Missense variants sit at the lowest allele frequencies, consistent
with purifying selection; the common/benign class is shifted markedly
toward intermediate-to-high frequency.

---

## 4 · Box / Violin + Swarm: Differential Expression

**Question:** Which genes respond to treatment, in which direction,
and how consistently across replicates?

```python
df = pd.read_csv(f"{DATA}/gene_expression.csv")
fig, ax = categorical.expression_boxplot(df)
```

![Expression boxplot](../figures/04_expression_boxplot.png)

```python
fig, ax = categorical.expression_violin_swarm(df)
```

![Expression violin + swarm](../figures/04b_expression_violin_swarm.png)

`MYC`/`IL6` shift up, `TP53`/`CDKN1A` shift down, and the housekeeping
genes `GAPDH`/`ACTB` show no meaningful change. The swarm overlay
confirms this holds across individual replicates, not just outliers.

---

## 5 · Regression + Nonlinear Fit: Enzyme Kinetics

**Question:** Is a candidate inhibitor competitive or non-competitive?

```python
df = pd.read_csv(f"{DATA}/enzyme_kinetics.csv")
g = regression.enzyme_kinetics_lmplot(df)
```

![Enzyme kinetics lmplot](../figures/05_enzyme_lmplot.png)

```python
fit = regression.fit_michaelis_menten(df)
print(fit)
```

```text
        inhibitor        vmax        km
0     competitive  103.29675  27.482396
1  noncompetitive   54.27754   8.127880
2            none  102.54479   8.591107
```

The fitted parameters make the mechanism unambiguous: `competitive`
raises Km (~3x) with Vmax unchanged; `noncompetitive` halves Vmax with
Km unchanged, textbook signatures of each inhibition type, correctly
recovered from noisy simulated data (`tests/test_bioviz.py` checks
this holds within 15–20% of ground truth on every CI run).

---

## 6 · Heatmap: Metabolite Correlation

**Question:** Do metabolite correlations reflect known pathway
membership (glycolysis / TCA cycle / amino acids)?

```python
df = pd.read_csv(f"{DATA}/metabolites.csv")
fig, ax = matrix.metabolite_corr_heatmap(df)
```

![Metabolite heatmap](../figures/06_metabolite_heatmap.png)

Three clear correlation blocks emerge, matching the three latent
pathway factors used to simulate the data.

---

## 7 · Clustermap: Microbiome Composition

**Question:** Do gut vs. skin samples cluster separately by species
composition?

```python
df = pd.read_csv(f"{DATA}/microbiome_abundance.csv")
g = matrix.microbiome_clustermap(df)
```

![Microbiome clustermap](../figures/07_microbiome_clustermap.png)

Samples cluster into two clean groups matching body site exactly, and
species cluster into gut-dominant vs. skin-dominant taxa, recovering
a known ecological distinction from composition alone.

---

## 8 · Pairplot: Sequencing QC

**Question:** Are there systematic QC artifacts (e.g., low coverage
correlating with high PCR duplication)?

```python
df = pd.read_csv(f"{DATA}/qc_metrics.csv")
g = matrix.qc_pairplot(df)
```

![QC pairplot](../figures/08_qc_pairplot.png)

`coverage_mean` and `duplicates_pct` are clearly negatively
correlated, a common low-input library-prep artifact. No batch
stands out as a systematic outlier.

---

## 9 · Jointplot: Trait Relationships by Clade

**Question:** Does the relationship between two morphological traits
depend on clade?

```python
df = pd.read_csv(f"{DATA}/phylo_traits.csv")
g = matrix.phylo_traits_jointplot(df)
```

![Phylo jointplot](../figures/09_phylo_jointplot.png)

`Clade_B` is fully separated in trait-space with a shallow slope.
`Clade_A` and `Clade_C` share a similar trait-1 range but visibly
different slopes. `Clade_C` rises more steeply per unit of trait 1
than `Clade_A` does. Pooling all three clades into one regression
would blur both distinctions: Clade_B's separate location and
Clade_A/C's different slopes.

---

## 10 · Annotated Heatmap: Pathway Enrichment

**Question:** Which pathways are enriched for up- or
down-regulated genes?

```python
df = pd.read_csv(f"{DATA}/pathway_status_table.csv")
fig, ax = matrix.pathway_status_heatmap(df)
```

![Pathway heatmap](../figures/10_pathway_heatmap.png)

`Apoptosis` is enriched for upregulated genes and `Cell_Cycle` for
downregulated genes, consistent with a treatment that triggers
programmed cell death while halting proliferation.

---

## Bonus · Raw Matplotlib: Annotated QC Scatter

From [`notebooks/matplotlib_practice.ipynb`](../notebooks/matplotlib_practice.ipynb),
showing the Figure/Axes API that every `bioviz` function builds on:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.scatter(df["coverage_mean"], df["duplicates_pct"], alpha=0.5, color="gray")

low_cov = df[df["coverage_mean"] < 30]
ax.scatter(low_cov["coverage_mean"], low_cov["duplicates_pct"], color="crimson", label="coverage < 30x")
ax.axvline(30, color="crimson", linestyle="--", linewidth=1)
ax.legend()
```

![Annotated QC scatter](../figures/practice_annotated_qc.png)

---

**Regenerate every figure above from scratch:**

```bash
python scripts/generate_datasets.py
jupyter nbconvert --to notebook --execute --inplace notebooks/seaborn_beginner_guide.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/matplotlib_practice.ipynb
```
