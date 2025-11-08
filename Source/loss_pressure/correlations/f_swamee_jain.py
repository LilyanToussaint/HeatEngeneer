"""Swamee-Jain explicit turbulent friction-factor correlation."""
from __future__ import annotations

from math import isfinite, log10

__all__ = ["f_swamee_jain"]


def f_swamee_jain(reynolds: float, relative_roughness: float) -> float:
    """Return the Darcy friction factor using the Swamee–Jain formula."""

    for name, value in {"Re": reynolds, "eD": relative_roughness}.items():
        if not isfinite(value):
            raise ValueError(f"f_swamee_jain: '{name}' doit être fini.")

    if reynolds <= 0:
        raise ValueError("f_swamee_jain: Re doit être positif.")
    if relative_roughness < 0:
        raise ValueError("f_swamee_jain: e/D doit être positif ou nul.")
    if reynolds < 4.0e3:
        raise ValueError("f_swamee_jain: valable pour Re >= 4e3.")

    return 0.25 / (
        log10(relative_roughness / 3.7 + 5.74 / (reynolds ** 0.9)) ** 2
    )


f_swamee_jain.metadata = {
    "flow_domain": "internal",
    "regime": "turbulent",
    "geometry": "circular_duct",
    "phase": "single-phase",
    "quantity": "darcy_friction_factor",
    "roughness": "general",
}
