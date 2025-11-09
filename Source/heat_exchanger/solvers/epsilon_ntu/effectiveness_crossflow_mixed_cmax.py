"""Effectiveness for crossflow exchangers with Cmax mixed."""

from __future__ import annotations

from .constants import _EPS_TOL
from .exp_safe import _exp_safe


def effectiveness_crossflow_mixed_cmax(NTU: float, capacity_ratio: float, **_: float) -> float:
    """Return the effectiveness for crossflow with the Cmax side mixed."""

    if capacity_ratio < _EPS_TOL:
        return 1.0 - _exp_safe(-NTU)
    numerator = 1.0 - _exp_safe(-NTU)
    denominator = 1.0 - capacity_ratio * _exp_safe(-NTU)
    if abs(denominator) < _EPS_TOL:
        raise ValueError("Configuration croisée mixte: dénominateur nul.")
    return numerator / denominator


__all__ = ["effectiveness_crossflow_mixed_cmax"]
