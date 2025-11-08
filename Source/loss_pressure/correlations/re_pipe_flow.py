"""Convenience Reynolds-number helper for pipe flows."""
from __future__ import annotations

from math import isfinite

from ...common import reynolds_number

__all__ = ["re_pipe_flow"]


def re_pipe_flow(
    mass_flow_rate: float,
    diameter: float,
    dynamic_viscosity: float,
    density: float,
) -> float:
    """Return the Reynolds number from mass flow rate in a circular duct."""

    for name, value in {
        "m_dot": mass_flow_rate,
        "D": diameter,
        "mu": dynamic_viscosity,
        "rho": density,
    }.items():
        if not isfinite(value):
            raise ValueError(f"re_pipe_flow: '{name}' doit être fini.")

    if mass_flow_rate <= 0 or diameter <= 0 or dynamic_viscosity <= 0 or density <= 0:
        raise ValueError("re_pipe_flow: paramètres physiques invalides.")

    area = 0.25 * 3.141592653589793 * diameter**2
    velocity = mass_flow_rate / (density * area)
    return reynolds_number(
        velocity=velocity,
        characteristic_length=diameter,
        density=density,
        dynamic_viscosity=dynamic_viscosity,
    )


re_pipe_flow.metadata = {
    "flow_domain": "internal",
    "quantity": "reynolds_number",
}
