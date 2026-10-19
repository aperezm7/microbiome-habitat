import pytest
from fastapi.testclient import TestClient

from services.gateway.app import app


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setenv("HABITAT_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("HABITAT_SOURCE", "fixture")
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_fixture_sample(client):
    response = client.post("/predict", json={"sample_id": "S.host.1"})
    assert response.status_code == 200
    body = response.json()
    assert body["habitat"] == "host-associated"
    assert set(body["probabilities"]) == {
        "free-living saline",
        "free-living non-saline",
        "host-associated",
    }
    assert body["probabilities"]["host-associated"] == max(body["probabilities"].values())
    assert sum(body["probabilities"].values()) == pytest.approx(1.0)


def test_predict_abundance_vector(client):
    response = client.post(
        "/predict",
        json={
            "abundances": {
                "p__Proteobacteria": 430,
                "p__Cyanobacteria": 210,
                "p__Firmicutes": 15,
            }
        },
    )
    assert response.status_code == 200
    assert response.json()["habitat"] == "free-living saline"


def test_predict_list_uses_feature_order(client):
    phyla = client.get("/features").json()["phyla"]
    vector = [0.0] * len(phyla)
    vector[phyla.index("p__Acidobacteria")] = 380
    vector[phyla.index("p__Actinobacteria")] = 160
    response = client.post("/predict", json={"abundances": vector})
    assert response.status_code == 200
    assert response.json()["habitat"] == "free-living non-saline"


def test_unknown_sample(client):
    response = client.post("/predict", json={"sample_id": "missing"})
    assert response.status_code == 404


def test_rejects_both_inputs(client):
    response = client.post(
        "/predict",
        json={"sample_id": "S.host.1", "abundances": {"p__Firmicutes": 1}},
    )
    assert response.status_code == 422


def test_metrics_include_confusion_matrix(client):
    body = client.get("/metrics").json()
    assert "balanced_accuracy" in body
    assert "matrix" in body["confusion_matrix"]
