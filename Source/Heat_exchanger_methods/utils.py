"""Shared helpers for the heat-exchanger method classes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class StreamConditions:
    """Input data required for heat-exchanger calculations."""

    m_dot: float
    cp: float
    inlet_temp: float
    correlation_kwargs: Dict[str, Any]
    fin_efficiency: float = 1.0
    area: Optional[float] = None
    fouling_resistance: float = 0.0

    def heat_capacity_rate(self) -> float:
        return self.m_dot * self.cp


def compute_overall_u(
    h_hot: float,
    h_cold: float,
    area_total: float,
    hot: StreamConditions,
    cold: StreamConditions,
    wall_resistance: float = 0.0,
) -> float:
    """Return the overall heat-transfer coefficient referenced to ``area_total``.

    The function includes optional fin efficiencies, unequal surface areas, and
    fouling resistances supplied within :class:`StreamConditions`.
    """

    if area_total <= 0:
        raise ValueError("La surface totale doit être positive.")

    if h_hot <= 0 or h_cold <= 0:
        raise ValueError("Les coefficients de convection doivent être positifs.")

    if hot.fin_efficiency <= 0 or cold.fin_efficiency <= 0:
        raise ValueError("Les efficacités d'ailettes doivent être positives.")

    hot_area = hot.area or area_total
    cold_area = cold.area or area_total

    if hot_area <= 0 or cold_area <= 0:
        raise ValueError("Les surfaces chaudes et froides doivent être positives.")

    area_ratio_hot = area_total / hot_area
    area_ratio_cold = area_total / cold_area

    r_hot = area_ratio_hot / (hot.fin_efficiency * h_hot)
    r_cold = area_ratio_cold / (cold.fin_efficiency * h_cold)

    total_resistance = (
        r_hot + hot.fouling_resistance + wall_resistance + cold.fouling_resistance + r_cold
    )

    if total_resistance <= 0:
        raise ValueError("La résistance thermique totale doit être positive.")

    return 1.0 / total_resistance
