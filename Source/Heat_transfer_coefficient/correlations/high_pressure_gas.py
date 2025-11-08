"""High-pressure gas forced-convection correction."""
from __future__ import annotations


_METADATA = {
    "domain": "internal",
    "convection": "forced",
    "geometry": "high-pressure gas flow",
}


def h_high_pressure_gas(
    Re: float,
    Pr: float,
    k: float,
    d_h: float,
    mu: float,
    mu_w: float,
    cp: float,
    cp_w: float,
) -> float:
    """Return HTC for high-pressure gas with property correction at wall."""

    if min(Re, Pr, k, d_h, mu, mu_w, cp, cp_w) <= 0:
        raise ValueError("Gaz haute pression: paramètres doivent être > 0.")

    Nu = 0.023 * Re ** 0.8 * Pr ** 0.4
    Nu *= (mu / mu_w) ** 0.14 * (cp / cp_w) ** 0.3
    return Nu * k / d_h


h_high_pressure_gas.metadata = _METADATA.copy()


__all__ = ["h_high_pressure_gas"]
