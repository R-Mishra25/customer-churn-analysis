import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def set_style():
    sns.set_theme(style="whitegrid")

def plot_churn_correlations(df: pd.DataFrame, output_dir: str):
    """Plots and saves Pearson correlation against churn_flag."""
    set_style()
    num_cols = df.select_dtypes(include=["float64", "int64", "int8"])
    if "churn_flag" not in num_cols.columns:
        return

    corrs = num_cols.corr()["churn_flag"].drop("churn_flag").sort_values(ascending=False)

    plt.figure(figsize=(9, 4.5))
    palette = ["#d9534f" if v > 0 else "#5cb85c" for v in corrs.values]
    
    # Passing y explicitly to hue avoids the seaborn deprecation warning
    sns.barplot(x=corrs.values, y=corrs.index, hue=corrs.index, palette=palette, legend=False)
    plt.axvline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Correlation of Numeric Metrics with Churn", fontsize=12, weight="bold")
    plt.xlabel("Pearson Correlation Coefficient")
    plt.tight_layout()

    out_path = os.path.join(output_dir, "churn_correlations.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[Visualization] Exported: {out_path}")

def plot_contract_churn(df: pd.DataFrame, output_dir: str):
    """Plots and saves churn rate by contract type."""
    set_style()
    if "contract" not in df.columns or "churn_flag" not in df.columns:
        return

    contract_churn = df.groupby("contract")["churn_flag"].mean().reset_index()
    contract_churn["churn_rate_pct"] = contract_churn["churn_flag"] * 100

    plt.figure(figsize=(7, 4))
    ax = sns.barplot(
        data=contract_churn, 
        x="contract", 
        y="churn_rate_pct", 
        hue="contract", 
        palette="Blues_r", 
        legend=False
    )
    plt.title("Customer Churn Rate by Contract Type", fontsize=12, weight="bold")
    plt.ylabel("Churn Rate (%)")
    plt.xlabel("Contract Agreement")
    plt.ylim(0, contract_churn["churn_rate_pct"].max() + 12)

    for i, r in contract_churn.iterrows():
        ax.text(i, r["churn_rate_pct"] + 1, f"{r['churn_rate_pct']:.1f}%", ha="center", weight="semibold")

    plt.tight_layout()
    out_path = os.path.join(output_dir, "churn_by_contract.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[Visualization] Exported: {out_path}")

def plot_cohort_churn(df: pd.DataFrame, output_dir: str):
    """Plots and saves churn attrition across tenure cohorts."""
    set_style()
    if "tenure_cohort" not in df.columns or "churn_flag" not in df.columns:
        return

    cohort_churn = df.groupby("tenure_cohort", observed=True)["churn_flag"].mean().reset_index()
    cohort_churn["churn_rate_pct"] = cohort_churn["churn_flag"] * 100

    plt.figure(figsize=(8, 4))
    ax = sns.barplot(
        data=cohort_churn, 
        x="tenure_cohort", 
        y="churn_rate_pct", 
        color="#2c7bb6"
    )
    plt.title("Churn Attrition Across Customer Lifecycle", fontsize=12, weight="bold")
    plt.ylabel("Churn Rate (%)")
    plt.xlabel("Tenure Segment")
    plt.ylim(0, cohort_churn["churn_rate_pct"].max() + 10)

    for i, r in cohort_churn.iterrows():
        ax.text(i, r["churn_rate_pct"] + 1, f"{r['churn_rate_pct']:.1f}%", ha="center", weight="semibold")

    plt.tight_layout()
    out_path = os.path.join(output_dir, "churn_by_tenure_cohort.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[Visualization] Exported: {out_path}")
