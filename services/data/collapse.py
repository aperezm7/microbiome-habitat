"""Collapse a BIOM table to phylum counts and attach EMPO habitat labels."""

from pathlib import Path

import numpy as np
import pandas as pd

from habitat.labels import habitat_from_empo
from habitat.taxonomy import extract_phylum


def read_mapping(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, sep="\t", dtype=str)
    if "#SampleID" in frame.columns:
        frame = frame.rename(columns={"#SampleID": "sample_id"})
    if "sample_id" not in frame.columns:
        raise ValueError("mapping file has no #SampleID column")
    for column in ("study_id", "empo_1", "empo_2"):
        if column not in frame.columns:
            raise ValueError(f"mapping file has no {column} column")
    return frame


def collapse_biom(table) -> pd.DataFrame:
    """Sum observation counts by phylum. One row per sample, wide columns."""
    sample_ids = [str(sample) for sample in table.ids(axis="sample")]
    phyla = [
        extract_phylum(table.metadata(obs, axis="observation"))
        for obs in table.ids(axis="observation")
    ]
    matrix = table.matrix_data.tocsr()
    groups: dict[str, list[int]] = {}
    for index, phylum in enumerate(phyla):
        groups.setdefault(phylum, []).append(index)
    collapsed = {
        phylum: np.asarray(matrix[indexes].sum(axis=0)).ravel()
        for phylum, indexes in groups.items()
    }
    frame = pd.DataFrame(collapsed, index=sample_ids)
    frame.index.name = "sample_id"
    frame = frame.reset_index()
    phylum_cols = sorted(column for column in frame.columns if column != "sample_id")
    return frame[["sample_id", *phylum_cols]]


def attach_labels(counts: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
    """Inner-join phylum counts to labeled samples. Drop controls and zero rows."""
    labels = mapping.copy()
    labels["sample_id"] = labels["sample_id"].astype(str)
    labels["study_id"] = labels["study_id"].astype(str)
    labels["habitat"] = [
        habitat_from_empo(empo_1, empo_2)
        for empo_1, empo_2 in zip(labels["empo_1"], labels["empo_2"])
    ]
    labeled = labels.dropna(subset=["habitat"])
    merged = counts.merge(
        labeled[["sample_id", "study_id", "habitat"]],
        on="sample_id",
        how="inner",
    )
    meta = ["sample_id", "study_id", "habitat"]
    phyla = sorted(column for column in merged.columns if column not in meta)
    if not phyla:
        raise ValueError("collapsed table has no phylum columns")
    totals = merged[phyla].sum(axis=1)
    merged = merged.loc[totals > 0, meta + phyla].reset_index(drop=True)
    if merged.empty:
        raise ValueError("no labeled samples overlapped the BIOM table")
    return merged


def phylum_table_from_files(biom_path: Path, mapping_path: Path) -> pd.DataFrame:
    from biom import load_table

    table = load_table(str(biom_path))
    counts = collapse_biom(table)
    return attach_labels(counts, read_mapping(mapping_path))
