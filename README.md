# Customer Retention & Churn Analysis

## Overview
An end-to-end exploratory data analysis (EDA) and feature engineering pipeline built in Python to identify core drivers of customer attrition. This project transforms raw customer demographic, billing, and subscription logs into actionable retention insights.

## Project Structure
```text
customer-churn-analysis/
├── data/
│   ├── raw/                 # Immutable source dataset
│   └── processed/           # Cleaned and feature-engineered CSV
├── notebooks/
│   └── 01_churn_eda_insights.ipynb
├── reports/
│   └── figures/             # High-resolution exported visualizations
├── src/
│   ├── __init__.py
│   ├── data_loader.py       # Automated dataset ingestion
│   ├── cleaning.py          # Type casting, whitespace resolution, null imputation
│   ├── features.py          # Lifecycle cohorts, bill shock ratios, service indices
│   └── visualization.py     # Standardized Seaborn/Matplotlib plotting routines
├── main.py                  # CLI master pipeline runner
├── requirements.txt         # Locked environment dependencies
└── README.md
```

## Key Engineered Features
- **Tenure Lifecycle Cohorts:** Segments customer lifespan into `0-6 Months`, `6-12 Months`, `1-2 Years`, `2-4 Years`, and `4+ Years`.
- **Charge Disparity Ratio:** Detects billing anomalies (bill shock) by comparing current monthly charges against historical run rates.
- **Protective Services Count:** Aggregates sticky add-on subscriptions (`OnlineSecurity`, `TechSupport`, `OnlineBackup`, `DeviceProtection`).
- **High-Spender Flag:** Identifies top-quartile revenue customers (`>= 75th percentile` Monthly Charges).

## Key Analytical Findings
1. **Contract Structure:** Customers on **Month-to-month** contracts exhibit a **42.7% churn rate**, compared to **11.3%** for One-year and **2.8%** for Two-year contracts.
2. **Onboarding Vulnerability:** Attrition peaks at **52.9%** during the **0-6 Months** cohort, stabilizing below **10%** after 4 years.
3. **Service Ecosystem Lock-In:** Customers with zero protective add-ons churn at **~45%**, while those subscribed to 3+ protective services churn at **less than 12%**.

## Quickstart
```bash
git clone https://github.com/R-Mishra25/customer-churn-analysis.git
cd customer-churn-analysis
pip install -r requirements.txt
python main.py
```
