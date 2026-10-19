"""Train the habitat forest and write model, metrics, and the parquet cache."""

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

from habitat.labels import HABITATS
from habitat.metrics import balanced_accuracy
from habitat.split import split_by_study
from services.data.cache import cache_emp, cache_fixture, read_phylum_table
from services.data.validate import phylum_columns
from services.features.transform import to_relative_abundance
from services.paths import METRICS_NAME, MODEL_NAME

N_ESTIMATORS = 200


def train_frame(
    frame: pd.DataFrame,
    *,
    test_size: float = 0.25,
    seed: int = 0,
    n_estimators: int = N_ESTIMATORS,
) -> tuple[dict, dict]:
    relative = to_relative_abundance(frame)
    columns = [column for column in phylum_columns(relative) if float(relative[column].sum()) > 0]
    columns = sorted(columns)
    if not columns:
        raise ValueError("no non-zero phylum columns to train on")
    features = relative[columns].to_numpy(dtype=float)
    labels = relative["habitat"].astype(str).tolist()
    studies = relative["study_id"].astype(str).tolist()
    train_index, test_index = split_by_study(studies, test_size=test_size, seed=seed)
    train_studies = sorted({studies[i] for i in train_index})
    test_studies = sorted({studies[i] for i in test_index})
    if set(train_studies) & set(test_studies):
        raise ValueError("a study landed in both train and test")
    forest = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=seed,
        class_weight="balanced_subsample",
        n_jobs=1,
    )
    forest.fit(features[train_index], [labels[i] for i in train_index])
    y_true = [labels[i] for i in test_index]
    y_pred = forest.predict(features[test_index]).tolist()
    score = balanced_accuracy(y_true, y_pred)
    present = [habitat for habitat in HABITATS if habitat in set(y_true) or habitat in set(y_pred)]
    matrix = confusion_matrix(y_true, y_pred, labels=present).tolist()
    artifact = {
        "model": forest,
        "feature_columns": columns,
        "habitats": list(HABITATS),
        "seed": seed,
        "test_size": test_size,
    }
    metrics = {
        "balanced_accuracy": score,
        "confusion_matrix": {"labels": present, "matrix": matrix},
        "n_train": len(train_index),
        "n_test": len(test_index),
        "train_studies": train_studies,
        "test_studies": test_studies,
        "n_samples": len(labels),
        "n_phyla": len(columns),
        "seed": seed,
        "test_size": test_size,
    }
    return artifact, metrics


def _write_outputs(out_dir: Path, artifact: dict, metrics: dict) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, out_dir / MODEL_NAME)
    (out_dir / METRICS_NAME).write_text(json.dumps(metrics, indent=2) + "\n")
    return metrics


def train_from_fixture(out_dir: Path, *, test_size: float = 0.25, seed: int = 0) -> dict:
    """Train on the committed fixture. This path does not use the network."""
    table_path = cache_fixture(out_dir)
    frame = read_phylum_table(table_path)
    artifact, metrics = train_frame(frame, test_size=test_size, seed=seed)
    metrics["source"] = "fixture"
    return _write_outputs(out_dir, artifact, metrics)


def train_from_emp(out_dir: Path, *, test_size: float = 0.25, seed: int = 0) -> dict:
    """Download the EMP subset, cache phylum counts as parquet, and train."""
    table_path = cache_emp(out_dir)
    frame = read_phylum_table(table_path)
    artifact, metrics = train_frame(frame, test_size=test_size, seed=seed)
    metrics["source"] = "emp"
    return _write_outputs(out_dir, artifact, metrics)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Train the EMPO habitat random forest")
    parser.add_argument(
        "--fixture",
        action="store_true",
        help="Train on the committed fixture. Does not download the EMP table.",
    )
    parser.add_argument(
        "--emp",
        action="store_true",
        help="Download the EMP 2k subset, collapse to phylum, cache parquet, and train.",
    )
    parser.add_argument("--out", type=Path, default=Path("var"))
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--test-size", type=float, default=0.25)
    args = parser.parse_args(argv)
    if args.fixture and args.emp:
        parser.error("pass only one of --fixture or --emp")
    if args.emp:
        metrics = train_from_emp(args.out, test_size=args.test_size, seed=args.seed)
    else:
        metrics = train_from_fixture(args.out, test_size=args.test_size, seed=args.seed)
    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
