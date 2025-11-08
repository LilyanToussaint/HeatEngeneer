"""Convert a pressure drop to a Darcy friction factor."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_to_f"]


def dp_to_f(
    pressure_drop: float,
    length: float,
    diameter: float,
    density: float,
    velocity: float,
) -> float:
    """Return the Darcy friction factor corresponding to a pressure drop."""

    for name, value in {
        "Δp": pressure_drop,
        "L": length,
        "D": diameter,
        "rho": density,
        "v": velocity,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_to_f: '{name}' doit être fini.")

    if pressure_drop <= 0 or length <= 0 or diameter <= 0 or density <= 0 or velocity <= 0:
        raise ValueError("dp_to_f: paramètres physiques invalides.")

    dynamic_pressure = 0.5 * density * velocity**2
    return pressure_drop * diameter / (length * dynamic_pressure)


dp_to_f.metadata = {
    "flow_domain": "internal",
    "quantity": "darcy_friction_factor",
    "type": "conversion",
}
