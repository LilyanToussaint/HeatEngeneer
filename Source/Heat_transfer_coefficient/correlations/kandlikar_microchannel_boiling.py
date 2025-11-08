"""Kandlikar style flow-boiling correlation for microchannels."""
from __future__ import annotations

import math


_METADATA = {
    "domain": "internal",
    "convection": "boiling",
    "geometry": "microchannel",
}

_G = 9.80665  # m/s^2


def h_kandlikar_microchannel_boiling(
    q_flux: float,
    G: float,
    x: float,
    d_h: float,
    k_l: float,
    Pr_l: float,
    rho_l: float,
    rho_g: float,
    mu_l: float,
    mu_g: float,
    h_fg: float,
    sigma: float,
    C_sf: float = 0.013,
    n: float = 1.7,
) -> float:
    """Return a heat-transfer coefficient for microchannel flow boiling.

    Parameters
    ----------
    q_flux:
        Imposed wall heat flux [W/m²].
    G:
        Mass flux [kg/m²/s].
    x:
        Outlet (or local) quality (0 -- liquide saturé, 1 -- vapeur sèche).
    d_h:
        Hydraulic diameter [m].
    k_l, Pr_l:
        Liquid conductivity [W/m/K] and Prandtl number.
    rho_l, rho_g:
        Liquid and vapor densities [kg/m³].
    mu_l, mu_g:
        Liquid and vapor viscosities [Pa·s].
    h_fg:
        Latent heat of vaporisation [J/kg].
    sigma:
        Surface tension [N/m].
    C_sf, n:
        Rohsenow-like surface coefficient and exponent for the nucleate part.
    """

    if not (0.0 <= x <= 1.0):
        raise ValueError("Kandlikar microchannel boiling: x doit être dans [0, 1].")
    if min(q_flux, G, d_h, k_l, Pr_l, rho_l - rho_g, mu_l, mu_g, h_fg, sigma) <= 0:
        raise ValueError("Kandlikar microchannel boiling: paramètres physiques doivent être > 0.")

    Bo = q_flux / (G * h_fg)
    Co = math.sqrt(sigma / (_G * (rho_l - rho_g))) / d_h
    Re_lo = G * (1.0 - x + 1e-9) * d_h / mu_l
    Re_v = G * (x + 1e-9) * d_h / mu_g

    if Re_lo <= 0:
        raise ValueError("Kandlikar microchannel boiling: Re_liquide <= 0.")
    if Re_v <= 0:
        raise ValueError("Kandlikar microchannel boiling: Re_vapeur <= 0.")

    h_lo = 0.023 * max(Re_lo, 1.0) ** 0.8 * Pr_l ** 0.4 * k_l / d_h

    # Rohsenow-like nucleate boiling enhancement
    term = (_G * (rho_l - rho_g) / sigma) ** 0.25
    h_nb = (
        (q_flux / (C_sf * h_fg))
        * term
        * Pr_l ** (-n)
    )

    X_tt = ((1.0 - x + 1e-9) / (x + 1e-9)) ** 0.9 * (rho_g / rho_l) ** 0.5 * (mu_l / mu_g) ** 0.1
    F_fl = 1.0 + 0.0004 * max(Re_lo, 1.0) ** 0.7 * Co ** 0.8 * X_tt ** 0.2
    S = 1.0 + 2.4 * Bo ** 0.5

    h_tp = max(F_fl * h_lo, S * h_nb)
    if h_tp <= 0:
        raise ValueError("Kandlikar microchannel boiling: h négatif ou nul calculé.")
    return h_tp


h_kandlikar_microchannel_boiling.metadata = _METADATA.copy()


__all__ = ["h_kandlikar_microchannel_boiling"]
