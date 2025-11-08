"""Log-mean temperature difference method implementation."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Optional

from Source.Heat_transfer_coefficient import HeatTransferCoefficient

from .utils import StreamConditions, compute_overall_u


@dataclass
class LMTDResult:
    Q: float
    U: float
    delta_t_lm: float
    correction_factor: float
    details: Dict[str, Any]


class MethodeLMTD:
    """Compute duty via the LMTD approach."""

    def __init__(self, hot_correlation: str, cold_correlation: Optional[str] = None):
        self.hot_wrapper = HeatTransferCoefficient(hot_correlation)
        self.cold_wrapper = HeatTransferCoefficient(cold_correlation or hot_correlation)

    @staticmethod
    def _log_mean_delta_t(delta_t1: float, delta_t2: float) -> float:
        if delta_t1 <= 0 or delta_t2 <= 0:
            raise ValueError("Les différences de température doivent être positives pour le LMTD.")
        if math.isclose(delta_t1, delta_t2):
            return delta_t1
        return (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)

    def compute(
        self,
        hot: StreamConditions,
        cold: StreamConditions,
        area: float,
        hot_outlet_temp: float,
        cold_outlet_temp: float,
        correction_factor: float = 1.0,
        wall_resistance: float = 0.0,
        extra_resistances: Optional[Dict[str, float]] = None,
    ) -> LMTDResult:
        extra_resistances = extra_resistances or {}

        hot_result = self.hot_wrapper.compute(**hot.correlation_kwargs)
        cold_result = self.cold_wrapper.compute(**cold.correlation_kwargs)

        if not hot_result.valid:
            raise ValueError(f"Corrélation chaude invalide: {hot_result.message}")
        if not cold_result.valid:
            raise ValueError(f"Corrélation froide invalide: {cold_result.message}")

        total_wall_resistance = wall_resistance + sum(extra_resistances.values())

        overall_u = compute_overall_u(
            h_hot=hot_result.h,
            h_cold=cold_result.h,
            area_total=area,
            hot=hot,
            cold=cold,
            wall_resistance=total_wall_resistance,
        )

        delta_t1 = hot.inlet_temp - cold_outlet_temp
        delta_t2 = hot_outlet_temp - cold.inlet_temp
        delta_t_lm = self._log_mean_delta_t(delta_t1, delta_t2)

        q = overall_u * area * correction_factor * delta_t_lm

        details: Dict[str, Any] = {
            "h_hot": hot_result.h,
            "h_cold": cold_result.h,
            "delta_t1": delta_t1,
            "delta_t2": delta_t2,
            "hot_metadata": hot_result.correlation_meta,
            "cold_metadata": cold_result.correlation_meta,
        }

        return LMTDResult(
            Q=q,
            U=overall_u,
            delta_t_lm=delta_t_lm,
            correction_factor=correction_factor,
            details=details,
        )
