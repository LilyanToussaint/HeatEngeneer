"""Fanning friction factor for offset-strip fins."""
from __future__ import annotations

from math import isfinite

__all__ = ["f_manglik_bergles_offset_strip_fin"]


def f_manglik_bergles_offset_strip_fin(reynolds: float) -> float:
    """Return the Fanning friction factor using Manglik & Bergles correlation."""

    if not isfinite(reynolds) or reynolds <= 0:
        raise ValueError("f_manglik_bergles_offset_strip_fin: Re doit être > 0.")

    return 9.6243 * reynolds ** -1.084


f_manglik_bergles_offset_strip_fin.metadata = {
    "flow_domain": "compact_heat_exchanger",
    "surface": "offset_strip_fin",
    "quantity": "fanning_friction_factor",
    "reference": "Manglik-Bergles",
}
