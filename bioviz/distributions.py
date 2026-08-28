"""Distribution plots: histogram, KDE, ECDF."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from . import theme


def variant_af_histogram(df: pd.DataFrame, ax: plt.Axes | None = None) -> tuple[plt.Figure, plt.Axes]:
    """Step histogram of variant allele frequency, split by consequence class."""
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=theme.FIGSIZE_DEFAULT)
    sns.histplot(
        data=df, x="allele_frequency", hue="consequence", element="step",
        stat="density", common_norm=False, palette=theme.CATEGORICAL_PALETTE, ax=ax,
    )
    ax.set_title("Variant Allele Frequency Spectrum by Consequence")
    ax.set_xlabel("Allele frequency")
    ax.set_ylabel("Density")
    return fig, ax


def variant_af_ecdf(df: pd.DataFrame, ax: plt.Axes | None = None) -> tuple[plt.Figure, plt.Axes]:
    """Empirical CDF of allele frequency, split by consequence class."""
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=theme.FIGSIZE_DEFAULT)
    sns.ecdfplot(data=df, x="allele_frequency", hue="consequence", palette=theme.CATEGORICAL_PALETTE, ax=ax)
    ax.set_title("Cumulative Distribution of Allele Frequency")
    ax.set_xlabel("Allele frequency")
    return fig, ax
