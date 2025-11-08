"""Blasius smooth-pipe turbulent friction-factor correlation."""
from __future__ import annotations

from math import isfinite

__all__ = ["f_blasius"]


def f_blasius(reynolds: float) -> float:
    """Return the Darcy friction factor for smooth turbulent pipes.

    The Blasius correlation is applicable approximately for
    ``4e3 <= Re <= 1e5``.
    """

    if not isfinite(reynolds):
        raise ValueError("f_blasius: Re doit être fini.")
    if reynolds <= 0:
        raise ValueError("f_blasius: Re doit être positif.")
    if reynolds < 4.0e3 or reynolds > 1.0e5:
        raise ValueError("f_blasius: valable pour 4e3 <= Re <= 1e5.")

    return 0.3164 / (reynolds ** 0.25)


f_blasius.metadata = {
    "flow_domain": "internal",
    "regime": "turbulent",
    "geometry": "circular_duct",
    "phase": "single-phase",
    "quantity": "darcy_friction_factor",
    "roughness": "smooth",
}
