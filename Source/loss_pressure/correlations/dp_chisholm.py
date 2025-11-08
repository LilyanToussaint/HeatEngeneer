"""Simplified Chisholm two-phase pressure-drop correlation."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_chisholm"]


def dp_chisholm(
    reynolds_liquid: float,
    reynolds_gas: float,
    beta: float,
    dp_liquid_only: float | None = None,
) -> float:
    """Return the Chisholm two-phase multiplier or pressure drop."""

    for name, value in {
        "Re_l": reynolds_liquid,
        "Re_g": reynolds_gas,
        "beta": beta,
    }.items():
        if not isfinite(value) or value <= 0:
            raise ValueError(f"dp_chisholm: '{name}' doit être > 0 et fini.")

    c_param = 20.0 if reynolds_liquid > 2.0e4 and reynolds_gas > 2.0e4 else 12.0
    phi_lo_sq = 1.0 + c_param / beta + 1.0 / (beta * beta)

    if dp_liquid_only is not None:
        if dp_liquid_only <= 0:
            raise ValueError("dp_chisholm: dp_liquid_only doit être > 0.")
        return phi_lo_sq * dp_liquid_only

    return phi_lo_sq


dp_chisholm.metadata = {
    "flow_domain": "two_phase",
    "model": "chisholm",
    "quantity": "pressure_drop_or_multiplier",
}
