"""Pressure-drop correlation for inline tube banks (Zukauskas)."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_zukauskas_tube_bank_inline"]


def dp_zukauskas_tube_bank_inline(
    reynolds: float,
    n_rows: int,
    density: float | None = None,
    velocity: float | None = None,
) -> float:
    """Return either a loss coefficient or a pressure drop for inline tube banks."""

    if not isfinite(reynolds) or reynolds <= 0:
        raise ValueError("dp_zukauskas_tube_bank_inline: Re doit être positif et fini.")
    if n_rows <= 0:
        raise ValueError("dp_zukauskas_tube_bank_inline: n_rows doit être positif.")
    if density is not None and density <= 0:
        raise ValueError("dp_zukauskas_tube_bank_inline: densité doit être positive.")
    if velocity is not None and velocity < 0:
        raise ValueError("dp_zukauskas_tube_bank_inline: vitesse doit être >= 0.")

    phi = (1.1 + 0.14 * (n_rows - 1)) * reynolds ** -0.15
    if density is not None and velocity is not None:
        return phi * 0.5 * density * velocity**2
    return phi


dp_zukauskas_tube_bank_inline.metadata = {
    "flow_domain": "external",
    "configuration": "tube_bank_inline",
    "quantity": "loss_coefficient",
    "reference": "Zukauskas",
}
