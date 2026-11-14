"""Inferential statistics and confidence intervals."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def cramers_v(
    contingency: pd.DataFrame,
    chi2: float,
) -> float:
    """Bias-corrected Cramer's V."""

    n = contingency.to_numpy().sum()

    if n <= 1:
        return 0.0

    rows, columns = (
        contingency.shape
    )

    phi2 = chi2 / n

    correction = (
        (columns - 1)
        * (rows - 1)
        / (n - 1)
    )

    phi2_corrected = max(
        0,
        phi2 - correction,
    )

    rows_corrected = (
        rows
        - ((rows - 1) ** 2)
        / (n - 1)
    )

    columns_corrected = (
        columns
        - ((columns - 1) ** 2)
        / (n - 1)
    )

    denominator = min(
        rows_corrected - 1,
        columns_corrected - 1,
    )

    if denominator <= 0:
        return 0.0

    return float(
        np.sqrt(
            phi2_corrected
            / denominator
        )
    )


def categorical_association_summary(
    df: pd.DataFrame,
    features: list[str],
) -> pd.DataFrame:
    """Chi-square tests and Cramer's V for categorical features."""

    rows = []

    for feature in features:
        table = pd.crosstab(
            df[feature],
            df["Churn"],
            dropna=False,
        )

        if min(
            table.shape
        ) < 2:
            continue

        chi2, p_value, dof, _ = (
            stats.chi2_contingency(
                table
            )
        )

        rows.append(
            {
                "feature": feature,
                "chi_square": round(
                    float(chi2),
                    4,
                ),
                "degrees_of_freedom": int(
                    dof
                ),
                "p_value": float(
                    p_value
                ),
                "cramers_v": round(
                    cramers_v(
                        table,
                        chi2,
                    ),
                    4,
                ),
                "significant_0_05": (
                    p_value < 0.05
                ),
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values(
            "cramers_v",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def numeric_test_summary(
    df: pd.DataFrame,
    features: list[str],
) -> pd.DataFrame:
    """Mann-Whitney U comparisons for numeric fields."""

    rows = []

    for feature in features:
        churned = (
            df.loc[
                df["Churn"].eq("Yes"),
                feature,
            ]
            .dropna()
            .to_numpy()
        )

        retained = (
            df.loc[
                df["Churn"].eq("No"),
                feature,
            ]
            .dropna()
            .to_numpy()
        )

        if (
            len(churned) == 0
            or len(retained) == 0
        ):
            continue

        statistic, p_value = (
            stats.mannwhitneyu(
                churned,
                retained,
                alternative="two-sided",
            )
        )

        denominator = (
            len(churned)
            * len(retained)
        )

        rank_biserial_abs = abs(
            1
            - (
                2
                * statistic
                / denominator
            )
        )

        rows.append(
            {
                "feature": feature,
                "churned_n": int(
                    len(churned)
                ),
                "retained_n": int(
                    len(retained)
                ),
                "churned_median": round(
                    float(
                        np.median(
                            churned
                        )
                    ),
                    2,
                ),
                "retained_median": round(
                    float(
                        np.median(
                            retained
                        )
                    ),
                    2,
                ),
                "mann_whitney_u": round(
                    float(statistic),
                    2,
                ),
                "p_value": float(
                    p_value
                ),
                "rank_biserial_abs": round(
                    float(
                        rank_biserial_abs
                    ),
                    4,
                ),
                "significant_0_05": (
                    p_value < 0.05
                ),
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values(
            "rank_biserial_abs",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def bootstrap_intervals(
    df: pd.DataFrame,
    dimensions: list[str],
    iterations: int = 1000,
    seed: int = 42,
) -> pd.DataFrame:
    """Bootstrap 95% churn-rate intervals by segment."""

    rng = np.random.default_rng(
        seed
    )

    rows = []

    for dimension in dimensions:
        grouped = df.groupby(
            dimension,
            observed=True,
            dropna=False,
        )

        for category, segment in grouped:
            values = (
                segment["churned"]
                .astype(float)
                .to_numpy()
            )

            if not len(values):
                continue

            simulated = rng.choice(
                values,
                size=(
                    iterations,
                    len(values),
                ),
                replace=True,
            ).mean(axis=1)

            rows.append(
                {
                    "dimension": dimension,
                    "category": str(
                        category
                    ),
                    "customers": int(
                        len(values)
                    ),
                    "churn_rate_pct": round(
                        values.mean()
                        * 100,
                        2,
                    ),
                    "ci_95_lower_pct": round(
                        float(
                            np.percentile(
                                simulated,
                                2.5,
                            )
                            * 100
                        ),
                        2,
                    ),
                    "ci_95_upper_pct": round(
                        float(
                            np.percentile(
                                simulated,
                                97.5,
                            )
                            * 100
                        ),
                        2,
                    ),
                }
            )

    return pd.DataFrame(rows)
