"""Shah correlation for saturated flow boiling inside tubes."""

_METADATA = {
    "domain": "boiling",
    "convection": "flow boiling",
    "geometry": "internal flow",
}


def h_shah_flow_boiling(
    G: float,
    x: float,
    q_flux: float,
    h_fg: float,
    rho_l: float,
    rho_v: float,
    mu_l: float,
    k_l: float,
    Pr_l: float,
    D: float,
) -> float:
    """Return the Shah saturated flow-boiling HTC.

    Parameters
    ----------
    G:
        Mass flux [kg/m2/s].
    x:
        Vapor quality (mass fraction of vapor).
    q_flux:
        Applied heat flux [W/m2].
    h_fg:
        Latent heat of vaporization [J/kg].
    rho_l, rho_v:
        Liquid and vapor densities [kg/m3].
    mu_l:
        Liquid viscosity [Pa*s].
    k_l:
        Liquid thermal conductivity [W/m/K].
    Pr_l:
        Liquid Prandtl number.
    D:
        Hydraulic diameter [m].
    """
    if any(param <= 0.0 for param in (G, q_flux, h_fg, rho_l, rho_v, mu_l, k_l, Pr_l, D)):
        raise ValueError("Shah: paramètres physiques doivent être > 0.")
    if not (0.0 <= x < 1.0):
        raise ValueError("Shah: qualité vapeur x doit être dans [0, 1).")

    Re_lo = G * D / mu_l
    if Re_lo <= 0.0:
        raise ValueError("Shah: Re_lo doit être > 0.")

    h_lo = 0.023 * (Re_lo ** 0.8) * (Pr_l ** 0.4) * k_l / D
    Bo = q_flux / (G * h_fg)
    x_eff = max(x, 1.0e-6)
    Co = ((1.0 - x_eff) / x_eff) ** 0.8 * (rho_v / rho_l) ** 0.5

    F = 1.0 + 0.55 * Co ** 0.5
    S = 1.0 + 2.4 * (Bo ** 0.53)

    multiplier = max(F, S)
    return h_lo * multiplier


h_shah_flow_boiling.metadata = _METADATA.copy()

__all__ = ["h_shah_flow_boiling"]
