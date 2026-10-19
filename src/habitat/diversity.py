"""Shannon diversity of a count vector."""

import math
from collections.abc import Mapping

from habitat.abundance import relative_abundance


def shannon_diversity(counts: Mapping[str, float] | list[float]) -> float:
    """Shannon index, natural log, of a count vector.

    H = -sum(p * ln(p)) over proportions p that are greater than zero.
    A single taxon scores 0. Zero counts are omitted because p ln(p) tends
    to 0 as p tends to 0. The input is counts, not a proportion vector that
    has already been normalized; this function normalizes first.
    """
    proportions = relative_abundance(counts)
    if isinstance(proportions, Mapping):
        values = list(proportions.values())
    else:
        values = list(proportions)
    score = 0.0
    for proportion in values:
        if proportion > 0:
            score -= proportion * math.log(proportion)
    return score
