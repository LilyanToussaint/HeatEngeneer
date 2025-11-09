"""Effectiveness for crossflow heat exchangers with both fluids unmixed."""

from __future__ import annotations

from .constants import _EPS_TOL
from .exp_safe import _exp_safe


def effectiveness_crossflow_unmixed(NTU: float, capacity_ratio: float, **_: float) -> float:
    """Return the effectiveness for a crossflow exchanger with unmixed fluids."""

    if capacity_ratio < _EPS_TOL:
        return 1.0 - _exp_safe(-NTU ** 0.78)
    exponent = -capacity_ratio * NTU ** 0.78
    return 1.0 - _exp_safe((NTU ** 0.78) * (_exp_safe(exponent) - 1.0) / capacity_ratio)


__all__ = ["effectiveness_crossflow_unmixed"]
