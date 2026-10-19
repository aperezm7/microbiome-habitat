import pytest

from challenges.loader import load


def test_joins_multiline_sequence():
    records = load("01_read-fasta").read_fasta_records(">seq1\nAT\nGC\n>seq2\nTT\n")
    assert records == [("seq1", "ATGC"), ("seq2", "TT")]


def test_id_is_first_token():
    records = load("01").read_fasta_records(">seq1 a description\nAAAA\n")
    assert records == [("seq1", "AAAA")]


def test_empty_header():
    with pytest.raises(ValueError, match="empty"):
        load("01_read-fasta").read_fasta_records(">\nATCG\n")


def test_whitespace_header():
    with pytest.raises(ValueError, match="empty"):
        load("01_read-fasta").read_fasta_records(">   \nATCG\n")


def test_duplicate_header():
    text = ">seq1\nATCG\n>seq1\nGGGG\n"
    with pytest.raises(ValueError, match="duplicate"):
        load("01_read-fasta").read_fasta_records(text)


def test_duplicate_id_with_different_description():
    text = ">seq1 one\nATCG\n>seq1 two\nGGGG\n"
    with pytest.raises(ValueError, match="duplicate"):
        load("01_read-fasta").read_fasta_records(text)
