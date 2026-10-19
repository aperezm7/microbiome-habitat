import numpy as np
from biom.table import Table

from services.data.collapse import attach_labels, collapse_biom, phylum_table_from_files, read_mapping
from services.paths import tiny_biom, tiny_mapping


def _tiny_table() -> Table:
    data = np.array(
        [
            [10, 0, 1],
            [5, 0, 0],
            [0, 3, 0],
            [0, 7, 0],
        ],
        dtype=int,
    )
    return Table(
        data,
        observation_ids=["otu1", "otu2", "otu3", "otu4"],
        sample_ids=["sampleA", "sampleB", "sampleZ"],
        observation_metadata=[
            {"taxonomy": ["k__Bacteria", "p__Firmicutes"]},
            {"taxonomy": ["k__Bacteria", "p__Firmicutes"]},
            {"taxonomy": ["k__Bacteria", "p__Proteobacteria"]},
            {"taxonomy": "k__Bacteria; p__Bacteroidetes; c__Bacteroidia"},
        ],
    )


def test_collapse_sums_phyla_and_drops_unlabeled_samples():
    counts = collapse_biom(_tiny_table())
    labeled = attach_labels(counts, read_mapping(tiny_mapping()))
    assert labeled["sample_id"].tolist() == ["sampleA", "sampleB"]
    assert labeled["habitat"].tolist() == ["host-associated", "free-living saline"]
    assert labeled["study_id"].tolist() == ["10", "11"]
    by_id = labeled.set_index("sample_id")
    assert by_id.loc["sampleA", "p__Firmicutes"] == 15
    assert by_id.loc["sampleA", "p__Proteobacteria"] == 0
    assert by_id.loc["sampleB", "p__Bacteroidetes"] == 7
    assert by_id.loc["sampleB", "p__Proteobacteria"] == 3
    assert "sampleC" not in set(labeled["sample_id"])
    assert "sampleZ" not in set(labeled["sample_id"])
    assert "blank1" not in set(labeled["sample_id"])


def test_committed_biom_fixture_matches_the_in_memory_table():
    from_file = phylum_table_from_files(tiny_biom(), tiny_mapping())
    from_memory = attach_labels(collapse_biom(_tiny_table()), read_mapping(tiny_mapping()))
    assert from_file["sample_id"].tolist() == from_memory["sample_id"].tolist()
    assert from_file["p__Firmicutes"].tolist() == [15, 0]
