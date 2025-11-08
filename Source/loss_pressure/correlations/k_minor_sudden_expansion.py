"""Loss coefficient for a sudden expansion."""
from __future__ import annotations

from math import isfinite

__all__ = ["k_minor_sudden_expansion"]


def k_minor_sudden_expansion(d1: float, d2: float) -> float:
    """Return the K value for a sudden expansion from ``d1`` to ``d2``."""

    for name, value in {"D1": d1, "D2": d2}.items():
        if not isfinite(value):
            raise ValueError(f"k_minor_sudden_expansion: '{name}' doit être fini.")
        if value <= 0:
            raise ValueError(
                "k_minor_sudden_expansion: les diamètres doivent être strictement positifs."
            )
    if d2 < d1:
        raise ValueError("k_minor_sudden_expansion: D2 doit être >= D1.")

    area_ratio = (d1 / d2) ** 2
    return (1.0 - area_ratio) ** 2


k_minor_sudden_expansion.metadata = {
    "component": "sudden_expansion",
    "flow_domain": "internal",
    "quantity": "loss_coefficient",
}
