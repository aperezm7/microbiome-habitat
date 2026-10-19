import math

import pytest

from challenges.loader import load


def test_single_taxon_is_zero():
    assert load("03").shannon_diversity([10, 0, 0]) == 0.0


def test_even_two_taxa_is_ln2():
    assert load("03_shannon-diversity").shannon_diversity([1, 1]) == pytest.approx(math.log(2))


def test_zeros_do_not_change_the_score():
    even = load("03").shannon_diversity([4, 4])
    with_zeros = load("03").shannon_diversity([4, 0, 4, 0])
    assert with_zeros == pytest.approx(even)


def test_rejects_all_zeros():
    with pytest.raises(ValueError):
        load("03").shannon_diversity([0, 0])
