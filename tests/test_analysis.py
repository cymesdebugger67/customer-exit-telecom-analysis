from pathlib import Path

import pandas as pd
import pytest

import analysis


def sample_dataframe():
    return pd.DataFrame(
        {
            "customerID": [
                "A",
                "B",
                "C",
                "D",
            ],
            "gender": [
                "Female",
                "Male",
                "Female",
                "Male",
            ],
            "SeniorCitizen": [
                0,
                1,
                0,
                1,
            ],
            "Partner": [
                "Yes",
                "No",
                "Yes",
                "No",
            ],
            "Dependents": [
                "No",
                "No",
                "Yes",
                "No",
            ],
            "tenure": [
                1,
                10,
                30,
                60,
            ],
            "PhoneService": [
                "Yes",
                "Yes",
                "Yes",
                "Yes",
            ],
            "MultipleLines": [
                "No",
                "Yes",
                "No",
                "Yes",
            ],
            "InternetService": [
                "DSL",
                "Fiber optic",
                "DSL",
                "No",
            ],
            "OnlineSecurity": [
                "No",
                "No",
                "Yes",
                "No internet service",
            ],
            "OnlineBackup": [
                "No",
                "Yes",
                "Yes",
                "No internet service",
            ],
            "DeviceProtection": [
                "No",
                "Yes",
                "Yes",
                "No internet service",
            ],
            "TechSupport": [
                "No",
                "No",
                "Yes",
                "No internet service",
            ],
            "StreamingTV": [
                "No",
                "Yes",
                "No",
                "No internet service",
            ],
            "StreamingMovies": [
                "No",
                "Yes",
                "No",
                "No internet service",
            ],
            "Contract": [
                "Month-to-month",
                "Month-to-month",
                "One year",
                "Two year",
            ],
            "PaperlessBilling": [
                "Yes",
                "Yes",
                "No",
                "No",
            ],
            "PaymentMethod": [
                "Electronic check",
                "Electronic check",
                "Bank transfer (automatic)",
                "Mailed check",
            ],
            "MonthlyCharges": [
                30.0,
                80.0,
                60.0,
                25.0,
            ],
            "TotalCharges": [
                "30",
                "800",
                "1800",
                " ",
            ],
            "Churn": [
                "Yes",
                "Yes",
                "No",
                "No",
            ],
        }
    )


def test_prepare_data_creates_analysis_fields():
    df = analysis.prepare_data(
        sample_dataframe()
    )

    assert "churned" in df.columns
    assert "tenure_group" in df.columns
    assert "monthly_charge_band" in df.columns
    assert "senior_status" in df.columns

    assert df["churned"].tolist() == [
        1,
        1,
        0,
        0,
    ]


def test_blank_totalcharges_becomes_missing():
    df = analysis.prepare_data(
        sample_dataframe()
    )

    assert df["TotalCharges"].isna().sum() == 1


def test_grouped_rate_population_is_preserved():
    df = analysis.prepare_data(
        sample_dataframe()
    )

    table = analysis.grouped_rate(
        df,
        "Contract",
    )

    assert table["customers"].sum() == len(df)
    assert table["churned_customers"].sum() == df["churned"].sum()


def test_grouped_rates_are_valid_percentages():
    df = analysis.prepare_data(
        sample_dataframe()
    )

    table = analysis.grouped_rate(
        df,
        "InternetService",
    )

    assert (
        table["churn_rate_pct"]
        .between(0, 100)
        .all()
    )


def test_real_dataset_contract_if_available():
    if not analysis.SOURCE.exists():
        pytest.skip(
            "Raw dataset is not stored in Git."
        )

    df = analysis.load_data()

    assert len(df) == 7043
    assert df["customerID"].nunique() == 7043
    assert set(df["Churn"].unique()) == {
        "Yes",
        "No",
    }

    assert (
        df["TotalCharges"]
        .isna()
        .sum()
        == 11
    )


def test_output_generation_if_dataset_available(
    tmp_path,
):
    if not analysis.SOURCE.exists():
        pytest.skip(
            "Raw dataset is not stored in Git."
        )

    df = analysis.load_data()

    tables = analysis.generate_outputs(
        df,
        tmp_path,
    )

    assert len(tables) == 11

    assert len(
        list(
            (tmp_path / "tables")
            .glob("*.csv")
        )
    ) == 11

    assert len(
        list(
            (tmp_path / "charts")
            .glob("*.png")
        )
    ) == 8

    assert (
        tmp_path
        / "executive_summary.md"
    ).exists()

    assert (
        tmp_path
        / "findings.md"
    ).exists()
