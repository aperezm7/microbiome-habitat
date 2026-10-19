# Microbiome habitat

Can a phylum-level 16S profile predict EMPO habitat: **free-living saline**, **free-living non-saline**, or **host-associated**?

The model is a random forest on relative abundances. Samples are split by `study_id`, so a study is never in both train and test. The test report is balanced accuracy and a confusion matrix.

This repo classifies environmental habitat from published Earth Microbiome Project profiles. It does not culture pathogens, design sequences, or engineer resistance genes.

Data and the train/test rule: [DATA.md](DATA.md). Why the cache is parquet: [learn/storage.md](learn/storage.md). Why the stack stays Python: [learn/why-python.md](learn/why-python.md).

Citation: Thompson et al., *Nature* (2017), https://doi.org/10.1038/nature24621. Archive: https://doi.org/10.5281/zenodo.890000.

## What the 2k subset says

`python -m services.model.train --emp` downloads the closed-reference Greengenes 2k table, collapses it to 89 phyla, and splits by study. With seed 0 and a test fraction of 0.25, 1,495 samples are in train and 505 are in test. No study is on both sides. Balanced accuracy on that test set is **0.572**.

The 2,000 labeled samples are uneven: 1,019 host-associated, 595 free-living non-saline, 386 free-living saline. A model that always predicts host-associated has balanced accuracy 1/3, about 0.333, because the other two recalls are zero. 0.572 is above that baseline.

Rows of the confusion matrix are the true habitat and columns are the prediction, in the order free-living saline, free-living non-saline, host-associated:

|  | saline | non-saline | host |
| --- | ---: | ---: | ---: |
| saline | 37 | 25 | 15 |
| non-saline | 2 | 66 | 129 |
| host | 10 | 13 | 208 |

Host-associated profiles are usually recognized (208 of 231). Free-living non-saline profiles are often called host-associated (129 of 197). A phylum-level relative-abundance vector carries habitat signal, and it does not cleanly separate all three classes when whole studies are held out.

## Run the tests and the fixture train

Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m services.model.train --fixture
```

`pytest` grades the service against the committed fixture and grades the challenges against `challenges/hidden`. It does not download the EMP table.

`--fixture` reads `fixtures/phylum_counts.csv`, writes `var/phylum_counts.parquet`, fits the forest, and prints balanced accuracy and the confusion matrix. No network. On this fixture, seed 0 holds out `studyH1`, `studyS1`, and `studyN1` (9 samples) and the balanced accuracy is 1.0. The rows were built so the three habitats separate. That score is not the EMP result.

To test a starter you are writing:

```bash
USE_HIDDEN_SOLUTIONS=0 pytest challenges/03_shannon-diversity
```

## Serve a prediction

Docker Compose publishes only the gateway, on port **8091**. The container trains on the fixture at startup if `/data` has no model yet. Parquet and the forest stay on the `habitat-data` volume.

```bash
docker compose up --build
```

In another shell:

```bash
curl -sS -X POST http://127.0.0.1:8091/predict \
  -H 'Content-Type: application/json' \
  -d '{"sample_id":"S.host.1"}'
```

A count vector works the same way. Missing phyla are treated as zero, then the vector is scaled to relative abundance. A list must follow the order from `GET /features`.

```bash
curl -sS -X POST http://127.0.0.1:8091/predict \
  -H 'Content-Type: application/json' \
  -d '{"abundances":{"p__Proteobacteria":430,"p__Cyanobacteria":210,"p__Firmicutes":15}}'
```

```bash
curl -sS http://127.0.0.1:8091/metrics
```

Without Docker, the same API is:

```bash
python -m services.gateway
curl -sS -X POST http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"sample_id":"S.host.1"}'
```

`POST /predict` returns `habitat` and `probabilities` for the three classes.

## Train on the EMP 2k subset

This downloads the mapping file from Zenodo and the matching closed-reference Greengenes subset BIOM from the EMP FTP (about 34 MB), collapses it to phylum, and caches parquet under `var/`. The raw BIOM is not committed.

```bash
python -m services.model.train --emp --out var
```

Set `HABITAT_SOURCE=emp` and `HABITAT_DATA_DIR` if the gateway should train on that cache instead of the fixture. The default is the fixture, including in CI and Compose.

## Layout

| Path | Role |
| --- | --- |
| `services/gateway` | FastAPI. The only public entrypoint. |
| `services/data` | Download, validate, collapse to phylum, write parquet. |
| `services/features` | Relative abundance, aligned to the model columns. |
| `services/model` | Study split, random forest, inference. |
| `src/habitat` | Functions the services import. |
| `challenges/` | Starters, public tests, and hidden solutions. |

The forest uses 200 trees, `class_weight="balanced_subsample"`, and phylum relative abundances only. `study_id` is used for the split and is not a feature.

## Challenges

| # | Task | Reveal |
| --- | --- | --- |
| 01 | Read a FASTA record; reject an empty or duplicate header (Biopython in the solution). | `python -m challenges reveal 01` |
| 02 | Convert counts to relative abundance. | `python -m challenges reveal 02` |
| 03 | Shannon diversity from a count vector. | `python -m challenges reveal 03` |
| 04 | Group split by study id. | `python -m challenges reveal 04` |
| 05 | Balanced accuracy from labels and predictions. | `python -m challenges reveal 05` |

Each directory has `task.md`, `starter.py` (raises `NotImplementedError`), and `test_challenge.py`. Hidden solutions are in `challenges/hidden/` and are not imported by the starters.
