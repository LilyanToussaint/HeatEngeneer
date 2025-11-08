"""Zukauskas staggered tube bank correlation."""
from __future__ import annotations


_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "tube bank staggered",
}


_COEFFS = (
    (1e2, 1.04, 0.4),
    (1e3, 1.11, 0.36),
    (2e5, 1.18, 0.33),
    (5e5, 1.22, 0.27),
)


def _coefficients(Re: float) -> tuple[float, float]:
    for limit, C, m in _COEFFS:
        if Re <= limit:
            return C, m
    return 1.27, 0.24


def h_zukauskas_staggered_tube_bank(
    Re: float,
    Pr: float,
    k: float,
    d_o: float,
    N_rows: int = 10,
    Pr_s: float | None = None,
) -> float:
    """Return the HTC for a staggered bank of tubes (Zukauskas)."""

    if Re <= 0 or Pr <= 0:
        raise ValueError("Zukauskas staggered: Re et Pr doivent être > 0.")
    if d_o <= 0:
        raise ValueError("Zukauskas staggered: diamètre extérieur > 0 requis.")
    if N_rows <= 0:
        raise ValueError("Zukauskas staggered: nombre de rangées doit être > 0.")

    C, m = _coefficients(Re)
    Nu = C * Re ** m * Pr ** 0.36
    if Pr_s is not None and Pr_s > 0:
        Nu *= (Pr / Pr_s) ** 0.25

    if N_rows < 3:
        Nu *= (N_rows / 3.0) ** 0.15

    return Nu * k / d_o


h_zukauskas_staggered_tube_bank.metadata = _METADATA.copy()


__all__ = ["h_zukauskas_staggered_tube_bank"]
