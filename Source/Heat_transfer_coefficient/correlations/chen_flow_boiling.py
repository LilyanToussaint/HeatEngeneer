"""Chen correlation for convective flow boiling inside tubes."""

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


def h_chen_flow_boiling(
    Re_l: float,
    Pr_l: float,
    k_l: float,
    D: float,
    delta_T: float,
    x: float,
    rho_l: float,
    rho_v: float,
    mu_l: float,
    mu_v: float,
    h_fg: float,
    sigma: float,
    cp_l: float,
    *,
    C_sf: float = 0.013,
    n: float = 1.7,
) -> float:
    """Return the Chen flow-boiling HTC for internal flows."""
    if Re_l <= 0.0 or Pr_l <= 0.0 or k_l <= 0.0 or D <= 0.0:
        raise ValueError("Chen: paramètres géométriques ou adimensionnels invalides.")
    if delta_T <= 0.0:
        raise ValueError("Chen: ΔT doit être > 0.")
    if not (0.0 <= x < 1.0):
        raise ValueError("Chen: qualité vapeur x doit être dans [0, 1).")
    if any(param <= 0.0 for param in (rho_l, rho_v, mu_l, mu_v, h_fg, sigma, cp_l, C_sf)):
        raise ValueError("Chen: paramètres physiques doivent être > 0.")

    h_nb = _rohsenow_h(delta_T, mu_l, rho_l, rho_v, h_fg, sigma, cp_l, Pr_l, C_sf, n)
    h_fc = 0.023 * (Re_l ** 0.8) * (Pr_l ** 0.4) * k_l / D

    S = 1.0 / (1.0 + 2.53e-6 * (Re_l ** 1.17))
    x_eff = max(x, 1.0e-6)
    x_tt = ((1.0 - x_eff) / x_eff) ** 0.9 * (rho_v / rho_l) ** 0.5 * (mu_l / mu_v) ** 0.1
    F = 1.0 + 0.12 * (x_tt ** -0.7)

    return S * h_nb + F * h_fc


h_chen_flow_boiling.metadata = _METADATA.copy()

__all__ = ["h_chen_flow_boiling"]
