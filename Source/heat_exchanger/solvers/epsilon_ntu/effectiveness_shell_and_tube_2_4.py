"""Effectiveness relation for 2-4 shell-and-tube exchangers."""

from __future__ import annotations

from .exp_safe import _exp_safe


def effectiveness_shell_and_tube_2_4(NTU: float, capacity_ratio: float, **_: float) -> float:
    """Approximate effectiveness for a 2-4 shell-and-tube exchanger."""

    r = capacity_ratio
    if r == 0:
        return 1.0 - _exp_safe(-NTU)
    term = _exp_safe(-NTU / 2.0 * (1.0 - r))
    numerator = 1.0 - term
    denominator = 1.0 + r * term
    return numerator / denominator


__all__ = ["effectiveness_shell_and_tube_2_4"]
