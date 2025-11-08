"""Fanning friction factor for louvered fins (Kays & London)."""
from __future__ import annotations

from math import isfinite

__all__ = ["f_kays_london_louvered_fin"]


def f_kays_london_louvered_fin(reynolds: float) -> float:
    """Return a louvered-fin Fanning factor from Kays & London charts."""

    if not isfinite(reynolds) or reynolds <= 0:
        raise ValueError("f_kays_london_louvered_fin: Re doit être > 0.")

    return 1.95 * reynolds ** -0.75


f_kays_london_louvered_fin.metadata = {
    "flow_domain": "compact_heat_exchanger",
    "surface": "louvered_fin",
    "quantity": "fanning_friction_factor",
    "reference": "Kays-London",
}
