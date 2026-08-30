# %% [markdown]
# # Biology Data Visualization with Seaborn
#
# A hands-on tutorial that teaches core Seaborn plot types using
# simulated but biologically realistic datasets: virtual screening,
# cytokine kinetics, variant allele frequencies, differential
# expression, enzyme kinetics, metabolomics, microbiome composition,
# sequencing QC, and morphological trait data.
#
# Each section follows the same structure:
# 1. **Biological question**: what are we trying to learn from the data?
# 2. **Why this plot type**: the statistical rationale for the choice.
# 3. **Code**: using the reusable `bioviz` package.
# 4. **Interpretation**: what the resulting figure actually shows.
#
# See `data/data_dictionary.md` for full column definitions and the
# simulation model behind each dataset (`scripts/generate_datasets.py`).

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path.cwd().parent))
from bioviz import categorical, distributions, matrix, regression, relational, theme

theme.set_theme()
DATA = Path.cwd().parent / "data"
FIGS = Path.cwd().parent / "figures"
FIGS.mkdir(exist_ok=True)

# %% [markdown]
# ## 1. Scatter plot: Virtual Screening / Molecular Docking
#
# **Biological question:** Across three drug targets, how does ligand
# lipophilicity (logP) relate to predicted binding affinity (Vina
# score)? Are the best-scoring ligands clustered in a particular logP
# range, or is the relationship linear?
#
# **Why a scatter plot:** We have two continuous variables
# (`logP`, `vina_score`) and want to see the *shape* of their
# relationship, including any non-linearity, plus a categorical
# grouping (`target`) and a third continuous variable (`ring_count`)
# encoded as point size.

# %%
df_dock = pd.read_csv(DATA / "docking_scores.csv")
df_dock.head()

# %%
fig, ax = relational.docking_scatter(df_dock)
theme.savefig(fig, FIGS / "01_docking_scatter.png")
plt.show()

# %% [markdown]
# **Interpretation:** Binding score is *not* monotonic in logP: each
# target shows a clear inverted-U pattern, worsening at both very low
# and very high lipophilicity. This is expected: overly hydrophilic
# ligands bind poorly to a typically hydrophobic pocket, while overly
# hydrophobic ligands lose entropic favorability and solubility. `GPCR_C`
# has the best (most negative) scores overall, consistent with its
# lower simulated optimum.

# %% [markdown]
# ## 2. Line plot: Cytokine Time Course
#
# **Biological question:** Does an anti-IL-6R antibody blunt the
# IL-6 response to an inflammatory (LPS) challenge, and if so, at
# which time points does the effect become apparent?
#
# **Why a line plot:** `time_h` is an ordered continuous axis and we
# have repeated measures per subject. A line plot with `errorbar="sd"`
# shows both the mean trajectory and between-subject variability at
# each time point, which a scatter plot would not communicate as clearly.

# %%
df_cyto = pd.read_csv(DATA / "timecourse_cytokines.csv")
fig, ax = relational.cytokine_timecourse(df_cyto)
theme.savefig(fig, FIGS / "02_cytokine_timecourse.png")
plt.show()

# %% [markdown]
# **Interpretation:** Both arms show the expected acute-phase shape:
# rapid rise, peak around 4h, slow decay. The antibody-treated arm's
# peak is visibly damped (~55% of vehicle peak, matching the simulated
# effect size). The SD bands describe between-subject variation; their
# overlap or separation is not a significance test. A mixed-effects model
# with subject as a random effect would be needed for formal inference.

# %% [markdown]
# ## 3. Histogram / KDE / ECDF: Variant Allele Frequency Spectrum
#
# **Biological question:** Do synonymous, missense, and loss-of-function
# variants show increasingly rare allele-frequency spectra, as expected
# when purifying selection is stronger against disruptive changes?
#
# **Why these plots:** A single distribution is best summarized with a
# histogram or KDE. Comparing *distributions* across groups is often
# clearer with an ECDF, since it avoids binning artifacts and makes
# it easy to read off "what fraction of variants are below frequency X."

# %%
df_var = pd.read_csv(DATA / "variants.csv")
fig, ax = distributions.variant_af_histogram(df_var)
theme.savefig(fig, FIGS / "03_variant_af_histogram.png")
plt.show()

# %%
fig, ax = distributions.variant_af_ecdf(df_var)
theme.savefig(fig, FIGS / "03b_variant_af_ecdf.png")
plt.show()

# %%
df_var.groupby("consequence")["allele_frequency"].median().sort_values()

# %% [markdown]
# **Interpretation:** Loss-of-function variants have the lowest median
# allele frequency, missense variants are intermediate, and synonymous
# variants are least strongly shifted toward rare frequencies. This is
# the seeded simulation truth. A real dataset would require demographic,
# ancestry, ascertainment, and annotation effects to be considered.

# %% [markdown]
# ## 4. Box / Violin / Swarm: Differential Gene Expression
#
# **Biological question:** Which genes change expression under
# treatment, in which direction, and how consistent is that change
# across replicates?
#
# **Why these plots:** Boxplots summarize the group comparison
# (median, IQR, outliers) compactly across many genes at once. Violin
# + swarm goes a step further, showing the *shape* of each
# distribution and every individual replicate, useful for catching
# bimodality or outlier-driven effects that a boxplot alone would hide.

# %%
df_expr = pd.read_csv(DATA / "gene_expression.csv")
fig, ax = categorical.expression_boxplot(df_expr)
theme.savefig(fig, FIGS / "04_expression_boxplot.png")
plt.show()

# %%
fig, ax = categorical.expression_violin_swarm(df_expr)
theme.savefig(fig, FIGS / "04b_expression_violin_swarm.png")
plt.show()

# %% [markdown]
# **Interpretation:** `MYC` and `IL6` shift up under treatment,
# `TP53` and `CDKN1A` shift down, while `GAPDH` and `ACTB`, included
# as unchanged reference genes, show negligible change in this simulation.
# The swarm overlay
# confirms these shifts are consistent across replicates rather than
# being driven by one or two outliers.

# %% [markdown]
# ## 5. Regression: Enzyme Kinetics
#
# **Biological question:** Does a candidate inhibitor act
# competitively (raises apparent Km, Vmax unchanged) or
# non-competitively (lowers Vmax, Km unchanged)?
#
# **Why regression:** `lmplot` is useful for visualizing trend +
# uncertainty across groups on a transformed axis. But visual
# inspection alone can't distinguish competitive vs. non-competitive
# inhibition reliably, so we *also* fit the actual Michaelis-Menten
# equation with nonlinear least squares and compare fitted parameters,
# which is the correct way to answer this biological question.

# %%
df_enz = pd.read_csv(DATA / "enzyme_kinetics.csv")
g = regression.enzyme_kinetics_lmplot(df_enz)
theme.savefig(g.figure, FIGS / "05_enzyme_lmplot.png")
plt.show()

# %%
fit = regression.fit_michaelis_menten(df_enz)
fit

# %% [markdown]
# **Interpretation:** The fitted parameters make the mechanism
# unambiguous: the `competitive` condition has Km roughly 3x that of
# `none` while Vmax is essentially unchanged: the textbook signature
# of competitive inhibition. The `noncompetitive` condition instead
# shows Vmax dropping by roughly half with Km unchanged: the textbook
# signature of non-competitive inhibition. This is a case where a
# quantitative model answers a question the plot alone leaves
# ambiguous.

# %% [markdown]
# ## 6. Heatmap: Metabolite Correlation
#
# **Biological question:** Which metabolites co-vary across samples,
# and do those correlations reflect known pathway membership
# (glycolysis, TCA cycle, amino acid pool)?
#
# **Why a heatmap:** With 9 metabolites there are 36 pairwise
# correlations. A heatmap lets us scan all of them at once and spot
# block structure that would be tedious to find in a correlation table.

# %%
df_metab = pd.read_csv(DATA / "metabolites.csv")
fig, ax = matrix.metabolite_corr_heatmap(df_metab)
theme.savefig(fig, FIGS / "06_metabolite_heatmap.png")
plt.show()

# %% [markdown]
# **Interpretation:** Three visible blocks of strong positive
# correlation correspond to the three latent pathway factors used to
# simulate the data: glycolysis (glucose/pyruvate/lactate), TCA cycle
# (citrate/α-ketoglutarate/succinate), and the amino-acid pool
# (glutamine/alanine/serine). Serine shows weaker cross-correlation
# with the glycolytic block, reflecting its partial biosynthetic link
# to glycolysis via 3-phosphoglycerate.

# %% [markdown]
# ## 7. Clustermap: Microbiome Composition
#
# **Biological question:** Do gut and skin microbiome samples cluster
# separately based on species composition, and which taxa drive that
# separation?
#
# **Why a clustermap:** Hierarchical clustering on top of the heatmap
# automatically groups similar samples and similar species, revealing
# structure (like body-site separation) without needing to specify it
# in advance.

# %%
df_micro = pd.read_csv(DATA / "microbiome_abundance.csv")
g = matrix.microbiome_clustermap(df_micro)
theme.savefig(g.figure, FIGS / "07_microbiome_clustermap.png")
plt.show()

# %% [markdown]
# **Interpretation:** Samples cluster into two clean groups that
# correspond exactly to body site, and the species dendrogram
# separates gut-dominant taxa (*Bacteroides*, *Faecalibacterium*,
# *Prevotella*) from skin-dominant taxa (*Staphylococcus*,
# *Cutibacterium*, *Corynebacterium*), recovering the known ecological
# distinction between these two niches from composition data alone.

# %% [markdown]
# ## 8. Pairplot: Sequencing QC Metrics
#
# **Biological question:** Are there systematic relationships between
# QC metrics (e.g., do low-coverage samples also show more PCR
# duplication?), and do any batches look like outliers?
#
# **Why a pairplot:** With 4 QC metrics, a pairplot shows every
# pairwise scatter plus each metric's marginal distribution in a
# single figure, the fastest way to screen a QC table for problems.

# %%
df_qc = pd.read_csv(DATA / "qc_metrics.csv")
g = matrix.qc_pairplot(df_qc)
theme.savefig(g.figure, FIGS / "08_qc_pairplot.png")
plt.show()

# %%
df_qc[["coverage_mean", "duplicates_pct"]].corr()

# %% [markdown]
# **Interpretation:** `coverage_mean` and `duplicates_pct` are clearly
# negatively correlated: samples with lower coverage tend to show
# higher PCR duplication, a common artifact of low-input library
# preparation. `q30_pct` tracks the same latent "input quality" factor.
# No batch stands out as a systematic outlier, which is reassuring for
# downstream batch-correction decisions.

# %% [markdown]
# ## 9. Jointplot: Trait-Trait Relationships by Clade
#
# **Biological question:** Is the relationship between two
# morphological traits consistent across clades, or does it depend on
# which clade a sample belongs to (a Simpson's-paradox-style scenario)?
#
# **Why a jointplot:** It combines the bivariate relationship with
# each trait's marginal distribution, and `hue="clade"` with
# `kind="kde"` lets us compare both the *slope* and the *location* of
# each clade's trait distribution simultaneously.

# %%
df_phylo = pd.read_csv(DATA / "phylo_traits.csv")
g = matrix.phylo_traits_jointplot(df_phylo)
theme.savefig(g.figure, FIGS / "09_phylo_jointplot.png")
plt.show()

# %% [markdown]
# **Interpretation:** Each clade occupies a distinct region of
# trait-space with its own trait1–trait2 slope. Notably, if you ignored
# clade membership and fit a single pooled regression, the estimated
# slope would be a poor summary of any individual clade's true
# relationship, a reminder that phylogenetic (or any grouped)
# structure should be modeled explicitly rather than pooled naively. This
# visualization stratifies by clade; it is not a phylogenetic comparative
# model and does not correct for shared ancestry within clades.

# %% [markdown]
# ## 10. Annotated Heatmap: Pathway Status Counts
#
# **Biological question:** How many upregulated, downregulated, and
# unchanged genes were assigned to each pathway?
#
# **Why an annotated heatmap:** With counts this small, showing the
# actual numbers on the heatmap (not just color) lets a reader verify
# the descriptive pattern directly instead of trusting color intensity.

# %%
df_path = pd.read_csv(DATA / "pathway_status_table.csv")
fig, ax = matrix.pathway_status_heatmap(df_path)
theme.savefig(fig, FIGS / "10_pathway_heatmap.png")
plt.show()

# %% [markdown]
# **Interpretation:** `Apoptosis` has the largest upregulated count and
# `Cell_Cycle` the largest downregulated count in the simulated table.
# Calling these pathways enriched would require a background gene universe,
# an enrichment test, and multiple-testing correction, none of which is
# encoded in this descriptive figure.

# %% [markdown]
# ## Summary
#
# | # | Plot type | Dataset | Biological question answered |
# |---|-----------|---------|-------------------------------|
# | 1 | Scatter | docking_scores | logP vs. binding affinity per target |
# | 2 | Line | timecourse_cytokines | Treatment effect on IL-6 kinetics |
# | 3 | Histogram/ECDF | variants | Selection pressure by consequence class |
# | 4 | Box/Violin/Swarm | gene_expression | Which genes respond to treatment |
# | 5 | Regression + curve fit | enzyme_kinetics | Inhibition mechanism (competitive vs. not) |
# | 6 | Heatmap | metabolites | Pathway-driven metabolite co-variation |
# | 7 | Clustermap | microbiome_abundance | Body-site-driven community clustering |
# | 8 | Pairplot | qc_metrics | QC artifact detection across a sample batch |
# | 9 | Jointplot | phylo_traits | Clade-specific trait relationships |
# | 10 | Annotated heatmap | pathway_status_table | Pathway status counts |
#
# Next steps: see `CONTRIBUTING.md` to add a new dataset + plot pair,
# or explore `bioviz/` directly to reuse these functions in your own
# analysis.
