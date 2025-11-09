"""Utility to convert Fanning friction factor to pressure drop."""
from __future__ import annotations


_METADATA = {
    "domain": "compact exchanger",
    "convection": "forced",
    "geometry": "pressure-drop conversion",
}


def fanning_f_to_dp(
    f: float,
    G: float,
    L: float,
    D_h: float,
    rho: float,
) -> float:
    """Return the pressure drop [Pa] from a Fanning friction factor."""

    if f <= 0:
        raise ValueError("Fanning -> dP: f doit être > 0.")
    if min(G, L, D_h, rho) <= 0:
        raise ValueError("Fanning -> dP: paramètres physiques doivent être > 0.")

    return 4.0 * f * (L / D_h) * G ** 2 / (2.0 * rho)


fanning_f_to_dp.metadata = _METADATA.copy()


__all__ = ["fanning_f_to_dp"]
