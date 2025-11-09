"""Counter-flow heat-exchanger effectiveness relation."""

from __future__ import annotations

from .constants import _EPS_TOL
from .exp_safe import _exp_safe


def effectiveness_counterflow(NTU: float, capacity_ratio: float, **_: float) -> float:
    """Return the epsilon-NTU effectiveness for a counter-flow exchanger."""

    if abs(1.0 - capacity_ratio) < _EPS_TOL:
        return NTU / (1.0 + NTU)

    numerator = 1.0 - _exp_safe(-NTU * (1.0 - capacity_ratio))
    denominator = 1.0 - capacity_ratio * _exp_safe(-NTU * (1.0 - capacity_ratio))
    if denominator == 0:
        raise ValueError("Dénominateur nul dans la formule contre-courant.")
    return numerator / denominator


__all__ = ["effectiveness_counterflow"]
