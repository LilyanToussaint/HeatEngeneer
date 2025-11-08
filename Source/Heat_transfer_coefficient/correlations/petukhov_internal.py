"""Petukhov correlation for turbulent internal flow in smooth tubes."""
from math import log

_METADATA = {
    "domain": "internal",
    "convection": "forced",
    "geometry": "smooth circular tube",
    "regime": "turbulent",
}


def h_petukhov_internal(Re: float, Pr: float, k: float, d_i: float) -> float:
    """Return the convection coefficient from the Petukhov correlation."""
    if not (3.0e3 <= Re <= 5.0e6):
        raise ValueError("Petukhov: Re hors domaine (3e3 <= Re <= 5e6).")
    if not (0.5 <= Pr <= 2000.0):
        raise ValueError("Petukhov: Pr hors domaine (Pr).")

    f = (0.79 * log(Re) - 1.64) ** -2
    nu = (
        (f / 8.0)
        * (Re - 1000.0)
        * Pr
        /
        (1.0 + 12.7 * (f / 8.0) ** 0.5 * (Pr ** (2.0 / 3.0) - 1.0))
    )
    return nu * k / d_i


h_petukhov_internal.metadata = _METADATA.copy()

__all__ = ["h_petukhov_internal"]
