from __future__ import annotations

import numpy as np
import pandas as pd


def _convert_bins(values):
    """Convert JSON null upper bounds to positive infinity."""

    return [
        np.inf if value is None else value
        for value in values
    ]


def add_features(
    df: pd.DataFrame,
    config: dict,
) -> pd.DataFrame:
    """Create reproducible analytical features."""

    data = df.copy()

    data["churned"] = (
        data["Churn"]
        .eq("Yes")
        .astype(int)
    )

    data["senior_status"] = (
        data["SeniorCitizen"]
        .map({
            0: "No",
            1: "Yes",
        })
        .fillna("Unknown")
    )

    data["tenure_group"] = pd.cut(
        data["tenure"],
        _convert_bins(
            config["tenure_bins"]
        ),
        labels=config["tenure_labels"],
    )

    data["monthly_charge_band"] = pd.cut(
        data["MonthlyCharges"],
        _convert_bins(
            config["charge_bins"]
        ),
        labels=config["charge_labels"],
        include_lowest=True,
        right=False,
    )

    data["automatic_payment"] = np.where(
        data["PaymentMethod"]
        .str.contains(
            "automatic",
            case=False,
            na=False,
        ),
        "Automatic",
        "Manual",
    )

    protection_columns = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
    ]

    data["internet_protection_count"] = (
        data[protection_columns]
        .eq("Yes")
        .sum(axis=1)
    )

    data["protection_level"] = np.where(
        data["InternetService"].eq("No"),
        "No internet",
        data["internet_protection_count"]
        .astype(str)
        + " protection services",
    )

    security = data["OnlineSecurity"].eq("Yes")
    support = data["TechSupport"].eq("Yes")
    no_internet = data["InternetService"].eq("No")

    data["support_security_profile"] = np.select(
        [
            no_internet,
            security & support,
            security & ~support,
            ~security & support,
        ],
        [
            "No internet",
            "Security + support",
            "Security only",
            "Support only",
        ],
        default="Neither",
    )

    data["streaming_service_count"] = (
        data[
            [
                "StreamingTV",
                "StreamingMovies",
            ]
        ]
        .eq("Yes")
        .sum(axis=1)
    )

    return data
