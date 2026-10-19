"""Load the cached forest and score one sample."""

import json
from pathlib import Path

import joblib
import pandas as pd

from habitat.labels import HABITATS
from services.data.cache import read_phylum_table
from services.features.transform import align_abundance
from services.paths import METRICS_NAME, MODEL_NAME, TABLE_NAME


class ArtifactNotFound(FileNotFoundError):
    pass


class UnknownSample(KeyError):
    pass


def load_artifact(data_dir: Path) -> dict:
    path = data_dir / MODEL_NAME
    if not path.is_file():
        raise ArtifactNotFound(f"no model at {path}")
    artifact = joblib.load(path)
    if "model" not in artifact or "feature_columns" not in artifact:
        raise ValueError(f"model file {path} is missing feature columns")
    return artifact


def load_metrics(data_dir: Path) -> dict:
    path = data_dir / METRICS_NAME
    if not path.is_file():
        raise ArtifactNotFound(f"no metrics at {path}")
    return json.loads(path.read_text())


def load_table(data_dir: Path) -> pd.DataFrame:
    path = data_dir / TABLE_NAME
    if not path.is_file():
        raise ArtifactNotFound(f"no phylum table at {path}")
    return read_phylum_table(path)


def _probabilities(artifact: dict, vector: list[float]) -> dict[str, float]:
    model = artifact["model"]
    proba = model.predict_proba([vector])[0]
    by_class = {str(label): float(score) for label, score in zip(model.classes_, proba)}
    return {habitat: by_class.get(habitat, 0.0) for habitat in HABITATS}


def predict_abundances(artifact: dict, values) -> dict:
    columns = list(artifact["feature_columns"])
    vector = align_abundance(values, columns)
    probabilities = _probabilities(artifact, vector)
    habitat = max(probabilities, key=probabilities.get)
    return {"habitat": habitat, "probabilities": probabilities}


def predict_sample(artifact: dict, table: pd.DataFrame, sample_id: str) -> dict:
    columns = list(artifact["feature_columns"])
    rows = table.loc[table["sample_id"] == str(sample_id)]
    if rows.empty:
        raise UnknownSample(sample_id)
    row = rows.iloc[0]
    counts = {column: float(row[column]) if column in table.columns else 0.0 for column in columns}
    return predict_abundances(artifact, counts)
