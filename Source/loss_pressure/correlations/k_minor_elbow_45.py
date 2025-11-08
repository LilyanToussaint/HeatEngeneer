"""Loss coefficient for a standard 45° elbow."""
from __future__ import annotations

__all__ = ["k_minor_elbow_45"]


def k_minor_elbow_45() -> float:
    """Return a representative K value for a 45° elbow (long radius)."""

    return 0.4


k_minor_elbow_45.metadata = {
    "component": "elbow_45",
    "flow_domain": "internal",
    "quantity": "loss_coefficient",
    "source": "Crane TP-410 typical",
}
