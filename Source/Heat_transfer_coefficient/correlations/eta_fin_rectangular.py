"""Rectangular straight fin efficiency for adiabatic tip."""
from math import sqrt, tanh

_METADATA = {
    "domain": "extended surfaces",
    "convection": "fin",
    "geometry": "rectangular straight fin",
}


def eta_fin_rectangular(
    h: float,
    k_fin: float,
    length: float,
    perimeter: float,
    area_cross: float,
) -> float:
    """Return the efficiency of a straight rectangular fin with adiabatic tip."""
    if any(param <= 0.0 for param in (h, k_fin, length, perimeter, area_cross)):
        raise ValueError("Rectangular fin: paramètres doivent être > 0.")

    m = sqrt(h * perimeter / (k_fin * area_cross))
    mL = m * length
    if mL == 0.0:
        return 1.0
    return tanh(mL) / mL


eta_fin_rectangular.metadata = _METADATA.copy()

__all__ = ["eta_fin_rectangular"]
