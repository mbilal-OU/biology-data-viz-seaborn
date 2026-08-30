"""Omics-focused statistical visualizations built with Seaborn.

The functions in this module separate visualization from inference. They
expect analysis-ready tables and make thresholds, transformations, and
distance choices explicit so a polished figure does not hide an invalid
comparison.
"""

from __future__ import annotations

from collections.abc import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from . import theme


def _require_columns(df: pd.DataFrame, required: Iterable[str]) -> None:
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    if df.empty:
        raise ValueError("Input data must contain at least one row")


def volcano_plot(
    df: pd.DataFrame,
    ax: plt.Axes | None = None,
    *,
    fdr_threshold: float = 0.05,
    effect_threshold: float = 1.0,
    label_top: int = 8,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot differential-expression effect size against FDR evidence.

    Required columns are ``gene``, ``log2_fold_change``, and ``padj``.
    Points are classified using both the effect-size and adjusted-p-value
    thresholds. The plot does not calculate differential expression.
    """
    _require_columns(df, ["gene", "log2_fold_change", "padj"])
    if not 0 < fdr_threshold < 1:
        raise ValueError("fdr_threshold must be between 0 and 1")
    if effect_threshold <= 0:
        raise ValueError("effect_threshold must be positive")

    plot_df = df.copy()
    plot_df["padj"] = plot_df["padj"].clip(lower=np.finfo(float).tiny, upper=1)
    plot_df["minus_log10_fdr"] = -np.log10(plot_df["padj"])
    plot_df["status"] = "Not significant"
    significant = plot_df["padj"].lt(fdr_threshold)
    plot_df.loc[significant & plot_df["log2_fold_change"].ge(effect_threshold), "status"] = "Up"
    plot_df.loc[significant & plot_df["log2_fold_change"].le(-effect_threshold), "status"] = "Down"

    palette = {
        "Not significant": "#9A9A9A",
        "Up": theme.OKABE_ITO[1],
        "Down": theme.OKABE_ITO[0],
    }
    order = ["Not significant", "Down", "Up"]
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=(7.4, 5.4))
    sns.scatterplot(
        data=plot_df,
        x="log2_fold_change",
        y="minus_log10_fdr",
        hue="status",
        hue_order=order,
        palette=palette,
        alpha=0.72,
        s=28,
        linewidth=0,
        ax=ax,
    )
    ax.axhline(-np.log10(fdr_threshold), color="#555555", linestyle="--", linewidth=1)
    ax.axvline(-effect_threshold, color="#555555", linestyle=":", linewidth=1)
    ax.axvline(effect_threshold, color="#555555", linestyle=":", linewidth=1)

    candidates = plot_df[plot_df["status"] != "Not significant"].copy()
    candidates["label_rank"] = candidates["minus_log10_fdr"] * candidates["log2_fold_change"].abs()
    for row in candidates.nlargest(label_top, "label_rank").itertuples():
        ax.annotate(
            row.gene,
            (row.log2_fold_change, row.minus_log10_fdr),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=8,
        )

    ax.set_title("Differential Expression: Effect Size and FDR")
    ax.set_xlabel("log2 fold change")
    ax.set_ylabel("-log10 adjusted p-value")
    ax.legend(title="Classification", frameon=False)
    return fig, ax


def ma_plot(
    df: pd.DataFrame,
    ax: plt.Axes | None = None,
    *,
    fdr_threshold: float = 0.05,
    effect_threshold: float = 1.0,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot log-fold change against mean normalized abundance."""
    _require_columns(df, ["base_mean", "log2_fold_change", "padj"])
    if (df["base_mean"] < 0).any():
        raise ValueError("base_mean cannot contain negative values")

    plot_df = df.copy()
    plot_df["mean_axis"] = np.log10(plot_df["base_mean"] + 1)
    plot_df["significant"] = plot_df["padj"].lt(fdr_threshold) & plot_df["log2_fold_change"].abs().ge(
        effect_threshold
    )
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=(7.4, 5.4))
    sns.scatterplot(
        data=plot_df,
        x="mean_axis",
        y="log2_fold_change",
        hue="significant",
        hue_order=[False, True],
        palette={False: "#A0A0A0", True: theme.OKABE_ITO[2]},
        alpha=0.7,
        s=26,
        linewidth=0,
        ax=ax,
    )
    ax.axhline(0, color="#444444", linewidth=1)
    ax.axhline(effect_threshold, color="#666666", linestyle=":", linewidth=1)
    ax.axhline(-effect_threshold, color="#666666", linestyle=":", linewidth=1)
    ax.set_title("MA Plot: Abundance and Effect Size")
    ax.set_xlabel("log10 mean normalized abundance + 1")
    ax.set_ylabel("log2 fold change")
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        ["Not selected", "FDR and effect threshold"],
        title="Result",
        frameon=False,
    )
    return fig, ax


def pangenome_frequency_spectrum(
    summary: pd.DataFrame,
    ax: plt.Axes | None = None,
) -> tuple[plt.Figure, plt.Axes]:
    """Show gene-family counts across explicit prevalence classes."""
    _require_columns(summary, ["gene_family", "prevalence", "frequency_class"])
    if not summary["prevalence"].between(0, 1).all():
        raise ValueError("prevalence must be between 0 and 1")

    class_order = ["Core", "Soft core", "Shell", "Cloud"]
    counts = (
        summary["frequency_class"]
        .value_counts()
        .reindex(class_order, fill_value=0)
        .rename_axis("frequency_class")
        .reset_index(name="gene_families")
    )
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=(7.2, 4.8))
    sns.barplot(
        data=counts,
        x="frequency_class",
        y="gene_families",
        hue="frequency_class",
        order=class_order,
        hue_order=class_order,
        palette=theme.OKABE_ITO[:4],
        legend=False,
        ax=ax,
    )
    for container in ax.containers:
        ax.bar_label(container, padding=3, fontsize=9)
    ax.set_title("Pangenome Gene-Frequency Spectrum")
    ax.set_xlabel("Prevalence class")
    ax.set_ylabel("Gene families")
    return fig, ax


def pangenome_pca(presence: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
    """Calculate a centered PCA of a binary gene presence-absence matrix.

    Metadata columns are ``genome_id``, ``lineage``, and ``habitat``. All
    remaining columns must be binary gene-family indicators.
    """
    _require_columns(presence, ["genome_id", "lineage", "habitat"])
    metadata_cols = ["genome_id", "lineage", "habitat"]
    gene_cols = [column for column in presence.columns if column not in metadata_cols]
    if len(gene_cols) < 2:
        raise ValueError("At least two gene-family columns are required")
    matrix = presence[gene_cols].to_numpy(dtype=float)
    if not np.isin(matrix, [0, 1]).all():
        raise ValueError("Gene-family columns must contain only 0 and 1")
    variable = matrix.var(axis=0) > 0
    if variable.sum() < 2:
        raise ValueError("At least two variable gene families are required")

    centered = matrix[:, variable] - matrix[:, variable].mean(axis=0)
    u, singular_values, _ = np.linalg.svd(centered, full_matrices=False)
    scores = u[:, :2] * singular_values[:2]
    variance = singular_values**2
    explained = variance[:2] / variance.sum()
    score_df = presence[metadata_cols].copy()
    score_df["PC1"] = scores[:, 0]
    score_df["PC2"] = scores[:, 1]
    return score_df, explained


def pangenome_pca_plot(
    presence: pd.DataFrame,
    ax: plt.Axes | None = None,
) -> tuple[plt.Figure, plt.Axes, np.ndarray]:
    """Plot the first two PCA axes of a pangenome presence-absence matrix."""
    scores, explained = pangenome_pca(presence)
    lineages = sorted(scores["lineage"].unique())
    lineage_colors = {
        lineage: theme.OKABE_ITO[index % len(theme.OKABE_ITO)] for index, lineage in enumerate(lineages)
    }
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=(7.2, 5.4))
    sns.scatterplot(
        data=scores,
        x="PC1",
        y="PC2",
        hue="lineage",
        style="habitat",
        palette=lineage_colors,
        s=75,
        alpha=0.85,
        ax=ax,
    )
    ax.axhline(0, color="#BBBBBB", linewidth=0.8)
    ax.axvline(0, color="#BBBBBB", linewidth=0.8)
    ax.set_title("Genome Structure from Accessory-Gene Content")
    ax.set_xlabel(f"PC1 ({explained[0] * 100:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({explained[1] * 100:.1f}% variance)")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)
    return fig, ax, explained


def pangenome_clustermap(presence: pd.DataFrame):
    """Cluster genomes and gene families using Jaccard distance."""
    _require_columns(presence, ["genome_id", "lineage", "habitat"])
    metadata_cols = ["genome_id", "lineage", "habitat"]
    gene_cols = [column for column in presence.columns if column not in metadata_cols]
    matrix = presence.set_index("genome_id")[gene_cols]
    if not np.isin(matrix.to_numpy(), [0, 1]).all():
        raise ValueError("Gene-family columns must contain only 0 and 1")
    variable_cols = matrix.columns[matrix.nunique() > 1]
    matrix = matrix[variable_cols]
    lineage_order = sorted(presence["lineage"].unique())
    lineage_colors = {
        lineage: theme.OKABE_ITO[index % len(theme.OKABE_ITO)] for index, lineage in enumerate(lineage_order)
    }
    row_colors = presence.set_index("genome_id")["lineage"].map(lineage_colors)
    g = sns.clustermap(
        matrix,
        metric="jaccard",
        method="average",
        cmap=["#F4F4F4", theme.OKABE_ITO[0]],
        row_colors=row_colors,
        xticklabels=False,
        yticklabels=True,
        figsize=(10, 8),
        cbar_pos=None,
    )
    g.figure.suptitle("Accessory-Gene Presence and Absence", y=1.01, fontweight="bold")
    g.ax_heatmap.set_xlabel("Variable gene families")
    g.ax_heatmap.set_ylabel("Genomes")
    return g


def microbiome_clr_clustermap(df: pd.DataFrame):
    """Cluster samples after centered-log-ratio transformation.

    Euclidean distance in CLR space is Aitchison distance. Zeros are
    replaced with half the smallest observed positive abundance before
    renormalization and transformation.
    """
    _require_columns(df, ["sample", "body_site", "species", "relative_abundance"])
    if (df["relative_abundance"] < 0).any():
        raise ValueError("relative_abundance cannot contain negative values")
    table = df.pivot_table(index="sample", columns="species", values="relative_abundance", fill_value=0)
    positive = table.to_numpy()[table.to_numpy() > 0]
    if positive.size == 0:
        raise ValueError("At least one positive abundance is required")
    pseudocount = max(float(positive.min()) / 2, 1e-8)
    replaced = table.mask(table <= 0, pseudocount)
    proportions = replaced.div(replaced.sum(axis=1), axis=0)
    log_values = np.log(proportions)
    clr = log_values.sub(log_values.mean(axis=1), axis=0)

    site = df.drop_duplicates("sample").set_index("sample")["body_site"].reindex(clr.index)
    site_order = sorted(site.unique())
    site_colors = {
        value: theme.OKABE_ITO[index % len(theme.OKABE_ITO)] for index, value in enumerate(site_order)
    }
    row_colors = site.map(site_colors)
    g = sns.clustermap(
        clr,
        metric="euclidean",
        method="average",
        cmap=theme.DIVERGING_PALETTE,
        center=0,
        row_colors=row_colors,
        figsize=(10, 8),
        cbar_kws={"label": "CLR abundance"},
    )
    g.figure.suptitle("Microbiome Composition in CLR Space", y=1.02, fontweight="bold")
    g.ax_heatmap.set_xlabel("Taxa")
    g.ax_heatmap.set_ylabel("Samples")
    return g
