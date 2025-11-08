"""Gronneveld adiabatic two-phase pressure-drop correlation."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_gronneveld_adiabatic_two_phase"]


def dp_gronneveld_adiabatic_two_phase(
    quality: float,
    dp_liquid_only: float | None = None,
) -> float:
    """Return a Gronneveld adiabatic two-phase multiplier or pressure drop."""

    if not isfinite(quality):
        raise ValueError("dp_gronneveld_adiabatic_two_phase: x doit être fini.")
    if not 0.0 <= quality <= 1.0:
        raise ValueError(
            "dp_gronneveld_adiabatic_two_phase: x doit être compris entre 0 et 1."
        )

    phi_lo_sq = 1.0 + 20.0 * quality * (1.0 - quality)

    if dp_liquid_only is not None:
        if dp_liquid_only <= 0:
            raise ValueError("dp_gronneveld_adiabatic_two_phase: dp_liquid_only > 0 requis.")
        return phi_lo_sq * dp_liquid_only

    return phi_lo_sq


dp_gronneveld_adiabatic_two_phase.metadata = {
    "flow_domain": "two_phase",
    "model": "gronneveld",
    "quantity": "pressure_drop_or_multiplier",
}
