"""Networks of finned tubes."""
from __future__ import annotations

from dataclasses import dataclass

from .tube_fin_geometry import TubeFinGeometry

__all__ = ["TubeFinNetworkGeometry"]


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
