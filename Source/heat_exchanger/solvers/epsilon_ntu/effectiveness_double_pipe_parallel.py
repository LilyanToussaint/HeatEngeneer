"""Effectiveness for double-pipe exchangers in parallel flow."""

from __future__ import annotations

from .effectiveness_parallel import effectiveness_parallel


def effectiveness_double_pipe_parallel(NTU: float, capacity_ratio: float, **kwargs: float) -> float:
    """Delegate to the parallel-flow effectiveness relation."""

    return effectiveness_parallel(NTU, capacity_ratio, **kwargs)


__all__ = ["effectiveness_double_pipe_parallel"]
