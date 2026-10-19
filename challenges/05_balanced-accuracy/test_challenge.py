import pytest

from challenges.loader import load


def _score(y_true, y_pred):
    return load("05").balanced_accuracy(y_true, y_pred)


def test_mean_of_recalls():
    assert _score(["a", "a", "b", "b"], ["a", "b", "b", "b"]) == 0.75


def test_perfect_score():
    assert _score(["a", "b", "a"], ["a", "b", "a"]) == 1.0


def test_missed_class_counts_as_zero_recall():
    # Both true labels are "a"; predicting "b" has recall 0.
    assert _score(["a", "a"], ["b", "b"]) == 0.0


def test_three_classes_are_unweighted():
    y_true = ["a", "a", "a", "b", "c"]
    y_pred = ["a", "a", "a", "b", "b"]
    # recall a = 1, b = 1, c = 0 -> 2/3
    assert _score(y_true, y_pred) == pytest.approx(2 / 3)


def test_length_mismatch():
    with pytest.raises(ValueError):
        _score(["a"], ["a", "a"])


def test_empty():
    with pytest.raises(ValueError):
        _score([], [])
