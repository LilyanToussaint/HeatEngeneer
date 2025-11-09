"""Simple heat-capacity correlation for steel."""
from __future__ import annotations

__all__ = ["cp_steel"]


def cp_steel(temperature: float) -> float:
    """Return the isobaric heat capacity of carbon steel [J/kg/K]."""

    # Approximation: cp(T) = a + b·T with coefficients fitted around 300 K.
    a = 420.0
    b = 0.12
    return a + b * max(temperature, 0.0)
