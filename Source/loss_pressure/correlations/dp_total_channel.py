"""Utility to combine linear pressure losses for a single channel."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_total_channel"]


def dp_total_channel(
    friction_factor: float,
    mass_flux: float,
    length: float,
    hydraulic_diameter: float,
    density: float,
    minor_losses: float = 0.0,
) -> float:
    """Return the total pressure drop in a single channel including minor losses."""

    for name, value in {
        "f": friction_factor,
        "G": mass_flux,
        "L": length,
        "Dh": hydraulic_diameter,
        "rho": density,
        "k_minor": minor_losses,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_total_channel: '{name}' doit être fini.")

    if friction_factor <= 0 or mass_flux <= 0 or length <= 0 or hydraulic_diameter <= 0 or density <= 0:
        raise ValueError("dp_total_channel: paramètres physiques invalides.")
    if minor_losses < 0:
        raise ValueError("dp_total_channel: pertes mineures doivent être >= 0.")

    linear = friction_factor * (length / hydraulic_diameter) * mass_flux**2 / (2.0 * density)
    minor = minor_losses * mass_flux**2 / (2.0 * density)
    return linear + minor


dp_total_channel.metadata = {
    "flow_domain": "internal",
    "quantity": "pressure_drop",
    "includes": ["linear", "minor"],
}
