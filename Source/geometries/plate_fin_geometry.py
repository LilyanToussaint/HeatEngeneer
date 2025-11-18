"""Plate-fin surface geometry."""
from __future__ import annotations

from dataclasses import dataclass

from ..materials import Material
from .common import ensure_positive

__all__ = ["PlateFinGeometry"]


@dataclass(frozen=True, kw_only=True)
class PlateFinGeometry(Material):
    """Plate-fin surface composed of a base plate and straight fins."""

    length: float
    fin_height: float
    fin_thickness: float
    fin_count: int
    channel_width: float
    plate_thickness: float

    def __post_init__(self) -> None:  # type: ignore[override]
        if self.density is None:
            raise ValueError("PlateFinGeometry requiert une densité matérielle.")
        ensure_positive(self.length, "length")
        ensure_positive(self.fin_height, "fin_height")
        ensure_positive(self.fin_thickness, "fin_thickness")
        ensure_positive(self.channel_width, "channel_width")
        if self.fin_count < 0:
            raise ValueError("fin_count doit être >= 0.")
        if self.plate_thickness < 0:
            raise ValueError("plate_thickness doit être >= 0.")

    @property
    def channel_count(self) -> int:
        """Nombre d'interstices fluides."""

        return self.fin_count + 1

    @property
    def total_width(self) -> float:
        """Largeur totale de la plaque avec ailettes."""

        return self.fin_count * self.fin_thickness + self.channel_count * self.channel_width

    @property
    def fluid_volume(self) -> float:
        """Volume disponible pour l'écoulement fluide entre ailettes [m³]."""

        return self.channel_count * self.length * self.fin_height * self.channel_width

    @property
    def material_volume(self) -> float:
        """Volume du matériau des ailettes et de la plaque [m³]."""

        base_volume = self.length * self.total_width * self.plate_thickness
        fin_volume = self.fin_count * self.length * self.fin_height * self.fin_thickness
        return base_volume + fin_volume

    @property
    def total_volume(self) -> float:
        return self.material_volume + self.fluid_volume
