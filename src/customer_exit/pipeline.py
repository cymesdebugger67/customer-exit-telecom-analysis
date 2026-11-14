from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .cleaning import (
    audit_raw_data,
    clean_data,
)
from .config import (
    load_config,
    project_path,
)
from .data_loader import load_raw_data
from .features import add_features
from .metrics import (
    grouped_rate,
    numeric_churn_summary,
    overview_table,
)
from .reporting import write_reports
from .segmentation import (
    churn_concentration,
    highest_risk_segments,
)
from .statistics import (
    bootstrap_intervals,
    categorical_association_summary,
    numeric_test_summary,
)
from .visualization import (
    save_association_strength,
    save_concentration_curve,
    save_contract_tenure_heatmap,
    save_numeric_boxplot,
    save_overview,
    save_rate_bar,
)


def run_pipeline(
    config: dict | None = None,
    source_path: Path | None = None,
    output_dir: Path | None = None,
    report_dir: Path | None = None,
    processed_path: Path | None = None,
) -> dict:
    """Run the full analytics workflow."""

    config = config or load_config()

    source = (
        source_path
        or project_path(
            config["source_path"]
        )
    )

    output = (
        output_dir
        or project_path(
            config["output_dir"]
        )
    )

    reports = (
        report_dir
        or project_path(
            config["report_dir"]
        )
    )

    processed = (
        processed_path
        or project_path(
            config["processed_path"]
        )
    )

    table_dir = output / "tables"
    chart_dir = output / "charts"
    diagnostics_dir = (
        output / "diagnostics"
    )

    for directory in [
        table_dir,
        chart_dir,
        diagnostics_dir,
        reports,
        processed.parent,
    ]:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    raw = load_raw_data(source)

    audit = audit_raw_data(raw)

    cleaned = clean_data(raw)

    data = add_features(
        cleaned,
        config,
    )

    data.to_csv(
        processed,
        index=False,
    )

    overview = overview_table(data)

    contract = grouped_rate(
        data,
        "Contract",
    )

    tenure = grouped_rate(
        data.dropna(
            subset=["tenure_group"]
        ),
        "tenure_group",
    )

    internet = grouped_rate(
        data,
        "InternetService",
    )

    charge = grouped_rate(
        data.dropna(
            subset=[
                "monthly_charge_band"
            ]
        ),
        "monthly_charge_band",
    )

    payment = grouped_rate(
        data,
        "PaymentMethod",
    )

    paperless = grouped_rate(
        data,
        "PaperlessBilling",
    )

    support_profile = grouped_rate(
        data,
        "support_security_profile",
    )

    protection = grouped_rate(
        data,
        "protection_level",
    )

    senior = grouped_rate(
        data,
        "senior_status",
    )

    partner = grouped_rate(
        data,
        "Partner",
    )

    dependents = grouped_rate(
        data,
        "Dependents",
    )

    gender = grouped_rate(
        data,
        "gender",
    )

    contract_tenure = grouped_rate(
        data.dropna(
            subset=["tenure_group"]
        ),
        [
            "Contract",
            "tenure_group",
        ],
    )

    internet_contract = grouped_rate(
        data,
        [
            "InternetService",
            "Contract",
        ],
    )

    payment_paperless = grouped_rate(
        data,
        [
            "PaymentMethod",
            "PaperlessBilling",
        ],
    )

    risk = highest_risk_segments(
        data,
        minimum_customers=config[
            "minimum_segment_size"
        ],
    )

    concentration = (
        churn_concentration(
            risk,
            total_churned=int(data["churned"].sum()),
        )
    )

    numeric_summary = (
        numeric_churn_summary(
            data,
            config[
                "numeric_features"
            ],
        )
    )

    categorical_stats = (
        categorical_association_summary(
            data,
            config[
                "categorical_features"
            ],
        )
    )

    numeric_tests = (
        numeric_test_summary(
            data,
            config[
                "numeric_features"
            ],
        )
    )

    bootstrap = (
        bootstrap_intervals(
            data,
            [
                "Contract",
                "tenure_group",
                "InternetService",
                "PaymentMethod",
                "support_security_profile",
                "protection_level",
            ],
            iterations=config[
                "bootstrap_iterations"
            ],
            seed=config[
                "bootstrap_seed"
            ],
        )
    )

    tables = {
        "churn_overview":
            overview,
        "churn_by_contract":
            contract,
        "churn_by_tenure":
            tenure,
        "churn_by_internet":
            internet,
        "churn_by_monthly_charge":
            charge,
        "churn_by_payment_method":
            payment,
        "churn_by_paperless_billing":
            paperless,
        "churn_by_support_security_profile":
            support_profile,
        "churn_by_protection_level":
            protection,
        "churn_by_senior_status":
            senior,
        "churn_by_partner":
            partner,
        "churn_by_dependents":
            dependents,
        "churn_by_gender":
            gender,
        "churn_by_contract_tenure":
            contract_tenure,
        "churn_by_internet_contract":
            internet_contract,
        "churn_by_payment_paperless":
            payment_paperless,
        "highest_risk_segments":
            risk,
        "churn_concentration":
            concentration,
        "numeric_churn_summary":
            numeric_summary,
        "categorical_associations":
            categorical_stats,
        "numeric_tests":
            numeric_tests,
        "bootstrap_intervals":
            bootstrap,
    }

    for name, table in tables.items():
        table.to_csv(
            table_dir
            / f"{name}.csv",
            index=False,
        )

    (
        diagnostics_dir
        / "data_quality_audit.json"
    ).write_text(
        json.dumps(
            audit,
            indent=2,
        ),
        encoding="utf-8",
    )

    save_overview(
        data,
        chart_dir
        / "churn_overview.png",
    )

    save_rate_bar(
        contract,
        "Contract",
        chart_dir
        / "churn_by_contract.png",
        "Churn Rate by Contract",
    )

    save_rate_bar(
        tenure,
        "tenure_group",
        chart_dir
        / "churn_by_tenure.png",
        "Churn Rate by Tenure",
    )

    save_rate_bar(
        internet,
        "InternetService",
        chart_dir
        / "churn_by_internet.png",
        "Churn Rate by Internet Service",
    )

    save_rate_bar(
        charge,
        "monthly_charge_band",
        chart_dir
        / "churn_by_monthly_charge.png",
        "Churn Rate by Monthly Charge Band",
    )

    save_rate_bar(
        payment,
        "PaymentMethod",
        chart_dir
        / "churn_by_payment_method.png",
        "Churn Rate by Payment Method",
    )

    save_rate_bar(
        support_profile,
        "support_security_profile",
        chart_dir
        / "churn_by_support_security_profile.png",
        "Churn Rate by Support / Security Profile",
    )

    save_rate_bar(
        protection,
        "protection_level",
        chart_dir
        / "churn_by_protection_level.png",
        "Churn Rate by Protection-Service Level",
    )

    save_rate_bar(
        senior,
        "senior_status",
        chart_dir
        / "churn_by_senior_status.png",
        "Churn Rate by Senior-Citizen Status",
    )

    save_contract_tenure_heatmap(
        contract_tenure,
        chart_dir
        / "churn_by_contract_tenure.png",
        config[
            "tenure_labels"
        ],
    )

    risk_plot = risk.copy()

    risk_plot["segment"] = (
        risk_plot["Contract"]
        + " | "
        + risk_plot[
            "tenure_group"
        ].astype(str)
        + " | "
        + risk_plot[
            "InternetService"
        ]
    )

    save_rate_bar(
        risk_plot.head(10),
        "segment",
        chart_dir
        / "highest_risk_segments.png",
        "Highest-Risk Customer Segments",
    )

    save_numeric_boxplot(
        data,
        "MonthlyCharges",
        chart_dir
        / "monthly_charges_by_churn.png",
        "Monthly Charges by Churn Status",
    )

    save_association_strength(
        categorical_stats,
        chart_dir
        / "categorical_association_strength.png",
    )

    save_concentration_curve(
        concentration,
        chart_dir
        / "churn_concentration.png",
    )

    payment_plot = (
        payment_paperless.copy()
    )

    payment_plot["segment"] = (
        payment_plot[
            "PaymentMethod"
        ]
        + " | Paperless="
        + payment_plot[
            "PaperlessBilling"
        ]
    )

    save_rate_bar(
        payment_plot,
        "segment",
        chart_dir
        / "churn_by_payment_paperless.png",
        "Churn Rate by Payment Method and Paperless Billing",
    )

    write_reports(
        tables,
        audit,
        reports,
    )

    return {
        "customers": len(data),
        "tables": len(tables),
        "charts": len(
            list(
                chart_dir.glob(
                    "*.png"
                )
            )
        ),
        "reports": len(
            list(
                reports.glob(
                    "*.md"
                )
            )
        ),
        "audit": audit,
    }


def main():
    """CLI entry point."""

    summary = run_pipeline()

    print(
        "Large analytics pipeline complete."
    )

    print(
        f"Customers: {summary['customers']:,}"
    )

    print(
        f"Tables: {summary['tables']}"
    )

    print(
        f"Charts: {summary['charts']}"
    )

    print(
        f"Reports: {summary['reports']}"
    )


if __name__ == "__main__":
    main()
