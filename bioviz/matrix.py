"""Matrix and multi-variable plots: heatmap, clustermap, pairplot, jointplot."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from . import theme


def metabolite_corr_heatmap(df: pd.DataFrame, ax: plt.Axes | None = None) -> tuple[plt.Figure, plt.Axes]:
    """Annotated correlation heatmap of metabolite levels.

    Parameters
    ----------
    df : wide-format DataFrame, one row per sample, one column per
        metabolite (``sample_id`` column excluded automatically if present).
    """
    numeric = df.drop(columns=[c for c in df.columns if c == "sample_id"])
    corr = numeric.corr()
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=(8, 7))
    sns.heatmap(
        corr, cmap=theme.DIVERGING_PALETTE, center=0, annot=True, fmt=".2f",
        square=True, linewidths=0.5, ax=ax, cbar_kws={"label": "Pearson r"},
    )
    ax.set_title("Metabolite-Metabolite Correlation")
    return fig, ax


def microbiome_clustermap(df: pd.DataFrame):
    """Clustered heatmap of species relative abundance across samples.

    Parameters
    ----------
    df : long-format DataFrame with columns ``species``, ``sample``,
        ``relative_abundance``.
    """
    piv = df.pivot_table(index="species", columns="sample", values="relative_abundance", fill_value=0)
    g = sns.clustermap(
        piv, cmap="mako", z_score=0, figsize=(9, 8), linewidths=0.3,
        cbar_kws={"label": "z-scored relative abundance"},
    )
    g.figure.suptitle("Microbiome Composition Clustering", y=1.02, fontweight="bold")
    return g


def qc_pairplot(df: pd.DataFrame):
    """Pairwise scatter matrix of sequencing QC metrics, colored by batch."""
    cols = ["duplicates_pct", "coverage_mean", "gc_content", "q30_pct"]
    g = sns.pairplot(
        df, vars=cols, hue="batch", palette=theme.CATEGORICAL_PALETTE,
        diag_kind="kde", plot_kws={"alpha": 0.6, "s": 25},
    )
    g.figure.suptitle("Sequencing QC Metrics", y=1.02, fontweight="bold")
    return g


def phylo_traits_jointplot(df: pd.DataFrame):
    """Jointplot (KDE) of two morphological traits, colored by clade."""
    g = sns.jointplot(
        data=df, x="trait1", y="trait2", hue="clade", kind="kde",
        palette=theme.CATEGORICAL_PALETTE, height=6.5, fill=True, alpha=0.6,
    )
    g.set_axis_labels("Trait 1 (body-size proxy)", "Trait 2 (metabolic-rate proxy)")
    g.figure.suptitle("Trait-Trait Relationship by Clade", y=1.02, fontweight="bold")
    # Move the legend outside the plotted area so it never occludes data.
    sns.move_legend(g.ax_joint, "upper left", bbox_to_anchor=(1.18, 1.28), title="clade", frameon=True)
    g.figure.subplots_adjust(right=0.82)
    return g


def pathway_status_heatmap(df: pd.DataFrame, ax: plt.Axes | None = None) -> tuple[plt.Figure, plt.Axes]:
    """Annotated integer heatmap of gene counts per pathway x status."""
    indexed = df.set_index("pathway") if "pathway" in df.columns else df
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=(7, 6))
    sns.heatmap(
        indexed, annot=True, fmt="d", cmap="crest", linewidths=0.5,
        cbar_kws={"label": "Gene count"}, ax=ax,
    )
    ax.set_title("Pathway Enrichment by Functional Status")
    return fig, ax
