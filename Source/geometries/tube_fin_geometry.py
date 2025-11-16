"""Finned tube geometry."""
from __future__ import annotations

from dataclasses import dataclass
from math import pi

from .pipe_geometry import PipeGeometry
from .common import ensure_positive

__all__ = ["TubeFinGeometry"]


@dataclass(frozen=True, kw_only=True)
class TubeFinGeometry(PipeGeometry):
    """Finned tube with annular fins sharing the tube material."""

    fin_outer_diameter: float
    fin_thickness: float
    fin_count: int

    def __post_init__(self) -> None:  # type: ignore[override]
        super().__post_init__()
        ensure_positive(self.fin_outer_diameter, "fin_outer_diameter")
        ensure_positive(self.fin_thickness, "fin_thickness")
        if self.fin_count < 0:
            raise ValueError("fin_count doit être >= 0.")
        if self.fin_outer_diameter <= self.outer_diameter:
            raise ValueError("fin_outer_diameter doit être > outer_diameter.")

    @property
    def material_volume(self) -> float:  # type: ignore[override]
        tube_volume = super().material_volume
        annulus_area = 0.25 * pi * (self.fin_outer_diameter ** 2 - self.outer_diameter ** 2)
        fins_volume = self.fin_count * annulus_area * self.fin_thickness
        return tube_volume + fins_volume

    @property
    def total_volume(self) -> float:  # type: ignore[override]
        return self.material_volume + self.fluid_volume
