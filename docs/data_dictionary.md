# Data Dictionary

| Field | Description |
|---|---|
| customerID | Unique customer identifier |
| gender | Customer gender recorded in the sample |
| SeniorCitizen | Indicator for senior-citizen status |
| Partner | Whether the customer has a partner |
| Dependents | Whether the customer has dependents |
| tenure | Number of months with the company |
| PhoneService | Whether phone service is active |
| MultipleLines | Multiple-line phone-service status |
| InternetService | DSL, fiber optic, or no internet service |
| OnlineSecurity | Online-security service status |
| OnlineBackup | Online-backup service status |
| DeviceProtection | Device-protection service status |
| TechSupport | Technical-support service status |
| StreamingTV | Streaming-TV service status |
| StreamingMovies | Streaming-movie service status |
| Contract | Month-to-month, one-year, or two-year contract |
| PaperlessBilling | Whether paperless billing is enabled |
| PaymentMethod | Customer payment method |
| MonthlyCharges | Current monthly charge |
| TotalCharges | Accumulated customer charges |
| Churn | Whether the customer left the service |

## Derived Fields

| Field | Description |
|---|---|
| churned | Numeric churn indicator: 1 = churned, 0 = retained |
| tenure_group | Customer lifecycle grouping based on tenure |
| monthly_charge_band | Monthly billing range used for segmentation |
| senior_status | Readable version of SeniorCitizen |
