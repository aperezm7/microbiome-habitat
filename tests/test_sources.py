from services.data.sources import BIOM_URL, MAPPING_MD5, MAPPING_URL


def test_urls_are_the_2k_subset():
    assert "emp_qiime_mapping_subset_2k_20170912.tsv" in MAPPING_URL
    assert "emp_cr_gg_13_8.subset_2k.biom" in BIOM_URL
    assert "release1.biom" not in BIOM_URL
    assert len(MAPPING_MD5) == 32
