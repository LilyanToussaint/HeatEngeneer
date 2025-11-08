"""Petukhov smooth-tube friction-factor correlation."""
from __future__ import annotations

from math import isfinite, log

__all__ = ["f_petukhov"]


def f_petukhov(reynolds: float) -> float:
    """Return the Petukhov turbulent friction factor for smooth tubes.

    Valid roughly for ``1e4 <= Re <= 5e6``.
    """

    if not isfinite(reynolds):
        raise ValueError("f_petukhov: Re doit être fini.")
    if reynolds <= 0:
        raise ValueError("f_petukhov: Re doit être positif.")
    if reynolds < 1.0e4 or reynolds > 5.0e6:
        raise ValueError("f_petukhov: valable pour 1e4 <= Re <= 5e6.")

    return 1.0 / (0.79 * log(reynolds) - 1.64) ** 2


f_petukhov.metadata = {
    "flow_domain": "internal",
    "regime": "turbulent",
    "geometry": "circular_duct",
    "phase": "single-phase",
    "quantity": "darcy_friction_factor",
    "roughness": "smooth",
}
