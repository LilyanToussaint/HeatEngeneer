"""Effectiveness for double-pipe exchangers in counterflow."""

from __future__ import annotations

from .effectiveness_counterflow import effectiveness_counterflow


def effectiveness_double_pipe_counterflow(NTU: float, capacity_ratio: float, **kwargs: float) -> float:
    """Delegate to the counterflow effectiveness relation."""

    return effectiveness_counterflow(NTU, capacity_ratio, **kwargs)


__all__ = ["effectiveness_double_pipe_counterflow"]
