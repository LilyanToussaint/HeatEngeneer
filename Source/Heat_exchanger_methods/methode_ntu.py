"""Epsilon-NTU method implementation relying on the HTC wrapper."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from Source.Heat_transfer_coefficient import HeatTransferCoefficient

from .eps_ntu.get_effectiveness_function import get_effectiveness_function
from .eps_ntu.registry import EPSILON_FUNCTIONS, EPSILON_WITH_FIN_FUNCTIONS
from .utils import StreamConditions, compute_overall_u


@dataclass
class HeatExchangerResult:
    """Return data for heat-exchanger calculations."""

    epsilon: float
    NTU: float
    U: float
    Q: float
    hot_outlet_temp: float
    cold_outlet_temp: float
    details: Dict[str, Any] = field(default_factory=dict)


class MethodeNTU:
    """Compute heat-exchanger duty via the epsilon-NTU approach."""

    def __init__(self, hot_correlation: str, cold_correlation: Optional[str] = None):
        self.hot_wrapper = HeatTransferCoefficient(hot_correlation)
        self.cold_wrapper = HeatTransferCoefficient(cold_correlation or hot_correlation)

    @staticmethod
    def available_configurations() -> list[str]:
        return sorted(list(EPSILON_FUNCTIONS) + list(EPSILON_WITH_FIN_FUNCTIONS))

    def compute(
        self,
        hot: StreamConditions,
        cold: StreamConditions,
        area: float,
        configuration: str = "counterflow",
        wall_resistance: float = 0.0,
        configuration_kwargs: Optional[Dict[str, Any]] = None,
        use_eta_fin_method: bool = False,
    ) -> HeatExchangerResult:
        configuration_kwargs = configuration_kwargs or {}

        hot_result = self.hot_wrapper.compute(**hot.correlation_kwargs)
        cold_result = self.cold_wrapper.compute(**cold.correlation_kwargs)

        if not hot_result.valid:
            raise ValueError(f"Corrélation chaude invalide: {hot_result.message}")
        if not cold_result.valid:
            raise ValueError(f"Corrélation froide invalide: {cold_result.message}")

        overall_u = compute_overall_u(
            h_hot=hot_result.h,
            h_cold=cold_result.h,
            area_total=area,
            hot=hot,
            cold=cold,
            wall_resistance=wall_resistance,
        )

        c_hot = hot.heat_capacity_rate()
        c_cold = cold.heat_capacity_rate()

        if c_hot <= 0 or c_cold <= 0:
            raise ValueError("Les capacités calorifiques doivent être positives.")

        c_min = min(c_hot, c_cold)
        c_max = max(c_hot, c_cold)
        capacity_ratio = c_min / c_max if c_max > 0 else 0.0

        NTU = overall_u * area / c_min

        func, needs_eta = get_effectiveness_function(configuration)

        if needs_eta or use_eta_fin_method:
            eta_hot = hot.fin_efficiency
            eta_cold = cold.fin_efficiency
            epsilon = func(NTU, capacity_ratio, eta_hot=eta_hot, eta_cold=eta_cold, **configuration_kwargs)
        else:
            epsilon = func(NTU, capacity_ratio, **configuration_kwargs)

        delta_t_inlet = hot.inlet_temp - cold.inlet_temp
        Q_max = c_min * delta_t_inlet
        Q = epsilon * Q_max

        hot_outlet = hot.inlet_temp - Q / c_hot
        cold_outlet = cold.inlet_temp + Q / c_cold

        details = {
            "h_hot": hot_result.h,
            "h_cold": cold_result.h,
            "NTU": NTU,
            "capacity_ratio": capacity_ratio,
            "configuration": configuration,
            "hot_metadata": hot_result.correlation_meta,
            "cold_metadata": cold_result.correlation_meta,
            "overall_u": overall_u,
        }

        return HeatExchangerResult(
            epsilon=epsilon,
            NTU=NTU,
            U=overall_u,
            Q=Q,
            hot_outlet_temp=hot_outlet,
            cold_outlet_temp=cold_outlet,
            details=details,
        )
