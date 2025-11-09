"""Kays & London style correlation for louvered fins."""
from __future__ import annotations

import math


_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "compact exchanger louvered fin",
}


def h_louvered_fin_kays_london(
    Re: float,
    Pr: float,
    k: float,
    D_h: float,
    pitch_ratio: float = 1.5,
    louver_angle_deg: float = 27.0,
) -> float:
    """Return the HTC for louvered fins using a Kays & London style fit."""

    if Re <= 0 or Pr <= 0:
        raise ValueError("Louvered fin: Re et Pr doivent être > 0.")
    if D_h <= 0 or pitch_ratio <= 0:
        raise ValueError("Louvered fin: D_h et pitch_ratio doivent être > 0.")

    theta = math.radians(louver_angle_deg)
    j = 0.086 * Re ** -0.17 * pitch_ratio ** -0.3 * math.cos(theta) ** 0.5
    Nu = j * Re * Pr ** (1.0 / 3.0)
    return Nu * k / D_h


h_louvered_fin_kays_london.metadata = _METADATA.copy()


__all__ = ["h_louvered_fin_kays_london"]
