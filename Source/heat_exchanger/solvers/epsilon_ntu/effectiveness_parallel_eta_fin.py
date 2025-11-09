"""Parallel-flow effectiveness including fin efficiencies."""

from __future__ import annotations

from .effectiveness_with_eta_fin import effectiveness_with_eta_fin


def effectiveness_parallel_eta_fin(
    NTU: float,
    capacity_ratio: float,
    eta_hot: float,
    eta_cold: float,
    **kwargs: float,
) -> float:
    """Return the parallel-flow effectiveness adjusted for fin efficiencies."""

    return effectiveness_with_eta_fin(
        NTU,
        capacity_ratio,
        eta_hot,
        eta_cold,
        base="parallel",
        **kwargs,
    )


__all__ = ["effectiveness_parallel_eta_fin"]
