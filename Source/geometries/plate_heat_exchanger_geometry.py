"""Plate heat exchanger geometry."""
from __future__ import annotations

from dataclasses import dataclass

from ..materials import Material
from .common import ensure_positive

__all__ = ["PlateHeatExchangerGeometry"]


@dataclass(frozen=True, kw_only=True)
class PlateHeatExchangerGeometry(Material):
    """Stacked-plate heat exchanger with uniform spacing."""

    length: float
    width: float
    plate_thickness: float
    channel_gap: float
    plate_count: int

    def __post_init__(self) -> None:  # type: ignore[override]
        if self.density is None:
            raise ValueError("PlateHeatExchangerGeometry requiert une densité matérielle.")
        ensure_positive(self.length, "length")
        ensure_positive(self.width, "width")
        ensure_positive(self.plate_thickness, "plate_thickness")
        ensure_positive(self.channel_gap, "channel_gap")
        if self.plate_count < 2:
            raise ValueError("plate_count doit être >= 2.")

    @property
    def channel_count(self) -> int:
        """Nombre de canaux de fluide (plate_count - 1)."""

        return self.plate_count - 1

    @property
    def fluid_volume(self) -> float:
        """Volume d'écoulement total dans les canaux fluides [m³]."""

        return self.channel_count * self.length * self.width * self.channel_gap

    @property
    def material_volume(self) -> float:
        """Volume total des plaques [m³]."""

        return self.plate_count * self.length * self.width * self.plate_thickness

    @property
    def total_volume(self) -> float:
        return self.material_volume + self.fluid_volume

    @property
    def stack_thickness(self) -> float:
        """Épaisseur totale de l'empilement plaques + canaux [m]."""

        return self.plate_count * self.plate_thickness + self.channel_count * self.channel_gap
