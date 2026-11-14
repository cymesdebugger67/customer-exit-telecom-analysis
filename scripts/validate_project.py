"""Validate the complete large analytics project."""

from pathlib import Path
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

checks = {}


def count_files(path, pattern):
    return len(
        list(
            path.glob(pattern)
        )
    )


checks[
    "22 analytical tables"
] = (
    count_files(
        ROOT / "outputs" / "tables",
        "*.csv",
    )
    == 22
)

checks[
    "15 analytical charts"
] = (
    count_files(
        ROOT / "outputs" / "charts",
        "*.png",
    )
    == 15
)

checks[
    "3 reports"
] = (
    count_files(
        ROOT / "reports",
        "*.md",
    )
    == 3
)

checks[
    "3 README graphics"
] = (
    count_files(
        ROOT / "assets" / "readme",
        "*.png",
    )
    == 3
)

checks[
    "6 notebooks"
] = (
    count_files(
        ROOT / "notebooks",
        "*.ipynb",
    )
    == 6
)

checks[
    "8 test modules"
] = (
    count_files(
        ROOT / "tests",
        "test_*.py",
    )
    == 8
)

checks["9 documentation files"] = count_files(ROOT / "docs", "*.md") == 9

for notebook in (
    ROOT / "notebooks"
).glob("*.ipynb"):
    with notebook.open(
        encoding="utf-8"
    ) as handle:
        json.load(handle)


raw_tracking = subprocess.run(
    [
        "git",
        "ls-files",
        "data/raw/Telco-Customer-Churn.csv",
    ],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=True,
).stdout.strip()

checks[
    "Raw dataset excluded from Git"
] = not raw_tracking


print(
    "\nLARGE PROJECT VALIDATION"
)

print(
    "-" * 60
)

for name, passed in checks.items():
    print(
        f"{'PASS' if passed else 'FAIL'} | {name}"
    )


if not all(
    checks.values()
):
    sys.exit(
        "\nLarge project validation failed."
    )


print(
    "\nALL LARGE PROJECT CHECKS PASSED"
)
