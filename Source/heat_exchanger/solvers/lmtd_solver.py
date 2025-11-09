"""Log-mean temperature difference solver."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ..heat_exchanger import HeatExchanger
from ..solver import HeatExchangerSolver


@dataclass(slots=True)
class LMTDResult:
    Q: float
    U: float
    delta_t_lm: float
    correction_factor: float
    details: Dict[str, Any] = field(default_factory=dict)


class LMTDSolver(HeatExchangerSolver):
    """Compute duty via the LMTD approach."""

    def __init__(self) -> None:
        super().__init__(name="lmtd")

    @staticmethod
    def _log_mean_delta_t(delta_t1: float, delta_t2: float) -> float:
        if delta_t1 <= 0 or delta_t2 <= 0:
            raise ValueError("Les différences de température doivent être positives pour le LMTD.")
        if math.isclose(delta_t1, delta_t2):
            return delta_t1
        return (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)

    def solve(
        self,
        exchanger: HeatExchanger,
        area: float,
        hot_outlet_temp: float,
        cold_outlet_temp: float,
        correction_factor: float = 1.0,
        extra_resistances: Optional[Dict[str, float]] = None,
    ) -> LMTDResult:
        extra_resistances = extra_resistances or {}
        extra_total = sum(extra_resistances.values())

        h_hot = exchanger.hot.compute_htc()
        h_cold = exchanger.cold.compute_htc()

        overall_u = exchanger.compute_overall_u(
            h_hot=h_hot,
            h_cold=h_cold,
            area_reference=area,
            additional_resistance=extra_total,
        )

        delta_t1 = exchanger.hot.inlet_temp - cold_outlet_temp
        delta_t2 = hot_outlet_temp - exchanger.cold.inlet_temp
        delta_t_lm = self._log_mean_delta_t(delta_t1, delta_t2)

        q = overall_u * area * correction_factor * delta_t_lm

        details: Dict[str, Any] = {
            "h_hot": h_hot,
            "h_cold": h_cold,
            "delta_t1": delta_t1,
            "delta_t2": delta_t2,
            "extra_resistances": extra_resistances,
            "hot_metadata": exchanger.hot.htc_model.metadata,
            "cold_metadata": exchanger.cold.htc_model.metadata,
        }

        return LMTDResult(
            Q=q,
            U=overall_u,
            delta_t_lm=delta_t_lm,
            correction_factor=correction_factor,
            details=details,
        )
