import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Generates tenure cohorts, bill disparity ratio, and protective services score."""
    data = df.copy()

    # 1. Lifecycle Tenure Cohorts
    if "tenure" in data.columns:
        bins = [-np.inf, 6, 12, 24, 48, np.inf]
        labels = ["0-6 Months", "6-12 Months", "1-2 Years", "2-4 Years", "4+ Years"]
        data["tenure_cohort"] = pd.cut(data["tenure"], bins=bins, labels=labels)

    # 2. Charge Disparity Ratio (Bill Shock indicator)
    if "monthlycharges" in data.columns and "totalcharges" in data.columns and "tenure" in data.columns:
        data["avg_historical_charge"] = np.where(
            data["tenure"] > 0,
            data["totalcharges"] / data["tenure"],
            data["monthlycharges"]
        )
        data["charge_disparity_ratio"] = (
            data["monthlycharges"] / (data["avg_historical_charge"] + 1e-5)
        ).round(3)

    # 3. Protective Services Count
    security_features = ["onlinesecurity", "techsupport", "onlinebackup", "deviceprotection"]
    valid_cols = [c for c in security_features if c in data.columns]
    data["protective_services_count"] = 0
    for col in valid_cols:
        data["protective_services_count"] += (data[col] == "yes").astype(int)

    # 4. High Monthly Spender Indicator (Top 25% percentile)
    if "monthlycharges" in data.columns:
        cutoff = data["monthlycharges"].quantile(0.75)
        data["is_high_spender"] = (data["monthlycharges"] >= cutoff).astype(int)

    print(f"[Features] Feature engineering complete. Total columns: {data.shape[1]}")
    return data
