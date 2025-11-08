"""Fanning friction factor for wavy fins (Kays & London)."""
from __future__ import annotations

from math import isfinite

__all__ = ["f_kays_london_wavy_fin"]


def f_kays_london_wavy_fin(reynolds: float) -> float:
    """Return a wavy-fin Fanning factor from Kays & London charts."""

    if not isfinite(reynolds) or reynolds <= 0:
        raise ValueError("f_kays_london_wavy_fin: Re doit être > 0.")

    return 2.7 * reynolds ** -0.65


f_kays_london_wavy_fin.metadata = {
    "flow_domain": "compact_heat_exchanger",
    "surface": "wavy_fin",
    "quantity": "fanning_friction_factor",
    "reference": "Kays-London",
}
