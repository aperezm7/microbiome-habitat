import httpx

from services.model.train import train_from_fixture


def test_fixture_train_is_offline_and_study_disjoint(monkeypatch, tmp_path):
    def explode(*args, **kwargs):
        raise AssertionError("fixture training tried to use the network")

    monkeypatch.setattr(httpx, "stream", explode)
    monkeypatch.setattr(httpx, "get", explode)
    metrics = train_from_fixture(tmp_path)
    assert (tmp_path / "phylum_counts.parquet").is_file()
    assert (tmp_path / "model.joblib").is_file()
    assert (tmp_path / "metrics.json").is_file()
    assert metrics["source"] == "fixture"
    assert 0.0 <= metrics["balanced_accuracy"] <= 1.0
    assert set(metrics["train_studies"]).isdisjoint(metrics["test_studies"])
    matrix = metrics["confusion_matrix"]["matrix"]
    labels = metrics["confusion_matrix"]["labels"]
    assert len(matrix) == len(labels)
    assert all(len(row) == len(labels) for row in matrix)
    assert sum(sum(row) for row in matrix) == metrics["n_test"]
    assert metrics["n_train"] + metrics["n_test"] == metrics["n_samples"]
