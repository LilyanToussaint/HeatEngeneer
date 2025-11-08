"""Wrapper selecting inline or staggered Zukauskas tube-bank correlation."""
from __future__ import annotations

from math import isfinite

from .dp_zukauskas_tube_bank_inline import dp_zukauskas_tube_bank_inline
from .dp_zukauskas_tube_bank_staggered import dp_zukauskas_tube_bank_staggered

__all__ = ["dp_zukauskas_tube_bank"]


def dp_zukauskas_tube_bank(
    reynolds: float,
    n_rows: int,
    configuration: str,
    density: float | None = None,
    velocity: float | None = None,
) -> float:
    """Select the appropriate Zukauskas tube-bank correlation."""

    if configuration not in {"inline", "staggered"}:
        raise ValueError("dp_zukauskas_tube_bank: configuration doit être 'inline' ou 'staggered'.")

    if not isfinite(reynolds) or reynolds <= 0:
        raise ValueError("dp_zukauskas_tube_bank: Re doit être > 0 et fini.")
    if n_rows <= 0:
        raise ValueError("dp_zukauskas_tube_bank: n_rows doit être positif.")

    if configuration == "inline":
        return dp_zukauskas_tube_bank_inline(reynolds, n_rows, density=density, velocity=velocity)
    return dp_zukauskas_tube_bank_staggered(
        reynolds,
        n_rows,
        density=density,
        velocity=velocity,
    )


dp_zukauskas_tube_bank.metadata = {
    "flow_domain": "external",
    "configuration": "tube_bank",
    "quantity": "loss_coefficient",
    "selector": True,
}
