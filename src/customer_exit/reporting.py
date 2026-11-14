"""Markdown reporting utilities."""

from __future__ import annotations

from pathlib import Path


def write_reports(
    tables: dict,
    audit: dict,
    report_dir: Path,
) -> None:
    """Generate executive, analytical and portfolio reports."""

    report_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    overview = tables[
        "churn_overview"
    ].iloc[0]

    contract = tables[
        "churn_by_contract"
    ].iloc[0]

    tenure = tables[
        "churn_by_tenure"
    ].iloc[0]

    internet = tables[
        "churn_by_internet"
    ].iloc[0]

    payment = tables[
        "churn_by_payment_method"
    ].iloc[0]

    risk = tables[
        "highest_risk_segments"
    ].iloc[0]

    association = tables[
        "categorical_associations"
    ].iloc[0]

    numeric = tables[
        "numeric_tests"
    ].iloc[0]

    executive = f"""# Executive Summary

## The Customer Exit - Telecom Analytics

The analysis covers **{int(overview['customers']):,} customers**.
A total of **{int(overview['churned_customers']):,} customers churned**,
producing an overall churn rate of **{overview['churn_rate_pct']:.2f}%**.

The largest descriptive churn signals include:

- **{contract['Contract']}** contract churn:
  **{contract['churn_rate_pct']:.2f}%**
- **{tenure['tenure_group']}** tenure churn:
  **{tenure['churn_rate_pct']:.2f}%**
- **{internet['InternetService']}** internet-service churn:
  **{internet['churn_rate_pct']:.2f}%**
- **{payment['PaymentMethod']}** payment-method churn:
  **{payment['churn_rate_pct']:.2f}%**

The highest-risk sufficiently large combined profile is:

**{risk['Contract']} / {risk['tenure_group']} /
{risk['InternetService']}**

with **{risk['churn_rate_pct']:.2f}% churn**
across **{int(risk['customers']):,} customers**.

The strongest categorical association in the tested feature set is
**{association['feature']}** with Cramer's V =
**{association['cramers_v']:.3f}**.

The strongest tested numeric separation is **{numeric['feature']}**
with absolute rank-biserial effect =
**{numeric['rank_biserial_abs']:.3f}**.

These findings are descriptive and observational and do not establish
causation.
"""

    analytical = f"""# Analytical Report

## Dataset Quality

- Source rows: **{audit['rows']:,}**
- Source columns: **{audit['columns']}**
- Unique customer IDs: **{audit['unique_customer_ids']:,}**
- Duplicate customer IDs: **{audit['duplicate_customer_ids']}**
- Duplicate rows: **{audit['duplicate_rows']}**
- Invalid numeric TotalCharges: **{audit['invalid_total_charges']}**

All known blank TotalCharges records are retained as customers and
converted to missing numeric values.

## Business Scale

- Customers: **{int(overview['customers']):,}**
- Churned customers: **{int(overview['churned_customers']):,}**
- Churn rate: **{overview['churn_rate_pct']:.2f}%**
- Monthly-charge exposure among churned customers:
  **{overview['churn_monthly_charge_exposure']:,.2f}**

The exposure metric is the sum of current monthly charges associated
with churned customers. It is not presented as realized lost revenue.

## Contract and Lifecycle

The highest contract-level churn occurs among
**{contract['Contract']}** customers at
**{contract['churn_rate_pct']:.2f}%**.

The highest tenure-group churn occurs among
**{tenure['tenure_group']}** customers at
**{tenure['churn_rate_pct']:.2f}%**.

## Service and Payment

The highest internet-service churn occurs among
**{internet['InternetService']}** customers at
**{internet['churn_rate_pct']:.2f}%**.

The highest payment-method churn occurs among
**{payment['PaymentMethod']}** customers at
**{payment['churn_rate_pct']:.2f}%**.

## Multidimensional Segmentation

The highest-risk sufficiently large segment is:

- Contract: **{risk['Contract']}**
- Tenure: **{risk['tenure_group']}**
- Internet service: **{risk['InternetService']}**
- Customers: **{int(risk['customers']):,}**
- Churned: **{int(risk['churned_customers']):,}**
- Churn rate: **{risk['churn_rate_pct']:.2f}%**
- Share of all churn: **{risk['share_of_all_churn_pct']:.2f}%**

## Statistical Analysis

The categorical association table ranks tested variables using
bias-corrected Cramer's V alongside chi-square p-values.

The numeric test table uses two-sided Mann-Whitney U tests and reports
absolute rank-biserial effect sizes.

Bootstrap confidence intervals are generated for selected major
segment churn rates.

Statistical significance is not treated as equivalent to business
importance.

## Interpretation

The project prioritizes the combination of:

- churn rate,
- churn volume,
- monthly-charge exposure,
- association strength,
- customer-segment size.

This avoids using a single percentage as the sole prioritization rule.

## Limitations

The IBM dataset is a historical sample.

The analysis does not establish causal relationships, forecast future
churn, or validate any proposed retention intervention.

Important unobserved factors may include satisfaction, service
outages, competitor activity, geography, promotions and customer
support interactions.
"""

    portfolio = f"""# Portfolio Summary

**The Customer Exit** is an end-to-end telecom churn analytics case
study covering **{int(overview['customers']):,} customers**.

The project demonstrates:

- source-data auditing,
- reusable Python modules,
- feature engineering,
- exploratory data analysis,
- multidimensional segmentation,
- statistical association testing,
- confidence intervals,
- business-volume analysis,
- automated testing,
- reproducible visualization,
- executive reporting.

The most prominent combined risk segment is
**{risk['Contract']} / {risk['tenure_group']} /
{risk['InternetService']}**, with an observed churn rate of
**{risk['churn_rate_pct']:.2f}%**.

Results are interpreted as descriptive evidence rather than causal
claims.
"""

    (
        report_dir
        / "executive_summary.md"
    ).write_text(
        executive,
        encoding="utf-8",
    )

    (
        report_dir
        / "analytical_report.md"
    ).write_text(
        analytical,
        encoding="utf-8",
    )

    (
        report_dir
        / "portfolio_summary.md"
    ).write_text(
        portfolio,
        encoding="utf-8",
    )
