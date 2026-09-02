# Data Dictionary

All datasets in this repository are **simulated** (not real experimental
data) using [`scripts/generate_datasets.py`](../scripts/generate_datasets.py),
with a fixed random seed (`np.random.default_rng(42)`) so results are
exactly reproducible. Each dataset is built with a specific biological
and statistical rationale. The goal is to give every plot type in the
tutorial genuine, interpretable signal rather than arbitrary numbers.
Full rationale for each dataset is documented as a docstring in the
generation script; this file summarizes the resulting schema.

---

### `docking_scores.csv` (360 rows)
Simulated virtual-screening results against 3 protein targets.

| Column | Type | Description |
|---|---|---|
| `target` | str | Protein target (`Kinase_A`, `Protease_B`, `GPCR_C`) |
| `ligand_id` | str | Unique ligand identifier |
| `logP` | float | Simulated lipophilicity |
| `molecular_weight` | float | Simulated molecular weight (Da) |
| `ring_count` | int | Number of ring systems |
| `vina_score` | float | Docking score, kcal/mol (more negative = stronger binding) |

### `timecourse_cytokines.csv` (140 rows)
IL-6 response to LPS challenge, vehicle vs. anti-IL-6R antibody, 10 subjects/arm.

| Column | Type | Description |
|---|---|---|
| `subject_id` | str | Subject identifier |
| `treatment` | str | `Vehicle` or `Anti-IL6R_Ab` |
| `time_h` | int | Hours post-challenge (0, 1, 2, 4, 8, 12, 24) |
| `IL6` | float | Simulated IL-6 concentration (pg/mL) |

### `variants.csv` (2000 rows)
Simulated variant call set with functional consequence and allele frequency.

| Column | Type | Description |
|---|---|---|
| `variant_id` | str | Simulated rsID |
| `chromosome` | int | Chromosome (1-22) |
| `consequence` | str | `synonymous`, `missense`, or `loss_of_function` |
| `allele_frequency` | float | Simulated population allele frequency (0-1) |

### `gene_expression.csv` (180 rows)
log2 expression for 6 genes, control vs. treatment, 15 replicates/condition.

| Column | Type | Description |
|---|---|---|
| `gene` | str | Gene symbol |
| `direction` | str | Ground-truth simulated direction: `up`, `down`, `unchanged` |
| `condition` | str | `control` or `treatment` |
| `replicate` | int | Replicate index |
| `expression` | float | Simulated log2 expression |

### `enzyme_kinetics.csv` (96 rows)
Michaelis-Menten kinetics under no inhibitor, a competitive inhibitor, and a non-competitive inhibitor.

| Column | Type | Description |
|---|---|---|
| `inhibitor` | str | `none`, `competitive`, `noncompetitive` |
| `replicate` | int | Replicate index (4 per condition) |
| `substrate_conc` | float | Substrate concentration (arbitrary units) |
| `rate` | float | Simulated reaction rate |

Ground truth: `none` → Vmax=100, Km=8. `competitive` → Vmax=100, Km=24
(Km raised, Vmax unchanged). `noncompetitive` → Vmax=55, Km=8 (Vmax
lowered, Km unchanged). See `bioviz.regression.fit_michaelis_menten`.

### `metabolites.csv` (60 rows)
Wide-format targeted metabolomics panel, 9 metabolites drawn from 3 correlated latent pathway factors.

| Column | Type | Description |
|---|---|---|
| `sample_id` | str | Sample identifier |
| `glucose`, `pyruvate`, `lactate` | float | Glycolysis-pathway-correlated metabolites |
| `citrate`, `alpha_ketoglutarate`, `succinate` | float | TCA-cycle-correlated metabolites |
| `glutamine`, `alanine`, `serine` | float | Amino-acid-pool-correlated metabolites |

### `microbiome_abundance.csv` (288 rows)
Long-format relative abundance, 12 species x 24 samples (12 gut, 12 skin), Dirichlet-simulated so each sample sums to 1.

| Column | Type | Description |
|---|---|---|
| `sample` | str | Sample identifier |
| `body_site` | str | `gut` or `skin` |
| `species` | str | Species name |
| `relative_abundance` | float | Relative abundance (0-1, sums to 1 per sample) |

### `qc_metrics.csv` (96 rows)
Per-sample sequencing QC for a 96-sample batch across 3 sub-batches.

| Column | Type | Description |
|---|---|---|
| `sample_id` | str | Sample identifier |
| `batch` | str | `batch_1`, `batch_2`, `batch_3` |
| `coverage_mean` | float | Mean sequencing coverage (X) |
| `duplicates_pct` | float | PCR duplication rate (%) |
| `gc_content` | float | GC content (%) |
| `q30_pct` | float | Fraction of bases with Q30+ quality (%) |

`coverage_mean` and `duplicates_pct` are simulated to be negatively
correlated (low-input artifact).

### `phylo_traits.csv` (120 rows)
Two continuous morphological traits across 3 clades with clade-specific allometric slopes.

| Column | Type | Description |
|---|---|---|
| `clade` | str | `Clade_A`, `Clade_B`, `Clade_C` |
| `trait1` | float | Simulated trait (e.g., body-size proxy) |
| `trait2` | float | Simulated trait (e.g., metabolic-rate proxy), clade-specific slope on trait1 |

### `pathway_status_table.csv` (6 rows)
Pathway by differential-expression-status gene counts. This is a descriptive
contingency table, not a formal enrichment analysis.

| Column | Type | Description |
|---|---|---|
| `pathway` | str | Pathway name |
| `Upregulated` | int | Gene count |
| `Downregulated` | int | Gene count |
| `Unchanged` | int | Gene count |

The larger counts are designed to be visually apparent. Enrichment would
additionally require a gene universe, a statistical test, and multiple-testing
correction.

### `differential_expression.csv` (1200 rows)

Analysis-ready differential-expression summary with balanced simulated
positive and negative effects.

| Column | Type | Description |
|---|---|---|
| `gene` | str | Simulated gene identifier |
| `base_mean` | float | Mean normalized abundance |
| `log2_fold_change` | float | Observed treatment effect |
| `lfc_se` | float | Standard error of the log2 fold change |
| `p_value` | float | Two-sided p-value from the simulated z statistic |
| `padj` | float | Benjamini-Hochberg adjusted p-value |
| `truth` | str | Simulation truth: `up`, `down`, or `unchanged` |

### `pangenome_presence_absence.csv` (36 rows)

Binary gene-family presence-absence matrix for three structured lineages.

| Column | Type | Description |
|---|---|---|
| `genome_id` | str | Genome identifier |
| `lineage` | str | Simulated evolutionary lineage |
| `habitat` | str | Host, soil, or water metadata |
| `GF_0000` ... `GF_0099` | int | Binary gene-family indicators |

### `pangenome_gene_summary.csv` (100 rows)

Prevalence summary calculated directly from the binary matrix.

| Column | Type | Description |
|---|---|---|
| `gene_family` | str | Gene-family identifier |
| `genomes_present` | int | Number of genomes containing the family |
| `prevalence` | float | Fraction of genomes containing the family |
| `frequency_class` | str | Core (100%), soft core (95 to <100%), shell (15 to <95%), or cloud (<15%) |
