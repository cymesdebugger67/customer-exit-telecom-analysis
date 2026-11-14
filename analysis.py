"""Reproducible descriptive analysis for The Customer Exit."""

from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data" / "raw" / "Telco-Customer-Churn.csv"
OUT = ROOT / "outputs"

TENURE_LABELS = [
    "0-6 months",
    "7-12 months",
    "13-24 months",
    "25-48 months",
    "49+ months",
]

TENURE_BINS = [-1, 6, 12, 24, 48, float("inf")]

CHARGE_LABELS = [
    "Under 40",
    "40-69.99",
    "70-99.99",
    "100+",
]

CHARGE_BINS = [0, 40, 70, 100, float("inf")]

REQUIRED_COLUMNS = {
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
}


def prepare_data(df):
    """Validate and prepare the source dataset for analysis."""

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing)}"
        )

    data = df.copy()

    data = data.drop_duplicates(subset="customerID").copy()

    text_columns = data.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        data[column] = (
            data[column]
            .astype("string")
            .str.strip()
        )

    data["tenure"] = pd.to_numeric(
        data["tenure"],
        errors="coerce",
    )

    data["MonthlyCharges"] = pd.to_numeric(
        data["MonthlyCharges"],
        errors="coerce",
    )

    data["TotalCharges"] = pd.to_numeric(
        data["TotalCharges"],
        errors="coerce",
    )

    data["SeniorCitizen"] = pd.to_numeric(
        data["SeniorCitizen"],
        errors="coerce",
    )

    data = data.loc[
        data["Churn"].isin(["Yes", "No"])
    ].copy()

    data["churned"] = (
        data["Churn"]
        .eq("Yes")
        .astype(int)
    )

    data["tenure_group"] = pd.cut(
        data["tenure"],
        TENURE_BINS,
        labels=TENURE_LABELS,
    )

    data["monthly_charge_band"] = pd.cut(
        data["MonthlyCharges"],
        CHARGE_BINS,
        labels=CHARGE_LABELS,
        include_lowest=True,
        right=False,
    )

    data["senior_status"] = (
        data["SeniorCitizen"]
        .map({
            0: "No",
            1: "Yes",
        })
        .fillna("Unknown")
    )

    if data.empty:
        raise ValueError(
            "No valid customer rows remain after preparation."
        )

    return data


def load_data(source=SOURCE):
    """Load and prepare the source CSV."""

    if not source.exists():
        raise FileNotFoundError(
            f"Dataset missing: {source}"
        )

    return prepare_data(
        pd.read_csv(source)
    )


def grouped_rate(df, group):
    """Calculate population, churn volume and churn rate."""

    groups = [group] if isinstance(group, str) else list(group)

    result = (
        df.groupby(
            groups,
            dropna=False,
            observed=True,
        )
        .agg(
            customers=("churned", "size"),
            churned_customers=("churned", "sum"),
            churn_rate=("churned", "mean"),
        )
        .reset_index()
    )

    result["retained_customers"] = (
        result["customers"]
        - result["churned_customers"]
    )

    result["churn_rate_pct"] = (
        result["churn_rate"] * 100
    ).round(2)

    total_churn = df["churned"].sum()

    if total_churn:
        result["share_of_all_churn_pct"] = (
            result["churned_customers"]
            / total_churn
            * 100
        ).round(2)
    else:
        result["share_of_all_churn_pct"] = 0.0

    result = result.drop(
        columns="churn_rate"
    )

    return result.sort_values(
        ["churn_rate_pct", "customers"],
        ascending=[False, False],
    ).reset_index(drop=True)


def overview_table(df):
    """Return one-row project KPI summary."""

    customers = len(df)
    churned = int(df["churned"].sum())

    return pd.DataFrame(
        [{
            "customers": customers,
            "churned_customers": churned,
            "retained_customers": customers - churned,
            "churn_rate_pct": round(
                df["churned"].mean() * 100,
                2,
            ),
            "average_tenure_months": round(
                df["tenure"].mean(),
                2,
            ),
            "median_tenure_months": round(
                df["tenure"].median(),
                2,
            ),
            "average_monthly_charges": round(
                df["MonthlyCharges"].mean(),
                2,
            ),
            "median_monthly_charges": round(
                df["MonthlyCharges"].median(),
                2,
            ),
        }]
    )


def support_table(df):
    """Combine TechSupport and OnlineSecurity analysis."""

    frames = []

    for dimension in [
        "TechSupport",
        "OnlineSecurity",
    ]:
        table = grouped_rate(
            df,
            dimension,
        )

        table = table.rename(
            columns={dimension: "category"}
        )

        table.insert(
            0,
            "dimension",
            dimension,
        )

        frames.append(table)

    return (
        pd.concat(
            frames,
            ignore_index=True,
        )
        .sort_values(
            ["churn_rate_pct", "customers"],
            ascending=[False, False],
        )
        .reset_index(drop=True)
    )


def highest_risk_segments(df, minimum_customers=100):
    """Rank sufficiently large combined customer segments."""

    table = grouped_rate(
        df,
        [
            "Contract",
            "tenure_group",
            "InternetService",
        ],
    )

    table = table.loc[
        table["customers"] >= minimum_customers
    ].copy()

    return (
        table.sort_values(
            [
                "churn_rate_pct",
                "churned_customers",
            ],
            ascending=[
                False,
                False,
            ],
        )
        .head(10)
        .reset_index(drop=True)
    )


def save_rate_bar(
    table,
    category,
    destination,
    title,
):
    """Save a horizontal churn-rate chart."""

    plot = table.dropna(
        subset=[category]
    ).copy()

    plot = plot.sort_values(
        "churn_rate_pct"
    )

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    bars = ax.barh(
        plot[category].astype(str),
        plot["churn_rate_pct"],
    )

    ax.set_xlabel(
        "Churn rate (%)"
    )

    ax.set_ylabel("")

    ax.set_title(title)

    upper = max(
        10,
        float(
            plot["churn_rate_pct"].max()
        ) * 1.2,
    )

    ax.set_xlim(
        0,
        min(100, upper),
    )

    for bar, value in zip(
        bars,
        plot["churn_rate_pct"],
    ):
        ax.text(
            bar.get_width() + 0.4,
            bar.get_y()
            + bar.get_height() / 2,
            f"{value:.1f}%",
            va="center",
        )

    fig.tight_layout()

    fig.savefig(
        destination,
        dpi=160,
        bbox_inches="tight",
    )

    plt.close(fig)


def save_overview_chart(df, destination):
    """Save retained-versus-churned customer counts."""

    counts = (
        df["Churn"]
        .value_counts()
        .reindex(["No", "Yes"])
    )

    labels = [
        "Retained",
        "Churned",
    ]

    fig, ax = plt.subplots(
        figsize=(7, 5)
    )

    bars = ax.bar(
        labels,
        counts.values,
    )

    ax.set_ylabel(
        "Customers"
    )

    ax.set_title(
        "Customer Churn Overview"
    )

    for bar, value in zip(
        bars,
        counts.values,
    ):
        ax.text(
            bar.get_x()
            + bar.get_width() / 2,
            bar.get_height(),
            f"{int(value):,}",
            ha="center",
            va="bottom",
        )

    fig.tight_layout()

    fig.savefig(
        destination,
        dpi=160,
        bbox_inches="tight",
    )

    plt.close(fig)


def save_support_chart(table, destination):
    """Save support/security churn comparisons."""

    plot = table.copy()

    plot["label"] = (
        plot["dimension"]
        .str.replace(
            "TechSupport",
            "Tech Support",
        )
        .str.replace(
            "OnlineSecurity",
            "Online Security",
        )
        + ": "
        + plot["category"].astype(str)
    )

    save_rate_bar(
        plot,
        "label",
        destination,
        "Churn Rate by Support and Security Status",
    )


def save_contract_tenure_chart(
    table,
    destination,
):
    """Save contract-by-tenure churn-rate matrix."""

    pivot = table.pivot(
        index="tenure_group",
        columns="Contract",
        values="churn_rate_pct",
    )

    pivot = pivot.reindex(
        TENURE_LABELS
    )

    contract_order = [
        "Month-to-month",
        "One year",
        "Two year",
    ]

    pivot = pivot.reindex(
        columns=contract_order
    )

    fig, ax = plt.subplots(
        figsize=(9, 6)
    )

    image = ax.imshow(
        pivot.values,
        aspect="auto",
    )

    ax.set_xticks(
        range(len(pivot.columns))
    )

    ax.set_xticklabels(
        pivot.columns,
        rotation=20,
        ha="right",
    )

    ax.set_yticks(
        range(len(pivot.index))
    )

    ax.set_yticklabels(
        pivot.index,
    )

    ax.set_title(
        "Churn Rate: Contract Type × Customer Tenure"
    )

    ax.set_xlabel(
        "Contract"
    )

    ax.set_ylabel(
        "Tenure group"
    )

    for row in range(
        len(pivot.index)
    ):
        for column in range(
            len(pivot.columns)
        ):
            value = pivot.iloc[
                row,
                column,
            ]

            if pd.notna(value):
                ax.text(
                    column,
                    row,
                    f"{value:.1f}%",
                    ha="center",
                    va="center",
                )

    fig.colorbar(
        image,
        ax=ax,
        label="Churn rate (%)",
    )

    fig.tight_layout()

    fig.savefig(
        destination,
        dpi=160,
        bbox_inches="tight",
    )

    plt.close(fig)


def build_reports(
    df,
    overview,
    contract,
    tenure,
    internet,
    monthly_charge,
    payment,
    support,
    senior,
    risk,
):
    """Create decision-focused Markdown reports."""

    top_contract = contract.iloc[0]
    top_tenure = tenure.iloc[0]
    top_internet = internet.iloc[0]
    top_charge = monthly_charge.iloc[0]
    top_payment = payment.iloc[0]
    top_support = support.iloc[0]
    top_senior = senior.iloc[0]
    top_risk = risk.iloc[0]

    total_churn = int(
        overview.loc[
            0,
            "churned_customers",
        ]
    )

    churn_rate = float(
        overview.loc[
            0,
            "churn_rate_pct",
        ]
    )

    invalid_total = int(
        df["TotalCharges"]
        .isna()
        .sum()
    )

    executive = f"""# Executive Summary

## The Customer Exit - Telecom Analytics

The dataset contains **{len(df):,} customers**, of whom
**{total_churn:,} churned**, producing an overall churn rate of
**{churn_rate:.2f}%**.

The strongest descriptive patterns identified by the expanded
analysis include:

- **{top_contract['Contract']}** customers show the highest contract-level
  churn rate at **{top_contract['churn_rate_pct']:.2f}%**.
- The **{top_tenure['tenure_group']}** tenure group shows the highest
  lifecycle churn rate at **{top_tenure['churn_rate_pct']:.2f}%**.
- **{top_internet['InternetService']}** customers show the highest
  internet-service churn rate at **{top_internet['churn_rate_pct']:.2f}%**.
- The highest monthly-charge-band churn rate occurs in
  **{top_charge['monthly_charge_band']}** at
  **{top_charge['churn_rate_pct']:.2f}%**.
- The highest payment-method churn rate occurs among
  **{top_payment['PaymentMethod']}** customers at
  **{top_payment['churn_rate_pct']:.2f}%**.

A combined-segment analysis identified one of the highest-risk
sufficiently large customer profiles as:

**{top_risk['Contract']} contract / {top_risk['tenure_group']} /
{top_risk['InternetService']}**, with
**{top_risk['churn_rate_pct']:.2f}% churn**
across **{int(top_risk['customers']):,} customers**.

The analysis indicates that customer lifecycle stage, contract
structure, billing characteristics, service type, and support-related
features should be considered together when prioritizing retention
investigation.

These results are descriptive associations and do not establish
causation.
"""

    findings = f"""# The Customer Exit - Detailed Analytical Findings

## Dataset Overview

- Customers analyzed: **{len(df):,}**
- Churned customers: **{total_churn:,}**
- Overall churn rate: **{churn_rate:.2f}%**
- Invalid numeric TotalCharges values: **{invalid_total}**

## Data Quality

No duplicate customer IDs or duplicate complete rows were identified.

The original dataset contains 11 `TotalCharges` values represented
by a blank space. After numeric conversion these values are treated
as missing. All 11 affected customers have zero months of tenure and
are retained in the analysis.

`TotalCharges` is not used as a primary segmentation variable.

## 1. Contract Type

The highest observed contract-level churn rate is
**{top_contract['Contract']}** at
**{top_contract['churn_rate_pct']:.2f}%**.

That segment contains **{int(top_contract['customers']):,} customers**
and accounts for **{top_contract['share_of_all_churn_pct']:.2f}%**
of all churned customers in the sample.

## 2. Customer Tenure

The highest observed lifecycle churn occurs among customers with
**{top_tenure['tenure_group']}** of tenure at
**{top_tenure['churn_rate_pct']:.2f}%**.

The tenure analysis shows a strong descriptive decline in churn
across longer-tenure groups.

## 3. Internet Service

The highest internet-service churn rate occurs among
**{top_internet['InternetService']}** customers at
**{top_internet['churn_rate_pct']:.2f}%**.

This pattern should be investigated alongside pricing, contract type,
support features, and customer lifecycle stage rather than treated as
a standalone causal explanation.

## 4. Monthly Charges

The monthly-charge segment with the highest observed churn rate is
**{top_charge['monthly_charge_band']}** at
**{top_charge['churn_rate_pct']:.2f}%**.

This result provides a descriptive indication that billing level may
be relevant when investigating churn behavior.

## 5. Payment Method

The highest observed payment-method churn rate occurs for
**{top_payment['PaymentMethod']}** customers at
**{top_payment['churn_rate_pct']:.2f}%**.

Payment method may proxy for other customer characteristics and
should not be interpreted as a causal churn driver.

## 6. Support and Online Security

The highest support/security comparison is
**{top_support['dimension']} = {top_support['category']}**
at **{top_support['churn_rate_pct']:.2f}% churn**.

The relationship between service-support features and churn should
be examined jointly with internet service because some categories
include customers without internet service.

## 7. Senior-Citizen Status

The higher observed senior-status churn group is
**{top_senior['senior_status']}**
at **{top_senior['churn_rate_pct']:.2f}%**.

This is a descriptive segmentation result and should not be used to
infer individual customer behavior.

## 8. Combined Customer Segments

The highest-risk combined segment meeting the minimum population
threshold is:

- Contract: **{top_risk['Contract']}**
- Tenure: **{top_risk['tenure_group']}**
- Internet service: **{top_risk['InternetService']}**
- Customers: **{int(top_risk['customers']):,}**
- Churned customers: **{int(top_risk['churned_customers']):,}**
- Churn rate: **{top_risk['churn_rate_pct']:.2f}%**
- Share of total sample churn:
  **{top_risk['share_of_all_churn_pct']:.2f}%**

This combined analysis is more useful for retention prioritization
than considering any one variable in isolation.

## Business Implications

The analysis supports further investigation into:

1. Early-lifecycle customer experience and onboarding.
2. Retention opportunities among month-to-month customers.
3. Pricing and service experience among high-charge customers.
4. Fiber optic customer experience and support requirements.
5. Payment-method segments with elevated churn.
6. Combined profiles where high churn rate and meaningful customer
   volume occur together.

## Interpretation

A segment should not be prioritized using churn rate alone.

Business impact depends on both the **rate of churn** and the
**number of customers affected**.

The generated tables therefore report customer population,
churned-customer count, churn rate, and each segment's share of
overall churn.

## Limitations

This project uses a historical IBM sample dataset.

The analysis is descriptive and observational. It does not establish
causation, represent current telecommunications market conditions,
or demonstrate that a proposed retention intervention would reduce
churn.

Additional customer experience, service quality, competitor,
geographic, and operational variables could materially influence
customer behavior.
"""

    return executive, findings


def generate_outputs(
    df,
    out_dir=OUT,
):
    """Generate all project tables, charts and reports."""

    tables_dir = (
        out_dir / "tables"
    )

    charts_dir = (
        out_dir / "charts"
    )

    tables_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    charts_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    overview = overview_table(df)

    contract = grouped_rate(
        df,
        "Contract",
    )

    tenure = grouped_rate(
        df.dropna(
            subset=["tenure_group"]
        ),
        "tenure_group",
    )

    internet = grouped_rate(
        df,
        "InternetService",
    )

    monthly_charge = grouped_rate(
        df.dropna(
            subset=[
                "monthly_charge_band"
            ]
        ),
        "monthly_charge_band",
    )

    payment = grouped_rate(
        df,
        "PaymentMethod",
    )

    support = support_table(df)

    senior = grouped_rate(
        df,
        "senior_status",
    )

    contract_tenure = grouped_rate(
        df.dropna(
            subset=["tenure_group"]
        ),
        [
            "Contract",
            "tenure_group",
        ],
    )

    internet_contract = grouped_rate(
        df,
        [
            "InternetService",
            "Contract",
        ],
    )

    risk = highest_risk_segments(df)

    tables = {
        "churn_overview": overview,
        "churn_by_contract": contract,
        "churn_by_tenure": tenure,
        "churn_by_internet": internet,
        "churn_by_monthly_charge": monthly_charge,
        "churn_by_payment_method": payment,
        "churn_by_support": support,
        "churn_by_senior_status": senior,
        "churn_by_contract_tenure": contract_tenure,
        "churn_by_internet_contract": internet_contract,
        "highest_risk_segments": risk,
    }

    for name, table in tables.items():
        table.to_csv(
            tables_dir / f"{name}.csv",
            index=False,
        )

    save_overview_chart(
        df,
        charts_dir
        / "churn_overview.png",
    )

    save_rate_bar(
        contract,
        "Contract",
        charts_dir
        / "churn_by_contract.png",
        "Churn Rate by Contract Type",
    )

    save_rate_bar(
        tenure,
        "tenure_group",
        charts_dir
        / "churn_by_tenure.png",
        "Churn Rate by Customer Tenure",
    )

    save_rate_bar(
        internet,
        "InternetService",
        charts_dir
        / "churn_by_internet.png",
        "Churn Rate by Internet Service",
    )

    save_rate_bar(
        monthly_charge,
        "monthly_charge_band",
        charts_dir
        / "churn_by_monthly_charge.png",
        "Churn Rate by Monthly Charge Band",
    )

    save_rate_bar(
        payment,
        "PaymentMethod",
        charts_dir
        / "churn_by_payment_method.png",
        "Churn Rate by Payment Method",
    )

    save_support_chart(
        support,
        charts_dir
        / "churn_by_support.png",
    )

    save_contract_tenure_chart(
        contract_tenure,
        charts_dir
        / "churn_by_contract_tenure.png",
    )

    executive, findings = build_reports(
        df,
        overview,
        contract,
        tenure,
        internet,
        monthly_charge,
        payment,
        support,
        senior,
        risk,
    )

    (
        out_dir
        / "executive_summary.md"
    ).write_text(
        executive,
        encoding="utf-8",
    )

    (
        out_dir
        / "findings.md"
    ).write_text(
        findings,
        encoding="utf-8",
    )

    return tables


def main():
    df = load_data()

    tables = generate_outputs(df)

    print(
        f"Analysis complete: "
        f"{len(df):,} customers."
    )

    print(
        f"Generated "
        f"{len(tables)} tables, "
        f"8 charts, "
        f"and 2 reports."
    )


if __name__ == "__main__":
    main()
