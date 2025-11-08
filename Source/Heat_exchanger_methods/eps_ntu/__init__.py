"""Effectiveness relationships for the epsilon-NTU method."""
from __future__ import annotations

from math import exp
from typing import Callable, Dict, Tuple


_EPS_TOL = 1e-12


def _exp_safe(value: float) -> float:
    if value < -700:  # avoid underflow
        return 0.0
    return exp(value)


def effectiveness_parallel(NTU: float, capacity_ratio: float, **_: float) -> float:
    denominator = 1.0 + capacity_ratio
    if denominator <= 0:
        raise ValueError("Le rapport des capacités thermiques doit être >= 0.")
    return (1.0 - _exp_safe(-NTU * denominator)) / denominator


def effectiveness_counterflow(NTU: float, capacity_ratio: float, **_: float) -> float:
    if abs(1.0 - capacity_ratio) < _EPS_TOL:
        return NTU / (1.0 + NTU)
    numerator = 1.0 - _exp_safe(-NTU * (1.0 - capacity_ratio))
    denominator = 1.0 - capacity_ratio * _exp_safe(-NTU * (1.0 - capacity_ratio))
    if denominator == 0:
        raise ValueError("Dénominateur nul dans la formule contre-courant.")
    return numerator / denominator


def effectiveness_shell_and_tube_1_2(NTU: float, capacity_ratio: float, **_: float) -> float:
    r = capacity_ratio
    p = 1.0 - _exp_safe(-NTU * (1.0 - r))
    denominator = 2.0 - p * (1.0 + r)
    if abs(denominator) < _EPS_TOL:
        raise ValueError("Formule 1-2 indéterminée pour ces paramètres.")
    return 2.0 * p / denominator


def effectiveness_shell_and_tube_2_4(NTU: float, capacity_ratio: float, **_: float) -> float:
    # Approximation via multiple shell passes (Shah & London correlation)
    r = capacity_ratio
    if r == 0:
        return 1.0 - _exp_safe(-NTU)
    term = _exp_safe(-NTU / 2.0 * (1.0 - r))
    numerator = 1.0 - term
    denominator = 1.0 + r * term
    return numerator / denominator


def effectiveness_crossflow_unmixed(NTU: float, capacity_ratio: float, **_: float) -> float:
    if capacity_ratio < _EPS_TOL:
        return 1.0 - _exp_safe(-NTU ** 0.78)
    exponent = -capacity_ratio * NTU ** 0.78
    return 1.0 - _exp_safe((NTU ** 0.78) * (_exp_safe(exponent) - 1.0) / capacity_ratio)


def effectiveness_crossflow_mixed_cmax(NTU: float, capacity_ratio: float, **_: float) -> float:
    if capacity_ratio < _EPS_TOL:
        return (1.0 - _exp_safe(-NTU))
    numerator = 1.0 - _exp_safe(-NTU)
    denominator = 1.0 - capacity_ratio * _exp_safe(-NTU)
    if abs(denominator) < _EPS_TOL:
        raise ValueError("Configuration croisée mixte: dénominateur nul.")
    return numerator / denominator


def effectiveness_crossflow_mixed_cmin(NTU: float, capacity_ratio: float, **_: float) -> float:
    # Kays & London approximation when Cmin side is mixed.
    if capacity_ratio < _EPS_TOL:
        return 1.0 - _exp_safe(-NTU)
    exponent = -capacity_ratio * NTU
    base = 1.0 - _exp_safe(exponent)
    if base <= 0:
        return 0.0
    return 1.0 - _exp_safe(-base / capacity_ratio)


def effectiveness_double_pipe_counterflow(NTU: float, capacity_ratio: float, **_: float) -> float:
    return effectiveness_counterflow(NTU, capacity_ratio)


def effectiveness_double_pipe_parallel(NTU: float, capacity_ratio: float, **_: float) -> float:
    return effectiveness_parallel(NTU, capacity_ratio)


def effectiveness_with_eta_fin(
    NTU: float,
    capacity_ratio: float,
    eta_hot: float,
    eta_cold: float,
    base: str = "counterflow",
    **kwargs: float,
) -> float:
    if eta_hot <= 0 or eta_cold <= 0:
        raise ValueError("Les efficacités d'ailettes doivent être positives.")
    func, needs_eta = get_effectiveness_function(base)
    if needs_eta:
        raise ValueError("La configuration de base requiert déjà des eta fin.")
    eta_factor = max(min((eta_hot + eta_cold) * 0.5, 1.0), _EPS_TOL)
    return func(NTU * eta_factor, capacity_ratio, **kwargs)


def effectiveness_counterflow_eta_fin(
    NTU: float, capacity_ratio: float, eta_hot: float, eta_cold: float, **kwargs: float
) -> float:
    return effectiveness_with_eta_fin(NTU, capacity_ratio, eta_hot, eta_cold, base="counterflow", **kwargs)


def effectiveness_parallel_eta_fin(
    NTU: float, capacity_ratio: float, eta_hot: float, eta_cold: float, **kwargs: float
) -> float:
    return effectiveness_with_eta_fin(NTU, capacity_ratio, eta_hot, eta_cold, base="parallel", **kwargs)


EPSILON_FUNCTIONS: Dict[str, Callable[..., float]] = {
    "parallel": effectiveness_parallel,
    "counterflow": effectiveness_counterflow,
    "shell_and_tube_1_2": effectiveness_shell_and_tube_1_2,
    "shell_and_tube_2_4": effectiveness_shell_and_tube_2_4,
    "crossflow_both_unmixed": effectiveness_crossflow_unmixed,
    "crossflow_mixed_cmax": effectiveness_crossflow_mixed_cmax,
    "crossflow_mixed_cmin": effectiveness_crossflow_mixed_cmin,
    "double_pipe_counterflow": effectiveness_double_pipe_counterflow,
    "double_pipe_parallel": effectiveness_double_pipe_parallel,
}

EPSILON_WITH_FIN_FUNCTIONS: Dict[str, Callable[..., float]] = {
    "counterflow_eta_fin": effectiveness_counterflow_eta_fin,
    "parallel_eta_fin": effectiveness_parallel_eta_fin,
}


def get_effectiveness_function(name: str) -> Tuple[Callable[..., float], bool]:
    if name in EPSILON_FUNCTIONS:
        return EPSILON_FUNCTIONS[name], False
    if name in EPSILON_WITH_FIN_FUNCTIONS:
        return EPSILON_WITH_FIN_FUNCTIONS[name], True
    raise ValueError(
        f"Configuration epsilon-NTU inconnue '{name}'. Dispos: {list(EPSILON_FUNCTIONS) + list(EPSILON_WITH_FIN_FUNCTIONS)}"
    )


__all__ = [
    "get_effectiveness_function",
    "EPSILON_FUNCTIONS",
    "EPSILON_WITH_FIN_FUNCTIONS",
]
