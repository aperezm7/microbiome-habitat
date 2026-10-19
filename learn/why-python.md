# Why this stays Python

An R version of the same study is easy to picture.

- Read the subset with `biomformat::read_biom`.
- Turn it into a phyloseq object, then `tax_glom(rank = "Phylum")`.
- Convert counts with `transform_sample_counts(table, function(x) x / sum(x))`.
- Shannon diversity is `vegan::diversity(counts, index = "shannon")`.
- The forest is `randomForest::randomForest` or `ranger`.
- A study-wise split is a few lines of base R. `caret::createDataPartition` splits rows, not studies, so you still have to group on `study_id` yourself.
- The HTTP API would be a second process, usually `plumber`.

That stack can answer the science question. This repo stays in Python because the running service and the practice tasks are the same code. `src/habitat` holds relative abundance, the study split, and balanced accuracy. The feature service and the model service import those functions. The hidden challenge solutions repeat the same algorithms so a learner can compare them. One process loads the BIOM table, writes parquet, fits the scikit-learn forest, and serves `POST /predict`.

Splitting the work across R and Python would add a boundary, `rpy2` or a side car, for no change in the estimate. The BIOM reader, the forest, and FastAPI are all ordinary Python packages.
