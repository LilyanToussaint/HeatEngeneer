"""Volumetric flow helper functions."""
from __future__ import annotations


def velocity_from_mass_flow(m_dot: float, density: float, area: float) -> float:
    """Compute the average velocity from mass flow rate, density and area."""

    if area <= 0:
        raise ValueError("La surface doit être strictement positive.")
    if density <= 0:
        raise ValueError("La masse volumique doit être strictement positive.")
    return m_dot / (density * area)


def mass_flow_from_velocity(velocity: float, density: float, area: float) -> float:
    """Compute the mass flow rate from velocity, density and flow area."""

    if area <= 0:
        raise ValueError("La surface doit être strictement positive.")
    if density <= 0:
        raise ValueError("La masse volumique doit être strictement positive.")
    return velocity * density * area


__all__ = ["velocity_from_mass_flow", "mass_flow_from_velocity"]
