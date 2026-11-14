from __future__ import annotations

import pandas as pd

from .metrics import grouped_rate


def highest_risk_segments(
    df: pd.DataFrame,
    minimum_customers: int = 100,
) -> pd.DataFrame:
    """Rank high-churn multi-dimensional segments."""

    result = grouped_rate(
        df.dropna(
            subset=["tenure_group"]
        ),
        [
            "Contract",
            "tenure_group",
            "InternetService",
        ],
    )

    result = result.loc[
        result["customers"]
        >= minimum_customers
    ].copy()

    return (
        result.sort_values(
            [
                "churn_rate_pct",
                "churned_customers",
            ],
            ascending=[
                False,
                False,
            ],
        )
        .head(20)
        .reset_index(drop=True)
    )


def churn_concentration(
    segment_table: pd.DataFrame,
    total_churned: int,
) -> pd.DataFrame:
    """Show cumulative churn concentration by segment."""

    result = (
        segment_table.sort_values(
            "churned_customers",
            ascending=False,
        )
        .reset_index(drop=True)
        .copy()
    )

    result["segment_rank"] = (
        result.index + 1
    )

    if total_churned <= 0:
        raise ValueError("total_churned must be positive")

    total = total_churned

    result[
        "cumulative_churn_share_pct"
    ] = (
        result[
            "churned_customers"
        ].cumsum()
        / total
        * 100
    ).round(2)

    return result
