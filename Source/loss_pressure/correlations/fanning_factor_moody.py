"""Fanning friction factor using a Moody-chart style evaluation."""
from __future__ import annotations

from math import isfinite

from .f_colebrook_white import f_colebrook_white
from .f_transition import f_transition

__all__ = ["fanning_factor_moody"]


def fanning_factor_moody(reynolds: float, relative_roughness: float = 0.0) -> float:
    """Return the Fanning friction factor approximated from the Moody chart."""

    if not isfinite(reynolds) or reynolds <= 0:
        raise ValueError("fanning_factor_moody: Re doit être > 0 et fini.")
    if not isfinite(relative_roughness) or relative_roughness < 0:
        raise ValueError("fanning_factor_moody: e/D doit être >= 0 et fini.")

    if reynolds < 2300.0:
        return 16.0 / reynolds
    if reynolds < 4000.0:
        return f_transition(reynolds, relative_roughness) / 4.0

    return f_colebrook_white(reynolds, relative_roughness) / 4.0


fanning_factor_moody.metadata = {
    "flow_domain": "internal",
    "quantity": "fanning_friction_factor",
    "method": "moody_chart",
}
