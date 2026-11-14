# The Customer Exit - Detailed Analytical Findings

## Dataset Overview

- Customers analyzed: **7,043**
- Churned customers: **1,869**
- Overall churn rate: **26.54%**
- Invalid numeric TotalCharges values: **11**

## Data Quality

No duplicate customer IDs or duplicate complete rows were identified.

The original dataset contains 11 `TotalCharges` values represented
by a blank space. After numeric conversion these values are treated
as missing. All 11 affected customers have zero months of tenure and
are retained in the analysis.

`TotalCharges` is not used as a primary segmentation variable.

## 1. Contract Type

The highest observed contract-level churn rate is
**Month-to-month** at
**42.71%**.

That segment contains **3,875 customers**
and accounts for **88.55%**
of all churned customers in the sample.

## 2. Customer Tenure

The highest observed lifecycle churn occurs among customers with
**0-6 months** of tenure at
**52.94%**.

The tenure analysis shows a strong descriptive decline in churn
across longer-tenure groups.

## 3. Internet Service

The highest internet-service churn rate occurs among
**Fiber optic** customers at
**41.89%**.

This pattern should be investigated alongside pricing, contract type,
support features, and customer lifecycle stage rather than treated as
a standalone causal explanation.

## 4. Monthly Charges

The monthly-charge segment with the highest observed churn rate is
**70-99.99** at
**37.91%**.

This result provides a descriptive indication that billing level may
be relevant when investigating churn behavior.

## 5. Payment Method

The highest observed payment-method churn rate occurs for
**Electronic check** customers at
**45.29%**.

Payment method may proxy for other customer characteristics and
should not be interpreted as a causal churn driver.

## 6. Support and Online Security

The highest support/security comparison is
**OnlineSecurity = No**
at **41.77% churn**.

The relationship between service-support features and churn should
be examined jointly with internet service because some categories
include customers without internet service.

## 7. Senior-Citizen Status

The higher observed senior-status churn group is
**Yes**
at **41.68%**.

This is a descriptive segmentation result and should not be used to
infer individual customer behavior.

## 8. Combined Customer Segments

The highest-risk combined segment meeting the minimum population
threshold is:

- Contract: **Month-to-month**
- Tenure: **0-6 months**
- Internet service: **Fiber optic**
- Customers: **619**
- Churned customers: **459**
- Churn rate: **74.15%**
- Share of total sample churn:
  **24.56%**

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
