"""Hidden solutions and src stay on the same algorithm."""

import math

import numpy as np
import pytest
from sklearn.metrics import balanced_accuracy_score

from challenges.loader import load
from habitat.abundance import relative_abundance
from habitat.diversity import shannon_diversity
from habitat.fasta import read_fasta_records
from habitat.metrics import balanced_accuracy
from habitat.split import split_by_study


def test_fasta_matches():
    text = ">seq1\nAT\nGC\n>seq2 note\nTT\n"
    assert load("01").read_fasta_records(text) == read_fasta_records(text)


def test_relative_matches():
    assert load("02").relative_abundance([2, 2, 0]) == relative_abundance([2, 2, 0])


def test_shannon_matches_src_and_scipy():
    from scipy.stats import entropy

    counts = [10, 0, 5, 5]
    hidden = load("03").shannon_diversity(counts)
    assert hidden == shannon_diversity(counts)
    total = sum(counts)
    proportions = [c / total for c in counts if c > 0]
    assert hidden == pytest.approx(entropy(proportions, base=math.e))


def test_split_matches():
    studies = ["b", "a", "b", "c", "a", "d"]
    assert load("04").split_by_study(studies, 0.3, 4) == split_by_study(studies, 0.3, 4)


def test_balanced_accuracy_matches_sklearn():
    rng = np.random.default_rng(0)
    labels = np.array(["saline", "non-saline", "host"])
    y_true = labels[rng.integers(0, 3, size=40)]
    y_pred = labels[rng.integers(0, 3, size=40)]
    hidden = load("05").balanced_accuracy(y_true, y_pred)
    assert hidden == balanced_accuracy(y_true, y_pred)
    assert hidden == balanced_accuracy_score(y_true, y_pred)
