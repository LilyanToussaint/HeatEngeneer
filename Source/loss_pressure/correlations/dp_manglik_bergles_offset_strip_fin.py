"""Pressure-drop correlation for offset-strip fins (Manglik & Bergles)."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_manglik_bergles_offset_strip_fin"]


def dp_manglik_bergles_offset_strip_fin(
    reynolds: float,
    density: float,
    mass_flux: float,
    hydraulic_diameter: float,
    length: float,
) -> float:
    """Estimate Δp for offset-strip fins using Manglik & Bergles data."""

    for name, value in {
        "Re": reynolds,
        "rho": density,
        "G": mass_flux,
        "Dh": hydraulic_diameter,
        "L": length,
    }.items():
        if not isfinite(value):
            raise ValueError(
                f"dp_manglik_bergles_offset_strip_fin: '{name}' doit être fini."
            )

    if reynolds <= 0 or density <= 0 or mass_flux <= 0 or hydraulic_diameter <= 0 or length <= 0:
        raise ValueError("dp_manglik_bergles_offset_strip_fin: entrées invalides.")

    friction_factor = 9.6243 * reynolds ** -0.7422
    return friction_factor * (length / hydraulic_diameter) * mass_flux**2 / (2.0 * density)


dp_manglik_bergles_offset_strip_fin.metadata = {
    "flow_domain": "compact_heat_exchanger",
    "surface": "offset_strip_fin",
    "quantity": "pressure_drop",
    "reference": "Manglik-Bergles",
}
