"""Parallel assembly of identical pipes."""
from __future__ import annotations

from dataclasses import dataclass

from .pipe_geometry import PipeGeometry

__all__ = ["PipeNetworkGeometry"]


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
