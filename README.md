# The Customer Exit — Telecom Analytics

## Author

**Cyril James Lunzaga**

---

## Introduction

Customer churn is an important business concern for subscription-based companies because losing existing customers can affect recurring revenue, acquisition costs, and long-term customer value.

**The Customer Exit — Telecom Analytics** is a medium-sized descriptive data analytics case study based on the IBM Telco Customer Churn sample dataset.

The project investigates customer churn across contract structure, customer tenure, internet service, billing characteristics, payment behavior, support services, and customer segments. It combines exploratory data analysis, reproducible Python analysis, automated testing, documentation, visualization, and business interpretation.

---

## Objectives

The project aims to:

- Measure overall customer churn.
- Assess dataset quality before analysis.
- Explore customer, billing, service, and contract characteristics.
- Compare churn rates across important customer segments.
- Consider both churn rate and absolute churn volume.
- Analyze interactions between contract type, tenure, and internet service.
- Identify customer profiles associated with elevated churn.
- Produce reproducible analytical tables and visualizations.
- Translate findings into practical areas for further business investigation.
- Document methodology, assumptions, data-quality decisions, and limitations.
- Validate important analytical logic using automated tests.

---

## Dataset

The project uses the **IBM Telco Customer Churn sample dataset**.

| Metric | Value |
|---|---:|
| Customer records | 7,043 |
| Original variables | 21 |
| Churned customers | 1,869 |
| Retained customers | 5,174 |
| Overall churn rate | 26.54% |
| Tenure range | 0–72 months |

The raw dataset is intentionally excluded from Git version control.

Expected local path:

```text
data/raw/Telco-Customer-Churn.csv
```

---

## Discussion

### Data Quality

The dataset contains:

- 0 duplicate customer IDs
- 0 duplicate complete rows
- 0 invalid `tenure` values
- 0 invalid `MonthlyCharges` values
- 11 non-numeric `TotalCharges` values

The 11 affected `TotalCharges` entries contain a blank space rather than a valid number.

All 11 affected customers have:

- `tenure = 0`
- `Churn = No`

These customers are retained in the analysis. Their `TotalCharges` values are converted to missing numeric values rather than being replaced with zero.

`TotalCharges` is not used as a primary segmentation variable in the reported comparisons.

### Exploratory Data Analysis

Two Jupyter notebooks support the analytical workflow:

- `01_data_quality.ipynb` — dataset structure, duplicates, missing and invalid values, numeric conversion, and category validation.
- `02_exploratory_analysis.ipynb` — churn distribution, numerical distributions, customer segments, service characteristics, billing behavior, and combined-segment exploration.

The notebooks document exploration and analytical reasoning, while `analysis.py` provides the reproducible final pipeline.

### Main Analytical Dimensions

The project analyzes churn by:

- Contract type
- Customer tenure
- Internet service
- Monthly-charge band
- Payment method
- Technical support
- Online security
- Senior-citizen status
- Contract × tenure
- Internet service × contract
- Contract × tenure × internet service

Each applicable segment reports customer population, churned-customer count, retained-customer count, churn rate, and share of total churn.

---

## Execution

### Create the Python Environment

```powershell
py -3.15 -m venv .venv
```

### Install Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Run the Python Analysis

Place the source dataset at:

```text
data/raw/Telco-Customer-Churn.csv
```

Then run:

```powershell
.\.venv\Scripts\python.exe analysis.py
```

The pipeline generates:

- 11 analytical CSV tables
- 8 analytical charts
- Executive summary
- Detailed findings report

### Run the Jupyter Notebooks

Open:

```text
notebooks/01_data_quality.ipynb
notebooks/02_exploratory_analysis.ipynb
```

Select the project's `.venv` Python kernel in VS Code and execute the cells from top to bottom.

### Run Automated Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

The automated test suite validates:

- Data preparation
- Blank `TotalCharges` handling
- Group population preservation
- Valid churn-rate ranges
- Real-dataset expectations
- Final output generation

Current validated result:

**6 tests passed.**

---

## Results

### Overall Customer Churn

The dataset contains **7,043 customers**, of whom **1,869 churned**.

Overall churn rate:

**26.54%**

### Contract Type

Month-to-month customers have a churn rate of **42.71%**.

This group also accounts for approximately **88.55% of all churned customers**, making it important from both a churn-rate and customer-volume perspective.

### Customer Tenure

Customers with **0–6 months of tenure** have the highest tenure-group churn rate at **52.94%**.

Observed churn decreases across longer-tenure groups.

### Internet Service

Fiber optic customers have an observed churn rate of **41.89%**.

This is substantially higher than the observed churn rates among DSL customers and customers without internet service.

### Monthly Charges

The **70–99.99** monthly-charge group has the highest charge-band churn rate at **37.91%**.

This group also accounts for approximately **54.41% of all churned customers**.

The pattern is not strictly linear. Customers paying `100+` per month have a lower churn rate of **28.30%**.

### Payment Method

Customers using **Electronic check** have an observed churn rate of **45.29%**.

This group accounts for approximately **57.30% of all churn cases**.

### Support and Online Security

Customers without online security have an observed churn rate of approximately **41.77%**.

Customers without technical support show a similar churn rate of approximately **41.64%**.

These service characteristics overlap with internet-service status and should not be interpreted independently as causal drivers.

### Senior-Citizen Status

Senior customers have an observed churn rate of **41.68%**.

However, non-senior customers account for most absolute churn cases because they make up a much larger portion of the dataset.

This illustrates why churn rate and churn volume should be considered together.

### Combined Customer Segment

The highest-risk sufficiently large combined segment identified is:

**Month-to-month contract + 0–6 months tenure + Fiber optic service**

| Metric | Result |
|---|---:|
| Customers | 619 |
| Churned customers | 459 |
| Churn rate | 74.15% |
| Share of all churn cases | 24.56% |

This combined analysis provides a stronger retention signal than examining contract, tenure, or internet service independently.

---

## Assumptions and Limitations

The project assumes that each customer ID represents one unique customer and that `Churn = Yes` identifies a customer who left the service.

Blank `TotalCharges` values for zero-tenure customers are treated as missing rather than assumed to equal zero.

The analysis is descriptive and observational. It identifies associations but does not establish causation.

The dataset is a historical IBM sample and should not be interpreted as representing the current telecommunications market.

Important variables that are not available may include:

- Customer satisfaction
- Service outages
- Competitor pricing
- Geographic location
- Acquisition channels
- Customer-service interactions
- Promotional history

High churn percentages in small populations can also be misleading. Business prioritization should therefore consider both churn rate and customer volume.

The recommendations in this project identify areas for further investigation rather than proven retention interventions.

---

## Conclusion

The analysis identifies several meaningful patterns in customer churn.

Month-to-month customers represent the largest source of churn, customers in the earliest stages of their relationship with the company show elevated churn, fiber optic customers have higher observed churn, and electronic-check customers form another important high-churn segment.

The strongest combined result is the **month-to-month, 0–6 month tenure, fiber optic** customer profile, where **74.15%** of the 619 customers in that segment churned.

These findings suggest that customer lifecycle stage, contract structure, service experience, billing characteristics, payment behavior, and support availability should be considered together when investigating retention opportunities.

Because the analysis is descriptive, the results should guide further investigation and controlled business testing rather than be interpreted as proven causes of churn.

---

## Project Structure

```text
customer-exit-telecom-analytics-project/
│
├── README.md
├── analysis.py
├── requirements.txt
├── pytest.ini
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
│
├── notebooks/
│   ├── 01_data_quality.ipynb
│   └── 02_exploratory_analysis.ipynb
│
├── tests/
│   └── test_analysis.py
│
├── docs/
│   ├── methodology.md
│   ├── data_dictionary.md
│   ├── data_quality.md
│   └── assumptions_and_limitations.md
│
└── outputs/
    ├── executive_summary.md
    ├── findings.md
    ├── charts/
    └── tables/
```

---

## Technology

- Python
- Pandas
- Matplotlib
- Jupyter Notebook
- Pytest
- VS Code
- Git
- GitHub

---

## Project Status