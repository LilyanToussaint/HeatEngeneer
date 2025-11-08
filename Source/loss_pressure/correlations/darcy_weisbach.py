"""Classical Darcy-Weisbach pressure-drop correlation."""
from __future__ import annotations

__all__ = ["dp_darcy_weisbach"]


def dp_darcy_weisbach(
    friction_factor: float,
    length: float,
    diameter: float,
    density: float,
    velocity: float,
) -> float:
    """Return the pressure drop in a straight duct using Darcy-Weisbach."""

    if diameter <= 0 or length <= 0:
        raise ValueError("Darcy-Weisbach: longueur et diamètre doivent être positifs.")
    if density <= 0 or velocity < 0:
        raise ValueError("Darcy-Weisbach: densité et vitesse doivent être positives.")
    if friction_factor <= 0:
        raise ValueError("Darcy-Weisbach: facteur de frottement doit être positif.")

    dynamic_pressure = 0.5 * density * velocity**2
    return friction_factor * (length / diameter) * dynamic_pressure
dp_darcy_weisbach.metadata = {
    "flow_domain": "internal",
    "driving": "forced",
    "geometry": "circular_duct",
    "phase": "single-phase",
}

if __debug__:
    dp_darcy_weisbach.metadata = {
        **dp_darcy_weisbach.metadata,
        "notes": "Utilise le facteur de frottement Darcy (4*fanning).",
    }
