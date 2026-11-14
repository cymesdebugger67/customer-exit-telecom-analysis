"""Portfolio visualization helpers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_rate_bar(
    table: pd.DataFrame,
    category: str,
    destination: Path,
    title: str,
    value_column: str = "churn_rate_pct",
    value_suffix: str = "%",
) -> None:
    """Save a horizontal ranked bar chart."""

    data = (
        table.dropna(
            subset=[category]
        )
        .sort_values(
            value_column
        )
        .copy()
    )

    fig, ax = plt.subplots(
        figsize=(10, max(
            5,
            len(data) * 0.55,
        ))
    )

    bars = ax.barh(
        data[category].astype(str),
        data[value_column],
    )

    ax.set_title(title)
    ax.set_xlabel(
        value_column.replace(
            "_",
            " ",
        ).title()
    )
    ax.set_ylabel("")

    for bar, value in zip(
        bars,
        data[value_column],
    ):
        ax.text(
            bar.get_width(),
            bar.get_y()
            + bar.get_height() / 2,
            f" {value:.2f}{value_suffix}",
            va="center",
        )

    fig.tight_layout()

    fig.savefig(
        destination,
        dpi=170,
        bbox_inches="tight",
    )

    plt.close(fig)


def save_overview(
    df: pd.DataFrame,
    destination: Path,
) -> None:
    """Save retained/churned customer counts."""

    counts = (
        df["Churn"]
        .value_counts()
        .reindex(["No", "Yes"])
    )

    fig, ax = plt.subplots(
        figsize=(7, 5)
    )

    bars = ax.bar(
        ["Retained", "Churned"],
        counts.values,
    )

    ax.set_title(
        "Customer Churn Overview"
    )

    ax.set_ylabel(
        "Customers"
    )

    for bar, value in zip(
        bars,
        counts.values,
    ):
        ax.text(
            bar.get_x()
            + bar.get_width() / 2,
            bar.get_height(),
            f"{int(value):,}",
            ha="center",
            va="bottom",
        )

    fig.tight_layout()

    fig.savefig(
        destination,
        dpi=170,
        bbox_inches="tight",
    )

    plt.close(fig)


def save_contract_tenure_heatmap(
    table: pd.DataFrame,
    destination: Path,
    tenure_order: list[str],
) -> None:
    """Save contract-by-tenure churn heatmap."""

    pivot = table.pivot(
        index="tenure_group",
        columns="Contract",
        values="churn_rate_pct",
    )

    pivot = pivot.reindex(
        tenure_order
    )

    contract_order = [
        "Month-to-month",
        "One year",
        "Two year",
    ]

    pivot = pivot.reindex(
        columns=contract_order
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    image = ax.imshow(
        pivot.values,
        aspect="auto",
    )

    ax.set_xticks(
        range(
            len(
                pivot.columns
            )
        )
    )

    ax.set_xticklabels(
        pivot.columns,
        rotation=20,
        ha="right",
    )

    ax.set_yticks(
        range(
            len(
                pivot.index
            )
        )
    )

    ax.set_yticklabels(
        pivot.index,
    )

    ax.set_title(
        "Churn Rate: Contract ? Tenure"
    )

    for row in range(
        len(pivot.index)
    ):
        for column in range(
            len(pivot.columns)
        ):
            value = pivot.iloc[
                row,
                column,
            ]

            if pd.notna(value):
                ax.text(
                    column,
                    row,
                    f"{value:.1f}%",
                    ha="center",
                    va="center",
                )

    fig.colorbar(
        image,
        ax=ax,
        label="Churn rate (%)",
    )

    fig.tight_layout()

    fig.savefig(
        destination,
        dpi=170,
        bbox_inches="tight",
    )

    plt.close(fig)


def save_numeric_boxplot(
    df: pd.DataFrame,
    column: str,
    destination: Path,
    title: str,
) -> None:
    """Compare a numeric variable by churn status."""

    retained = (
        df.loc[
            df["Churn"].eq("No"),
            column,
        ]
        .dropna()
    )

    churned = (
        df.loc[
            df["Churn"].eq("Yes"),
            column,
        ]
        .dropna()
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.boxplot(
        [
            retained,
            churned,
        ],
        tick_labels=[
            "Retained",
            "Churned",
        ],
        showfliers=False,
    )

    ax.set_title(title)

    ax.set_ylabel(column)

    fig.tight_layout()

    fig.savefig(
        destination,
        dpi=170,
        bbox_inches="tight",
    )

    plt.close(fig)


def save_association_strength(
    table: pd.DataFrame,
    destination: Path,
) -> None:
    """Visualize categorical association strengths."""

    data = (
        table.sort_values(
            "cramers_v"
        )
        .tail(12)
    )

    save_rate_bar(
        data,
        "feature",
        destination,
        "Categorical Association Strength with Churn",
        value_column="cramers_v",
        value_suffix="",
    )


def save_concentration_curve(
    table: pd.DataFrame,
    destination: Path,
) -> None:
    """Save cumulative churn concentration curve."""

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    ax.plot(
        table["segment_rank"],
        table[
            "cumulative_churn_share_pct"
        ],
        marker="o",
    )

    ax.set_title(
        "Cumulative Churn Share Across Eligible Segments"
    )

    ax.set_xlabel(
        "Eligible segment rank (by churn count)"
    )

    ax.set_ylabel(
        "Cumulative share of all churn (%)"
    )

    ax.set_ylim(
        0,
        105,
    )

    ax.grid(
        alpha=0.25
    )

    fig.tight_layout()

    fig.savefig(
        destination,
        dpi=170,
        bbox_inches="tight",
    )

    plt.close(fig)
