"""Driving pressure difference for a natural-convection loop."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_natural_convection_loop"]


def dp_natural_convection_loop(
    density_inlet: float,
    density_outlet: float,
    gravity: float,
    height_difference: float,
) -> float:
    """Return the buoyancy-driven pressure head in a natural-convection loop."""

    for name, value in {
        "rho_in": density_inlet,
        "rho_out": density_outlet,
        "g": gravity,
        "Δz": height_difference,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_natural_convection_loop: '{name}' doit être fini.")

    if gravity <= 0:
        raise ValueError("dp_natural_convection_loop: g doit être > 0.")

    return (density_outlet - density_inlet) * gravity * height_difference


dp_natural_convection_loop.metadata = {
    "flow_domain": "natural_convection",
    "quantity": "pressure_difference",
}
