"""Base class for material definitions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BaseMaterial:
    """Represent minimal metadata shared by all materials."""

    name: str
    density: Optional[float] = None
    heat_capacity: Optional[float] = None
    thermal_conductivity: Optional[float] = None
    emissivity: Optional[float] = None
    poisson_ratio: Optional[float] = None


__all__ = ["BaseMaterial"]
