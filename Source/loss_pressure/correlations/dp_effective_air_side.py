"""Effective air-side pressure-drop helper linking j and f data."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_effective_air_side"]


def dp_effective_air_side(
    j_factor: float,
    friction_factor: float,
    mass_flux: float,
    density: float,
) -> float:
    """Return an effective air-side pressure drop compatible with j/f correlations."""

    for name, value in {
        "j": j_factor,
        "f": friction_factor,
        "G": mass_flux,
        "rho": density,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_effective_air_side: '{name}' doit être fini.")

    if friction_factor <= 0 or mass_flux <= 0 or density <= 0 or j_factor < 0:
        raise ValueError("dp_effective_air_side: paramètres physiques invalides.")

    return friction_factor * mass_flux**2 / (2.0 * density)


dp_effective_air_side.metadata = {
    "flow_domain": "compact_heat_exchanger",
    "quantity": "pressure_drop",
    "notes": "Compatible avec corrélations j/f.",
}
