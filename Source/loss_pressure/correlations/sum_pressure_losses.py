"""Sum linear and minor pressure losses."""
from __future__ import annotations

from math import isfinite
from typing import Iterable

__all__ = ["sum_pressure_losses"]


def sum_pressure_losses(
    linear_losses: Iterable[float],
    minor_losses: Iterable[float],
) -> float:
    """Return the total pressure loss from iterables of contributions."""

    total = 0.0
    for category, losses in {"linéaires": linear_losses, "mineures": minor_losses}.items():
        for value in losses:
            if not isfinite(value):
                raise ValueError(
                    f"sum_pressure_losses: perte {category} non finie: {value!r}"
                )
            total += value
    return total


sum_pressure_losses.metadata = {
    "quantity": "pressure_drop",
    "type": "aggregation",
}
