"""Heuristic selector for Darcy friction-factor correlations."""
from __future__ import annotations

from math import isfinite

from .f_blasius import f_blasius
from .f_colebrook_white import f_colebrook_white
from .f_petukhov import f_petukhov
from .f_swamee_jain import f_swamee_jain
from .f_transition import f_transition

__all__ = ["select_friction_model"]


def select_friction_model(
    reynolds: float,
    relative_roughness: float = 0.0,
    regime: str | None = None,
) -> float:
    """Select and evaluate a friction-factor model based on flow regime."""

    if not isfinite(reynolds) or reynolds <= 0:
        raise ValueError("select_friction_model: Re doit être > 0 et fini.")
    if not isfinite(relative_roughness) or relative_roughness < 0:
        raise ValueError("select_friction_model: e/D doit être >= 0 et fini.")
    if regime is not None and regime not in {"laminar", "transitional", "turbulent"}:
        raise ValueError("select_friction_model: régime inconnu.")

    if regime == "laminar" or (regime is None and reynolds < 2300.0):
        return 64.0 / reynolds

    if regime == "transitional" or (regime is None and reynolds < 4000.0):
        return f_transition(reynolds, relative_roughness)

    if relative_roughness == 0:
        if reynolds < 5.0e6:
            return f_petukhov(reynolds)
        return f_blasius(min(reynolds, 1.0e5))

    if relative_roughness < 5e-3:
        return f_swamee_jain(reynolds, relative_roughness)

    return f_colebrook_white(reynolds, relative_roughness)


select_friction_model.metadata = {
    "flow_domain": "internal",
    "quantity": "darcy_friction_factor",
    "type": "selector",
}
