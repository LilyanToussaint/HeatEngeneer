"""Loss coefficient for a globe valve."""
from __future__ import annotations

__all__ = ["k_minor_valve_globe"]


def k_minor_valve_globe() -> float:
    """Return a representative K value for a globe valve."""

    return 10.0


k_minor_valve_globe.metadata = {
    "component": "valve_globe",
    "flow_domain": "internal",
    "quantity": "loss_coefficient",
    "source": "Crane TP-410 typical",
}
