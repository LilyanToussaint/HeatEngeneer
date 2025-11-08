"""Nusselt laminar-film condensation on horizontal tubes."""

_METADATA = {
    "domain": "condensation",
    "convection": "film",
    "geometry": "horizontal tube",
}

_G = 9.80665


def h_nusselt_film_horizontal_tube(
    delta_T: float,
    rho_l: float,
    rho_v: float,
    mu_l: float,
    k_l: float,
    h_fg: float,
    D: float,
) -> float:
    """Return the Nusselt laminar-film condensation HTC for a horizontal tube."""
    if any(param <= 0.0 for param in (delta_T, rho_l, rho_v, mu_l, k_l, h_fg, D)):
        raise ValueError("Nusselt tube horizontal: paramètres doivent être > 0.")

    term = (
        rho_l * (rho_l - rho_v) * _G * h_fg * (k_l ** 3)
        / (mu_l * D * delta_T)
    )
    return 0.725 * (term ** 0.25)


h_nusselt_film_horizontal_tube.metadata = _METADATA.copy()

__all__ = ["h_nusselt_film_horizontal_tube"]
