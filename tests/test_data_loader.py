import pandas as pd
import pytest

from customer_exit.data_loader import load_raw_data


def test_loader_reads_csv(tmp_path):
    path = tmp_path / "sample.csv"

    pd.DataFrame({
        "value": [10, 20, 30]
    }).to_csv(path, index=False)

    result = load_raw_data(path)

    assert len(result) == 3
    assert result["value"].sum() == 60


def test_loader_rejects_missing_file(tmp_path):
    missing = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_raw_data(missing)
