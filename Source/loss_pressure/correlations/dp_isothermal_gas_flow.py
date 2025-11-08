"""Isothermal compressible gas-flow pressure-drop estimate."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_isothermal_gas_flow"]


def dp_isothermal_gas_flow(
    fanning_factor: float,
    length: float,
    diameter: float,
    density_inlet: float,
    density_exit: float,
    pressure_inlet: float,
    pressure_exit: float,
    velocity: float,
) -> float:
    """Return an isothermal gas-flow pressure drop using average properties."""

    for name, value in {
        "f": fanning_factor,
        "L": length,
        "D": diameter,
        "rho_in": density_inlet,
        "rho_out": density_exit,
        "p_in": pressure_inlet,
        "p_out": pressure_exit,
        "v": velocity,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_isothermal_gas_flow: '{name}' doit être fini.")

    if fanning_factor <= 0 or length <= 0 or diameter <= 0 or velocity < 0:
        raise ValueError("dp_isothermal_gas_flow: paramètres géométriques invalides.")
    if density_inlet <= 0 or density_exit <= 0:
        raise ValueError("dp_isothermal_gas_flow: densités doivent être > 0.")
    if pressure_inlet <= 0 or pressure_exit <= 0:
        raise ValueError("dp_isothermal_gas_flow: pressions doivent être > 0.")

    density_avg = 0.5 * (density_inlet + density_exit)
    correction = 0.5 * (pressure_inlet + pressure_exit) / pressure_exit
    darcy_factor = 4.0 * fanning_factor
    dynamic_pressure = 0.5 * density_avg * velocity**2
    return darcy_factor * (length / diameter) * dynamic_pressure * correction


dp_isothermal_gas_flow.metadata = {
    "flow_domain": "compressible",
    "process": "isothermal",
    "quantity": "pressure_drop",
}
