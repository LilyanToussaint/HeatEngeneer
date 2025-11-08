"""Poiseuille pressure drop for fully developed laminar pipe flow."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_laminar_fully_developed"]


def dp_laminar_fully_developed(
    reynolds: float,
    length: float,
    diameter: float,
    dynamic_viscosity: float,
    velocity: float,
) -> float:
    """Return the pressure drop for laminar, fully developed internal flow.

    The correlation implements the classical Hagen–Poiseuille relation::

        Δp = 32 μ v L / D²

    where ``μ`` is the dynamic viscosity [Pa·s], ``v`` the bulk velocity [m/s],
    ``L`` the length [m], and ``D`` the hydraulic diameter [m]. The Reynolds
    number is used only to validate the applicability range of the correlation.
    """

    for name, value in {
        "Re": reynolds,
        "L": length,
        "D": diameter,
        "mu": dynamic_viscosity,
        "v": velocity,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_laminar_fully_developed: '{name}' doit être fini.")

    if length <= 0 or diameter <= 0:
        raise ValueError("dp_laminar_fully_developed: L et D doivent être positifs.")
    if dynamic_viscosity <= 0 or velocity < 0:
        raise ValueError(
            "dp_laminar_fully_developed: viscosité et vitesse doivent être positives."
        )
    if reynolds <= 0:
        raise ValueError("dp_laminar_fully_developed: Re doit être positif.")
    if reynolds >= 2300:
        raise ValueError(
            "dp_laminar_fully_developed: valable seulement pour Re < 2300 (laminaire)."
        )

    return 32.0 * dynamic_viscosity * velocity * length / (diameter**2)


dp_laminar_fully_developed.metadata = {
    "flow_domain": "internal",
    "regime": "laminar",
    "geometry": "circular_duct",
    "phase": "single-phase",
    "quantity": "pressure_drop",
}
