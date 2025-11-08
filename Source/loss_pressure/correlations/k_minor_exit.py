"""Loss coefficient for a pipe exit."""
from __future__ import annotations

__all__ = ["k_minor_exit"]


def k_minor_exit() -> float:
    """Return the K value for a sharp-edged exit."""

    return 1.0


k_minor_exit.metadata = {
    "component": "exit",
    "flow_domain": "internal",
    "quantity": "loss_coefficient",
}
