"""One-dimensional discretized heat-exchanger solver."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from ..heat_exchanger import HeatExchanger
from ..solver import HeatExchangerSolver


@dataclass(slots=True)
class OneDResult:
    heat_duty: float
    hot_outlet_temp: float
    cold_outlet_temp: float
    segments: int
    details: Dict[str, Any] = field(default_factory=dict)


class OneDimensionalSolver(HeatExchangerSolver):
    """March along the exchanger length and solve energy balances per cell."""

    def __init__(self) -> None:
        super().__init__(name="one-dimensional")

    def solve(
        self,
        exchanger: HeatExchanger,
        area: float,
        segments: int = 20,
        additional_resistance: float = 0.0,
    ) -> OneDResult:
        if segments <= 0:
            raise ValueError("Le nombre de segments doit être strictement positif.")

        h_hot = exchanger.hot.compute_htc()
        h_cold = exchanger.cold.compute_htc()

        segment_area = area / segments
        hot_temp = exchanger.hot.inlet_temp
        cold_temp = exchanger.cold.inlet_temp
        q_total = 0.0

        c_hot = exchanger.hot.heat_capacity_rate()
        c_cold = exchanger.cold.heat_capacity_rate()

        if c_hot <= 0 or c_cold <= 0:
            raise ValueError("Les capacités calorifiques doivent être positives.")

        for _ in range(segments):
            U_local = exchanger.compute_overall_u(
                h_hot=h_hot,
                h_cold=h_cold,
                area_reference=segment_area,
                additional_resistance=additional_resistance,
            )
            delta_t = hot_temp - cold_temp
            q_segment = U_local * segment_area * delta_t
            hot_temp -= q_segment / c_hot
            cold_temp += q_segment / c_cold
            q_total += q_segment

        details: Dict[str, Any] = {
            "h_hot": h_hot,
            "h_cold": h_cold,
            "segment_area": segment_area,
            "segments": segments,
            "additional_resistance": additional_resistance,
            "hot_metadata": exchanger.hot.htc_model.metadata,
            "cold_metadata": exchanger.cold.htc_model.metadata,
        }

        return OneDResult(
            heat_duty=q_total,
            hot_outlet_temp=hot_temp,
            cold_outlet_temp=cold_temp,
            segments=segments,
            details=details,
        )
