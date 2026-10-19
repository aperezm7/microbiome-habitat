"""Single-record and multi-record FASTA reading.

The habitat service does not call this. Profiles arrive as a BIOM table.
The function is here so the finished algorithm matches the FASTA challenge.
"""

from io import StringIO

from Bio import SeqIO


def read_fasta_records(text: str) -> list[tuple[str, str]]:
    """Return ``(id, sequence)`` pairs from FASTA text.

    The id is the first token after ``>``. An empty or whitespace-only header
    raises ValueError. A repeated id raises ValueError. Sequences are read
    with Biopython ``SeqIO``.
    """
    if text is None or not str(text).strip():
        raise ValueError("empty FASTA input")
    header_ids: list[str] = []
    seen: set[str] = set()
    for line in str(text).splitlines():
        if not line.startswith(">"):
            continue
        tokens = line[1:].strip().split()
        if not tokens or not tokens[0]:
            raise ValueError("empty FASTA header")
        header_id = tokens[0]
        if header_id in seen:
            raise ValueError(f"duplicate FASTA header: {header_id}")
        seen.add(header_id)
        header_ids.append(header_id)
    if not header_ids:
        raise ValueError("no FASTA records")
    parsed = list(SeqIO.parse(StringIO(str(text)), "fasta"))
    if len(parsed) != len(header_ids):
        raise ValueError("FASTA record count mismatch")
    records: list[tuple[str, str]] = []
    for header_id, record in zip(header_ids, parsed):
        if record.id != header_id:
            raise ValueError(f"FASTA header parse mismatch: {header_id!r} vs {record.id!r}")
        records.append((header_id, str(record.seq)))
    return records
