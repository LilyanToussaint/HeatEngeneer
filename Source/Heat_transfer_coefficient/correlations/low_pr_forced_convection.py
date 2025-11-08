"""Correlation for very low Prandtl number forced convection."""
from __future__ import annotations


_METADATA = {
    "domain": "internal",
    "convection": "forced",
    "geometry": "low Prandtl internal flow",
}


def h_low_Pr_forced_convection(
    Re: float,
    Pr: float,
    k: float,
    d_h: float,
    L: float,
) -> float:
    """Return HTC for low-Prandtl-number forced convection."""

    if Re <= 0 or Pr <= 0:
        raise ValueError("Low-Pr forced convection: Re et Pr doivent être > 0.")
    if d_h <= 0 or L <= 0:
        raise ValueError("Low-Pr forced convection: d_h et L doivent être > 0.")
    if Pr > 0.7:
        raise ValueError("Low-Pr forced convection: corrélation pensée pour Pr <= 0.7.")

    Nu = (
        0.664 * Re ** 0.5 * Pr ** (1.0 / 3.0)
        + 0.037 * Re ** 0.8 * Pr ** (1.0 / 3.0) * (1.0 - 2.443 * Re ** -0.1)
    )
    return Nu * k / d_h


h_low_Pr_forced_convection.metadata = _METADATA.copy()


__all__ = ["h_low_Pr_forced_convection"]
