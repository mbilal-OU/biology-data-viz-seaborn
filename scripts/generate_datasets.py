"""
generate_datasets.py
=====================
Simulates every dataset used in this repository with an explicit,
documented biological and statistical rationale (effect sizes, noise
models, group structure). Re-running this script regenerates the data
deterministically (seeded) so results in the notebooks are reproducible.

Usage:
    python scripts/generate_datasets.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
OUT = Path(__file__).resolve().parents[1] / "data"
OUT.mkdir(exist_ok=True)


def save(df: pd.DataFrame, name: str) -> None:
    path = OUT / name
    df.to_csv(path, index=False)
    print(f"wrote {path}  ({len(df)} rows, {len(df.columns)} cols)")


# ---------------------------------------------------------------------------
# 1. docking_scores.csv  -- virtual screening / molecular docking
# ---------------------------------------------------------------------------
def gen_docking_scores(n_per_target: int = 120) -> pd.DataFrame:
    """
    Simulates a virtual screening campaign against 3 protein targets.
    vina_score (kcal/mol, more negative = better binding) is modeled as a
    function of logP (lipophilicity) with a target-specific optimum
    (inverted-U, since very hydrophilic/hydrophobic ligands both dock
    poorly), plus noise. ring_count drives point size in the tutorial.
    """
    targets = {"Kinase_A": -7.5, "Protease_B": -6.8, "GPCR_C": -8.2}
    rows = []
    for target, best_score in targets.items():
        logP = RNG.normal(2.5, 1.3, n_per_target)
        optimal_logP = 2.8 if target != "GPCR_C" else 3.6
        penalty = 0.35 * (logP - optimal_logP) ** 2
        vina = best_score + penalty + RNG.normal(0, 0.6, n_per_target)
        ring_count = RNG.poisson(2.2, n_per_target) + 1
        mw = RNG.normal(380, 60, n_per_target).clip(180, 600)
        rows.append(
            pd.DataFrame(
                {
                    "target": target,
                    "ligand_id": [f"{target[:3].upper()}_{i:04d}" for i in range(n_per_target)],
                    "logP": logP.round(2),
                    "molecular_weight": mw.round(1),
                    "ring_count": ring_count,
                    "vina_score": vina.round(2),
                }
            )
        )
    return pd.concat(rows, ignore_index=True)


# ---------------------------------------------------------------------------
# 2. timecourse_cytokines.csv -- inflammatory time course
# ---------------------------------------------------------------------------
def gen_timecourse_cytokines(n_subjects: int = 10) -> pd.DataFrame:
    """
    IL-6 response over 24h following LPS challenge, comparing vehicle vs.
    an anti-inflammatory treatment. Uses a gamma-shaped response curve
    (rapid rise, slow decay) typical of acute cytokine kinetics, with
    the treatment arm damping peak amplitude ~55%. Subject-level random
    effects create realistic between-subject variability for errorbar
    (sd) bands in the lineplot.
    """
    timepoints = np.array([0, 1, 2, 4, 8, 12, 24])
    rows = []
    for treatment, amp_scale in [("Vehicle", 1.0), ("Anti-IL6R_Ab", 0.45)]:
        for subj in range(n_subjects):
            subj_amp = amp_scale * RNG.normal(1.0, 0.15)
            peak_time = RNG.normal(4, 0.5)
            # Gamma-like pulse: rise then decay
            shape_k, shape_theta = 2.0, peak_time / 2.0
            response = (
                60
                * subj_amp
                * (timepoints ** shape_k)
                * np.exp(-timepoints / shape_theta)
                / (shape_theta ** shape_k * np.exp(-shape_k))
            )
            noise = RNG.normal(0, 2.5, len(timepoints))
            il6 = np.clip(response + noise, 0.5, None)
            rows.append(
                pd.DataFrame(
                    {
                        "subject_id": f"{treatment[:3]}_{subj:02d}",
                        "treatment": treatment,
                        "time_h": timepoints,
                        "IL6": il6.round(2),
                    }
                )
            )
    return pd.concat(rows, ignore_index=True)


# ---------------------------------------------------------------------------
# 3. variants.csv -- variant allele frequencies from a sequencing panel
# ---------------------------------------------------------------------------
def gen_variants(n: int = 2000) -> pd.DataFrame:
    """
    Allele frequency spectrum split by functional consequence class.
    Synonymous variants follow the classic neutral-theory shape skewed
    toward rare alleles (Beta(0.4, 6)); missense variants are shifted
    further toward rare (purifying selection, Beta(0.3, 9)); a small
    class of likely-benign common variants (Beta(2, 2)) represents
    variants that have drifted/fixed toward intermediate-to-high
    frequency, giving histplot/KDE/ECDF genuinely distinct shapes.
    """
    consequence_params = {
        "synonymous": (0.4, 6.0, int(n * 0.45)),
        "missense": (0.3, 9.0, int(n * 0.40)),
        "common_benign": (2.0, 2.0, int(n * 0.15)),
    }
    rows = []
    for consequence, (a, b, count) in consequence_params.items():
        af = RNG.beta(a, b, count)
        chrom = RNG.integers(1, 23, count)
        rows.append(
            pd.DataFrame(
                {
                    "variant_id": [f"rs{RNG.integers(1e6, 9e6)}" for _ in range(count)],
                    "chromosome": chrom,
                    "consequence": consequence,
                    "allele_frequency": af.round(5),
                }
            )
        )
    return pd.concat(rows, ignore_index=True)


# ---------------------------------------------------------------------------
# 4. gene_expression.csv -- differential expression, control vs treatment
# ---------------------------------------------------------------------------
def gen_gene_expression(n_replicates: int = 15) -> pd.DataFrame:
    """
    log2 expression for 6 genes under control vs. treatment, with three
    ground-truth behaviours baked in so the boxplot/violin/swarm tutorial
    has real signal to interpret: two upregulated genes, two
    downregulated genes, two unaffected (null) genes. Expression is
    modeled log-normally (standard for RNA-seq-like count data).
    """
    genes = {
        "TP53": ("down", -1.2),
        "MYC": ("up", 1.6),
        "GAPDH": ("null", 0.0),
        "IL6": ("up", 2.1),
        "ACTB": ("null", 0.05),
        "CDKN1A": ("down", -0.8),
    }
    rows = []
    for gene, (direction, effect) in genes.items():
        baseline = RNG.normal(8.0, 0.4)
        for condition, delta in [("control", 0.0), ("treatment", effect)]:
            expr = baseline + delta + RNG.normal(0, 0.35, n_replicates)
            rows.append(
                pd.DataFrame(
                    {
                        "gene": gene,
                        "direction": direction,
                        "condition": condition,
                        "replicate": np.arange(n_replicates),
                        "expression": expr.round(3),
                    }
                )
            )
    return pd.concat(rows, ignore_index=True)


# ---------------------------------------------------------------------------
# 5. enzyme_kinetics.csv -- Michaelis-Menten with an inhibitor
# ---------------------------------------------------------------------------
def gen_enzyme_kinetics(n_reps: int = 4) -> pd.DataFrame:
    """
    Classic Michaelis-Menten saturation curve, v = Vmax*[S]/(Km+[S]),
    simulated for no-inhibitor vs. a competitive inhibitor (raises
    apparent Km, Vmax unchanged) vs. a noncompetitive inhibitor (lowers
    Vmax, Km unchanged). This gives lmplot's regression fits real
    (nonlinear, faceted-by-eye-linear-ish in log range) structure to
    discuss rather than an arbitrary linear trend.
    """
    substrate = np.array([0.5, 1, 2, 4, 8, 16, 32, 64])
    conditions = {
        "none": dict(vmax=100, km=8),
        "competitive": dict(vmax=100, km=24),
        "noncompetitive": dict(vmax=55, km=8),
    }
    rows = []
    for inhibitor, params in conditions.items():
        for rep in range(n_reps):
            v = params["vmax"] * substrate / (params["km"] + substrate)
            v_noisy = v + RNG.normal(0, 2.5, len(substrate))
            rows.append(
                pd.DataFrame(
                    {
                        "inhibitor": inhibitor,
                        "replicate": rep,
                        "substrate_conc": substrate,
                        "rate": v_noisy.round(2),
                    }
                )
            )
    return pd.concat(rows, ignore_index=True)


# ---------------------------------------------------------------------------
# 6. metabolites.csv -- targeted metabolomics panel (samples x metabolites)
# ---------------------------------------------------------------------------
def gen_metabolites(n_samples: int = 60) -> pd.DataFrame:
    """
    Wide-format metabolomics table (rows = samples, columns = metabolite
    levels) used for sns.heatmap(df.corr()). Metabolites are drawn from
    correlated latent pathway "factors" (glycolysis, TCA cycle, amino
    acid pool) so the correlation heatmap shows genuine block structure
    instead of random noise.
    """
    glycolysis_factor = RNG.normal(0, 1, n_samples)
    tca_factor = RNG.normal(0, 1, n_samples)
    aa_factor = RNG.normal(0, 1, n_samples)

    def make(factor, loading, name_noise=0.4):
        return factor * loading + RNG.normal(0, name_noise, n_samples)

    df = pd.DataFrame(
        {
            "sample_id": [f"S{idx:03d}" for idx in range(n_samples)],
            "glucose": make(glycolysis_factor, 1.0),
            "pyruvate": make(glycolysis_factor, 0.85),
            "lactate": make(glycolysis_factor, 0.7),
            "citrate": make(tca_factor, 1.0),
            "alpha_ketoglutarate": make(tca_factor, 0.8),
            "succinate": make(tca_factor, 0.75),
            "glutamine": make(aa_factor, 0.9),
            "alanine": make(aa_factor, 0.8),
            "serine": make(aa_factor, 0.6) + make(glycolysis_factor, 0.3, 0.3),
        }
    )
    for col in df.columns[1:]:
        df[col] = df[col].round(3)
    return df


# ---------------------------------------------------------------------------
# 7. microbiome_abundance.csv -- long-format relative abundance
# ---------------------------------------------------------------------------
def gen_microbiome_abundance(n_samples: int = 24) -> pd.DataFrame:
    """
    16S-style relative abundance table, long format (species x sample),
    for two body-site groups (gut vs. skin) with distinct dominant taxa,
    generated via a Dirichlet distribution per sample (guarantees each
    sample's abundances sum to 1, as true relative abundance data must)
    so clustermap(z_score=0) reveals real site-driven clustering.
    """
    species = [
        "Bacteroides_fragilis", "Faecalibacterium_prausnitzii", "Escherichia_coli",
        "Lactobacillus_acidophilus", "Prevotella_copri", "Bifidobacterium_longum",
        "Staphylococcus_epidermidis", "Cutibacterium_acnes", "Corynebacterium_striatum",
        "Streptococcus_mitis", "Akkermansia_muciniphila", "Ruminococcus_bromii",
    ]
    gut_alpha = np.array([8, 7, 3, 4, 6, 5, 0.5, 0.3, 0.4, 1, 3, 4])
    skin_alpha = np.array([0.3, 0.2, 1, 0.5, 0.2, 0.3, 9, 7, 6, 2, 0.2, 0.2])

    rows = []
    for site, alpha in [("gut", gut_alpha), ("skin", skin_alpha)]:
        for s in range(n_samples // 2):
            props = RNG.dirichlet(alpha)
            rows.append(
                pd.DataFrame(
                    {
                        "sample": f"{site}_{s:02d}",
                        "body_site": site,
                        "species": species,
                        "relative_abundance": props.round(5),
                    }
                )
            )
    return pd.concat(rows, ignore_index=True)


# ---------------------------------------------------------------------------
# 8. qc_metrics.csv -- sequencing run QC
# ---------------------------------------------------------------------------
def gen_qc_metrics(n_samples: int = 96) -> pd.DataFrame:
    """
    Per-sample sequencing QC metrics for a 96-sample batch, drawn so
    that coverage_mean and duplicates_pct are negatively correlated
    (low-input samples tend to have both lower coverage and higher PCR
    duplication -- a real, commonly observed artifact), giving
    pairplot() genuine off-diagonal structure.
    """
    input_quality = RNG.beta(5, 2, n_samples)  # proxy latent factor
    coverage_mean = 25 + 55 * input_quality + RNG.normal(0, 4, n_samples)
    duplicates_pct = 35 - 25 * input_quality + RNG.normal(0, 3, n_samples)
    gc_content = RNG.normal(41, 2.5, n_samples)
    q30_pct = 88 + 8 * input_quality + RNG.normal(0, 1.5, n_samples)
    batch = RNG.choice(["batch_1", "batch_2", "batch_3"], n_samples)

    df = pd.DataFrame(
        {
            "sample_id": [f"SMP{idx:03d}" for idx in range(n_samples)],
            "batch": batch,
            "coverage_mean": coverage_mean.clip(5, None).round(2),
            "duplicates_pct": duplicates_pct.clip(1, 60).round(2),
            "gc_content": gc_content.round(2),
            "q30_pct": q30_pct.clip(60, 99.9).round(2),
        }
    )
    return df


# ---------------------------------------------------------------------------
# 9. phylo_traits.csv -- trait-trait correlation within/between clades
# ---------------------------------------------------------------------------
def gen_phylo_traits(n_per_clade: int = 40) -> pd.DataFrame:
    """
    Two continuous morphological traits (e.g., body-mass proxy and
    metabolic-rate proxy) simulated for three clades, each with its own
    allometric slope -- a simplified stand-in for phylogenetically
    structured trait covariance -- so jointplot(kind='kde') shows
    genuinely different clade-specific trait relationships (Simpson's
    paradox-style: pooled vs. within-clade trends differ).
    """
    clades = {
        "Clade_A": dict(intercept=0.5, slope=0.55, trait1_mean=1.0),
        "Clade_B": dict(intercept=5.5, slope=0.35, trait1_mean=5.5),
        "Clade_C": dict(intercept=-2.0, slope=1.5, trait1_mean=2.2),
    }
    rows = []
    for clade, p in clades.items():
        trait1 = RNG.normal(p["trait1_mean"], 0.6, n_per_clade)
        trait2 = p["intercept"] + p["slope"] * trait1 + RNG.normal(0, 0.35, n_per_clade)
        rows.append(
            pd.DataFrame(
                {"clade": clade, "trait1": trait1.round(3), "trait2": trait2.round(3)}
            )
        )
    return pd.concat(rows, ignore_index=True)


# ---------------------------------------------------------------------------
# 10. pathway_status_table.csv -- pathway x status contingency counts
# ---------------------------------------------------------------------------
def gen_pathway_status_table() -> pd.DataFrame:
    """
    Counts of genes-per-pathway falling into each functional status
    category, from a mock enrichment analysis. Values are hand-tuned so
    that "Apoptosis" and "Cell_Cycle" show enrichment for
    Upregulated/Downregulated respectively -- i.e. the annotated heatmap
    tutorial has an actual enrichment pattern to point at and interpret.
    """
    pathways = [
        "Apoptosis", "Cell_Cycle", "DNA_Repair", "Immune_Response",
        "Lipid_Metabolism", "Oxidative_Stress",
    ]
    statuses = ["Upregulated", "Downregulated", "Unchanged"]
    base = RNG.integers(2, 8, size=(len(pathways), len(statuses)))
    df = pd.DataFrame(base, index=pathways, columns=statuses)
    df.loc["Apoptosis", "Upregulated"] += 14
    df.loc["Cell_Cycle", "Downregulated"] += 16
    df.loc["Immune_Response", "Upregulated"] += 9
    df.index.name = "pathway"
    return df.reset_index()


def main() -> None:
    save(gen_docking_scores(), "docking_scores.csv")
    save(gen_timecourse_cytokines(), "timecourse_cytokines.csv")
    save(gen_variants(), "variants.csv")
    save(gen_gene_expression(), "gene_expression.csv")
    save(gen_enzyme_kinetics(), "enzyme_kinetics.csv")
    save(gen_metabolites(), "metabolites.csv")
    save(gen_microbiome_abundance(), "microbiome_abundance.csv")
    save(gen_qc_metrics(), "qc_metrics.csv")
    save(gen_phylo_traits(), "phylo_traits.csv")
    save(gen_pathway_status_table(), "pathway_status_table.csv")


if __name__ == "__main__":
    main()
