"""Friedel two-phase pressure-drop multiplier."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_friedel"]

_GRAVITY = 9.80665


def dp_friedel(
    reynolds_liquid: float,
    reynolds_gas: float,
    quality: float,
    density_liquid: float,
    density_gas: float,
    viscosity_liquid: float,
    viscosity_gas: float,
    surface_tension: float,
    diameter: float,
    dp_liquid_only: float | None = None,
) -> float:
    """Return Friedel's two-phase multiplier or pressure drop."""

    for name, value in {
        "Re_l": reynolds_liquid,
        "Re_g": reynolds_gas,
        "x": quality,
        "rho_l": density_liquid,
        "rho_g": density_gas,
        "mu_l": viscosity_liquid,
        "mu_g": viscosity_gas,
        "sigma": surface_tension,
        "D": diameter,
    }.items():
        if not isfinite(value):
            raise ValueError(f"dp_friedel: '{name}' doit être fini.")

    if not (0.0 <= quality <= 1.0):
        raise ValueError("dp_friedel: la qualité doit être comprise entre 0 et 1.")
    if diameter <= 0 or density_liquid <= 0 or density_gas <= 0:
        raise ValueError("dp_friedel: diamètres et densités doivent être positifs.")
    if viscosity_liquid <= 0 or viscosity_gas <= 0 or surface_tension <= 0:
        raise ValueError("dp_friedel: viscosités et tension de surface doivent être > 0.")
    if reynolds_liquid <= 0 or reynolds_gas <= 0:
        raise ValueError("dp_friedel: Reynolds doivent être > 0.")

    mass_flux_liquid = reynolds_liquid * viscosity_liquid / diameter
    fr_l = mass_flux_liquid**2 / (density_liquid**2 * _GRAVITY * diameter)
    we_l = mass_flux_liquid**2 * diameter / (density_liquid * surface_tension)

    e_term = (1.0 - quality) ** 2 + quality**2 * (
        density_liquid * viscosity_gas / (density_gas * viscosity_liquid)
    )
    f_term = quality**0.78 * (1.0 - quality) ** 0.224
    g_term = (density_liquid / density_gas) ** 0.91 * (
        viscosity_gas / viscosity_liquid
    ) ** 0.19
    h_term = fr_l ** -0.045 * we_l ** -0.035

    phi_lo_sq = e_term + 3.24 * f_term * g_term * h_term

    if dp_liquid_only is not None:
        if dp_liquid_only <= 0:
            raise ValueError("dp_friedel: dp_liquid_only doit être > 0.")
        return phi_lo_sq * dp_liquid_only

    return phi_lo_sq


dp_friedel.metadata = {
    "flow_domain": "two_phase",
    "model": "friedel",
    "quantity": "pressure_drop_or_multiplier",
}
