"""Relational plots: scatter and line, for continuous-vs-continuous data."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from . import theme


def docking_scatter(df: pd.DataFrame, ax: plt.Axes | None = None) -> tuple[plt.Figure, plt.Axes]:
    """Scatter plot of docking score vs. lipophilicity (logP), by target.

    Parameters
    ----------
    df : DataFrame with columns ``logP``, ``vina_score``, ``target``, ``ring_count``.
    ax : optional existing Axes to draw on.

    Returns
    -------
    (fig, ax)
    """
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=theme.FIGSIZE_DEFAULT)
    sns.scatterplot(
        data=df,
        x="logP",
        y="vina_score",
        hue="target",
        size="ring_count",
        sizes=(30, 180),
        alpha=0.75,
        palette=theme.CATEGORICAL_PALETTE,
        ax=ax,
    )
    ax.set_title("Docking Landscape: Binding Score vs. Lipophilicity")
    ax.set_xlabel("logP (lipophilicity)")
    ax.set_ylabel("Vina score (kcal/mol, lower = stronger binding)")
    ax.invert_yaxis()
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)
    return fig, ax


def cytokine_timecourse(df: pd.DataFrame, ax: plt.Axes | None = None) -> tuple[plt.Figure, plt.Axes]:
    """Line plot of IL-6 over time, by treatment arm, with SD error bands.

    Parameters
    ----------
    df : DataFrame with columns ``time_h``, ``IL6``, ``treatment``.
    """
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots(figsize=theme.FIGSIZE_DEFAULT)
    sns.lineplot(
        data=df,
        x="time_h",
        y="IL6",
        hue="treatment",
        errorbar="sd",
        marker="o",
        palette=theme.CATEGORICAL_PALETTE,
        ax=ax,
    )
    ax.set_title("IL-6 Cytokine Response Following LPS Challenge")
    ax.set_xlabel("Time post-challenge (h)")
    ax.set_ylabel("IL-6 (pg/mL)")
    ax.legend(title="Treatment", frameon=False)
    return fig, ax
