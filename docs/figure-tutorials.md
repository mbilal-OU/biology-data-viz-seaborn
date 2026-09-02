# Seaborn figure tutorials for biological data

Every tutorial connects one rendered figure to its data, reusable function,
own-data workflow, and interpretation boundary. Run commands from the repository
root after installation. The bundled tables are seeded simulations.

```python
import pandas as pd
from bioviz import categorical, distributions, matrix, omics, regression, relational, theme

theme.set_theme()
```

## 01 Docking-score relationship

- **Use when:** two continuous variables may be associated and groups should be
  encoded by color or marker semantics.
- **Inputs:** [`docking_scores.csv`](../data/docking_scores.csv), including
  `logp`, `vina_score`, `target`, and `ring_count`.
- **Code:** [`relational.docking_scatter`](../bioviz/relational.py) creates the
  figure. Replace the file path in
  `relational.docking_scatter(pd.read_csv("my_scores.csv"))` after preserving or
  renaming your columns to the documented schema.
- **Interpret:** compare direction, curvature, dispersion, and target overlap.
  A visual relationship among simulated docking scores is not binding affinity,
  causation, or experimental validation.

## 02 Cytokine time course

- **Use when:** repeated responses are measured across ordered time points.
- **Inputs:** [`timecourse_cytokines.csv`](../data/timecourse_cytokines.csv),
  with subject, time, condition, and cytokine value columns.
- **Code:** call [`relational.cytokine_timecourse`](../bioviz/relational.py) on
  `pd.read_csv("my_timecourse.csv")`. Keep one row per subject-time observation.
- **Interpret:** inspect timing, peak response, recovery, and between-subject
  variation. SD-band overlap is not a significance test. Use an appropriate
  repeated-measures model for inference.

## 03 Variant-frequency histogram

- **Use when:** distribution shape and frequency bins are scientifically useful.
- **Inputs:** [`variants.csv`](../data/variants.csv), especially allele frequency
  and consequence class.
- **Code:** [`distributions.variant_af_histogram`](../bioviz/distributions.py).
  Supply a DataFrame with allele frequencies bounded from 0 to 1 and documented
  consequence labels.
- **Interpret:** compare modes, skew, tails, and rare-variant concentration.
  Conclusions depend on bin width, ascertainment, sample size, and filtering.

## 03b Variant-frequency ECDF

- **Use when:** a bin-free cumulative comparison is more informative than a
  histogram.
- **Inputs:** the same [`variants.csv`](../data/variants.csv) table as tutorial
  03.
- **Code:** [`distributions.variant_af_ecdf`](../bioviz/distributions.py). Use
  `distributions.variant_af_ecdf(pd.read_csv("my_variants.csv"))`.
- **Interpret:** at any x value, the curve gives the fraction of observations at
  or below that frequency. Separation describes distributions, not a formal
  test or selection mechanism.

## 04 Expression box plot

- **Use when:** medians, quartiles, ranges, and potential outliers should be
  compared across genes and conditions.
- **Inputs:** [`gene_expression.csv`](../data/gene_expression.csv), in tidy
  replicate-level format.
- **Code:** [`categorical.expression_boxplot`](../bioviz/categorical.py). For
  personal data, retain one row per biological replicate and explicit gene and
  condition columns.
- **Interpret:** compare location and spread, while checking sample counts.
  Box-plot separation is not equivalent to differential-expression inference.

## 04b Expression violin and swarm

- **Use when:** both distribution shape and every observed replicate should be
  visible.
- **Inputs:** the same [`gene_expression.csv`](../data/gene_expression.csv)
  contract as tutorial 04.
- **Code:** [`categorical.expression_violin_swarm`](../bioviz/categorical.py).
  Use personal long-format data and avoid a violin density for very small n.
- **Interpret:** look for multimodality, imbalance, and outlier-driven summaries.
  The density is an estimate whose appearance depends on bandwidth.

## 05 Enzyme-response regression

- **Use when:** groups have response trends and a mechanistic model may be fitted
  separately from the visualization.
- **Inputs:** [`enzyme_kinetics.csv`](../data/enzyme_kinetics.csv), with substrate
  concentration, velocity, inhibitor condition, and replicate identity.
- **Code:** [`regression.enzyme_kinetics_lmplot`](../bioviz/regression.py)
  visualizes trends; [`regression.fit_michaelis_menten`](../bioviz/regression.py)
  fits the declared model. Pass a matching personal DataFrame to both.
- **Interpret:** compare fitted Vmax and Km only after checking residuals,
  uncertainty, identifiability, and whether Michaelis-Menten assumptions apply.

## 06 Metabolite correlation heatmap

- **Use when:** many pairwise associations in a numeric feature matrix need a
  compact overview.
- **Inputs:** [`metabolites.csv`](../data/metabolites.csv), one sample per row and
  one metabolite per numeric column.
- **Code:** [`matrix.metabolite_corr_heatmap`](../bioviz/matrix.py). Remove ID and
  metadata columns before passing your own numeric matrix.
- **Interpret:** blocks indicate co-variation under the chosen correlation
  measure. They do not establish a shared pathway, regulation, or causation.

## 07 Microbiome clustermap

- **Use when:** exploratory sample and taxon structure should be viewed together.
- **Inputs:** [`microbiome_abundance.csv`](../data/microbiome_abundance.csv), one
  sample-taxon observation per row.
- **Code:** [`matrix.microbiome_clustermap`](../bioviz/matrix.py). For personal
  data, define zero handling and a composition-aware transformation and distance
  before clustering.
- **Interpret:** dendrograms reflect the selected transformation, distance,
  linkage, and filtering. Clusters are not independently validated populations.

## 08 Sequencing-QC pairplot

- **Use when:** several numeric QC metrics must be screened for correlations,
  batch effects, and outliers.
- **Inputs:** [`qc_metrics.csv`](../data/qc_metrics.csv), one library per row.
- **Code:** [`matrix.qc_pairplot`](../bioviz/matrix.py). Rename your columns to
  the documented metrics or adapt the function's `vars` list.
- **Interpret:** use the panels to identify candidates for review. QC thresholds
  are protocol-specific and should not be copied without justification.

## 09 Trait association with marginals

- **Use when:** a two-trait relationship and both marginal distributions should
  be compared among clades or groups.
- **Inputs:** [`phylo_traits.csv`](../data/phylo_traits.csv), with two traits and
  a clade label.
- **Code:** [`matrix.phylo_traits_jointplot`](../bioviz/matrix.py). Substitute a
  tidy personal table with the same semantic roles.
- **Interpret:** a clade-colored association is descriptive. Shared ancestry is
  not corrected by coloring points, so phylogenetic comparative methods may be
  required.

## 10 Pathway count heatmap

- **Use when:** a small table of observed categorical counts needs direct visual
  comparison.
- **Inputs:** [`pathway_status_table.csv`](../data/pathway_status_table.csv).
- **Code:** [`matrix.pathway_status_heatmap`](../bioviz/matrix.py). Pass a table
  with pathways as rows and mutually defined status categories as columns.
- **Interpret:** the cells report counts only. Enrichment requires a tested gene
  universe, an appropriate test, and multiple-testing correction.

## 11 Differential-expression dashboard

- **Use when:** effect size, mean abundance, and adjusted evidence should be
  assessed together.
- **Inputs:** [`differential_expression.csv`](../data/differential_expression.csv)
  containing gene IDs, log2 fold changes, mean abundance, and adjusted p-values.
- **Code:** [`omics.volcano_plot`](../bioviz/omics.py) and
  [`omics.ma_plot`](../bioviz/omics.py), assembled by
  [`build_advanced_gallery.py`](../scripts/build_advanced_gallery.py). Replace the
  CSV path and retain the required columns.
- **Interpret:** selected points pass declared display thresholds. The plot does
  not perform normalization, model fitting, shrinkage, or multiple testing.

## 12 Pangenome population structure

- **Use when:** gene-frequency classes and low-dimensional sample structure are
  needed from one presence-absence matrix.
- **Inputs:** [`pangenome_presence_absence.csv`](../data/pangenome_presence_absence.csv)
  and [`pangenome_gene_summary.csv`](../data/pangenome_gene_summary.csv).
- **Code:** [`omics.pangenome_frequency_spectrum`](../bioviz/omics.py) and
  [`omics.pangenome_pca_plot`](../bioviz/omics.py). Personal gene columns must be
  binary, with genome identifiers kept separate.
- **Interpret:** the spectrum depends on category thresholds; PCA is an
  exploratory projection and does not prove discrete biological populations.

## 13 Pangenome Jaccard clustermap

- **Use when:** genomes should be grouped by shared accessory-gene content.
- **Inputs:** the binary [`pangenome_presence_absence.csv`](../data/pangenome_presence_absence.csv)
  matrix.
- **Code:** [`omics.pangenome_clustermap`](../bioviz/omics.py). Provide one
  genome per row, one binary gene family per column, and a separate ID column.
- **Interpret:** similarity depends on gene calling, clustering threshold,
  missingness, sampling, Jaccard distance, and linkage choice.

## 14 CLR microbiome clustermap

- **Use when:** relative microbial composition should be explored in log-ratio
  coordinates.
- **Inputs:** [`microbiome_abundance.csv`](../data/microbiome_abundance.csv).
- **Code:** [`omics.microbiome_clr_clustermap`](../bioviz/omics.py). Personal
  counts must be nonnegative. Choose and report a defensible zero-replacement
  strategy before CLR transformation.
- **Interpret:** heatmap values are CLR coordinates, not proportions. Clusters
  remain sensitive to filtering, replacement, distance, and linkage.

## Practice annotated QC

- **Use when:** samples crossing a declared threshold should be directly
  identified in a report or lab notebook.
- **Inputs:** [`qc_metrics.csv`](../data/qc_metrics.csv).
- **Code:** the worked example is in
  [`matplotlib_practice.py`](../notebooks/matplotlib_practice.py). Substitute your
  own x/y metrics and a protocol-justified Boolean rule.
- **Interpret:** flags identify records for review. They do not automatically
  establish assay failure or justify exclusion.

## Reproduce the complete gallery

```bash
python scripts/generate_datasets.py
python scripts/build_advanced_gallery.py
pytest -q
```

See the [data dictionary](../data/data_dictionary.md) for every column and the
[scientific methods notes](methods.md) for cross-cutting limitations.
