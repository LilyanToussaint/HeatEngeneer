"""Nusselt laminar-film condensation on vertical plates."""

_METADATA = {
    "domain": "condensation",
    "convection": "film",
    "geometry": "vertical plate",
}

_G = 9.80665


def h_nusselt_film_vertical_plate(
    delta_T: float,
    rho_l: float,
    rho_v: float,
    mu_l: float,
    k_l: float,
    h_fg: float,
    L: float,
) -> float:
    """Return the Nusselt laminar-film condensation HTC for a vertical plate."""
    if any(param <= 0.0 for param in (delta_T, rho_l, rho_v, mu_l, k_l, h_fg, L)):
        raise ValueError("Nusselt vertical: paramètres doivent être > 0.")

    term = (
        rho_l * (rho_l - rho_v) * _G * h_fg * (k_l ** 3)
        / (mu_l * L * delta_T)
    )
    return 0.943 * (term ** 0.25)


h_nusselt_film_vertical_plate.metadata = _METADATA.copy()

__all__ = ["h_nusselt_film_vertical_plate"]
