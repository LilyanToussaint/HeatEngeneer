"""Pressure-drop correlation for staggered tube banks (Zukauskas)."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_zukauskas_tube_bank_staggered"]


def dp_zukauskas_tube_bank_staggered(
    reynolds: float,
    n_rows: int,
    density: float | None = None,
    velocity: float | None = None,
) -> float:
    """Return either a loss coefficient or a pressure drop for staggered tube banks."""

    if not isfinite(reynolds) or reynolds <= 0:
        raise ValueError("dp_zukauskas_tube_bank_staggered: Re doit être positif et fini.")
    if n_rows <= 0:
        raise ValueError("dp_zukauskas_tube_bank_staggered: n_rows doit être positif.")
    if density is not None and density <= 0:
        raise ValueError("dp_zukauskas_tube_bank_staggered: densité doit être positive.")
    if velocity is not None and velocity < 0:
        raise ValueError("dp_zukauskas_tube_bank_staggered: vitesse doit être >= 0.")

    phi = (0.9 + 0.12 * (n_rows - 1)) * reynolds ** -0.2
    if density is not None and velocity is not None:
        return phi * 0.5 * density * velocity**2
    return phi


dp_zukauskas_tube_bank_staggered.metadata = {
    "flow_domain": "external",
    "configuration": "tube_bank_staggered",
    "quantity": "loss_coefficient",
    "reference": "Zukauskas",
}
