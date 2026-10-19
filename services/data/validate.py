"""Checks for the cached phylum count table."""

import math

import pandas as pd

from habitat.labels import HABITATS

META_COLUMNS = ("sample_id", "study_id", "habitat")


def phylum_columns(frame: pd.DataFrame) -> list[str]:
    return [column for column in frame.columns if column not in META_COLUMNS]


def validate_phylum_table(frame: pd.DataFrame) -> None:
    missing = [column for column in META_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"phylum table is missing {missing}")
    if frame.empty:
        raise ValueError("phylum table has no rows")
    if frame["sample_id"].duplicated().any():
        raise ValueError("phylum table has duplicate sample_id values")
    unknown = sorted(set(frame["habitat"]) - set(HABITATS))
    if unknown:
        raise ValueError(f"unknown habitat labels: {unknown}")
    columns = phylum_columns(frame)
    if not columns:
        raise ValueError("phylum table has no count columns")
    counts = frame[columns]
    values = counts.to_numpy(dtype=float)
    if not math.isfinite(float(np_sum_abs(values))):
        raise ValueError("phylum counts must be finite")
    if (values < 0).any():
        raise ValueError("phylum counts must be non-negative")
    if (values.sum(axis=1) <= 0).any():
        raise ValueError("every sample needs a positive count total")


def np_sum_abs(values) -> float:
    return float(abs(values).sum())
