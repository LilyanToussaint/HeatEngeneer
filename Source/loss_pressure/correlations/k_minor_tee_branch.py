"""Loss coefficient for branch flow through a tee."""
from __future__ import annotations

__all__ = ["k_minor_tee_branch"]


def k_minor_tee_branch() -> float:
    """Return a representative K value for a tee branch flow."""

    return 1.8


k_minor_tee_branch.metadata = {
    "component": "tee_branch",
    "flow_domain": "internal",
    "quantity": "loss_coefficient",
    "source": "Crane TP-410 typical",
}
