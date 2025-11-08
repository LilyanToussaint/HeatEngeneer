"""Ergun equation for packed-bed pressure drop."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_ergun_packed_bed"]


def dp_ergun_packed_bed(
    reynolds_particle: float,
    porosity: float,
    particle_diameter: float,
    length: float,
    viscosity: float,
    velocity: float,
    density: float,
) -> float:
    """Return the pressure drop across a packed bed using the Ergun equation."""

    for name, value in {
        "Re_p": reynolds_particle,
        "epsilon": porosity,
        "D_p": particle_diameter,
        "L": length,
        "mu": viscosity,
        "v": velocity,
        "rho": density,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_ergun_packed_bed: '{name}' doit être fini.")

    if not 0 < porosity < 1:
        raise ValueError("dp_ergun_packed_bed: porosité doit être dans ]0, 1[.")
    if particle_diameter <= 0 or length <= 0 or viscosity <= 0 or density <= 0:
        raise ValueError("dp_ergun_packed_bed: paramètres physiques invalides.")

    term_laminar = (
        150.0 * (1.0 - porosity) ** 2 / porosity**3 * viscosity * velocity / particle_diameter**2
    )
    term_turbulent = (
        1.75 * (1.0 - porosity) / porosity**3 * density * velocity**2 / particle_diameter
    )
    return (term_laminar + term_turbulent) * length


dp_ergun_packed_bed.metadata = {
    "flow_domain": "porous_media",
    "model": "ergun",
    "quantity": "pressure_drop",
}
