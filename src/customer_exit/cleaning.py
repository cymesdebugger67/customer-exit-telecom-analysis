"""Source-data validation and cleaning."""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
}


def validate_schema(df: pd.DataFrame) -> None:
    """Raise if required source columns are missing."""

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            "Dataset is missing required columns: "
            f"{sorted(missing)}"
        )


def audit_raw_data(df: pd.DataFrame) -> dict:
    """Return reproducible raw-data quality diagnostics."""

    validate_schema(df)

    total_numeric = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce",
    )

    invalid_total = total_numeric.isna()

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "unique_customer_ids": int(
            df["customerID"].nunique()
        ),
        "duplicate_customer_ids": int(
            df["customerID"].duplicated().sum()
        ),
        "duplicate_rows": int(
            df.duplicated().sum()
        ),
        "invalid_total_charges": int(
            invalid_total.sum()
        ),
        "zero_tenure_customers": int(
            (df["tenure"] == 0).sum()
        ),
        "invalid_total_zero_tenure": int(
            (
                invalid_total
                & df["tenure"].eq(0)
            ).sum()
        ),
        "invalid_total_non_churned": int(
            (
                invalid_total
                & df["Churn"].eq("No")
            ).sum()
        ),
    }


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw dataset without inventing values."""

    validate_schema(df)

    data = df.copy()

    data = data.drop_duplicates(
        subset="customerID",
        keep="first",
    ).copy()

    object_columns = data.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in object_columns:
        data[column] = (
            data[column]
            .astype("string")
            .str.strip()
        )

    numeric_columns = [
        "SeniorCitizen",
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce",
        )

    data = data.loc[
        data["Churn"].isin(["Yes", "No"])
    ].copy()

    if data.empty:
        raise ValueError(
            "No valid customer rows remain."
        )

    return data
