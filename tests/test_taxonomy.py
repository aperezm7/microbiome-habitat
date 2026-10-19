from habitat.taxonomy import extract_phylum


def test_greengenes_list():
    meta = {"taxonomy": ["k__Bacteria", "p__Firmicutes", "c__Clostridia"]}
    assert extract_phylum(meta) == "p__Firmicutes"


def test_greengenes_string():
    assert extract_phylum("k__Bacteria; p__Proteobacteria; c__Gammaproteobacteria") == "p__Proteobacteria"


def test_silva_rank():
    assert extract_phylum("D_0__Bacteria;D_1__Bacteroidetes") == "p__Bacteroidetes"


def test_missing_is_unclassified():
    assert extract_phylum(None) == "p__unclassified"
    assert extract_phylum({"taxonomy": ["k__Bacteria", "p__"]}) == "p__unclassified"
