"""Effectiveness for crossflow exchangers with Cmin mixed."""

from __future__ import annotations

from .constants import _EPS_TOL
from .exp_safe import _exp_safe


def effectiveness_crossflow_mixed_cmin(NTU: float, capacity_ratio: float, **_: float) -> float:
    """Return the effectiveness for crossflow with the Cmin side mixed."""

    if capacity_ratio < _EPS_TOL:
        return 1.0 - _exp_safe(-NTU)
    exponent = -capacity_ratio * NTU
    base = 1.0 - _exp_safe(exponent)
    if base <= 0:
        return 0.0
    return 1.0 - _exp_safe(-base / capacity_ratio)


__all__ = ["effectiveness_crossflow_mixed_cmin"]
