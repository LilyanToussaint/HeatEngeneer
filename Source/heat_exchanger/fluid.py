"""Fluid representation for heat-exchanger sides."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FluidModel:
    """Describe the working fluid for a heat-exchanger side."""

    name: str
    heat_capacity: float
    density: float | None = None

    def capacity_rate(self, mass_flow: float) -> float:
        """Return the heat-capacity rate ``C = m_dot * cp`` for the fluid."""

        if mass_flow <= 0:
            raise ValueError("Le débit massique doit être strictement positif.")
        if self.heat_capacity <= 0:
            raise ValueError("La capacité thermique doit être strictement positive.")
        return mass_flow * self.heat_capacity
