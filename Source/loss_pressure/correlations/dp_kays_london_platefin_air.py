"""Pressure-drop correlation for plate-fin surfaces (Kays & London)."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_kays_london_platefin_air"]


def dp_kays_london_platefin_air(
    reynolds: float,
    density: float,
    mass_flux: float,
    hydraulic_diameter: float,
    length: float,
) -> float:
    """Estimate Δp for plate-fin surfaces based on Kays & London charts."""

    for name, value in {
        "Re": reynolds,
        "rho": density,
        "G": mass_flux,
        "Dh": hydraulic_diameter,
        "L": length,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_kays_london_platefin_air: '{name}' doit être fini.")

    if reynolds <= 0 or density <= 0 or mass_flux <= 0 or hydraulic_diameter <= 0 or length <= 0:
        raise ValueError("dp_kays_london_platefin_air: entrées physiques invalides.")

    friction_factor = 0.664 * reynolds ** -0.5
    return friction_factor * (length / hydraulic_diameter) * mass_flux**2 / (2.0 * density)


dp_kays_london_platefin_air.metadata = {
    "flow_domain": "compact_heat_exchanger",
    "surface": "plate_fin",
    "quantity": "pressure_drop",
    "reference": "Kays-London",
}
