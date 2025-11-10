"""Sieder-Tate correlation for turbulent internal flow with property variation."""
from math import pow

_METADATA = {
    "domain": "internal",
    "convection": "forced",
    "geometry": "smooth circular tube",
    "regime": "turbulent",
}


def h_sieder_tate_internal(
    Re: float,
    Pr: float,
    k: float,
    d_i: float,
    mu: float,
    mu_w: float,
) -> float:
    """Return the convection coefficient from the Sieder-Tate correlation.

    Parameters
    ----------
    Re:
        Reynolds number based on the inner diameter.
    Pr:
        Prandtl number evaluated at bulk conditions.
    k:
        Thermal conductivity of the fluid [W/m/K].
    d_i:
        Inner diameter of the tube [m].
    mu:
        Dynamic viscosity of the fluid at bulk temperature [Pa*s].
    mu_w:
        Dynamic viscosity at the wall temperature [Pa*s].
    """
    if Re <= 1.0e4:
        raise ValueError("Sieder-Tate: Re trop faible.")
    if not (0.6 <= Pr <= 1000.0):
        raise ValueError("Sieder-Tate: Pr hors domaine (Pr).")
    if mu <= 0.0 or mu_w <= 0.0:
        raise ValueError("Sieder-Tate: viscosités doivent être > 0.")

    nu = 0.027 * pow(Re, 0.8) * pow(Pr, 1.0 / 3.0) * pow(mu / mu_w, 0.14)
    return nu * k / d_i


h_sieder_tate_internal.metadata = _METADATA.copy()

__all__ = ["h_sieder_tate_internal"]
