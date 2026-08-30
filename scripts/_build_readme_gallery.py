"""
_build_readme_gallery.py
==========================
Generates the "Full Tutorial: Every Plot, Explained" section of
README.md programmatically, so all 13 figure sections follow an
identical structure (what it is / question / figure / interpretation
/ create it / adapt it to your data) without manual copy-paste drift.

This is a one-off authoring tool, not part of the tested package.
Run it, then paste/verify the output into README.md.

Usage:
    python scripts/_build_readme_gallery.py > /tmp/gallery_section.md
"""

SECTIONS = [
    dict(
        num="1",
        title="Scatter Plot: Docking Landscape",
        plot_kind="Scatter plot",
        what_it_is=(
            "A scatter plot maps two continuous variables to x/y position. "
            "It's the right choice when you want to see the *shape* of a "
            "relationship (linear, non-linear, clustered) rather than "
            "just a summary statistic. Here, point size and color add two "
            "more variables (`ring_count`, `target`) without needing a "
            "third axis."
        ),
        question=(
            "Across three drug targets, how does ligand lipophilicity "
            "(logP) relate to predicted binding affinity (Vina score)? "
            "Are the best-scoring ligands clustered in a particular logP "
            "range?"
        ),
        dataset="`data/docking_scores.csv`",
        dataset_desc="360 rows. Simulated virtual-screening results against 3 protein targets.",
        image="figures/01_docking_scatter.png",
        code=('df = pd.read_csv("data/docking_scores.csv")\nfig, ax = relational.docking_scatter(df)'),
        interpretation=(
            "Binding score is **not** monotonic in logP: each target "
            "shows a clear inverted-U pattern, worsening at both very low "
            "and very high lipophilicity. This matches known "
            "medicinal-chemistry behavior: overly hydrophilic ligands bind "
            "poorly to a typically hydrophobic pocket, while overly "
            "hydrophobic ligands lose entropic favorability and "
            "solubility. `GPCR_C` shows the best (most negative) scores "
            "overall."
        ),
        requirements=[
            "one continuous x variable (a numeric column)",
            "one continuous y variable (a numeric column)",
            "optionally: a categorical column for `hue`, a numeric column for `size`",
        ],
        adapt_code=(
            "import seaborn as sns\n\n"
            "sns.scatterplot(\n"
            '    data=my_df, x="your_x_column", y="your_y_column",\n'
            '    hue="your_group_column", size="your_size_column",\n'
            ")"
        ),
    ),
    dict(
        num="2",
        title="Line Plot: Cytokine Time Course",
        plot_kind="Line plot",
        what_it_is=(
            "A line plot connects ordered observations, and with "
            '`errorbar="sd"` it also draws a shaded band showing spread '
            "at each point. Use it whenever the x-axis is naturally "
            "ordered (time, dose, distance) and you have repeated "
            "measurements at each x value; a scatter plot alone would "
            "hide the trend and the variability together."
        ),
        question=(
            "Does an anti-IL-6R antibody blunt the IL-6 response to an "
            "inflammatory (LPS) challenge, and at which time points does "
            "the effect become visible?"
        ),
        dataset="`data/timecourse_cytokines.csv`",
        dataset_desc="140 rows. IL-6 concentration over 24h, vehicle vs. antibody, 10 subjects/arm.",
        image="figures/02_cytokine_timecourse.png",
        code=(
            'df = pd.read_csv("data/timecourse_cytokines.csv")\nfig, ax = relational.cytokine_timecourse(df)'
        ),
        interpretation=(
            "Both arms show the expected acute-phase shape: rapid rise, "
            "peak around 4h, slow decay. The antibody-treated arm's peak "
            "is visibly damped to roughly half the vehicle peak, and the "
            "SD bands don't overlap near the peak, suggestive of a real "
            "effect, though a formal mixed-effects model would be needed "
            "to confirm significance."
        ),
        requirements=[
            "one ordered x variable (time, dose, etc.)",
            "one continuous y variable",
            "a categorical `hue` column to compare groups/arms",
            "multiple observations per x value per group, so `errorbar` has something to summarize",
        ],
        adapt_code=(
            "sns.lineplot(\n"
            '    data=my_df, x="time_column", y="measurement_column",\n'
            '    hue="group_column", errorbar="sd", marker="o",\n'
            ")"
        ),
    ),
    dict(
        num="3",
        title="Histogram & ECDF: Variant Allele Frequency",
        plot_kind="Histogram / ECDF",
        what_it_is=(
            "A histogram (or KDE) shows the shape of a single "
            "distribution. An ECDF (empirical cumulative distribution "
            "function) shows the same information without binning "
            'artifacts, and makes it trivial to read off "what fraction '
            'of the data is below X", which is often the more useful '
            "question when comparing distributions across groups."
        ),
        question=(
            "Do missense variants show a different allele-frequency "
            "distribution than synonymous or common/benign variants, "
            "consistent with stronger purifying selection?"
        ),
        dataset="`data/variants.csv`",
        dataset_desc="2000 rows. Simulated variant calls with functional consequence and allele frequency.",
        image="figures/03_variant_af_histogram.png",
        image2="figures/03b_variant_af_ecdf.png",
        code=(
            'df = pd.read_csv("data/variants.csv")\n'
            "fig, ax = distributions.variant_af_histogram(df)\n\n"
            "# same data, cumulative view:\n"
            "fig, ax = distributions.variant_af_ecdf(df)"
        ),
        interpretation=(
            "Missense variants have the lowest median allele frequency, "
            "synonymous variants sit in between, and the common/benign "
            "class is shifted markedly toward intermediate-to-high "
            "frequency. The ECDF makes the rightward shift of the "
            "common/benign curve especially easy to see: a larger "
            "fraction of those variants sit at higher frequency at every "
            "point along the curve."
        ),
        requirements=[
            "one continuous numeric column to plot the distribution of",
            "optionally: a categorical `hue` column to compare distributions across groups",
        ],
        adapt_code=(
            'sns.histplot(data=my_df, x="value_column", hue="group_column", element="step", stat="density")\n'
            'sns.ecdfplot(data=my_df, x="value_column", hue="group_column")'
        ),
    ),
    dict(
        num="4",
        title="Box / Violin / Swarm: Differential Gene Expression",
        plot_kind="Box / Violin / Swarm",
        what_it_is=(
            "Boxplots summarize a group comparison compactly (median, "
            "IQR, outliers), good for scanning many groups at once. "
            "Violin + swarm goes further, showing the full distribution "
            "shape plus every individual data point, which catches "
            "bimodality or outlier-driven effects a boxplot alone would "
            "hide."
        ),
        question=(
            "Which genes change expression under treatment, in which "
            "direction, and how consistent is that change across "
            "replicates?"
        ),
        dataset="`data/gene_expression.csv`",
        dataset_desc="180 rows. Log2 expression for 6 genes, control vs. treatment, 15 replicates each.",
        image="figures/04_expression_boxplot.png",
        image2="figures/04b_expression_violin_swarm.png",
        code=(
            'df = pd.read_csv("data/gene_expression.csv")\n'
            "fig, ax = categorical.expression_boxplot(df)\n\n"
            "# distribution shape + every replicate:\n"
            "fig, ax = categorical.expression_violin_swarm(df)"
        ),
        interpretation=(
            "`MYC` and `IL6` shift up under treatment, `TP53` and "
            "`CDKN1A` shift down, while the housekeeping genes `GAPDH` "
            "and `ACTB` show negligible change, as expected of genes "
            "that shouldn't respond to this treatment. The swarm overlay "
            "confirms these shifts hold across replicates rather than "
            "being driven by one or two outliers."
        ),
        requirements=[
            "one categorical x column (the groups being compared, e.g. gene or condition)",
            "one continuous y column (the measurement)",
            "optionally: a second categorical `hue` column for a grouped/split comparison",
        ],
        adapt_code=(
            'sns.boxplot(data=my_df, x="group_column", y="value_column", hue="condition_column")\n'
            'sns.violinplot(data=my_df, x="group_column", y="value_column", hue="condition_column", split=True)'
        ),
    ),
    dict(
        num="5",
        title="Regression & Nonlinear Curve Fitting: Enzyme Kinetics",
        plot_kind="Regression (lmplot) + SciPy curve_fit",
        what_it_is=(
            "`lmplot` visualizes a trend with uncertainty across groups. "
            "useful for a first look. But some biological questions need "
            "an actual mechanistic model, not just a trend line: here we "
            "also fit the real Michaelis-Menten equation with nonlinear "
            "least squares (`scipy.optimize.curve_fit`) and compare the "
            "fitted parameters directly, since visual inspection alone "
            "can't reliably distinguish inhibition mechanisms."
        ),
        question=(
            "Does a candidate inhibitor act competitively (raises "
            "apparent Km, Vmax unchanged) or non-competitively (lowers "
            "Vmax, Km unchanged)?"
        ),
        dataset="`data/enzyme_kinetics.csv`",
        dataset_desc="96 rows. Michaelis-Menten kinetics under no inhibitor / competitive / non-competitive inhibitor, 4 replicates each.",
        image="figures/05_enzyme_lmplot.png",
        code=(
            'df = pd.read_csv("data/enzyme_kinetics.csv")\n'
            "g = regression.enzyme_kinetics_lmplot(df)\n\n"
            "fit = regression.fit_michaelis_menten(df)\n"
            "print(fit)"
        ),
        code_output=(
            "        inhibitor        vmax        km\n"
            "0     competitive  103.29675  27.482396\n"
            "1  noncompetitive   54.27754   8.127880\n"
            "2            none  102.54479   8.591107"
        ),
        interpretation=(
            "The fitted parameters make the mechanism unambiguous: "
            "`competitive` raises Km roughly 3x with Vmax essentially "
            "unchanged; `noncompetitive` halves Vmax with Km unchanged, "
            "textbook signatures of each inhibition type, correctly "
            "recovered from noisy simulated data. `tests/test_bioviz.py` "
            "checks this holds within 15–20% of ground truth on every CI "
            "run, so a future bug in the fitting code would fail the "
            "build, not just look slightly off in a plot."
        ),
        requirements=[
            "one x column representing a dose/concentration/independent variable",
            "one y column representing the response",
            "optionally: a categorical `hue` column for the lmplot comparison",
            "for a real curve fit: choose (or write) a model function matching your system's known kinetics, don't default to a linear fit if the underlying process is nonlinear",
        ],
        adapt_code=(
            "from scipy.optimize import curve_fit\n\n"
            "def my_model(x, param1, param2):\n"
            "    return ...  # your mechanistic equation\n\n"
            'popt, pcov = curve_fit(my_model, my_df["x_column"], my_df["y_column"])'
        ),
    ),
    dict(
        num="6",
        title="Heatmap: Metabolite Correlation",
        plot_kind="Annotated correlation heatmap",
        what_it_is=(
            "A heatmap color-codes a matrix of values, most commonly a "
            "correlation matrix. With `annot=True` it also prints the "
            "numeric value in each cell, so a reader can verify a "
            "pattern directly instead of trusting color intensity alone. "
            "It's the fastest way to scan many pairwise relationships at "
            "once."
        ),
        question=(
            "Which metabolites co-vary across samples, and do those "
            "correlations reflect known pathway membership (glycolysis, "
            "TCA cycle, amino-acid pool)?"
        ),
        dataset="`data/metabolites.csv`",
        dataset_desc="60 rows. Targeted metabolomics panel, 9 metabolites drawn from 3 correlated latent pathway factors.",
        image="figures/06_metabolite_heatmap.png",
        code=('df = pd.read_csv("data/metabolites.csv")\nfig, ax = matrix.metabolite_corr_heatmap(df)'),
        interpretation=(
            "Three clear correlation blocks emerge: glycolysis "
            "(glucose/pyruvate/lactate), TCA cycle "
            "(citrate/α-ketoglutarate/succinate), and the amino-acid "
            "pool (glutamine/alanine/serine), matching the three latent "
            "pathway factors used to simulate the data. Serine shows "
            "weaker cross-correlation with the glycolytic block, "
            "reflecting its partial biosynthetic link via "
            "3-phosphoglycerate."
        ),
        requirements=[
            "a wide-format table: one row per sample, one column per numeric variable",
            "drop or exclude any ID columns before calling `.corr()`",
        ],
        adapt_code=(
            'numeric = my_df.drop(columns=["sample_id"])\n'
            'sns.heatmap(numeric.corr(), cmap="vlag", center=0, annot=True, fmt=".2f")'
        ),
    ),
    dict(
        num="7",
        title="Clustermap: Microbiome Composition",
        plot_kind="Clustermap",
        what_it_is=(
            "A clustermap is a heatmap with hierarchical clustering "
            "applied to both rows and columns, so similar samples and "
            "similar variables are grouped together automatically, "
            "revealing structure (like a natural split into subgroups) "
            "without you having to specify it in advance."
        ),
        question=(
            "Do gut and skin microbiome samples cluster separately based "
            "on species composition, and which taxa drive that "
            "separation?"
        ),
        dataset="`data/microbiome_abundance.csv`",
        dataset_desc="288 rows in long format: 12 species x 24 samples (12 gut, 12 skin), relative abundance.",
        image="figures/07_microbiome_clustermap.png",
        code=('df = pd.read_csv("data/microbiome_abundance.csv")\ng = matrix.microbiome_clustermap(df)'),
        interpretation=(
            "Samples cluster into two clean groups that correspond "
            "exactly to body site, and the species dendrogram separates "
            "gut-dominant taxa (*Bacteroides*, *Faecalibacterium*, "
            "*Prevotella*) from skin-dominant taxa (*Staphylococcus*, "
            "*Cutibacterium*, *Corynebacterium*), recovering the known "
            "ecological distinction between these two niches from "
            "composition data alone."
        ),
        requirements=[
            "long-format data with a sample column, a variable/feature column, and a value column",
            "pivot to wide format first (`pivot_table`): rows = features, columns = samples",
        ],
        adapt_code=(
            "piv = my_df.pivot_table(\n"
            '    index="feature_column", columns="sample_column",\n'
            '    values="value_column", fill_value=0,\n'
            ")\n"
            'sns.clustermap(piv, cmap="mako", z_score=0)'
        ),
    ),
    dict(
        num="8",
        title="Pairplot: Sequencing QC Metrics",
        plot_kind="Pairplot",
        what_it_is=(
            "A pairplot draws every pairwise scatter plot between a set "
            "of numeric columns, plus each column's marginal "
            "distribution on the diagonal, the fastest way to screen a "
            "QC table for artifacts or outliers across many metrics at "
            "once."
        ),
        question=(
            "Are there systematic relationships between QC metrics, for "
            "instance, do low-coverage samples also show more PCR "
            "duplication, and do any batches look like outliers?"
        ),
        dataset="`data/qc_metrics.csv`",
        dataset_desc="96 rows. Per-sample sequencing QC for a 96-sample batch across 3 sub-batches.",
        image="figures/08_qc_pairplot.png",
        code=('df = pd.read_csv("data/qc_metrics.csv")\ng = matrix.qc_pairplot(df)'),
        interpretation=(
            "`coverage_mean` and `duplicates_pct` are clearly negatively "
            "correlated: samples with lower coverage tend to show "
            "higher PCR duplication, a common artifact of low-input "
            "library preparation. `q30_pct` tracks the same latent "
            '"input quality" factor. No batch stands out as a '
            "systematic outlier."
        ),
        requirements=[
            "several numeric columns to compare pairwise (3–6 is usually the readable range)",
            "optionally: a categorical `hue` column to color points by group",
        ],
        adapt_code=(
            "sns.pairplot(\n"
            '    my_df, vars=["metric_1", "metric_2", "metric_3"],\n'
            '    hue="group_column", diag_kind="kde",\n'
            ")"
        ),
    ),
    dict(
        num="9",
        title="Jointplot: Trait Relationships by Clade",
        plot_kind="Jointplot (KDE)",
        what_it_is=(
            "A jointplot combines a bivariate relationship with each "
            'variable\'s marginal distribution. With `kind="kde"` and '
            "`hue`, it compares both the *shape/slope* of a relationship "
            "and the *location* of each group's distribution "
            "simultaneously, useful for spotting Simpson's-paradox-style "
            "situations where a pooled trend would misrepresent every "
            "individual group."
        ),
        question=(
            "Is the relationship between two morphological traits "
            "consistent across clades, or does it depend on which clade "
            "a sample belongs to?"
        ),
        dataset="`data/phylo_traits.csv`",
        dataset_desc="120 rows. Two continuous traits across 3 clades, each with its own allometric slope.",
        image="figures/09_phylo_jointplot.png",
        code=('df = pd.read_csv("data/phylo_traits.csv")\ng = matrix.phylo_traits_jointplot(df)'),
        interpretation=(
            "`Clade_B` is fully separated in trait-space with a shallow "
            "slope. `Clade_A` and `Clade_C` share a similar trait-1 "
            "range but visibly different slopes. `Clade_C` rises more "
            "steeply per unit of trait 1 than `Clade_A` does. Pooling "
            "all three clades into a single regression would blur both "
            "distinctions: it would average away Clade_B's separate "
            "location and Clade_A/C's different slopes, misrepresenting "
            "every individual clade's true relationship."
        ),
        requirements=[
            "two continuous columns (x and y)",
            "optionally: a categorical `hue` column to compare across groups",
            'if the legend overlaps your data, move it: `sns.move_legend(g.ax_joint, "upper left", bbox_to_anchor=(1.15, 1.2))`',
        ],
        adapt_code=(
            'g = sns.jointplot(data=my_df, x="trait_x", y="trait_y", hue="group_column", kind="kde", fill=True)\n'
            'sns.move_legend(g.ax_joint, "upper left", bbox_to_anchor=(1.15, 1.2))'
        ),
    ),
    dict(
        num="10",
        title="Annotated Heatmap: Pathway Status Counts",
        plot_kind="Annotated integer heatmap",
        what_it_is=(
            "The same annotated-heatmap technique as #6, applied to "
            "count data instead of correlations, useful whenever you "
            "have a small contingency-style table and want the reader to "
            "be able to verify the pattern from the printed numbers, not "
            "just color."
        ),
        question=(
            "How many upregulated, downregulated, and unchanged genes "
            "were assigned to each pathway?"
        ),
        dataset="`data/pathway_status_table.csv`",
        dataset_desc="6 rows. Descriptive gene counts per pathway and functional status.",
        image="figures/10_pathway_heatmap.png",
        code=(
            'df = pd.read_csv("data/pathway_status_table.csv")\nfig, ax = matrix.pathway_status_heatmap(df)'
        ),
        interpretation=(
            "`Apoptosis` has the largest upregulated count and "
            "`Cell_Cycle` the largest downregulated count. Calling either "
            "pathway enriched would require a background gene universe, "
            "a formal test, and multiple-testing correction."
        ),
        requirements=[
            "a table already shaped as rows × categories (a contingency table), with an index column to set as row labels",
        ],
        adapt_code=(
            'indexed = my_df.set_index("row_label_column")\n'
            'sns.heatmap(indexed, annot=True, fmt="d", cmap="crest")'
        ),
    ),
    dict(
        num="Bonus",
        title="Raw Matplotlib: Annotated QC Scatter",
        plot_kind="Matplotlib Figure/Axes API",
        what_it_is=(
            "Every Seaborn function returns real Matplotlib `Figure`/"
            "`Axes` objects. This bonus example (from "
            "`notebooks/matplotlib_practice.ipynb`) shows the raw API "
            "underneath, useful when you need custom annotations, "
            "flagged points, or manual multi-panel layouts that Seaborn "
            "doesn't expose directly."
        ),
        question=(
            "Which specific samples fail a QC coverage threshold, and "
            "can they be flagged directly on the plot for a lab notebook "
            "or report?"
        ),
        dataset="`data/qc_metrics.csv`",
        dataset_desc="Same QC dataset as #8, viewed through raw Matplotlib instead of Seaborn.",
        image="figures/practice_annotated_qc.png",
        code=(
            "import matplotlib.pyplot as plt\n\n"
            "fig, ax = plt.subplots(figsize=(6, 4.5))\n"
            'ax.scatter(df["coverage_mean"], df["duplicates_pct"], alpha=0.5, color="gray")\n\n'
            'low_cov = df[df["coverage_mean"] < 30]\n'
            'ax.scatter(low_cov["coverage_mean"], low_cov["duplicates_pct"], color="crimson", label="coverage < 30x")\n'
            'ax.axvline(30, color="crimson", linestyle="--", linewidth=1)\n'
            "ax.legend()"
        ),
        interpretation=(
            "A handful of samples fall below the 30x coverage threshold "
            "and are flagged in red directly on the plot. This pattern "
            "(compute a subset, plot it again in a different color on "
            "the same Axes) is the general recipe for highlighting "
            "outliers or QC failures in any Matplotlib/Seaborn figure."
        ),
        requirements=[
            "any DataFrame; this technique layers on top of any scatter/line plot",
            "a boolean filter defining the subset you want to highlight",
        ],
        adapt_code=(
            "fig, ax = plt.subplots()\n"
            'ax.scatter(my_df["x"], my_df["y"], alpha=0.5, color="gray")\n'
            'flagged = my_df[my_df["x"] < threshold]\n'
            'ax.scatter(flagged["x"], flagged["y"], color="crimson", label="flagged")\n'
            "ax.legend()"
        ),
    ),
]


def render_section(s: dict) -> str:
    lines = []
    lines.append(f"### {s['num']}. {s['title']}\n")
    lines.append(f"**Plot type:** {s['plot_kind']}\n")
    lines.append(f"**What this plot type is for:** {s['what_it_is']}\n")
    lines.append(f"**Biological question:** {s['question']}\n")
    lines.append(f"**Dataset:** {s['dataset']}. {s['dataset_desc']}\n")
    lines.append("**Create this figure:**\n")
    lines.append(f"```python\n{s['code']}\n```\n")
    if s.get("code_output"):
        lines.append(f"```text\n{s['code_output']}\n```\n")
    lines.append(f"![{s['title']}]({s['image']})\n")
    if s.get("image2"):
        lines.append(f"![{s['title']} (2)]({s['image2']})\n")
    lines.append(f"**Interpretation:** {s['interpretation']}\n")
    lines.append("**Requirements to use this on your own data:**\n")
    for req in s["requirements"]:
        lines.append(f"- {req}")
    lines.append("")
    lines.append("**Adapted code for your own DataFrame:**\n")
    lines.append(f"```python\n{s['adapt_code']}\n```\n")
    lines.append("---\n")
    return "\n".join(lines)


def main() -> None:
    print("## Full Tutorial: Every Plot, Explained\n")
    print(
        "For each plot below: what the plot type is for, the biological "
        "question it answers here, the exact code that produces it, an "
        "interpretation of the actual result, and what you'd need to use "
        "it on your own data. This mirrors "
        "`notebooks/seaborn_beginner_guide.ipynb` exactly. Every snippet "
        "below is executed end-to-end in CI on every push.\n"
    )
    print(
        "```python\n"
        "import pandas as pd\n"
        "from bioviz import theme, relational, distributions, categorical, regression, matrix\n\n"
        "theme.set_theme()\n"
        "```\n"
    )
    print("---\n")
    for s in SECTIONS:
        print(render_section(s))


if __name__ == "__main__":
    main()
