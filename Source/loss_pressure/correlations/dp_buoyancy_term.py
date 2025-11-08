"""Buoyancy-induced pressure difference utility."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_buoyancy_term"]


def dp_buoyancy_term(
    reference_density: float,
    density_difference: float,
    gravity: float,
    characteristic_length: float,
) -> float:
    """Return the pressure differential due to buoyancy forces."""

    for name, value in {
        "rho_ref": reference_density,
        "Δrho": density_difference,
        "g": gravity,
        "L": characteristic_length,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_buoyancy_term: '{name}' doit être fini.")

    if gravity <= 0 or characteristic_length <= 0:
        raise ValueError("dp_buoyancy_term: g et L doivent être > 0.")

    return density_difference * gravity * characteristic_length


dp_buoyancy_term.metadata = {
    "flow_domain": "natural_convection",
    "quantity": "pressure_difference",
}
