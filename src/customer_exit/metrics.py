from __future__ import annotations

import pandas as pd


def grouped_rate(
    df: pd.DataFrame,
    group,
) -> pd.DataFrame:
    """Calculate rate, volume and monthly-charge exposure."""

    groups = (
        [group]
        if isinstance(group, str)
        else list(group)
    )

    working = df.copy()

    working["_churn_monthly_exposure"] = (
        working["MonthlyCharges"]
        * working["churned"]
    )

    result = (
        working.groupby(
            groups,
            observed=True,
            dropna=False,
        )
        .agg(
            customers=(
                "churned",
                "size",
            ),
            churned_customers=(
                "churned",
                "sum",
            ),
            churn_monthly_charge_exposure=(
                "_churn_monthly_exposure",
                "sum",
            ),
        )
        .reset_index()
    )

    result["retained_customers"] = (
        result["customers"]
        - result["churned_customers"]
    )

    result["churn_rate_pct"] = (
        result["churned_customers"]
        / result["customers"]
        * 100
    ).round(2)

    total_churn = working[
        "churned"
    ].sum()

    total_exposure = working[
        "_churn_monthly_exposure"
    ].sum()

    result["share_of_all_churn_pct"] = (
        result["churned_customers"]
        / total_churn
        * 100
    ).round(2)

    if total_exposure:
        result[
            "share_of_churn_monthly_exposure_pct"
        ] = (
            result[
                "churn_monthly_charge_exposure"
            ]
            / total_exposure
            * 100
        ).round(2)
    else:
        result[
            "share_of_churn_monthly_exposure_pct"
        ] = 0.0

    result[
        "churn_monthly_charge_exposure"
    ] = result[
        "churn_monthly_charge_exposure"
    ].round(2)

    return result.sort_values(
        [
            "churn_rate_pct",
            "customers",
        ],
        ascending=[
            False,
            False,
        ],
    ).reset_index(drop=True)


def overview_table(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return project-level churn KPIs."""

    customers = len(df)

    churned = int(
        df["churned"].sum()
    )

    exposure = (
        df.loc[
            df["churned"].eq(1),
            "MonthlyCharges",
        ]
        .sum()
    )

    return pd.DataFrame(
        [{
            "customers": customers,
            "churned_customers": churned,
            "retained_customers": (
                customers - churned
            ),
            "churn_rate_pct": round(
                churned
                / customers
                * 100,
                2,
            ),
            "average_tenure_months": round(
                df["tenure"].mean(),
                2,
            ),
            "median_tenure_months": round(
                df["tenure"].median(),
                2,
            ),
            "average_monthly_charges": round(
                df["MonthlyCharges"].mean(),
                2,
            ),
            "median_monthly_charges": round(
                df["MonthlyCharges"].median(),
                2,
            ),
            "churn_monthly_charge_exposure": round(
                exposure,
                2,
            ),
        }]
    )


def numeric_churn_summary(
    df: pd.DataFrame,
    features: list[str],
) -> pd.DataFrame:
    """Summarize numeric fields for retained/churned groups."""

    rows = []

    for feature in features:
        for churn_status, group in df.groupby(
            "Churn"
        ):
            values = group[
                feature
            ].dropna()

            rows.append(
                {
                    "feature": feature,
                    "churn_status": churn_status,
                    "count": int(
                        len(values)
                    ),
                    "mean": round(
                        values.mean(),
                        2,
                    ),
                    "median": round(
                        values.median(),
                        2,
                    ),
                    "std": round(
                        values.std(),
                        2,
                    ),
                    "min": round(
                        values.min(),
                        2,
                    ),
                    "max": round(
                        values.max(),
                        2,
                    ),
                }
            )

    return pd.DataFrame(rows)
