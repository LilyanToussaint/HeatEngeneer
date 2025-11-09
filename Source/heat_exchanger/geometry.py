"""Geometry definition for a heat-exchanger side."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Geometry:
    """Represent the geometry associated with a flow passage."""

    area: float
    hydraulic_diameter: float | None = None

    def validate(self) -> None:
        if self.area <= 0:
            raise ValueError("La surface doit être strictement positive.")
        if self.hydraulic_diameter is not None and self.hydraulic_diameter <= 0:
            raise ValueError("Le diamètre hydraulique doit être strictement positif.")
