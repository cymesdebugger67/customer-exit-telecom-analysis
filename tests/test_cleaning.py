import pandas as pd
import pytest

from customer_exit.cleaning import (
    audit_raw_data,
    clean_data,
    validate_schema,
)


def test_audit_detects_blank_totalcharges(
    sample_raw,
):
    audit = audit_raw_data(
        sample_raw
    )

    assert (
        audit[
            "invalid_total_charges"
        ]
        == 1
    )


def test_cleaning_converts_blank_totalcharges(
    sample_raw,
):
    cleaned = clean_data(
        sample_raw
    )

    assert (
        cleaned[
            "TotalCharges"
        ]
        .isna()
        .sum()
        == 1
    )


def test_missing_schema_fails(
    sample_raw,
):
    broken = sample_raw.drop(
        columns=["Churn"]
    )

    with pytest.raises(
        ValueError
    ):
        validate_schema(
            broken
        )
