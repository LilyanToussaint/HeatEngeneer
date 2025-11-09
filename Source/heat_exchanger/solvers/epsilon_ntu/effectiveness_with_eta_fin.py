"""Effectiveness adjustment for fin efficiencies."""

from __future__ import annotations

from .constants import _EPS_TOL


def effectiveness_with_eta_fin(
    NTU: float,
    capacity_ratio: float,
    eta_hot: float,
    eta_cold: float,
    base: str = "counterflow",
    **kwargs: float,
) -> float:
    """Scale the NTU using fin efficiencies before evaluating the base relation."""

    if eta_hot <= 0 or eta_cold <= 0:
        raise ValueError("Les efficacités d'ailettes doivent être positives.")

    from .get_effectiveness_function import get_effectiveness_function

    func, needs_eta = get_effectiveness_function(base)
    if needs_eta:
        raise ValueError("La configuration de base requiert déjà des eta fin.")

    eta_factor = max(min((eta_hot + eta_cold) * 0.5, 1.0), _EPS_TOL)
    return func(NTU * eta_factor, capacity_ratio, **kwargs)


__all__ = ["effectiveness_with_eta_fin"]
