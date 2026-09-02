from pathlib import Path

FIGURES = [
    "01_docking_scatter.png",
    "02_cytokine_timecourse.png",
    "03_variant_af_histogram.png",
    "03b_variant_af_ecdf.png",
    "04_expression_boxplot.png",
    "04b_expression_violin_swarm.png",
    "05_enzyme_lmplot.png",
    "06_metabolite_heatmap.png",
    "07_microbiome_clustermap.png",
    "08_qc_pairplot.png",
    "09_phylo_jointplot.png",
    "10_pathway_heatmap.png",
    "11_differential_expression_dashboard.png",
    "12_pangenome_structure.png",
    "13_pangenome_clustermap.png",
    "14_microbiome_clr_clustermap.png",
    "practice_annotated_qc.png",
]


def test_every_gallery_figure_links_to_a_tutorial() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    guide = Path("docs/figure-tutorials.md").read_text(encoding="utf-8")

    for figure in FIGURES:
        assert f"figures/{figure})](docs/figure-tutorials.md#" in readme
        assert figure.split(".")[0].split("_")[0] in guide

    assert guide.count("**Use when:**") == len(FIGURES)
    assert guide.count("**Inputs:**") == len(FIGURES)
    assert guide.count("**Code:**") == len(FIGURES)
    assert guide.count("**Interpret:") == len(FIGURES)
