# Complete the functions below, do not change the signatures.

def read_fasta_records(text: str) -> list[tuple[str, str]]:
    """Return (id, sequence) pairs. Reject an empty or duplicate header."""
    # Read FASTA text into (id, sequence) pairs.
    # The id is the first token after '>'.
    # Raise ValueError if a header is empty or only whitespace.
    # Raise ValueError if the same id appears twice. Matching is case-sensitive.
    # Sequence lines belonging to one record are joined with whitespace removed.
    # Use Biopython SeqIO to read the sequences. SeqIO does not reject a
    # duplicate id, so check headers yourself.
    # Example:
    #   read_fasta_records(">seq1\nAT\nGC\n>seq2\nTT\n")
    #   returns [("seq1", "ATGC"), ("seq2", "TT")]
    raise NotImplementedError("read_fasta_records")
