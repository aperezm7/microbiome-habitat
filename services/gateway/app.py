"""POST /predict scores a stored sample or a phylum abundance vector."""

import logging
import os
from collections.abc import Mapping
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, model_validator

from habitat.labels import HABITATS
from services.model.infer import (
    ArtifactNotFound,
    UnknownSample,
    load_artifact,
    load_metrics,
    load_table,
    predict_abundances,
    predict_sample,
)
from services.model.train import train_from_emp, train_from_fixture
from services.paths import data_dir

logger = logging.getLogger("microbiome_habitat")


class PredictRequest(BaseModel):
    sample_id: str | None = None
    abundances: dict[str, float] | list[float] | None = None

    @model_validator(mode="after")
    def exactly_one_input(self):
        has_id = self.sample_id is not None
        has_vector = self.abundances is not None
        if has_id == has_vector:
            raise ValueError("provide exactly one of sample_id or abundances")
        return self


class PredictResponse(BaseModel):
    habitat: str
    probabilities: dict[str, float]


def _prepare(directory: Path) -> None:
    source = os.environ.get("HABITAT_SOURCE", "fixture")
    if (directory / "model.joblib").is_file() and (directory / "phylum_counts.parquet").is_file():
        logger.info("using cached model in %s", directory)
        return
    if source == "emp":
        metrics = train_from_emp(directory)
    else:
        metrics = train_from_fixture(directory)
    logger.info(
        "trained %s model; balanced accuracy %.4f",
        metrics["source"],
        metrics["balanced_accuracy"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    directory = data_dir()
    directory.mkdir(parents=True, exist_ok=True)
    _prepare(directory)
    app.state.data_dir = directory
    app.state.artifact = load_artifact(directory)
    app.state.table = load_table(directory)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="EMPO habitat from phylum 16S",
        summary="Predict free-living saline, free-living non-saline, or host-associated.",
        lifespan=lifespan,
    )

    @app.get("/")
    def root() -> dict:
        return {
            "question": (
                "Can a phylum-level 16S profile predict EMPO habitat "
                "(free-living saline, free-living non-saline, or host-associated)?"
            ),
            "habitats": list(HABITATS),
            "endpoints": ["/health", "/metrics", "/features", "/predict"],
        }

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/metrics")
    def metrics() -> dict:
        try:
            return load_metrics(app.state.data_dir)
        except ArtifactNotFound as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.get("/features")
    def features() -> dict:
        return {"phyla": list(app.state.artifact["feature_columns"])}

    @app.post("/predict", response_model=PredictResponse)
    def predict(body: PredictRequest) -> dict:
        try:
            if body.sample_id is not None:
                return predict_sample(app.state.artifact, app.state.table, body.sample_id)
            abundances = body.abundances
            if not isinstance(abundances, (Mapping, list)):
                raise ValueError("abundances must be a map or a list")
            return predict_abundances(app.state.artifact, abundances)
        except UnknownSample as exc:
            raise HTTPException(status_code=404, detail=f"unknown sample_id {exc}") from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_app()
