"""Choked-flow valve utility."""
from __future__ import annotations

from math import isfinite, sqrt

__all__ = ["dp_choked_flow_valve"]


def dp_choked_flow_valve(
    flow_coefficient: float,
    density: float,
    pressure_drop: float | None = None,
    mass_flow: float | None = None,
) -> float:
    """Return choked-flow valve mass flow or required pressure drop."""

    for name, value in {"Cv": flow_coefficient, "rho": density}.items():
        if not isfinite(value) or value <= 0:
            raise ValueError(f"dp_choked_flow_valve: '{name}' doit être > 0 et fini.")

    if pressure_drop is None and mass_flow is None:
        raise ValueError("dp_choked_flow_valve: fournir pressure_drop ou mass_flow.")

    if pressure_drop is not None:
        if not isfinite(pressure_drop) or pressure_drop <= 0:
            raise ValueError("dp_choked_flow_valve: Δp doit être > 0 et fini.")
        return flow_coefficient * sqrt(density * pressure_drop)

    if not isfinite(mass_flow) or mass_flow <= 0:
        raise ValueError("dp_choked_flow_valve: m_dot doit être > 0 et fini.")

    return (mass_flow / flow_coefficient) ** 2 / density


dp_choked_flow_valve.metadata = {
    "flow_domain": "compressible",
    "component": "control_valve",
    "quantity": "mass_flow_or_pressure_drop",
}
