"""Utility correlation: convert j-factor to heat-transfer coefficient."""
from __future__ import annotations


_METADATA = {
    "domain": "compact exchanger",
    "convection": "forced",
    "geometry": "j-factor conversion",
}


def j_colburn_to_h(j: float, G: float, cp: float, Pr: float) -> float:
    """Convert a Colburn *j* factor into an HTC."""

    if j <= 0:
        raise ValueError("j -> h: le facteur j doit être > 0.")
    if min(G, cp, Pr) <= 0:
        raise ValueError("j -> h: G, cp et Pr doivent être > 0.")

    return j * G * cp / (Pr ** (2.0 / 3.0))


j_colburn_to_h.metadata = _METADATA.copy()


__all__ = ["j_colburn_to_h"]
