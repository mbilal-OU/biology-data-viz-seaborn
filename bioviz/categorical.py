"""Categorical plots: box, violin, swarm, for group comparisons."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from . import theme


def expression_boxplot(df: pd.DataFrame, ax: plt.Axes | None = None) -> tuple[plt.Figure, plt.Axes]:
    """Boxplot of gene expression by gene, split control vs. treatment."""
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=(9, 5))
    sns.boxplot(
        data=df,
        x="gene",
        y="expression",
        hue="condition",
        palette=theme.CATEGORICAL_PALETTE,
        ax=ax,
    )
    ax.set_title("Gene Expression: Control vs. Treatment")
    ax.set_xlabel("Gene")
    ax.set_ylabel("log2 expression")
    ax.legend(title="Condition", frameon=False)
    return fig, ax


def expression_violin_swarm(df: pd.DataFrame, ax: plt.Axes | None = None) -> tuple[plt.Figure, plt.Axes]:
    """Violin plot (distribution shape) with an overlaid swarm (raw replicates)."""
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=(9, 5))
    sns.violinplot(
        data=df,
        x="gene",
        y="expression",
        hue="condition",
        split=True,
        inner=None,
        palette=theme.CATEGORICAL_PALETTE,
        ax=ax,
        alpha=0.6,
    )
    sns.swarmplot(
        data=df,
        x="gene",
        y="expression",
        hue="condition",
        dodge=True,
        size=3,
        palette=["black", "black"],
        alpha=0.6,
        ax=ax,
        legend=False,
    )
    ax.set_title("Expression Distribution with Individual Replicates")
    ax.set_xlabel("Gene")
    ax.set_ylabel("log2 expression")
    return fig, ax
