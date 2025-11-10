"""Thermal conductivity correlation for copper."""
from __future__ import annotations

__all__ = ["k_copper"]


def k_copper(temperature: float) -> float:
    """Return the thermal conductivity of copper [W/m/K]."""

    # Mild decrease with temperature approximated linearly around ambient.
    base = 401.0
    slope = -0.05
    return base + slope * (max(temperature, 0.0) - 300.0)
