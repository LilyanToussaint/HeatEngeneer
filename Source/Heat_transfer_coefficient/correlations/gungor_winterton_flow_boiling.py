"""Gungor & Winterton correlation for flow boiling inside tubes."""

_METADATA = {
    "domain": "boiling",
    "convection": "flow boiling",
    "geometry": "internal flow",
}

_G = 9.80665


def _rohsenow_h(delta_T: float, mu_l: float, rho_l: float, rho_v: float, h_fg: float,
                sigma: float, cp_l: float, Pr_l: float, C_sf: float, n: float) -> float:
    term = (cp_l * delta_T) / (C_sf * h_fg * (Pr_l ** n))
    q_double_prime = (
        mu_l
        * h_fg
        * ((_G * (rho_l - rho_v) / sigma) ** 0.5)
        * (term ** 3.0)
    )
    return q_double_prime / delta_T


def h_gungor_winterton_flow_boiling(
    G: float,
    Re_l: float,
    Pr_l: float,
    k_l: float,
    D: float,
    delta_T: float,
    q_flux: float,
    rho_l: float,
    rho_v: float,
    mu_l: float,
    h_fg: float,
    sigma: float,
    cp_l: float,
    *,
    C_sf: float = 0.013,
    n: float = 1.7,
) -> float:
    """Return the Gungor & Winterton flow-boiling HTC."""
    if any(param <= 0.0 for param in (G, Re_l, Pr_l, k_l, D, delta_T, q_flux, rho_l, rho_v, mu_l, h_fg, sigma, cp_l, C_sf)):
        raise ValueError("Gungor-Winterton: paramètres doivent être > 0.")

    h_nb = _rohsenow_h(delta_T, mu_l, rho_l, rho_v, h_fg, sigma, cp_l, Pr_l, C_sf, n)
    h_lo = 0.023 * (Re_l ** 0.8) * (Pr_l ** 0.4) * k_l / D

    S = 1.0 / (1.0 + 2.53e-6 * (Re_l ** 1.17))
    Bo = q_flux / (G * h_fg)
    F = 1.0 + 0.1 * (Bo ** 0.7)

    return S * h_nb + F * h_lo


h_gungor_winterton_flow_boiling.metadata = _METADATA.copy()

__all__ = ["h_gungor_winterton_flow_boiling"]
