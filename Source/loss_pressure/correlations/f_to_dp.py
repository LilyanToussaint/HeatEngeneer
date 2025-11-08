"""Convert a Darcy friction factor to a pressure drop."""
from __future__ import annotations

from math import isfinite

__all__ = ["f_to_dp"]


def f_to_dp(
    friction_factor: float,
    length: float,
    diameter: float,
    density: float,
    velocity: float,
) -> float:
    """Return Δp from a Darcy friction factor."""

    for name, value in {
        "f": friction_factor,
        "L": length,
        "D": diameter,
        "rho": density,
        "v": velocity,
    }.items():
        if not isfinite(value):
            raise ValueError(f"f_to_dp: '{name}' doit être fini.")

    if friction_factor <= 0 or length <= 0 or diameter <= 0 or density <= 0 or velocity < 0:
        raise ValueError("f_to_dp: paramètres physiques invalides.")

    return friction_factor * (length / diameter) * 0.5 * density * velocity**2


f_to_dp.metadata = {
    "flow_domain": "internal",
    "quantity": "pressure_drop",
    "type": "conversion",
}
