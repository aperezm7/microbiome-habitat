# Data

## Question

Can a phylum-level 16S profile predict EMPO habitat: free-living saline, free-living non-saline, or host-associated?

## Citation

Thompson, L. R. et al. A communal catalogue reveals Earth's multiscale microbial diversity. *Nature* 551, 457–463 (2017). https://doi.org/10.1038/nature24621

Archive: https://doi.org/10.5281/zenodo.890000 (Zenodo record 890000). License of that archive: CC BY 4.0.

EMP FTP listing: https://github.com/biocore/emp/blob/master/data/ftp_contents.txt

## What is downloaded

Only `python -m services.model.train --emp` downloads. CI, `pytest`, `--fixture`, and the default Compose service do not.

| File | Where | Role |
| --- | --- | --- |
| `emp_qiime_mapping_subset_2k_20170912.tsv` | Zenodo 890000 | Sample metadata, including `study_id`, `empo_1`, `empo_2`. MD5 `25cf231f596e9d0543f61b2985baed82`. |
| `emp_cr_gg_13_8.subset_2k.biom` | EMP FTP `otu_tables/closed_ref_greengenes/` | The matching 2,000-sample closed-reference Greengenes 13.8 table. About 34 MB. Observation metadata includes `taxonomy`. |

Zenodo record 890000 stores the 2k mapping file and the **full** release BIOM tables (`*.release1.biom`, hundreds of MB to about 3 GB). It does not store a pre-cut 2k BIOM. The matching subset table is on the EMP FTP. The closed-reference Greengenes subset is the one used here because its observation metadata already carries phylum labels. The Deblur subset BIOMs on the same FTP store exact sequences, not ranks.

URLs are constants in `services/data/sources.py`.

The data service filters to rows with an EMPO label, collapses observations to phylum, and writes `phylum_counts.parquet`. Counts are not rarefied. The feature service turns each row into relative abundance.

Downloaded files go to `{HABITAT_DATA_DIR}/downloads/`. They are gitignored.

## What is committed

| Path | What it is |
| --- | --- |
| `fixtures/phylum_counts.csv` | 27 synthetic samples, 9 studies, 6 phyla. Used by `--fixture`, tests, and Docker. |
| `fixtures/tiny_table.biom` | Four-observation BIOM used to test phylum collapse. |
| `fixtures/tiny_mapping.tsv` | Four-row mapping used with that BIOM. |

The EMP BIOM is not committed. The collapsed EMP parquet is a cache on the volume, not a file in git.

## Labels

| `empo_1` | `empo_2` | Habitat |
| --- | --- | --- |
| Host-associated | Animal or Plant | `host-associated` |
| Free-living | Saline | `free-living saline` |
| Free-living | Non-saline | `free-living non-saline` |

Controls and unlabeled rows are dropped.
