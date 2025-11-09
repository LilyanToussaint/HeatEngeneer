"""Epsilon-NTU solver that operates on the high-level exchanger model."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ...heat_exchanger import HeatExchanger
from ...solver import HeatExchangerSolver
from .get_effectiveness_function import get_effectiveness_function
from .registry import EPSILON_FUNCTIONS, EPSILON_WITH_FIN_FUNCTIONS


@dataclass(slots=True)
class NTUResult:
    """Return data for heat-exchanger calculations."""

    epsilon: float
    NTU: float
    U: float
    Q: float
    hot_outlet_temp: float
    cold_outlet_temp: float
    details: Dict[str, Any] = field(default_factory=dict)


class EpsilonNTUSolver(HeatExchangerSolver):
    """Compute heat-exchanger duty via the epsilon-NTU approach."""

    def __init__(self) -> None:
        super().__init__(name="epsilon-ntu")

    @staticmethod
    def available_configurations() -> list[str]:
        return sorted(list(EPSILON_FUNCTIONS) + list(EPSILON_WITH_FIN_FUNCTIONS))

    def solve(
        self,
        exchanger: HeatExchanger,
        area: float,
        configuration: Optional[str] = None,
        configuration_kwargs: Optional[Dict[str, Any]] = None,
        use_eta_fin_method: bool = False,
    ) -> NTUResult:
        configuration_kwargs = configuration_kwargs or {}
        config_name = configuration or exchanger.arrangement.name

        h_hot = exchanger.hot.compute_htc()
        h_cold = exchanger.cold.compute_htc()

        overall_u = exchanger.compute_overall_u(h_hot=h_hot, h_cold=h_cold, area_reference=area)

        c_hot = exchanger.hot.heat_capacity_rate()
        c_cold = exchanger.cold.heat_capacity_rate()

        if c_hot <= 0 or c_cold <= 0:
            raise ValueError("Les capacités calorifiques doivent être positives.")

        c_min = min(c_hot, c_cold)
        c_max = max(c_hot, c_cold)
        capacity_ratio = c_min / c_max if c_max > 0 else 0.0

        NTU = overall_u * area / c_min

        func, needs_eta = get_effectiveness_function(config_name)

        if use_eta_fin_method and not needs_eta:
            alt_name = f"{config_name}_eta_fin"
            func, needs_eta = get_effectiveness_function(alt_name)
            config_name = alt_name

        kwargs = dict(configuration_kwargs)

        if needs_eta:
            try:
                eta_hot = kwargs.pop("eta_hot")
                eta_cold = kwargs.pop("eta_cold")
            except KeyError as exc:
                raise ValueError(
                    "Les paramètres eta_hot et eta_cold sont requis pour cette configuration."
                ) from exc
            epsilon = func(NTU, capacity_ratio, eta_hot=eta_hot, eta_cold=eta_cold, **kwargs)
        else:
            epsilon = func(NTU, capacity_ratio, **kwargs)

        delta_t_inlet = exchanger.hot.inlet_temp - exchanger.cold.inlet_temp
        Q_max = c_min * delta_t_inlet
        Q = epsilon * Q_max

        hot_outlet = exchanger.hot.inlet_temp - Q / c_hot
        cold_outlet = exchanger.cold.inlet_temp + Q / c_cold

        details = {
            "h_hot": h_hot,
            "h_cold": h_cold,
            "NTU": NTU,
            "capacity_ratio": capacity_ratio,
            "configuration": config_name,
            "overall_u": overall_u,
            "hot_metadata": exchanger.hot.htc_model.metadata,
            "cold_metadata": exchanger.cold.htc_model.metadata,
        }

        return NTUResult(
            epsilon=epsilon,
            NTU=NTU,
            U=overall_u,
            Q=Q,
            hot_outlet_temp=hot_outlet,
            cold_outlet_temp=cold_outlet,
            details=details,
        )
