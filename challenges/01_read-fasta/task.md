# 01 Read a FASTA record

Read FASTA text into `(id, sequence)` pairs.

- The id is the first token after `>`.
- Raise `ValueError` if a header is empty or only whitespace.
- Raise `ValueError` if the same id appears twice. Matching is case-sensitive.
- Sequence lines belonging to one record are joined with whitespace removed.
- Use Biopython `SeqIO` to read the sequences. `SeqIO` does not reject a duplicate id, so check headers yourself.

```python
read_fasta_records(">seq1\nAT\nGC\n>seq2\nTT\n")
# [("seq1", "ATGC"), ("seq2", "TT")]
```

The habitat service does not parse FASTA. It reads the EMP BIOM table. This task is format practice.

Run your starter with:

```bash
USE_HIDDEN_SOLUTIONS=0 pytest challenges/01_read-fasta
```

The shipped test run grades `challenges/hidden/01_read-fasta.py`.
