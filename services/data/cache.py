"""Parquet cache of the wide phylum count table."""

from pathlib import Path

import pandas as pd

from services.data.collapse import phylum_table_from_files
from services.data.download import ensure_emp_downloads
from services.data.validate import validate_phylum_table
from services.paths import TABLE_NAME, fixture_csv


def write_phylum_table(frame: pd.DataFrame, dest: Path) -> Path:
    validate_phylum_table(frame)
    dest.parent.mkdir(parents=True, exist_ok=True)
    stored = frame.copy()
    stored["sample_id"] = stored["sample_id"].astype(str)
    stored["study_id"] = stored["study_id"].astype(str)
    stored.to_parquet(dest, index=False)
    return dest


def read_phylum_table(path: Path) -> pd.DataFrame:
    frame = pd.read_parquet(path)
    frame["sample_id"] = frame["sample_id"].astype(str)
    frame["study_id"] = frame["study_id"].astype(str)
    validate_phylum_table(frame)
    return frame


def read_fixture_frame() -> pd.DataFrame:
    frame = pd.read_csv(fixture_csv())
    frame["sample_id"] = frame["sample_id"].astype(str)
    frame["study_id"] = frame["study_id"].astype(str)
    frame["habitat"] = frame["habitat"].astype(str)
    validate_phylum_table(frame)
    return frame


def cache_fixture(out_dir: Path) -> Path:
    dest = out_dir / TABLE_NAME
    write_phylum_table(read_fixture_frame(), dest)
    return dest


def cache_emp(out_dir: Path) -> Path:
    """Download the subset, collapse it to phylum, and write parquet.

    The raw BIOM stays under ``out_dir/downloads`` and is not part of the repo.
    """
    mapping, biom = ensure_emp_downloads(out_dir)
    frame = phylum_table_from_files(biom, mapping)
    if len(frame) < 1500:
        raise ValueError(
            f"only {len(frame)} labeled samples matched the subset BIOM; "
            "the sample ids in the mapping and the table did not line up"
        )
    dest = out_dir / TABLE_NAME
    write_phylum_table(frame, dest)
    return dest
