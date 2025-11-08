"""Loss coefficient for a rounded entrance."""
from __future__ import annotations

from math import isfinite

__all__ = ["k_minor_inlet_rounded"]


def k_minor_inlet_rounded(curvature_ratio: float) -> float:
    """Return the K value for a rounded inlet with ``r/D`` = curvature_ratio."""

    if not isfinite(curvature_ratio):
        raise ValueError("k_minor_inlet_rounded: r/D non fini.")
    if curvature_ratio < 0:
        raise ValueError("k_minor_inlet_rounded: r/D doit être >= 0.")
    if curvature_ratio >= 0.5:
        return 0.02
    return 0.5 * (1.0 - curvature_ratio) ** 2


k_minor_inlet_rounded.metadata = {
    "component": "inlet_rounded",
    "flow_domain": "internal",
    "quantity": "loss_coefficient",
}
