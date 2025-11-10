"""Material definition holding thermophysical properties."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

__all__ = ["Material"]


@dataclass(frozen=True)
class Material:
    """Represent a homogeneous material."""

    name: str
    density: Optional[float] = None
    heat_capacity: Optional[float] = None
    thermal_conductivity: Optional[float] = None
    emissivity: Optional[float] = None
    poisson_ratio: Optional[float] = None
