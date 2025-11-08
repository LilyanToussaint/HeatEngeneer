"""Combine hot and cold side pressure drops for a heat exchanger."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_total_heat_exchanger"]


def dp_total_heat_exchanger(
    friction_factor_hot: float,
    friction_factor_cold: float,
    geometry: dict,
    mass_flux_hot: float,
    mass_flux_cold: float,
    density_hot: float,
    density_cold: float,
    minor_losses_hot: float = 0.0,
    minor_losses_cold: float = 0.0,
) -> float:
    """Return the combined pressure drop of both sides of a heat exchanger."""

    for name, value in {
        "f_hot": friction_factor_hot,
        "f_cold": friction_factor_cold,
        "G_hot": mass_flux_hot,
        "G_cold": mass_flux_cold,
        "rho_hot": density_hot,
        "rho_cold": density_cold,
        "k_hot": minor_losses_hot,
        "k_cold": minor_losses_cold,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_total_heat_exchanger: '{name}' doit être fini.")

    required_keys = {"L_hot", "Dh_hot", "L_cold", "Dh_cold"}
    if not required_keys.issubset(geometry):
        raise ValueError(
            "dp_total_heat_exchanger: geometry doit contenir L_hot, Dh_hot, L_cold, Dh_cold."
        )

    for key in required_keys:
        if not isfinite(geometry[key]) or geometry[key] <= 0:
            raise ValueError(f"dp_total_heat_exchanger: '{key}' doit être > 0 et fini.")

    def _side(friction_factor: float, mass_flux: float, length: float, dh: float, density: float, k_minor: float) -> float:
        linear = friction_factor * (length / dh) * mass_flux**2 / (2.0 * density)
        minor = k_minor * mass_flux**2 / (2.0 * density)
        return linear + minor

    dp_hot = _side(
        friction_factor_hot,
        mass_flux_hot,
        geometry["L_hot"],
        geometry["Dh_hot"],
        density_hot,
        minor_losses_hot,
    )
    dp_cold = _side(
        friction_factor_cold,
        mass_flux_cold,
        geometry["L_cold"],
        geometry["Dh_cold"],
        density_cold,
        minor_losses_cold,
    )
    return dp_hot + dp_cold


dp_total_heat_exchanger.metadata = {
    "flow_domain": "heat_exchanger",
    "quantity": "pressure_drop",
    "includes": ["hot_side", "cold_side"],
}
