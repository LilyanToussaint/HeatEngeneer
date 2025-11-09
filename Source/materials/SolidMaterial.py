"""Concrete material implementation for solid media."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .BaseMaterial import BaseMaterial


@dataclass(frozen=True)
class SolidMaterial(BaseMaterial):
    """Material with density, heat capacity and thermal conductivity."""

    density: float
    heat_capacity: float
    thermal_conductivity: float
    emissivity: Optional[float] = None
    poisson_ratio: Optional[float] = None


__all__ = ["SolidMaterial"]
