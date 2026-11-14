from customer_exit.cleaning import clean_data
from customer_exit.features import add_features
from customer_exit.statistics import (
    bootstrap_intervals,
    categorical_association_summary,
    numeric_test_summary,
)


def prepared(sample_raw):
    config = {
        "tenure_bins": [
            -1, 6, 12, 24, 48, None
        ],
        "tenure_labels": [
            "0-6 months",
            "7-12 months",
            "13-24 months",
            "25-48 months",
            "49+ months",
        ],
        "charge_bins": [
            0, 40, 70, 100, None
        ],
        "charge_labels": [
            "Under 40",
            "40-69.99",
            "70-99.99",
            "100+",
        ],
    }

    return add_features(
        clean_data(
            sample_raw
        ),
        config,
    )


def test_cramers_v_range(
    sample_raw,
):
    data = prepared(
        sample_raw
    )

    result = (
        categorical_association_summary(
            data,
            ["Contract"],
        )
    )

    assert (
        result[
            "cramers_v"
        ]
        .between(
            0,
            1,
        )
        .all()
    )


def test_numeric_statistics_generated(
    sample_raw,
):
    data = prepared(
        sample_raw
    )

    result = numeric_test_summary(
        data,
        [
            "tenure",
            "MonthlyCharges",
        ],
    )

    assert len(result) == 2


def test_bootstrap_bounds(
    sample_raw,
):
    data = prepared(
        sample_raw
    )

    result = bootstrap_intervals(
        data,
        ["Contract"],
        iterations=100,
        seed=1,
    )

    assert (
        result[
            "ci_95_lower_pct"
        ]
        <= result[
            "ci_95_upper_pct"
        ]
    ).all()
