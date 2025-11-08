"""Blending correlation between laminar and turbulent friction factors."""
from __future__ import annotations

from math import isfinite

__all__ = ["f_transition"]


_LAMINAR_LIMIT = 2100.0
_TURBULENT_LIMIT = 4000.0


def f_transition(reynolds: float, relative_roughness: float = 0.0) -> float:
    """Blend laminar and turbulent friction factors in the transitional regime."""

    if not isfinite(reynolds) or not isfinite(relative_roughness):
        raise ValueError("f_transition: entrées non finies.")
    if reynolds <= 0:
        raise ValueError("f_transition: Re doit être positif.")
    if relative_roughness < 0:
        raise ValueError("f_transition: e/D doit être positif ou nul.")

    if reynolds <= _LAMINAR_LIMIT:
        return 64.0 / reynolds

    if reynolds >= _TURBULENT_LIMIT:
        from .f_swamee_jain import f_swamee_jain

        return f_swamee_jain(reynolds, relative_roughness)

    from .f_swamee_jain import f_swamee_jain

    laminar = 64.0 / _LAMINAR_LIMIT
    turbulent = f_swamee_jain(_TURBULENT_LIMIT, relative_roughness)
    weight = (reynolds - _LAMINAR_LIMIT) / (_TURBULENT_LIMIT - _LAMINAR_LIMIT)
    return laminar + weight * (turbulent - laminar)


f_transition.metadata = {
    "flow_domain": "internal",
    "regime": "transitional",
    "geometry": "circular_duct",
    "phase": "single-phase",
    "quantity": "darcy_friction_factor",
    "method": "linear_blend",
}
