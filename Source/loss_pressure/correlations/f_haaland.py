"""Haaland explicit turbulent friction-factor correlation."""
from __future__ import annotations

from math import isfinite, log10

__all__ = ["f_haaland"]


def f_haaland(reynolds: float, relative_roughness: float) -> float:
    """Return the Darcy friction factor using the Haaland correlation."""

    for name, value in {"Re": reynolds, "eD": relative_roughness}.items():
        if not isfinite(value):
            raise ValueError(f"f_haaland: '{name}' doit être fini.")

    if reynolds <= 0:
        raise ValueError("f_haaland: Re doit être positif.")
    if relative_roughness < 0:
        raise ValueError("f_haaland: e/D doit être positif ou nul.")
    if reynolds < 3.0e3:
        raise ValueError("f_haaland: valable pour Re >= 3e3.")

    return 1.0 / (
        -1.8 * log10((relative_roughness / 3.7) ** 1.11 + 6.9 / reynolds)
    ) ** 2


f_haaland.metadata = {
    "flow_domain": "internal",
    "regime": "turbulent",
    "geometry": "circular_duct",
    "phase": "single-phase",
    "quantity": "darcy_friction_factor",
    "roughness": "general",
}
