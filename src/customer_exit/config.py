from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "analysis_config.json"


def load_config(path: Path | None = None) -> dict:
    """Load project configuration."""

    config_path = path or DEFAULT_CONFIG

    with config_path.open(
        encoding="utf-8"
    ) as handle:
        return json.load(handle)


def project_path(value: str) -> Path:
    """Resolve a configured project-relative path."""

    return PROJECT_ROOT / value
