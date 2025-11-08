"""Annular fin efficiency with adiabatic tip (approximate)."""
from math import sqrt, tanh

_METADATA = {
    "domain": "extended surfaces",
    "convection": "fin",
    "geometry": "annular fin",
}


def eta_fin_annular(
    h: float,
    k_fin: float,
    thickness: float,
    r_i: float,
    r_o: float,
) -> float:
    """Return an approximate efficiency for a constant-thickness annular fin."""
    if any(param <= 0.0 for param in (h, k_fin, thickness, r_i, r_o)):
        raise ValueError("Annular fin: paramètres doivent être > 0.")
    if r_o <= r_i:
        raise ValueError("Annular fin: r_o doit être > r_i.")

    L = r_o - r_i
    m = sqrt(2.0 * h / (k_fin * thickness))
    mL = m * L
    if mL == 0.0:
        return 1.0
    return tanh(mL) / mL


eta_fin_annular.metadata = _METADATA.copy()

__all__ = ["eta_fin_annular"]
