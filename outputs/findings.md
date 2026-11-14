# The Customer Exit - Analytical Findings

## Dataset Overview

- Source: IBM Telco Customer Churn sample dataset
- Original records: 7,043
- Unique valid customer records: 7,043
- Overall churn rate: 26.54%

## Data Quality

- Invalid or missing numeric TotalCharges: 11
- Affected records with zero tenure: 11
- Affected records labeled non-churned: 11

The original 11 invalid TotalCharges entries contain a single
space. They are retained as missing numeric values rather than
replaced with zero. All customers remain in the churn analysis.
TotalCharges is excluded from the three comparisons.

## 1. Churn by Contract Type

- Month-to-month: 42.71% (n=3,875)
- One year: 11.27% (n=1,473)
- Two year: 2.83% (n=1,695)

Month-to-month contracts have the highest observed churn rate.
This identifies a customer segment worth investigating,
but does not establish a causal effect.

## 2. Churn by Customer Tenure

- 0-6 months: 52.94% (n=1,481)
- 7-12 months: 35.89% (n=705)
- 13-24 months: 28.71% (n=1,024)
- 25-48 months: 20.39% (n=1,594)
- 49+ months: 9.51% (n=2,239)

Shorter-tenure customers show higher observed churn rates.
The results suggest that early customer retention may deserve
additional investigation.

## 3. Churn by Internet Service

- Fiber optic: 41.89% (n=3,096)
- DSL: 18.96% (n=2,421)
- No: 7.40% (n=1,526)

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
