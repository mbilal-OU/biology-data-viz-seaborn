# 🧬 Biology Data Visualization with Seaborn  

This repository is a **beginner-friendly tutorial** for learning Seaborn using **biology-inspired datasets**.  
It is designed for biology and bioinformatics students who want to **practice data visualization** step by step.  

---

## 📖 Introduction  

Data visualization is essential in **biology and bioinformatics**.  
Whether you are analyzing cytokine levels, docking results, gene expression, or microbiome abundance, good plots reveal patterns that numbers alone cannot.  

This repository provides:  
- 📊 **Datasets** (CSV files) with realistic biology examples  
- 🖼️ **Seaborn code templates** for each plot type  
- 📘 **Explanations** of when and why to use each visualization  
- 🧑‍🔬 A **beginner roadmap** for step-by-step practice  

---

## 📦 Repository Structure  

The repository is structured as follows:
biology-data-viz-seaborn/
├── data/ # Example datasets
│ ├── docking_scores.csv
│ ├── timecourse_cytokines.csv
│ ├── variants.csv
│ ├── gene_expression.csv
│ ├── enzyme_kinetics.csv
│ ├── metabolites.csv
│ ├── microbiome_abundance.csv
│ ├── qc_metrics.csv
│ ├── phylo_traits.csv
│ └── pathway_status_table.csv
│
├── figs/ # Save your generated plots here
├── src/ # Example scripts
│ └── seaborn_templates.py
├── notebooks/ # Optional Jupyter notebooks
├── README.md # Tutorial guide
└── requirements.txt # Package dependencies


---

## 🚀 Quick Start  

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/biology-data-viz-seaborn.git
   cd biology-data-viz-seaborn

Install requirements:
   ```bash
   pip install -r requirements.txt
   ```Run the template script:
   python src/seaborn_templates.py
Plots will open one by one
To save a figure instead of showing it
plt.savefig("figs/plot.png", dpi=300, bbox_inches="tight")

📊 Plot Types and Biology Examples
1️⃣ Scatterplot

Definition: Shows relationship between two variables.

Biology Example: Docking results (logP vs Vina score).
import seaborn as sns, pandas as pd, matplotlib.pyplot as plt
df = pd.read_csv("data/docking_scores.csv")
sns.scatterplot(data=df, x="logP", y="vina_score", hue="target", size="ring_count")
plt.title("Docking Landscape")
plt.show()

2️⃣ Lineplot

Definition: Trends over time or continuous variables.

Biology Example: Cytokine levels across treatments.

df = pd.read_csv("data/timecourse_cytokines.csv")
sns.lineplot(data=df, x="time_h", y="IL6", hue="treatment", errorbar=("sd"))
plt.title("IL-6 Cytokine Levels Over Time")
plt.show()

3️⃣ Histogram / KDE / ECDF

Definition: Show distribution of one variable.

Biology Example: Allele frequency distribution.

df = pd.read_csv("data/variants.csv")
sns.histplot(data=df, x="allele_frequency", hue="consequence", element="step", stat="density")
plt.title("Variant Allele Frequencies")
plt.show()

4️⃣ Box / Violin / Swarm

Definition: Compare groups or conditions.

Biology Example: Gene expression under control vs treatment.

df = pd.read_csv("data/gene_expression.csv")
sns.boxplot(data=df, x="gene", y="expression", hue="condition")
plt.title("Gene Expression Across Conditions")
plt.show()

5️⃣ Regression (lmplot)

Definition: Fits regression lines.

Biology Example: Enzyme kinetics.

df = pd.read_csv("data/enzyme_kinetics.csv")
sns.lmplot(data=df, x="substrate_conc", y="rate", hue="inhibitor")

6️⃣ Heatmap

Definition: Color-coded matrix of values.

Biology Example: Correlation of metabolites.

df = pd.read_csv("data/metabolites.csv")
sns.heatmap(df.corr(), cmap="vlag", center=0, annot=True)
plt.title("Metabolite Correlations")
plt.show()

7️⃣ Clustermap

Definition: Heatmap with clustering.

Biology Example: Microbiome species abundance.

df = pd.read_csv("data/microbiome_abundance.csv")
piv = df.pivot_table(index="species", columns="sample", values="relative_abundance", fill_value=0)
sns.clustermap(piv, cmap="mako", z_score=0, figsize=(8,8))

8️⃣ Pairplot

Definition: Matrix of scatterplots.

Biology Example: Sequencing QC metrics.

df = pd.read_csv("data/qc_metrics.csv")
sns.pairplot(df, vars=["duplicates_pct","coverage_mean","gc_content"])

9️⃣ Jointplot

Definition: Scatterplot + marginal distributions.

Biology Example: Trait–trait correlations in phylogenetics.

df = pd.read_csv("data/phylo_traits.csv")
sns.jointplot(data=df, x="trait1", y="trait2", hue="clade", kind="kde")

🔟 Annotated Heatmap

Definition: Heatmap with numbers.

Biology Example: Pathway × status counts.

df = pd.read_csv("data/pathway_status_table.csv", index_col=0)
sns.heatmap(df, annot=True, fmt="d", cmap="crest")
plt.title("Pathway Status Table")
plt.show()

🧑‍🔬 Beginner’s Practice Roadmap

Week 1 → Scatter & Line plots

Week 2 → Histograms & KDEs

Week 3 → Box/Violin/Swarm plots

Week 4 → Regression

Week 5 → Heatmaps

Week 6 → Clustermaps

Week 7 → Pairplots & Jointplots

Week 8 → Combine multiple plots into figures

🔖 Tags

seaborn · python · bioinformatics · biology · data-visualization · omics

✨ With this repo, you can learn Seaborn step by step using realistic biology datasets — and then apply it to your own research.


