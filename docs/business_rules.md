# Business and Analytical Rules

## Project

The Customer Exit — Telecom Analytics

**Author:** Cyril James Lunzaga

## Churn Definition

A customer is classified as churned when:

`Churn = Yes`

A customer is classified as retained when:

`Churn = No`

## Churn Rate

Churn rate is calculated as:

Churn Rate (%) = (Churned Customers / Total Customers in Segment) × 100

The denominator represents the total number of customers within the segment being analyzed.

## Share of Total Churn

This metric measures how much of the overall observed churn comes from a specific customer segment.

Share of Total Churn (%) = (Segment Churned Customers / All Churned Customers) × 100

## Monthly-Charge Exposure

Monthly-charge exposure is calculated as the sum of the recorded monthly charges associated with churned customers.

This is an analytical measure of billing value associated with churned customers.

It must not be interpreted as:

- Confirmed revenue loss
- Annual revenue loss
- Profit loss
- Customer lifetime value

The dataset does not provide enough information to establish those amounts.

## Minimum Segment Size

The high-risk combined-segment ranking requires at least 100 customers per segment.

This threshold helps reduce the emphasis on extreme churn percentages calculated from very small customer groups.

It is a practical analytical rule rather than a formal statistical guarantee.

## Statistical Significance

The project uses a conventional significance threshold of 0.05.

Statistical significance does not automatically indicate business importance.

Association strength, uncertainty, customer population, and practical relevance must also be considered.

## Business Prioritization

Customer groups are evaluated using:

- Observed churn rate
- Churned-customer count
- Customer population
- Share of total churn
- Monthly-charge exposure
- Statistical effect size
- Confidence intervals
- Business interpretability

No individual metric is considered sufficient on its own.

## Interpretation Limitations

The project is descriptive and observational.

Observed relationships between customer characteristics and churn do not establish causation.

Business recommendations identify areas for further investigation rather than proven retention interventions.
