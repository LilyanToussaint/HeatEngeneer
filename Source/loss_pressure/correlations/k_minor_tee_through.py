"""Loss coefficient for flow through a tee (run direction)."""
from __future__ import annotations

__all__ = ["k_minor_tee_through"]


def k_minor_tee_through() -> float:
    """Return a representative K value for flow straight through a tee."""

    return 0.6


k_minor_tee_through.metadata = {
    "component": "tee_through",
    "flow_domain": "internal",
    "quantity": "loss_coefficient",
    "source": "Crane TP-410 typical",
}
