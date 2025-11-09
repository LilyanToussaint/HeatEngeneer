"""Seban-Shimazaki correlation for liquid-metal internal flows."""
from __future__ import annotations


_METADATA = {
    "domain": "internal",
    "convection": "forced",
    "geometry": "liquid metal circular tube",
}


def h_liquid_metal_internals(
    Re: float,
    Pr: float,
    k: float,
    d_h: float,
) -> float:
    """Return HTC for liquid-metal flows inside tubes (low-Pr fluids)."""

    if Re <= 0 or Pr <= 0:
        raise ValueError("Liquide métal: Re et Pr doivent être > 0.")
    if d_h <= 0:
        raise ValueError("Liquide métal: d_h doit être > 0.")
    if Pr > 0.1:
        raise ValueError("Liquide métal: Pr doit être <= 0.1.")

    Nu = 4.8 + 0.0158 * Re ** 0.8 * Pr
    return Nu * k / d_h


h_liquid_metal_internals.metadata = _METADATA.copy()


__all__ = ["h_liquid_metal_internals"]
