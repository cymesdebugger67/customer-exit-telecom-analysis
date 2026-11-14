import json
from pathlib import Path

import pandas as pd

from customer_exit.reporting import write_reports


def test_reporting_generates_three_reports(tmp_path):
    root = Path(__file__).resolve().parents[1]

    table_dir = root / "outputs" / "tables"
    audit_path = (
        root / "outputs" / "diagnostics"
        / "data_quality_audit.json"
    )

    assert table_dir.is_dir()
    assert audit_path.is_file()

    tables = {
        path.stem: pd.read_csv(path)
        for path in table_dir.glob("*.csv")
    }

    audit = json.loads(
        audit_path.read_text(encoding="utf-8")
    )

    write_reports(tables, audit, tmp_path)

    expected = [
        "executive_summary.md",
        "analytical_report.md",
        "portfolio_summary.md",
    ]

    for filename in expected:
        report = tmp_path / filename

        assert report.is_file()
        assert report.stat().st_size > 100

    assert len(list(tmp_path.glob("*.md"))) == 3
