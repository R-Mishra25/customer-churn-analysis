import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Sanitizes column headers, coerces numeric fields, and creates churn_flag."""
    data = df.copy()

    # 1. Snake-case columns
    data.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in data.columns]

    # 2. TotalCharges whitespace anomaly
    if "totalcharges" in data.columns:
        data["totalcharges"] = pd.to_numeric(data["totalcharges"], errors="coerce")
        if "tenure" in data.columns:
            data.loc[(data["totalcharges"].isna()) & (data["tenure"] == 0), "totalcharges"] = 0.0
        data["totalcharges"] = data["totalcharges"].fillna(data["totalcharges"].median())

    # 3. MonthlyCharges validation
    if "monthlycharges" in data.columns:
        data["monthlycharges"] = pd.to_numeric(data["monthlycharges"], errors="coerce").fillna(0.0)

    # 4. Binary churn target
    target_col = "churn" if "churn" in data.columns else "exited"
    if target_col in data.columns:
        data["churn_flag"] = (
            data[target_col]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["yes", "1", "true"])
            .astype(int)
        )

    # 5. Normalize string values
    str_cols = data.select_dtypes(include=["object"]).columns
    for col in str_cols:
        data[col] = data[col].astype(str).str.strip().str.lower()

    print(f"[Cleaning] Cleaned {len(data)} rows. Remaining nulls: {data.isna().sum().sum()}")
    return data
