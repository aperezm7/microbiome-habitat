"""Count vectors to relative abundance."""

import math
from collections.abc import Mapping


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


def relative_abundance(counts: Mapping[str, float] | list[float]) -> dict[str, float] | list[float]:
    """Divide each count by the total.

    A mapping keeps its keys and returns a mapping. A sequence returns a list
    in the same order. The result sums to 1. An empty vector, a non-numeric
    value, a negative count, or a total of zero raises ValueError.
    """
    if isinstance(counts, str) or isinstance(counts, bytes):
        raise ValueError("counts must be numeric")
    if isinstance(counts, Mapping):
        keys = list(counts)
        values = [_as_float(counts[key]) for key in keys]
        scaled = _scale(values)
        return {key: value for key, value in zip(keys, scaled)}
    values = [_as_float(value) for value in counts]
    return _scale(values)


def _scale(values: list[float]) -> list[float]:
    if not values:
        raise ValueError("counts must not be empty")
    total = math.fsum(values)
    if total <= 0:
        raise ValueError("counts must sum to a positive number")
    return [value / total for value in values]
