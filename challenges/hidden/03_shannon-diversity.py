"""Shannon diversity from a count vector."""

import math
from collections.abc import Mapping

EXPLANATION = """
Shannon diversity is the entropy of the relative-abundance distribution,
H = -sum(p ln p), using the natural log. Zero counts are skipped because
p ln(p) tends to 0 as p tends to 0. A sample with one taxon scores 0. The
habitat model does not use this single number; it uses the whole phylum vector.
Normalize counts inside the function. Do not assume the caller already did.
""".strip()


def _as_float(value: object) -> float:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        raise ValueError("counts must be numeric") from exc
    if not math.isfinite(number):
        raise ValueError("counts must be finite")
    if number < 0:
        raise ValueError("counts must be non-negative")
    return number


def _relative(counts) -> list[float]:
    if isinstance(counts, Mapping):
        values = [_as_float(value) for value in counts.values()]
    else:
        values = [_as_float(value) for value in counts]
    if not values:
        raise ValueError("counts must not be empty")
    total = math.fsum(values)
    if total <= 0:
        raise ValueError("counts must sum to a positive number")
    return [value / total for value in values]


def shannon_diversity(counts) -> float:
    proportions = _relative(counts)
    score = 0.0
    for proportion in proportions:
        if proportion > 0:
            score -= proportion * math.log(proportion)
    return score
