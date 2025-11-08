"""Generic plate-fin pressure-drop calculator."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_plate_fin"]


def dp_plate_fin(
    friction_factor: float,
    mass_flux: float,
    length: float,
    hydraulic_diameter: float,
    density: float,
) -> float:
    """Return the pressure drop across a plate-fin channel."""

    for name, value in {
        "f": friction_factor,
        "G": mass_flux,
        "L": length,
        "Dh": hydraulic_diameter,
        "rho": density,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_plate_fin: '{name}' doit être fini.")

    if friction_factor <= 0 or mass_flux <= 0 or length <= 0 or hydraulic_diameter <= 0 or density <= 0:
        raise ValueError("dp_plate_fin: paramètres physiques invalides.")

    return friction_factor * (length / hydraulic_diameter) * mass_flux**2 / (2.0 * density)


dp_plate_fin.metadata = {
    "flow_domain": "compact_heat_exchanger",
    "quantity": "pressure_drop",
}
