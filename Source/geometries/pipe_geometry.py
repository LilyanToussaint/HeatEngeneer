"""Cylindrical pipe geometry definition."""
from __future__ import annotations

from dataclasses import dataclass
from math import pi

from ..materials import Material
from .common import ensure_positive

__all__ = ["PipeGeometry"]


@dataclass(frozen=True, kw_only=True)
class PipeGeometry(Material):
    """Cylindrical pipe with inner fluid passage."""

    inner_diameter: float
    outer_diameter: float
    length: float

    def __post_init__(self) -> None:  # type: ignore[override]
        if self.density is None:
            raise ValueError("PipeGeometry requiert une densité matérielle.")
        ensure_positive(self.inner_diameter, "inner_diameter")
        ensure_positive(self.outer_diameter, "outer_diameter")
        ensure_positive(self.length, "length")
        if self.outer_diameter <= self.inner_diameter:
            raise ValueError("outer_diameter doit être > inner_diameter.")

    @property
    def fluid_volume(self) -> float:
        """Volume interne disponible pour le fluide [m³]."""

        radius = 0.5 * self.inner_diameter
        return pi * radius * radius * self.length

    @property
    def material_volume(self) -> float:
        """Volume du matériau constituant le tube [m³]."""

        r_inner = 0.5 * self.inner_diameter
        r_outer = 0.5 * self.outer_diameter
        return pi * (r_outer * r_outer - r_inner * r_inner) * self.length

    @property
    def total_volume(self) -> float:
        """Somme des volumes matière et fluide."""

        return self.material_volume + self.fluid_volume
