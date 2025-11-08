"""Simple one-dimensional discretised heat-exchanger model."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from Source.Heat_transfer_coefficient import HeatTransferCoefficient

from .utils import StreamConditions, compute_overall_u


@dataclass
class OneDResult:
    heat_duty: float
    hot_outlet_temp: float
    cold_outlet_temp: float
    segments: int
    details: Dict[str, Any] = field(default_factory=dict)


class Methode1D:
    """March along the exchanger length and solve energy balances per cell."""

    def __init__(self, hot_correlation: str, cold_correlation: Optional[str] = None):
        self.hot_wrapper = HeatTransferCoefficient(hot_correlation)
        self.cold_wrapper = HeatTransferCoefficient(cold_correlation or hot_correlation)

    def compute(
        self,
        hot: StreamConditions,
        cold: StreamConditions,
        area: float,
        segments: int = 20,
        wall_resistance: float = 0.0,
    ) -> OneDResult:
        if segments <= 0:
            raise ValueError("Le nombre de segments doit être strictement positif.")

        hot_result = self.hot_wrapper.compute(**hot.correlation_kwargs)
        cold_result = self.cold_wrapper.compute(**cold.correlation_kwargs)

        if not hot_result.valid:
            raise ValueError(f"Corrélation chaude invalide: {hot_result.message}")
        if not cold_result.valid:
            raise ValueError(f"Corrélation froide invalide: {cold_result.message}")

        segment_area = area / segments

        hot_temp = hot.inlet_temp
        cold_temp = cold.inlet_temp
        q_total = 0.0

        c_hot = hot.heat_capacity_rate()
        c_cold = cold.heat_capacity_rate()

        if c_hot <= 0 or c_cold <= 0:
            raise ValueError("Les capacités calorifiques doivent être positives.")

        for _ in range(segments):
            U_local = compute_overall_u(
                h_hot=hot_result.h,
                h_cold=cold_result.h,
                area_total=segment_area,
                hot=hot,
                cold=cold,
                wall_resistance=wall_resistance,
            )
            delta_t = hot_temp - cold_temp
            q_segment = U_local * segment_area * delta_t
            hot_temp -= q_segment / c_hot
            cold_temp += q_segment / c_cold
            q_total += q_segment

        details: Dict[str, Any] = {
            "h_hot": hot_result.h,
            "h_cold": cold_result.h,
            "segment_area": segment_area,
            "segments": segments,
            "hot_metadata": hot_result.correlation_meta,
            "cold_metadata": cold_result.correlation_meta,
        }

        return OneDResult(
            heat_duty=q_total,
            hot_outlet_temp=hot_temp,
            cold_outlet_temp=cold_temp,
            segments=segments,
            details=details,
        )
