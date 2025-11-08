"""Whitaker correlation for forced convection over spheres."""
from math import pow

_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "sphere",
}


def h_whitaker_sphere(
    Re: float,
    Pr: float,
    k: float,
    D: float,
    mu: float,
    mu_s: float,
) -> float:
    """Return the average HTC using the Whitaker correlation for spheres."""
    if Re < 3.5 or Re > 7.6e4:
        raise ValueError("Whitaker: Re hors domaine (3.5 <= Re <= 7.6e4).")
    if not (0.71 <= Pr <= 380.0):
        raise ValueError("Whitaker: Pr hors domaine (Pr).")
    if D <= 0.0 or mu <= 0.0 or mu_s <= 0.0:
        raise ValueError("Whitaker: dimensions/viscosités doivent être > 0.")

    Nu = 2.0 + (
        0.4 * pow(Re, 0.5)
        + 0.06 * pow(Re, 2.0 / 3.0)
    ) * pow(Pr, 0.4) * pow(mu / mu_s, 0.25)
    return Nu * k / D


h_whitaker_sphere.metadata = _METADATA.copy()

__all__ = ["h_whitaker_sphere"]
