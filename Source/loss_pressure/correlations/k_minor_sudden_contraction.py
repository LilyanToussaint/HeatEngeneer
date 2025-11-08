"""Loss coefficient for a sudden contraction."""
from __future__ import annotations

from math import isfinite

__all__ = ["k_minor_sudden_contraction"]


def k_minor_sudden_contraction(d1: float, d2: float) -> float:
    """Return the K value for a sudden contraction from ``d1`` to ``d2``."""

    for name, value in {"D1": d1, "D2": d2}.items():
        if not isfinite(value):
            raise ValueError(f"k_minor_sudden_contraction: '{name}' doit être fini.")
        if value <= 0:
            raise ValueError(
                "k_minor_sudden_contraction: les diamètres doivent être strictement positifs."
            )
    if d1 <= d2:
        raise ValueError("k_minor_sudden_contraction: D1 doit être > D2.")

    beta = d2 / d1
    contraction_coefficient = 0.62 + 0.38 * beta**4
    return (1.0 / contraction_coefficient - 1.0) ** 2


k_minor_sudden_contraction.metadata = {
    "component": "sudden_contraction",
    "flow_domain": "internal",
    "quantity": "loss_coefficient",
}
