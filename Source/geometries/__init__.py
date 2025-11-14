"""Geometric primitives for heat-exchanger components."""
from __future__ import annotations

from dataclasses import dataclass
from math import pi
from ..materials import Material

__all__ = [
    "PipeGeometry",
    "PipeNetworkGeometry",
    "PlateFinGeometry",
    "TubeFinGeometry",
    "TubeFinNetworkGeometry",
]


def _ensure_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} doit être > 0.")


@dataclass(frozen=True, kw_only=True)
class PipeGeometry(Material):
    """Cylindrical pipe with inner fluid passage."""

    inner_diameter: float
    outer_diameter: float
    length: float

    def __post_init__(self) -> None:  # type: ignore[override]
        if self.density is None:
            raise ValueError("PipeGeometry requiert une densité matérielle.")
        _ensure_positive(self.inner_diameter, "inner_diameter")
        _ensure_positive(self.outer_diameter, "outer_diameter")
        _ensure_positive(self.length, "length")
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


@dataclass(frozen=True, kw_only=True)
class PipeNetworkGeometry(PipeGeometry):
    """Assemblage parallèle de tubes identiques."""

    count: int

    def __post_init__(self) -> None:  # type: ignore[override]
        super().__post_init__()
        if self.count <= 0:
            raise ValueError("count doit être > 0.")

    @property
    def fluid_volume(self) -> float:  # type: ignore[override]
        return self.count * super().fluid_volume

    @property
    def material_volume(self) -> float:  # type: ignore[override]
        return self.count * super().material_volume

    @property
    def total_volume(self) -> float:  # type: ignore[override]
        return self.count * (super().material_volume + super().fluid_volume)


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
        _ensure_positive(self.length, "length")
        _ensure_positive(self.fin_height, "fin_height")
        _ensure_positive(self.fin_thickness, "fin_thickness")
        _ensure_positive(self.channel_width, "channel_width")
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


@dataclass(frozen=True, kw_only=True)
class TubeFinGeometry(PipeGeometry):
    """Finned tube with annular fins sharing the tube material."""

    fin_outer_diameter: float
    fin_thickness: float
    fin_count: int

    def __post_init__(self) -> None:  # type: ignore[override]
        super().__post_init__()
        _ensure_positive(self.fin_outer_diameter, "fin_outer_diameter")
        _ensure_positive(self.fin_thickness, "fin_thickness")
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


@dataclass(frozen=True, kw_only=True)
class TubeFinNetworkGeometry(TubeFinGeometry):
    """Network of identical finned tubes."""

    tube_count: int

    def __post_init__(self) -> None:  # type: ignore[override]
        super().__post_init__()
        if self.tube_count <= 0:
            raise ValueError("tube_count doit être > 0.")

    @property
    def fluid_volume(self) -> float:  # type: ignore[override]
        return self.tube_count * super().fluid_volume

    @property
    def material_volume(self) -> float:  # type: ignore[override]
        return self.tube_count * super().material_volume

    @property
    def total_volume(self) -> float:  # type: ignore[override]
        base_total = super().material_volume + super().fluid_volume
        return self.tube_count * base_total
