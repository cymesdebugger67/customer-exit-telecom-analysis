from pathlib import Path

import pytest

from customer_exit.config import (
    PROJECT_ROOT,
    load_config,
)
from customer_exit.pipeline import run_pipeline


def test_real_pipeline_if_data_available(
    tmp_path,
):
    config = load_config()

    source = (
        PROJECT_ROOT
        / config[
            "source_path"
        ]
    )

    if not source.exists():
        pytest.skip(
            "Raw source data is intentionally excluded from Git."
        )

    summary = run_pipeline(
        config=config,
        source_path=source,
        output_dir=(
            tmp_path
            / "outputs"
        ),
        report_dir=(
            tmp_path
            / "reports"
        ),
        processed_path=(
            tmp_path
            / "processed.csv"
        ),
    )

    assert (
        summary["customers"]
        == 7043
    )

    assert (
        summary["tables"]
        == 22
    )

    assert (
        summary["charts"]
        == 15
    )

    assert (
        summary["reports"]
        == 3
    )
