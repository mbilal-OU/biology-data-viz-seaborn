# Advanced Gallery

## Differential expression

![Volcano and MA plots](https://raw.githubusercontent.com/mbilal-OU/biology-data-viz-seaborn/main/figures/11_differential_expression_dashboard.png)

Both effect magnitude and adjusted evidence are visible. The MA panel provides
an abundance-aware complement to the volcano plot.

Source: [`bioviz/omics.py`](https://github.com/mbilal-OU/biology-data-viz-seaborn/blob/main/bioviz/omics.py)

## Pangenome structure

![Pangenome frequency and PCA](https://raw.githubusercontent.com/mbilal-OU/biology-data-viz-seaborn/main/figures/12_pangenome_structure.png)

The left panel reports gene-family counts using explicit prevalence thresholds.
The right panel calculates PCA directly from variable binary gene families.

![Pangenome clustermap](https://raw.githubusercontent.com/mbilal-OU/biology-data-viz-seaborn/main/figures/13_pangenome_clustermap.png)

The clustermap uses Jaccard distance for binary presence-absence data. Lineage
color is annotation, not an input to clustering.

## Compositional microbiome data

![CLR microbiome clustermap](https://raw.githubusercontent.com/mbilal-OU/biology-data-viz-seaborn/main/figures/14_microbiome_clr_clustermap.png)

Samples are clustered in centered-log-ratio coordinates. The zero-replacement
rule is documented in the function and notebook.

## Core statistical patterns

The repository also contains distribution, categorical, regression, time-course,
correlation, QC, and annotated-count examples. See the
[core-pattern notebook](https://github.com/mbilal-OU/biology-data-viz-seaborn/blob/main/notebooks/seaborn_beginner_guide.ipynb)
for their code and interpretation.
