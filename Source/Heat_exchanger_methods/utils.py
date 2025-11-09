"""Shared helpers for the heat-exchanger method classes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class StreamConditions:
    """Input data required for heat-exchanger calculations."""

    fluid: Any
    m_dot: float
    cp: float
    inlet_temp: float
    correlation_kwargs: Dict[str, Any]
    C: Optional[float] = None
    area: Optional[float] = None
    velocity: Optional[float] = None

    def heat_capacity_rate(self) -> float:
        if self.C is not None:
            return self.C
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

    The function includes optional unequal surface areas supplied within
    :class:`StreamConditions`.
    """

    if area_total <= 0:
        raise ValueError("La surface totale doit être positive.")

    if h_hot <= 0 or h_cold <= 0:
        raise ValueError("Les coefficients de convection doivent être positifs.")

    hot_area = hot.area or area_total
    cold_area = cold.area or area_total

    if hot_area <= 0 or cold_area <= 0:
        raise ValueError("Les surfaces chaudes et froides doivent être positives.")

    area_ratio_hot = area_total / hot_area
    area_ratio_cold = area_total / cold_area

    r_hot = area_ratio_hot / h_hot
    r_cold = area_ratio_cold / h_cold

    total_resistance = r_hot + wall_resistance + r_cold

    if total_resistance <= 0:
        raise ValueError("La résistance thermique totale doit être positive.")

    return 1.0 / total_resistance
