# Data Quality

## Dataset Size

The source contains:

- 7,043 customer records
- 21 original variables

## Duplicate Review

The validated source contains:

- 0 duplicate customer IDs
- 0 duplicate complete rows

## Numeric Validation

No invalid values were identified for:

- tenure
- MonthlyCharges

`TotalCharges` contains 11 values that cannot be directly converted
to numbers.

Each original invalid value consists of a single blank space.

## TotalCharges Decision

The dataset contains exactly 11 customers with zero months of tenure.

All 11 zero-tenure customers are the same records containing blank
`TotalCharges` values.

All 11 have:

`Churn = No`

The project converts those blank values to missing numeric values.

The customers themselves are retained.

The analysis does not replace the values with zero and does not drop
the customers.

`TotalCharges` is not used as a primary segmentation variable in the
reported comparisons.

## Category Validation

The primary churn categories are:

- Yes
- No

Contract categories are:

- Month-to-month
- One year
- Two year

Internet-service categories are:

- Fiber optic
- DSL
- No

## Data Preservation

All 7,043 unique customers remain available for the primary churn
analysis.
