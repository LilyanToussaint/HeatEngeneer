"""Parallel-flow heat-exchanger effectiveness relation."""

from __future__ import annotations

from .exp_safe import _exp_safe


def effectiveness_parallel(NTU: float, capacity_ratio: float, **_: float) -> float:
    """Return the epsilon-NTU effectiveness for parallel flow."""

    denominator = 1.0 + capacity_ratio
    if denominator <= 0:
        raise ValueError("Le rapport des capacités thermiques doit être >= 0.")
    return (1.0 - _exp_safe(-NTU * denominator)) / denominator


__all__ = ["effectiveness_parallel"]
