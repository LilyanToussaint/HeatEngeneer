"""Numerically stable exponential helper for epsilon-NTU correlations."""

from __future__ import annotations

from math import exp


_DEF_MIN_EXP_ARGUMENT = -700.0


def _exp_safe(value: float) -> float:
    """Evaluate exp(value) while avoiding floating-point underflow."""

    if value < _DEF_MIN_EXP_ARGUMENT:
        return 0.0
    return exp(value)


__all__ = ["_exp_safe"]
