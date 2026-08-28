"""
Smoke + sanity tests for the bioviz package.

Two kinds of checks:
1. Every plotting function runs without error and returns a real
   Matplotlib/Seaborn object (a rendering smoke test).
2. Statistical sanity checks confirming the simulated datasets and the
   fitting utilities recover the ground truth baked into
   scripts/generate_datasets.py (so a silent bug in either the data
   generator or the analysis code gets caught).
"""

from pathlib import Path

import matplotlib
import pandas as pd
import pytest

matplotlib.use("Agg")

from bioviz import categorical, distributions, matrix, regression, relational, theme  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "data"

theme.set_theme()


@pytest.fixture(scope="module")
def docking_df():
    return pd.read_csv(DATA / "docking_scores.csv")


@pytest.fixture(scope="module")
def cytokine_df():
    return pd.read_csv(DATA / "timecourse_cytokines.csv")


@pytest.fixture(scope="module")
def variants_df():
    return pd.read_csv(DATA / "variants.csv")


@pytest.fixture(scope="module")
def expression_df():
    return pd.read_csv(DATA / "gene_expression.csv")


@pytest.fixture(scope="module")
def enzyme_df():
    return pd.read_csv(DATA / "enzyme_kinetics.csv")


@pytest.fixture(scope="module")
def metabolites_df():
    return pd.read_csv(DATA / "metabolites.csv")


@pytest.fixture(scope="module")
def microbiome_df():
    return pd.read_csv(DATA / "microbiome_abundance.csv")


@pytest.fixture(scope="module")
def qc_df():
    return pd.read_csv(DATA / "qc_metrics.csv")


@pytest.fixture(scope="module")
def phylo_df():
    return pd.read_csv(DATA / "phylo_traits.csv")


@pytest.fixture(scope="module")
def pathway_df():
    return pd.read_csv(DATA / "pathway_status_table.csv")


# --- rendering smoke tests -------------------------------------------------

def test_docking_scatter_renders(docking_df):
    fig, ax = relational.docking_scatter(docking_df)
    assert ax.has_data()


def test_cytokine_lineplot_renders(cytokine_df):
    fig, ax = relational.cytokine_timecourse(cytokine_df)
    assert ax.has_data()


def test_variant_histogram_renders(variants_df):
    fig, ax = distributions.variant_af_histogram(variants_df)
    assert ax.has_data()


def test_variant_ecdf_renders(variants_df):
    fig, ax = distributions.variant_af_ecdf(variants_df)
    assert ax.has_data()


def test_expression_boxplot_renders(expression_df):
    fig, ax = categorical.expression_boxplot(expression_df)
    assert ax.has_data()


def test_expression_violin_swarm_renders(expression_df):
    fig, ax = categorical.expression_violin_swarm(expression_df)
    assert ax.has_data()


def test_metabolite_heatmap_renders(metabolites_df):
    fig, ax = matrix.metabolite_corr_heatmap(metabolites_df)
    assert ax.has_data()


def test_pathway_heatmap_renders(pathway_df):
    fig, ax = matrix.pathway_status_heatmap(pathway_df)
    assert ax.has_data()


def test_qc_pairplot_renders(qc_df):
    g = matrix.qc_pairplot(qc_df)
    assert g.figure is not None


def test_phylo_jointplot_renders(phylo_df):
    g = matrix.phylo_traits_jointplot(phylo_df)
    assert g.figure is not None


def test_microbiome_clustermap_renders(microbiome_df):
    g = matrix.microbiome_clustermap(microbiome_df)
    assert g.figure is not None


def test_enzyme_lmplot_renders(enzyme_df):
    g = regression.enzyme_kinetics_lmplot(enzyme_df)
    assert g.figure is not None


# --- statistical sanity checks ---------------------------------------------

def test_michaelis_menten_fit_recovers_ground_truth(enzyme_df):
    """Fitted Vmax/Km should be within 15% of the simulation ground truth."""
    fit = regression.fit_michaelis_menten(enzyme_df).set_index("inhibitor")
    ground_truth = {
        "none": dict(vmax=100, km=8),
        "competitive": dict(vmax=100, km=24),
        "noncompetitive": dict(vmax=55, km=8),
    }
    for inhibitor, truth in ground_truth.items():
        assert fit.loc[inhibitor, "vmax"] == pytest.approx(truth["vmax"], rel=0.15)
        assert fit.loc[inhibitor, "km"] == pytest.approx(truth["km"], rel=0.20)


def test_competitive_inhibitor_raises_km_not_vmax(enzyme_df):
    fit = regression.fit_michaelis_menten(enzyme_df).set_index("inhibitor")
    assert fit.loc["competitive", "km"] > fit.loc["none", "km"]
    assert fit.loc["competitive", "vmax"] == pytest.approx(fit.loc["none", "vmax"], rel=0.15)


def test_noncompetitive_inhibitor_lowers_vmax_not_km(enzyme_df):
    fit = regression.fit_michaelis_menten(enzyme_df).set_index("inhibitor")
    assert fit.loc["noncompetitive", "vmax"] < fit.loc["none", "vmax"]
    assert fit.loc["noncompetitive", "km"] == pytest.approx(fit.loc["none", "km"], rel=0.20)


def test_missense_variants_skew_rarer_than_common_benign(variants_df):
    """Purifying selection: missense median AF should be well below the
    common/benign class's median AF."""
    missense_median = variants_df.loc[variants_df.consequence == "missense", "allele_frequency"].median()
    common_median = variants_df.loc[variants_df.consequence == "common_benign", "allele_frequency"].median()
    assert missense_median < common_median


def test_microbiome_abundances_sum_to_one_per_sample(microbiome_df):
    sums = microbiome_df.groupby("sample")["relative_abundance"].sum()
    assert (sums.round(3) == 1.0).all()


def test_gut_and_skin_have_distinct_dominant_taxa(microbiome_df):
    """The most abundant species in gut samples should differ from skin."""
    gut = microbiome_df[microbiome_df.body_site == "gut"]
    skin = microbiome_df[microbiome_df.body_site == "skin"]
    gut_top = gut.groupby("species")["relative_abundance"].mean().idxmax()
    skin_top = skin.groupby("species")["relative_abundance"].mean().idxmax()
    assert gut_top != skin_top


def test_qc_coverage_and_duplicates_are_negatively_correlated(qc_df):
    corr = qc_df["coverage_mean"].corr(qc_df["duplicates_pct"])
    assert corr < -0.3


def test_upregulated_and_downregulated_genes_separate(expression_df):
    """Genes tagged 'up' should show treatment > control; 'down' the reverse."""
    for gene, direction in expression_df.groupby("gene")["direction"].first().items():
        sub = expression_df[expression_df.gene == gene]
        ctrl_mean = sub[sub.condition == "control"]["expression"].mean()
        trt_mean = sub[sub.condition == "treatment"]["expression"].mean()
        if direction == "up":
            assert trt_mean > ctrl_mean
        elif direction == "down":
            assert trt_mean < ctrl_mean
        else:
            assert abs(trt_mean - ctrl_mean) < 0.5
