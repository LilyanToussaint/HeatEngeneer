"""Loss coefficient for a gate valve as a function of opening ratio."""
from __future__ import annotations

from math import isfinite

__all__ = ["k_minor_valve_gate"]


def k_minor_valve_gate(opening_ratio: float) -> float:
    """Return a K value for a gate valve given an opening ratio ``(0-1)``."""

    if not isfinite(opening_ratio):
        raise ValueError("k_minor_valve_gate: ouverture non finie.")
    if not 0 < opening_ratio <= 1:
        raise ValueError("k_minor_valve_gate: ouverture doit être dans ]0, 1].")

    # Empirical fit: fully open ≈ 0.19, strong rise when throttled.
    throttling = 1.0 / (opening_ratio**2) - 1.0
    return 0.19 + max(throttling, 0.0)


k_minor_valve_gate.metadata = {
    "component": "valve_gate",
    "flow_domain": "internal",
    "quantity": "loss_coefficient",
    "note": "Approximation basée sur Crane TP-410",
}
