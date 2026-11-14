from customer_exit.cleaning import clean_data
from customer_exit.features import add_features


def config():
    return {
        "tenure_bins": [
            -1,
            6,
            12,
            24,
            48,
            None,
        ],
        "tenure_labels": [
            "0-6 months",
            "7-12 months",
            "13-24 months",
            "25-48 months",
            "49+ months",
        ],
        "charge_bins": [
            0,
            40,
            70,
            100,
            None,
        ],
        "charge_labels": [
            "Under 40",
            "40-69.99",
            "70-99.99",
            "100+",
        ],
    }


def test_features_are_created(
    sample_raw,
):
    data = add_features(
        clean_data(
            sample_raw
        ),
        config(),
    )

    expected = {
        "churned",
        "senior_status",
        "tenure_group",
        "monthly_charge_band",
        "automatic_payment",
        "internet_protection_count",
        "protection_level",
        "support_security_profile",
        "streaming_service_count",
    }

    assert expected.issubset(
        data.columns
    )
