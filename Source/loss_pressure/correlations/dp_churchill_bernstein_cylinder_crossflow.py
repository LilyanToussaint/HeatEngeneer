"""Drag-based pressure-drop correlation for cross-flow over a cylinder."""
from __future__ import annotations

from math import isfinite, sqrt

__all__ = ["dp_churchill_bernstein_cylinder_crossflow"]


def dp_churchill_bernstein_cylinder_crossflow(
    reynolds: float,
    density: float,
    velocity: float,
    diameter: float,
) -> float:
    """Estimate the pressure drop per unit length over a cylinder in cross-flow."""

    for name, value in {
        "Re": reynolds,
        "rho": density,
        "v": velocity,
        "D": diameter,
    }.items():
        if not isfinite(value):
            raise ValueError(
                f"dp_churchill_bernstein_cylinder_crossflow: '{name}' doit être fini."
            )
    if reynolds <= 0 or density <= 0 or diameter <= 0 or velocity < 0:
        raise ValueError(
            "dp_churchill_bernstein_cylinder_crossflow: entrées physiques invalides."
        )

    drag_coefficient = (
        0.9 + 0.34 / sqrt(max(reynolds, 1.0))
    )  # Churchill-Bernstein style drag estimate
    dynamic_pressure = 0.5 * density * velocity**2
    return drag_coefficient * dynamic_pressure


dp_churchill_bernstein_cylinder_crossflow.metadata = {
    "flow_domain": "external",
    "geometry": "cylinder_crossflow",
    "quantity": "pressure_drop",
    "reference": "Churchill-Bernstein",
}
