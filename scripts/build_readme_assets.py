from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "readme"
TABLES = ROOT / "outputs" / "tables"

ASSETS.mkdir(
    parents=True,
    exist_ok=True,
)


overview = pd.read_csv(
    TABLES / "churn_overview.csv"
).iloc[0]

risk = pd.read_csv(
    TABLES / "highest_risk_segments.csv"
).iloc[0]


# Project banner
fig, ax = plt.subplots(
    figsize=(12, 3.2)
)

fig.patch.set_facecolor(
    "#0f172a"
)

ax.set_facecolor(
    "#0f172a"
)

ax.axis("off")

ax.text(
    0.04,
    0.65,
    "THE CUSTOMER EXIT",
    fontsize=30,
    fontweight="bold",
    color="white",
    transform=ax.transAxes,
)

ax.text(
    0.04,
    0.37,
    "Telecom Customer Churn Analytics",
    fontsize=16,
    color="#cbd5e1",
    transform=ax.transAxes,
)

ax.text(
    0.04,
    0.15,
    "Cyril James Lunzaga",
    fontsize=12,
    color="#94a3b8",
    transform=ax.transAxes,
)

fig.tight_layout()

fig.savefig(
    ASSETS / "project_banner.png",
    dpi=180,
    bbox_inches="tight",
    facecolor=fig.get_facecolor(),
)

plt.close(fig)


# KPI strip
fig, ax = plt.subplots(
    figsize=(12, 3)
)

ax.axis("off")

kpis = [
    (
        f"{int(overview['customers']):,}",
        "Customers",
    ),
    (
        f"{overview['churn_rate_pct']:.2f}%",
        "Overall churn",
    ),
    (
        f"{int(overview['churned_customers']):,}",
        "Churned",
    ),
    (
        f"{risk['churn_rate_pct']:.2f}%",
        "Highest-risk segment",
    ),
]

for index, (
    value,
    label,
) in enumerate(kpis):
    x = 0.05 + index * 0.24

    ax.text(
        x,
        0.62,
        value,
        fontsize=24,
        fontweight="bold",
        transform=ax.transAxes,
    )

    ax.text(
        x,
        0.35,
        label,
        fontsize=11,
        transform=ax.transAxes,
    )

fig.tight_layout()

fig.savefig(
    ASSETS / "kpi_summary.png",
    dpi=180,
    bbox_inches="tight",
)

plt.close(fig)


# Workflow graphic
steps = [
    "Raw data",
    "Data audit",
    "Cleaning",
    "EDA",
    "Segmentation",
    "Statistics",
    "Business insights",
    "Validation",
    "Reporting",
]

fig, ax = plt.subplots(
    figsize=(13, 3.2)
)

ax.axis("off")

positions = [
    index / (
        len(steps) - 1
    )
    for index in range(
        len(steps)
    )
]

for index, (
    x,
    step,
) in enumerate(
    zip(
        positions,
        steps,
    )
):
    ax.text(
        x,
        0.55,
        step,
        ha="center",
        va="center",
        fontsize=9,
        bbox={
            "boxstyle": "round,pad=0.5",
            "facecolor": "#f8fafc",
            "edgecolor": "#64748b",
        },
        transform=ax.transAxes,
    )

    if index < len(
        steps
    ) - 1:
        ax.annotate(
            "",
            xy=(
                positions[
                    index + 1
                ] - 0.035,
                0.55,
            ),
            xytext=(
                x + 0.035,
                0.55,
            ),
            xycoords=ax.transAxes,
            arrowprops={
                "arrowstyle": "->",
                "color": "#64748b",
            },
        )

ax.set_title(
    "Analytics Workflow",
    fontsize=16,
    pad=18,
)

fig.tight_layout()

fig.savefig(
    ASSETS / "analytics_workflow.png",
    dpi=180,
    bbox_inches="tight",
)

plt.close(fig)


print(
    "Generated 3 README assets."
)
