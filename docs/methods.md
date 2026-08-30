# Methods and Guardrails

## Differential expression

The plotting functions consume an analysis-ready table. They do not estimate
dispersion, fit a count model, or calculate normalization factors. A point is
highlighted only if it crosses both the adjusted-p-value and absolute effect-size
thresholds.

## Pangenome structure

PCA centers variable binary gene-family columns. It is an exploratory Euclidean
projection. The clustermap uses Jaccard distance and average linkage. Neither
view proves that clusters are independent populations.

Frequency classes in the simulated example are:

| Class | Prevalence |
|---|---:|
| Core | 100% |
| Soft core | 95% to less than 100% |
| Shell | 15% to less than 95% |
| Cloud | Less than 15% |

Thresholds vary among tools and studies, so they are reported rather than
treated as universal definitions.

## Microbiome composition

Zeros are replaced by half the smallest positive abundance, samples are
renormalized, and a centered-log-ratio transform is applied. Euclidean distance
in CLR space is Aitchison distance. Different zero-handling strategies can
change results and should be reported for real studies.

## Uncertainty

SD bands describe observed variability. Confidence intervals describe
uncertainty in an estimated quantity under a model. Neither should be judged as
a significance test solely from visual overlap.

## Pathway counts

A heatmap of gene counts is descriptive. Enrichment additionally requires a
background gene universe, a test such as Fisher's exact or a ranked-set method,
and multiple-testing correction.
