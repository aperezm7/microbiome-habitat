"""Locate the repo root and the on-disk cache."""

import os
from pathlib import Path

TABLE_NAME = "phylum_counts.parquet"
MODEL_NAME = "model.joblib"
METRICS_NAME = "metrics.json"


def repo_root() -> Path:
    override = os.environ.get("HABITAT_ROOT")
    if override:
        return Path(override)
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "fixtures" / "phylum_counts.csv").is_file():
            return parent
    raise FileNotFoundError("fixtures/phylum_counts.csv not found; set HABITAT_ROOT")


def data_dir() -> Path:
    return Path(os.environ.get("HABITAT_DATA_DIR", repo_root() / "var"))


def fixture_csv() -> Path:
    return repo_root() / "fixtures" / "phylum_counts.csv"


def tiny_biom() -> Path:
    return repo_root() / "fixtures" / "tiny_table.biom"


def tiny_mapping() -> Path:
    return repo_root() / "fixtures" / "tiny_mapping.tsv"
