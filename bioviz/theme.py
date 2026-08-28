"""Consistent visual theme used across every figure in this repository."""

from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns

PALETTE = "viridis"
DIVERGING_PALETTE = "vlag"
CATEGORICAL_PALETTE = "Set2"
FIGSIZE_DEFAULT = (7, 5)
DPI_SAVE = 300

FONT_SCALE = 1.05
CONTEXT = "notebook"
STYLE = "whitegrid"


def set_theme() -> None:
    """Apply the repository-wide Seaborn/Matplotlib theme.

    Call this once at the top of a notebook or script before plotting.
    """
    sns.set_theme(
        context=CONTEXT,
        style=STYLE,
        palette=CATEGORICAL_PALETTE,
        font_scale=FONT_SCALE,
        rc={
            "figure.figsize": FIGSIZE_DEFAULT,
            "axes.titleweight": "bold",
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "figure.dpi": 100,
            "savefig.dpi": DPI_SAVE,
            "savefig.bbox": "tight",
        },
    )


def savefig(fig: plt.Figure, path: str) -> None:
    """Save a figure at publication resolution with tight bounding box."""
    fig.savefig(path, dpi=DPI_SAVE, bbox_inches="tight")
