"""Shah correlation for condensation inside tubes."""

_METADATA = {
    "domain": "condensation",
    "convection": "film",
    "geometry": "internal flow",
}


def h_shah_condensation_inside_tube(
    G: float,
    x: float,
    rho_l: float,
    rho_v: float,
    mu_l: float,
    k_l: float,
    Pr_l: float,
    D: float,
) -> float:
    """Return the Shah condensation HTC for internal tube flow."""
    if any(param <= 0.0 for param in (G, rho_l, rho_v, mu_l, k_l, Pr_l, D)):
        raise ValueError("Shah condensation: paramètres doivent être > 0.")
    if not (0.0 <= x <= 1.0):
        raise ValueError("Shah condensation: qualité vapeur x doit être dans [0, 1].")

    Re_lo = G * D / mu_l
    if Re_lo <= 0.0:
        raise ValueError("Shah condensation: Re_lo doit être > 0.")

    h_lo = 0.023 * (Re_lo ** 0.8) * (Pr_l ** 0.4) * k_l / D
    x_eff = max(x, 1.0e-6)
    Co = ((1.0 - x_eff) / x_eff) ** 0.8 * (rho_v / rho_l) ** 0.5
    F = 1.0 + 3.8 * (Co ** -0.76)
    return h_lo * F


h_shah_condensation_inside_tube.metadata = _METADATA.copy()

__all__ = ["h_shah_condensation_inside_tube"]
