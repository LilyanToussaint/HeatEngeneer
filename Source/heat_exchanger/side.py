"""Heat-exchanger side definition."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .fluid import FluidModel
from .geometry import Geometry
from .htc import HTCModel
from .dp import DPModel


@dataclass(slots=True)
class HXSide:
    """Represent one side of a heat exchanger (hot or cold)."""

    label: str
    fluid: FluidModel
    mass_flow: float
    inlet_temp: float
    geometry: Geometry
    htc_model: HTCModel
    dp_model: DPModel | None = None
    heat_capacity_override: float | None = None
    velocity: float | None = None

    def __post_init__(self) -> None:
        self.geometry.validate()
        if self.mass_flow <= 0:
            raise ValueError("Le débit massique doit être strictement positif.")

    @property
    def area(self) -> float:
        return self.geometry.area

    def heat_capacity_rate(self) -> float:
        if self.heat_capacity_override is not None:
            if self.heat_capacity_override <= 0:
                raise ValueError("La capacité thermique doit être positive.")
            return self.heat_capacity_override
        return self.fluid.capacity_rate(self.mass_flow)

    def compute_htc(self, overrides: Dict[str, float] | None = None) -> float:
        return self.htc_model.compute(overrides)
