"""Pull a phylum name out of a BIOM observation's taxonomy metadata."""

import re

_UNCLASSIFIED = "p__unclassified"
_EMPTY = {"", "unclassified", "none", "nan", "null"}


def taxonomy_text(metadata: object) -> str:
    if metadata is None:
        return ""
    if isinstance(metadata, str):
        return metadata
    if isinstance(metadata, dict):
        if "taxonomy" in metadata:
            return taxonomy_text(metadata.get("taxonomy"))
        return ""
    if isinstance(metadata, (list, tuple)):
        return ";".join(str(part) for part in metadata)
    return str(metadata)


def extract_phylum(metadata: object) -> str:
    """Return a ``p__Name`` label.

    Greengenes ranks look like ``p__Firmicutes``. SILVA ranks in this release
    style look like ``D_1__Firmicutes``. Missing or blank ranks become
    ``p__unclassified``.
    """
    text = taxonomy_text(metadata)
    if not text.strip():
        return _UNCLASSIFIED
    for part in re.split(r"[;|]", text):
        token = part.strip()
        rank = None
        name = None
        if token.startswith("p__") or token.startswith("P__"):
            rank = "p__"
            name = token.split("__", 1)[1]
        elif token.startswith("D_1__") or token.startswith("d_1__"):
            rank = "p__"
            name = token.split("__", 1)[1]
        if rank is None or name is None:
            continue
        cleaned = name.strip()
        if cleaned.lower() in _EMPTY:
            return _UNCLASSIFIED
        return f"p__{cleaned}"
    return _UNCLASSIFIED
