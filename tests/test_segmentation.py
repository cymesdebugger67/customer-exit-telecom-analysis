from customer_exit.cleaning import clean_data
from customer_exit.features import add_features
from customer_exit.segmentation import highest_risk_segments


def test_minimum_segment_threshold(
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

    result = highest_risk_segments(
        data,
        minimum_customers=1,
    )

    assert (
        result[
            "customers"
        ]
        >= 1
    ).all()

def test_concentration_uses_full_churn_denominator():
    import pandas as pd
    from customer_exit.segmentation import churn_concentration

    segments = pd.DataFrame({
        "churned_customers": [6, 4]
    })

    result = churn_concentration(
        segments,
        total_churned=20,
    )

    assert result[
        "cumulative_churn_share_pct"
    ].tolist() == [30.0, 50.0]
