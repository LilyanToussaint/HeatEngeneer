"""Wall/core representation for a heat exchanger."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Wall:
    """Capture the conductive properties of the heat-exchanger wall."""

    thermal_resistance: float = 0.0

    def validate(self) -> None:
        if self.thermal_resistance < 0:
            raise ValueError("La résistance thermique ne peut pas être négative.")
