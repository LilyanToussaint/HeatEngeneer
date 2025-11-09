"""Effectiveness relation for 1-2 shell-and-tube exchangers."""

from __future__ import annotations

from .constants import _EPS_TOL
from .exp_safe import _exp_safe


def effectiveness_shell_and_tube_1_2(NTU: float, capacity_ratio: float, **_: float) -> float:
    """Return the effectiveness for a 1-2 shell-and-tube exchanger."""

    r = capacity_ratio
    p = 1.0 - _exp_safe(-NTU * (1.0 - r))
    denominator = 2.0 - p * (1.0 + r)
    if abs(denominator) < _EPS_TOL:
        raise ValueError("Formule 1-2 indéterminée pour ces paramètres.")
    return 2.0 * p / denominator


__all__ = ["effectiveness_shell_and_tube_1_2"]
