# %% Imports and paths
"""Descriptive customer churn analysis. Run: python analysis.py"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data" / "raw" / "Telco-Customer-Churn.csv"
OUT = ROOT / "outputs"


def grouped_rate(df, group):
    result = (df.groupby(group, dropna=False, observed=True)
              .agg(customers=("churned", "size"), churn_rate=("churned", "mean"))
              .reset_index())
    result["churn_rate_pct"] = (100 * result.pop("churn_rate")).round(2)
    return result.sort_values("churn_rate_pct", ascending=False)


def bar_chart(table, label, dest, title):
    data = table.dropna(subset=[label]).sort_values("churn_rate_pct")
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.barh(data[label].astype(str), data["churn_rate_pct"])
    ax.set(xlabel="Customers who churned (%)", title=title)
    ax.set_xlim(0, 100)
    fig.tight_layout()
    fig.savefig(dest, dpi=150)
    plt.close(fig)


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Dataset missing: {SOURCE}\nDownload the CSV linked in README.md and place it here.")
    df = pd.read_csv(SOURCE)
    required = {"customerID", "Churn", "Contract", "tenure", "InternetService", "MonthlyCharges", "TotalCharges"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    raw_rows = len(df)
    df = df.drop_duplicates(subset="customerID").copy()
    for c in ["Churn", "Contract", "InternetService"]:
        df[c] = df[c].astype("string").str.strip()
    df = df.loc[df["Churn"].isin(["Yes", "No"])].copy()
    df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce")
    df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["churned"] = df["Churn"].eq("Yes").astype(int)
    df["tenure_group"] = pd.cut(df["tenure"], [-1, 6, 12, 24, 48, float("inf")],
                                 labels=["0-6 months", "7-12 months", "13-24 months", "25-48 months", "49+ months"])
    if df.empty:
        raise ValueError("No valid rows remain")
    tables = OUT / "tables"
    charts = OUT / "charts"
    tables.mkdir(parents=True, exist_ok=True)
    charts.mkdir(parents=True, exist_ok=True)
    contract = grouped_rate(df, "Contract")
    tenure = grouped_rate(df.dropna(subset=["tenure_group"]), "tenure_group")
    internet = grouped_rate(df, "InternetService")
    for name, table in [("churn_by_contract", contract), ("churn_by_tenure", tenure), ("churn_by_internet", internet)]:
        table.to_csv(tables / f"{name}.csv", index=False)
    bar_chart(contract, "Contract", charts / "churn_by_contract.png", "Churn rate by contract")
    bar_chart(tenure, "tenure_group", charts / "churn_by_tenure.png", "Churn rate by tenure")
    bar_chart(internet, "InternetService", charts / "churn_by_internet.png", "Churn rate by internet service")
   
    rate = df["churned"].mean() * 100

    invalid_charges = int(df["TotalCharges"].isna().sum())
    zero_tenure_invalid = int(
        (df["TotalCharges"].isna() & df["tenure"].eq(0)).sum()
    )
    non_churned_invalid = int(
        (df["TotalCharges"].isna() & df["Churn"].eq("No")).sum()
    )

    def format_groups(table, category):
        return "\n".join(
            f"- {row[category]}: {row['churn_rate_pct']:.2f}% "
            f"(n={int(row['customers']):,})"
            for _, row in table.iterrows()
        )

    contract_results = format_groups(contract, "Contract")
    tenure_results = format_groups(tenure, "tenure_group")
    internet_results = format_groups(internet, "InternetService")

    report = f"""# The Customer Exit - Analytical Findings

## Dataset Overview

- Source: IBM Telco Customer Churn sample dataset
- Original records: {raw_rows:,}
- Unique valid customer records: {len(df):,}
- Overall churn rate: {rate:.2f}%

## Data Quality

- Invalid or missing numeric TotalCharges: {invalid_charges}
- Affected records with zero tenure: {zero_tenure_invalid}
- Affected records labeled non-churned: {non_churned_invalid}

The original 11 invalid TotalCharges entries contain a single
space. They are retained as missing numeric values rather than
replaced with zero. All customers remain in the churn analysis.
TotalCharges is excluded from the three comparisons.

## 1. Churn by Contract Type

{contract_results}

Month-to-month contracts have the highest observed churn rate.
This identifies a customer segment worth investigating,
but does not establish a causal effect.

## 2. Churn by Customer Tenure

{tenure_results}

Shorter-tenure customers show higher observed churn rates.
The results suggest that early customer retention may deserve
additional investigation.

## 3. Churn by Internet Service

{internet_results}

Fiber optic customers have the highest observed churn rate
among the listed internet-service groups. Service quality,
pricing, and other potential explanations require additional
evidence before conclusions can be drawn.

## Business Recommendations

1. Investigate customer experiences during the first six months.
2. Review retention opportunities among month-to-month customers.
3. Examine possible reasons for churn within the fiber optic group.

## Limitations

This analysis describes associations within a historical IBM
sample dataset. It does not establish causation, measure
current telecom market conditions, or validate the impact
of any proposed retention intervention.
"""

    (OUT / "findings.md").write_text(report, encoding="utf-8")

    print(f"Done. {len(df):,} customers analyzed. Results: {OUT}")


if __name__ == "__main__":
    main()
