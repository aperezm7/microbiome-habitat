import pytest

from challenges.loader import load


def _split(*args, **kwargs):
    return load("04_study-split").split_by_study(*args, **kwargs)


def test_golden_example():
    train, test = _split(["b", "a", "b", "c", "a"], test_size=0.4, seed=0)
    assert train == [1, 3, 4]
    assert test == [0, 2]


def test_no_study_on_both_sides():
    studies = ["a", "a", "b", "b", "c", "c", "d", "d"]
    train, test = _split(studies, test_size=0.5, seed=1)
    assert set(train).isdisjoint(test)
    assert set(train) | set(test) == set(range(len(studies)))
    train_studies = {studies[i] for i in train}
    test_studies = {studies[i] for i in test}
    assert train_studies.isdisjoint(test_studies)
    assert train_studies and test_studies


def test_seed_changes_which_studies_are_held_out():
    studies = list("abcdef")
    first = _split(studies, test_size=0.5, seed=0)
    second = _split(studies, test_size=0.5, seed=2)
    assert first != second


def test_one_study_is_rejected():
    with pytest.raises(ValueError):
        _split(["a", "a", "a"], test_size=0.5, seed=0)


def test_test_size_bounds():
    with pytest.raises(ValueError):
        _split(["a", "b"], test_size=0, seed=0)
    with pytest.raises(ValueError):
        _split(["a", "b"], test_size=1, seed=0)


def test_large_test_size_keeps_one_study_in_train():
    studies = ["a", "b", "c"]
    train, test = _split(studies, test_size=0.99, seed=0)
    assert len({studies[i] for i in train}) == 1
    assert len(test) == 2
