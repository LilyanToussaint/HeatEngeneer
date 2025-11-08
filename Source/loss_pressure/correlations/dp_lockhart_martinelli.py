"""Lockhart-Martinelli two-phase pressure-drop multiplier."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_lockhart_martinelli"]


def dp_lockhart_martinelli(
    x_tt: float,
    phi_lo_sq: float,
    phi_go_sq: float,
    dp_lo: float | None = None,
    dp_go: float | None = None,
) -> float:
    """Return a Lockhart-Martinelli two-phase pressure-drop estimate."""

    for name, value in {
        "X_tt": x_tt,
        "phi_lo^2": phi_lo_sq,
        "phi_go^2": phi_go_sq,
    }.items():
        if not isfinite(value) or value <= 0:
            raise ValueError(f"dp_lockhart_martinelli: '{name}' doit être > 0 et fini.")

    if dp_lo is not None:
        if dp_lo <= 0:
            raise ValueError("dp_lockhart_martinelli: dp_lo doit être > 0.")
        return phi_lo_sq * dp_lo
    if dp_go is not None:
        if dp_go <= 0:
            raise ValueError("dp_lockhart_martinelli: dp_go doit être > 0.")
        return phi_go_sq * dp_go

    return max(phi_lo_sq, phi_go_sq)


dp_lockhart_martinelli.metadata = {
    "flow_domain": "two_phase",
    "model": "lockhart_martinelli",
    "quantity": "pressure_drop_or_multiplier",
}
