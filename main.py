import os
from src.data_loader import load_raw_data
from src.cleaning import clean_data
from src.features import engineer_features
from src.visualization import (
    plot_churn_correlations,
    plot_contract_churn,
    plot_cohort_churn
)

def run():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(base_dir, "data", "raw", "telco_churn_raw.csv")
    processed_path = os.path.join(base_dir, "data", "processed", "telco_churn_processed.csv")
    figures_dir = os.path.join(base_dir, "reports", "figures")
    os.makedirs(figures_dir, exist_ok=True)

    # 1. Ingest
    df_raw = load_raw_data(save_raw_path=raw_path)

    # 2. Clean
    df_clean = clean_data(df_raw)

    # 3. Feature Engineer
    df_processed = engineer_features(df_clean)

    # 4. Save Processed Artifact
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df_processed.to_csv(processed_path, index=False)
    print(f"[Main] Processed dataset saved to: {processed_path}")

    # 5. Export Visualizations
    plot_churn_correlations(df_processed, figures_dir)
    plot_contract_churn(df_processed, figures_dir)
    plot_cohort_churn(df_processed, figures_dir)
    print("[Main] Pipeline execution finished successfully.")

if __name__ == "__main__":
    run()
