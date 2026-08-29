# %% [markdown]
# # Advanced Biological Visualization with Seaborn
#
# Three compact case studies demonstrate statistical judgment as well as
# plotting technique. The data are seeded simulations, so the ground truth is
# known and tested. These figures are descriptive views of analysis-ready
# tables, not substitutes for differential-expression, pangenome, or
# compositional-data inference.

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path.cwd().parent))
from bioviz import omics, theme

theme.set_theme()
DATA = Path.cwd().parent / "data"

# %% [markdown]
# ## 1. Differential expression: effect size and evidence
#
# A volcano plot emphasizes statistical evidence, while an MA plot reveals
# abundance-dependent behavior. A gene is highlighted only when it crosses
# both the FDR and effect-size thresholds.

# %%
differential = pd.read_csv(DATA / "differential_expression.csv")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.4))
omics.volcano_plot(differential, axes[0])
omics.ma_plot(differential, axes[1])
fig.tight_layout()
plt.show()

# %% [markdown]
# ## 2. Pangenome structure
#
# The frequency spectrum summarizes prevalence classes. PCA provides a
# low-dimensional exploratory view of accessory-gene content. The percentage
# labels are computed from the binary matrix rather than written by hand.

# %%
presence = pd.read_csv(DATA / "pangenome_presence_absence.csv")
summary = pd.read_csv(DATA / "pangenome_gene_summary.csv")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
omics.pangenome_frequency_spectrum(summary, axes[0])
omics.pangenome_pca_plot(presence, axes[1])
fig.tight_layout()
plt.show()

# %%
cluster = omics.pangenome_clustermap(presence)
plt.show()

# %% [markdown]
# ## 3. Compositional microbiome data
#
# Relative abundances are transformed to centered-log-ratio coordinates.
# Euclidean distance in this space is Aitchison distance. The plot states the
# zero-replacement rule explicitly because that choice affects the result.

# %%
microbiome = pd.read_csv(DATA / "microbiome_abundance.csv")
clr_cluster = omics.microbiome_clr_clustermap(microbiome)
plt.show()
