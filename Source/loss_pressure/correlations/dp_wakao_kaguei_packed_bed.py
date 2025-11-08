"""Wakao & Kaguei packed-bed pressure-drop correlation."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_wakao_kaguei_packed_bed"]


def dp_wakao_kaguei_packed_bed(
    reynolds_particle: float,
    porosity: float,
    particle_diameter: float,
    length: float,
    density: float,
    velocity: float,
) -> float:
    """Return the Wakao & Kaguei packed-bed pressure drop."""

    for name, value in {
        "Re_p": reynolds_particle,
        "epsilon": porosity,
        "D_p": particle_diameter,
        "L": length,
        "rho": density,
        "v": velocity,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_wakao_kaguei_packed_bed: '{name}' doit être fini.")

    if not 0 < porosity < 1:
        raise ValueError("dp_wakao_kaguei_packed_bed: porosité doit être dans ]0, 1[.")
    if particle_diameter <= 0 or length <= 0 or density <= 0 or velocity < 0:
        raise ValueError("dp_wakao_kaguei_packed_bed: paramètres physiques invalides.")
    if reynolds_particle <= 0:
        raise ValueError("dp_wakao_kaguei_packed_bed: Re_p doit être > 0.")

    coefficient = (
        (1.75 + 150.0 / reynolds_particle) * (1.0 - porosity) / porosity**3
    )
    return coefficient * density * velocity**2 * length / particle_diameter


dp_wakao_kaguei_packed_bed.metadata = {
    "flow_domain": "porous_media",
    "model": "wakao_kaguei",
    "quantity": "pressure_drop",
}
