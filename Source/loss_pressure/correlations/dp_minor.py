"""Minor-loss pressure-drop utility."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_minor"]


def dp_minor(loss_coefficient: float, density: float, velocity: float) -> float:
    """Return the pressure drop associated with a minor loss."""

    for name, value in {
        "k": loss_coefficient,
        "rho": density,
        "v": velocity,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_minor: '{name}' doit être fini.")

    if loss_coefficient < 0:
        raise ValueError("dp_minor: k doit être positif.")
    if density <= 0 or velocity < 0:
        raise ValueError("dp_minor: rho > 0 et v >= 0 requis.")

    return loss_coefficient * 0.5 * density * velocity**2


dp_minor.metadata = {
    "flow_domain": "internal",
    "regime": "minor_loss",
    "geometry": "component",
    "phase": "single-phase",
    "quantity": "pressure_drop",
}
