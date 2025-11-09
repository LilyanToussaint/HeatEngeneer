"""Heat exchanger aggregate object."""
from __future__ import annotations

from dataclasses import dataclass

from .arrangement import FlowArrangement
from .side import HXSide
from .wall import Wall


@dataclass(slots=True)
class HeatExchanger:
    """Aggregate hot and cold sides with wall and arrangement metadata."""

    hot: HXSide
    cold: HXSide
    arrangement: FlowArrangement
    wall: Wall

    def compute_overall_u(
        self,
        h_hot: float,
        h_cold: float,
        area_reference: float,
        additional_resistance: float = 0.0,
    ) -> float:
        """Compute the overall heat-transfer coefficient for the exchanger."""

        if area_reference <= 0:
            raise ValueError("La surface de référence doit être positive.")
        if h_hot <= 0 or h_cold <= 0:
            raise ValueError("Les coefficients de convection doivent être positifs.")

        hot_area = self.hot.area
        cold_area = self.cold.area

        if hot_area <= 0 or cold_area <= 0:
            raise ValueError("Les surfaces chaudes et froides doivent être positives.")

        r_hot = (area_reference / hot_area) / h_hot
        r_cold = (area_reference / cold_area) / h_cold
        self.wall.validate()
        if additional_resistance < 0:
            raise ValueError("Les résistances additionnelles doivent être positives.")

        total_resistance = r_hot + self.wall.thermal_resistance + additional_resistance + r_cold
        if total_resistance <= 0:
            raise ValueError("La résistance thermique totale doit être positive.")
        return 1.0 / total_resistance
