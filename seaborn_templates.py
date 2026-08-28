"""
seaborn_templates.py
=====================
Quick copy-paste reference for every plot type covered in this
repository. Each snippet is intentionally minimal and self-contained;
for the documented, tested, reusable versions of these plots, use the
`bioviz` package instead (see notebooks/seaborn_beginner_guide.ipynb
for full explanations and interpretation).

Run this file directly to regenerate all 10 core figures into figures/.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(context="notebook", style="whitegrid", palette="Set2")

# 1. Scatter plot ------------------------------------------------------------
df = pd.read_csv("data/docking_scores.csv")
sns.scatterplot(data=df, x="logP", y="vina_score", hue="target", size="ring_count")
plt.title("Docking Landscape")
plt.savefig("figures/tpl_01_scatter.png", dpi=200, bbox_inches="tight")
plt.close()

# 2. Line plot ----------------------------------------------------------------
df = pd.read_csv("data/timecourse_cytokines.csv")
sns.lineplot(data=df, x="time_h", y="IL6", hue="treatment", errorbar="sd")
plt.title("IL-6 Cytokine Levels Over Time")
plt.savefig("figures/tpl_02_lineplot.png", dpi=200, bbox_inches="tight")
plt.close()

# 3. Histogram / KDE / ECDF ---------------------------------------------------
df = pd.read_csv("data/variants.csv")
sns.histplot(data=df, x="allele_frequency", hue="consequence", element="step", stat="density")
plt.title("Variant Allele Frequencies")
plt.savefig("figures/tpl_03_histogram.png", dpi=200, bbox_inches="tight")
plt.close()

# 4. Box / Violin / Swarm ------------------------------------------------------
df = pd.read_csv("data/gene_expression.csv")
sns.boxplot(data=df, x="gene", y="expression", hue="condition")
plt.title("Gene Expression Across Conditions")
plt.savefig("figures/tpl_04_boxplot.png", dpi=200, bbox_inches="tight")
plt.close()

# 5. Regression (lmplot) -------------------------------------------------------
df = pd.read_csv("data/enzyme_kinetics.csv")
g = sns.lmplot(data=df, x="substrate_conc", y="rate", hue="inhibitor", order=2)
g.savefig("figures/tpl_05_lmplot.png", dpi=200, bbox_inches="tight")
plt.close("all")

# 6. Heatmap --------------------------------------------------------------------
df = pd.read_csv("data/metabolites.csv").drop(columns=["sample_id"])
sns.heatmap(df.corr(), cmap="vlag", center=0, annot=True)
plt.title("Metabolite Correlations")
plt.savefig("figures/tpl_06_heatmap.png", dpi=200, bbox_inches="tight")
plt.close()

# 7. Clustermap -------------------------------------------------------------------
df = pd.read_csv("data/microbiome_abundance.csv")
piv = df.pivot_table(index="species", columns="sample", values="relative_abundance", fill_value=0)
g = sns.clustermap(piv, cmap="mako", z_score=0, figsize=(8, 8))
g.savefig("figures/tpl_07_clustermap.png", dpi=200, bbox_inches="tight")
plt.close("all")

# 8. Pairplot -----------------------------------------------------------------------
df = pd.read_csv("data/qc_metrics.csv")
g = sns.pairplot(df, vars=["duplicates_pct", "coverage_mean", "gc_content", "q30_pct"], hue="batch")
g.savefig("figures/tpl_08_pairplot.png", dpi=200, bbox_inches="tight")
plt.close("all")

# 9. Jointplot -----------------------------------------------------------------------
df = pd.read_csv("data/phylo_traits.csv")
g = sns.jointplot(data=df, x="trait1", y="trait2", hue="clade", kind="kde")
g.savefig("figures/tpl_09_jointplot.png", dpi=200, bbox_inches="tight")
plt.close("all")

# 10. Annotated heatmap ------------------------------------------------------------
df = pd.read_csv("data/pathway_status_table.csv", index_col=0)
sns.heatmap(df, annot=True, fmt="d", cmap="crest")
plt.title("Pathway Status Table")
plt.savefig("figures/tpl_10_annotated_heatmap.png", dpi=200, bbox_inches="tight")
plt.close()

print("All template figures written to figures/")
