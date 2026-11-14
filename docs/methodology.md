# Methodology

## Analytical Approach

The Customer Exit uses descriptive analytics to examine customer
churn patterns in the IBM Telco Customer Churn sample dataset.

The workflow follows five stages:

1. Source-data validation.
2. Data preparation and derived-field creation.
3. Exploratory data analysis.
4. Segment and combined-segment analysis.
5. Business interpretation and reproducible reporting.

## Primary Metric

The primary outcome is customer churn.

A customer is considered churned when:

`Churn = Yes`

Segment churn rate is calculated as:

`churned customers / customers in segment`

The project also reports churned-customer count and the segment's
share of all churn so that high percentages can be interpreted
alongside business volume.

## Main Analytical Dimensions

The final pipeline evaluates:

- Contract type
- Customer tenure
- Internet service
- Monthly charge bands
- Payment method
- Tech support
- Online security
- Senior-citizen status
- Contract × tenure
- Internet service × contract
- Contract × tenure × internet service

## Combined-Segment Analysis

Single-variable comparisons can hide important interactions.

The project therefore evaluates multi-variable customer groups and
ranks sufficiently large segments by observed churn rate.

A minimum segment population is used for the highest-risk ranking to
avoid emphasizing extremely small groups.

## Interpretation

Results are descriptive associations.

The analysis does not claim that any individual variable causes
customer churn.

Business recommendations are framed as areas for further
investigation rather than validated interventions.
