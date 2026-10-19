import pytest

from challenges.loader import load


def test_list_proportions():
    assert load("02").relative_abundance([2, 2, 0]) == [0.5, 0.5, 0.0]


def test_mapping_keeps_keys():
    result = load("02_relative-abundance").relative_abundance({"Firmicutes": 1, "Proteobacteria": 3})
    assert result == {"Firmicutes": 0.25, "Proteobacteria": 0.75}


def test_already_a_proportion_is_unchanged():
    assert load("02").relative_abundance([0.5, 0.5]) == [0.5, 0.5]


def test_rejects_zero_total():
    with pytest.raises(ValueError):
        load("02").relative_abundance([0, 0, 0])


def test_rejects_negative():
    with pytest.raises(ValueError):
        load("02").relative_abundance([1, -1])


def test_rejects_empty():
    with pytest.raises(ValueError):
        load("02").relative_abundance([])
