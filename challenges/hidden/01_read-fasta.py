"""Read FASTA with Biopython and reject a bad header."""

from io import StringIO

from Bio import SeqIO

EXPLANATION = """
A FASTA id is the first token after '>'. An empty header cannot be joined to a
sequence later, and a repeated id would silently overwrite a record in a
dict-shaped parser. Biopython SeqIO reads the records and does not reject
duplicates, so this solution checks headers first and then uses SeqIO for the
sequences. The habitat service does not parse FASTA. It reads the EMP BIOM table.
""".strip()


def read_fasta_records(text: str) -> list[tuple[str, str]]:
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
