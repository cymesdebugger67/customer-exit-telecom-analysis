# Analytical Report

## Dataset Quality

- Source rows: **7,043**
- Source columns: **21**
- Unique customer IDs: **7,043**
- Duplicate customer IDs: **0**
- Duplicate rows: **0**
- Invalid numeric TotalCharges: **11**

All known blank TotalCharges records are retained as customers and
converted to missing numeric values.

## Business Scale

- Customers: **7,043**
- Churned customers: **1,869**
- Churn rate: **26.54%**
- Monthly-charge exposure among churned customers:
  **139,130.85**

The exposure metric is the sum of current monthly charges associated
with churned customers. It is not presented as realized lost revenue.

## Contract and Lifecycle

The highest contract-level churn occurs among
**Month-to-month** customers at
**42.71%**.

The highest tenure-group churn occurs among
**0-6 months** customers at
**52.94%**.

## Service and Payment

The highest internet-service churn occurs among
**Fiber optic** customers at
**41.89%**.

The highest payment-method churn occurs among
**Electronic check** customers at
**45.29%**.

## Multidimensional Segmentation

The highest-risk sufficiently large segment is:

- Contract: **Month-to-month**
- Tenure: **0-6 months**
- Internet service: **Fiber optic**
- Customers: **619**
- Churned: **459**
- Churn rate: **74.15%**
- Share of all churn: **24.56%**

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
