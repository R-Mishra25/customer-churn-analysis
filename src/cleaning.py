import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Sanitizes column headers, coerces numeric fields, and creates binary churn_flag."""
    data = df.copy()

    # 1. Standardize column names to snake_case
    data.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in data.columns]

    # 2. Fix TotalCharges: blank whitespace strings coerced to NaN, then filled
    if "totalcharges" in data.columns:
        data["totalcharges"] = pd.to_numeric(data["totalcharges"], errors="coerce")
        if "tenure" in data.columns:
            data.loc[(data["totalcharges"].isna()) & (data["tenure"] == 0), "totalcharges"] = 0.0
        data["totalcharges"] = data["totalcharges"].fillna(data["totalcharges"].median())

    # 3. Ensure MonthlyCharges is numeric float
    if "monthlycharges" in data.columns:
        data["monthlycharges"] = pd.to_numeric(data["monthlycharges"], errors="coerce").fillna(0.0)

    # 4. Standardize Churn to binary integer flag (1 = Churned, 0 = Retained)
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

    # 5. Clean text whitespace across categorical columns
    str_cols = data.select_dtypes(include=["object"]).columns
    for col in str_cols:
        data[col] = data[col].astype(str).str.strip().str.lower()

    print(f"[Cleaning] Hygiene complete. Rows: {len(data):,}, Nulls remaining: {data.isna().sum().sum()}")
    return data
