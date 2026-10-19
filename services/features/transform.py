"""Relative abundance, aligned to the model's phylum columns."""

from collections.abc import Mapping

import pandas as pd

from habitat.abundance import relative_abundance
from services.data.validate import phylum_columns


def to_relative_abundance(frame: pd.DataFrame) -> pd.DataFrame:
    columns = phylum_columns(frame)
    proportions: list[list[float]] = []
    for row in frame[columns].itertuples(index=False, name=None):
        scaled = relative_abundance([float(value) for value in row])
        proportions.append(list(scaled))
    relative = frame[["sample_id", "study_id", "habitat"]].copy()
    relative[columns] = pd.DataFrame(proportions, columns=columns, index=frame.index)
    return relative


def align_abundance(
    values: Mapping[str, float] | list[float],
    columns: list[str],
) -> list[float]:
    """Put one sample on the model column order and scale it to relative abundance.

    A list must already follow ``columns``. A mapping may omit phyla (those
    counts are zero) and may include unknown keys (those are ignored). Scaling
    then uses the aligned values, so a count vector and a proportion vector
    that already sums to 1 both become relative abundances.
    """
    if isinstance(values, str) or isinstance(values, bytes):
        raise ValueError("abundances must be a map or a list")
    if isinstance(values, Mapping):
        raw = [float(values.get(column, 0.0)) for column in columns]
    else:
        raw = [float(value) for value in values]
        if len(raw) != len(columns):
            raise ValueError(
                f"abundance vector length {len(raw)} does not match {len(columns)} phyla"
            )
    scaled = relative_abundance(raw)
    return list(scaled)
