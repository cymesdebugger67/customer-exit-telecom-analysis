from customer_exit.cleaning import clean_data
from customer_exit.features import add_features
from customer_exit.metrics import grouped_rate


def test_group_totals_are_preserved(
    sample_raw,
):
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

    data = add_features(
        clean_data(
            sample_raw
        ),
        config,
    )

    table = grouped_rate(
        data,
        "Contract",
    )

    assert (
        table[
            "customers"
        ].sum()
        == len(data)
    )

    assert (
        table[
            "churned_customers"
        ].sum()
        == data[
            "churned"
        ].sum()
    )


def test_churn_rates_are_valid(
    sample_raw,
):
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

    data = add_features(
        clean_data(
            sample_raw
        ),
        config,
    )

    table = grouped_rate(
        data,
        "InternetService",
    )

    assert (
        table[
            "churn_rate_pct"
        ]
        .between(
            0,
            100,
        )
        .all()
    )
