"""Loss coefficient for a standard 90° elbow."""
from __future__ import annotations

__all__ = ["k_minor_elbow_90"]


def k_minor_elbow_90() -> float:
    """Return a representative K value for a 90° elbow (long radius)."""

    return 0.9


k_minor_elbow_90.metadata = {
    "component": "elbow_90",
    "flow_domain": "internal",
    "quantity": "loss_coefficient",
    "source": "Crane TP-410 typical",
}
