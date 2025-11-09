"""Rohsenow correlation for nucleate pool boiling."""

_METADATA = {
    "domain": "boiling",
    "convection": "nucleate pool",
    "geometry": "surface",
}

_G = 9.80665  # m/s^2


def h_rohsenow_pool_boiling(
    delta_T: float,
    mu_l: float,
    rho_l: float,
    rho_v: float,
    h_fg: float,
    sigma: float,
    cp_l: float,
    Pr_l: float,
    C_sf: float,
    *,
    n: float = 1.7,
) -> float:
    """Return the nucleate-boiling HTC from the Rohsenow correlation."""
    if delta_T <= 0.0:
        raise ValueError("Rohsenow: ΔT doit être > 0.")
    if any(param <= 0.0 for param in (mu_l, rho_l, rho_v, h_fg, sigma, cp_l, Pr_l, C_sf)):
        raise ValueError("Rohsenow: paramètres physiques doivent être > 0.")

    term = (
        (cp_l * delta_T)
        / (C_sf * h_fg * (Pr_l ** n))
    )
    q_double_prime = (
        mu_l
        * h_fg
        * ((_G * (rho_l - rho_v) / sigma) ** 0.5)
        * (term ** 3.0)
    )
    return q_double_prime / delta_T


h_rohsenow_pool_boiling.metadata = _METADATA.copy()

__all__ = ["h_rohsenow_pool_boiling"]
