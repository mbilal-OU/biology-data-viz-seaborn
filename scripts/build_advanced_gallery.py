"""Build the advanced omics figures used in the README and documentation."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from bioviz import omics, theme

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "figures"


def save_both(fig: plt.Figure, stem: str) -> None:
    theme.savefig(fig, FIGURES / f"{stem}.png")
    theme.savefig(fig, FIGURES / f"{stem}.svg")


def main() -> None:
    theme.set_theme()
    FIGURES.mkdir(exist_ok=True)

    differential = pd.read_csv(DATA / "differential_expression.csv")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.4))
    omics.volcano_plot(differential, axes[0])
    omics.ma_plot(differential, axes[1])
    fig.suptitle("Case Study 1: Differential Expression", fontsize=15, fontweight="bold")
    fig.tight_layout()
    save_both(fig, "11_differential_expression_dashboard")
    plt.close(fig)

    presence = pd.read_csv(DATA / "pangenome_presence_absence.csv")
    summary = pd.read_csv(DATA / "pangenome_gene_summary.csv")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
    omics.pangenome_frequency_spectrum(summary, axes[0])
    omics.pangenome_pca_plot(presence, axes[1])
    fig.suptitle("Case Study 2: Pangenome Structure", fontsize=15, fontweight="bold")
    fig.tight_layout()
    save_both(fig, "12_pangenome_structure")
    plt.close(fig)

    cluster = omics.pangenome_clustermap(presence)
    save_both(cluster.figure, "13_pangenome_clustermap")
    plt.close(cluster.figure)

    microbiome = pd.read_csv(DATA / "microbiome_abundance.csv")
    clr_cluster = omics.microbiome_clr_clustermap(microbiome)
    save_both(clr_cluster.figure, "14_microbiome_clr_clustermap")
    plt.close(clr_cluster.figure)


if __name__ == "__main__":
    main()
