# Why parquet on a volume, not Postgres

The cached table is a matrix. After the data service collapses the BIOM file, each row is a sample and each remaining column is a phylum count. The 2k subset has about 2,000 samples and a few dozen phyla, plus three metadata fields: `sample_id`, `study_id`, and `habitat`. Most cells are zero. A sample does not contain every phylum.

Training reads that whole matrix once. Prediction of a stored sample reads one row. Nothing in that path is a join. The relational shape of the same data is a long table, `(sample_id, phylum, count)`, which you pivot back into a matrix on every train and every lookup. The pivot is the expensive step, and the database would be storing a matrix as a join.

Postgres would also bring transactions, indexes, and a server that this cache does not use. Rows are not edited in place. The data service rebuilds the table when the download changes, writes `phylum_counts.parquet`, and the gateway reads it. Columnar parquet compresses the zero runs and keeps the wide layout the forest already wants.

The file sits on a volume (`HABITAT_DATA_DIR`, `/data` in Compose) so the raw BIOM download and the fitted model can live with the cache without being committed. The committed fixture is a small CSV. The service writes the parquet copy of that fixture the same way it writes the EMP cache.

On this subset the closed-reference BIOM is 34 MB (69,901 observations by 2,000 samples). After the phylum collapse the parquet cache is about 250 KB: 2,000 rows by 89 phylum columns plus the three metadata fields.
