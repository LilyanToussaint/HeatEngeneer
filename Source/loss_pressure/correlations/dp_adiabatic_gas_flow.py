"""Adiabatic compressible gas-flow pressure-drop estimate."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_adiabatic_gas_flow"]


def dp_adiabatic_gas_flow(
    reynolds: float,
    mach: float,
    gamma: float,
    fanning_factor: float,
    length: float,
    diameter: float,
    static_pressure: float = 101325.0,
) -> float:
    """Return an adiabatic gas-flow pressure drop using Fanno-line assumptions."""

    for name, value in {
        "Re": reynolds,
        "Ma": mach,
        "gamma": gamma,
        "f": fanning_factor,
        "L": length,
        "D": diameter,
        "p": static_pressure,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_adiabatic_gas_flow: '{name}' doit être fini.")

    if reynolds <= 0 or mach <= 0 or gamma <= 1 or fanning_factor <= 0:
        raise ValueError("dp_adiabatic_gas_flow: paramètres physiques invalides.")
    if length <= 0 or diameter <= 0 or static_pressure <= 0:
        raise ValueError("dp_adiabatic_gas_flow: géométrie et pression doivent être positives.")

    dynamic_pressure = 0.5 * gamma * static_pressure * mach**2
    darcy_factor = 4.0 * fanning_factor
    return darcy_factor * (length / diameter) * dynamic_pressure


dp_adiabatic_gas_flow.metadata = {
    "flow_domain": "compressible",
    "process": "adiabatic",
    "quantity": "pressure_drop",
}
