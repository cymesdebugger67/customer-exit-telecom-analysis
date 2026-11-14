# Statistical Analysis

## Purpose

Statistical analysis supplements descriptive comparisons by measuring association strength, numeric group separation, and uncertainty.

Statistical significance is not treated as equivalent to business importance.

## Categorical Association Testing

Categorical features are evaluated using:

- chi-square tests of independence
- bias-corrected Cramer's V

Current strongest observed associations include approximately:

| Feature | Cramer's V |
|---|---:|
| protection_level | 0.412 |
| Contract | 0.410 |
| support_security_profile | 0.402 |
| tenure_group | 0.362 |
| OnlineSecurity | 0.347 |
| TechSupport | 0.343 |
| InternetService | 0.322 |
| PaymentMethod | 0.303 |

`protection_level` and `support_security_profile` are engineered variables.

They should therefore be interpreted as derived customer profiles rather than independent causal drivers.

Among major original source variables, Contract is one of the strongest observed categorical relationships with churn.

## Numeric Comparison

Numeric variables are compared using two-sided Mann-Whitney U tests.

Absolute rank-biserial effect size is also reported.

Current observed results are approximately:

| Feature | Absolute Rank-Biserial Effect |
|---|---:|
| tenure | 0.480 |
| TotalCharges | 0.304 |
| MonthlyCharges | 0.242 |

Tenure shows the strongest observed numeric separation between churned and retained customers.

`TotalCharges` is influenced by both tenure and monthly charges and should not be interpreted as an independent driver.

## Bootstrap Confidence Intervals

Bootstrap resampling is used to estimate 95% confidence intervals for selected segment churn rates.

Examples include approximately:

- Month-to-month contract: 41.19% to 44.34%
- 0-6 months tenure: 50.44% to 55.50%
- Fiber optic service: 40.25% to 43.64%
- Electronic check: 43.21% to 47.36%

## Interpretation

The dataset contains more than seven thousand observations, so several comparisons produce very small p-values.

For that reason, the project emphasizes:

1. effect size
2. segment size
3. churn volume
4. uncertainty
5. practical business relevance

rather than relying on p-values alone.

The statistical results remain observational and do not establish causal relationships.
