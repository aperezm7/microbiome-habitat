"""Where the Earth Microbiome Project 16S Release 1 subset lives.

Zenodo record 890000 is the citable archive for the Nature paper. It stores
``emp_qiime_mapping_subset_2k_20170912.tsv`` and the full release BIOM tables,
not a pre-cut 2k BIOM. The matching 2,000-sample closed-reference Greengenes
table is on the EMP FTP. That table's observation metadata already has a
``taxonomy`` category, so phylum collapse does not need a second taxonomy file.
"""

ZENODO_RECORD = "https://zenodo.org/records/890000"
ZENODO_DOI = "10.5281/zenodo.890000"
PAPER_DOI = "10.1038/nature24621"

MAPPING_URL = (
    "https://zenodo.org/records/890000/files/emp_qiime_mapping_subset_2k_20170912.tsv"
)
MAPPING_MD5 = "25cf231f596e9d0543f61b2985baed82"

BIOM_URL = (
    "https://ftp.microbio.me/emp/release1/otu_tables/"
    "closed_ref_greengenes/emp_cr_gg_13_8.subset_2k.biom"
)
