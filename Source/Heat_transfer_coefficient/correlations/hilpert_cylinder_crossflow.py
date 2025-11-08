"""Hilpert correlation for cylinders in cross-flow."""

_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "circular cylinder",
    "orientation": "crossflow",
}


_COEFFICIENTS = [
    (0.4, 4.0, 0.989, 0.33),
    (4.0, 40.0, 0.911, 0.385),
    (40.0, 4000.0, 0.683, 0.466),
    (4000.0, 40000.0, 0.193, 0.618),
    (40000.0, 400000.0, 0.027, 0.805),
    (400000.0, 4000000.0, 0.026, 0.805),
]


def h_hilpert_cylinder_crossflow(Re: float, Pr: float, k: float, D: float) -> float:
    """Return the average HTC using the Hilpert correlation."""
    if Re <= 0.0 or D <= 0.0:
        raise ValueError("Hilpert: Re et diamètre doivent être > 0.")
    if not (0.7 <= Pr <= 500.0):
        raise ValueError("Hilpert: Pr hors domaine (Pr).")

    C = m = None
    for Re_min, Re_max, c_val, m_val in _COEFFICIENTS:
        if Re_min <= Re < Re_max:
            C = c_val
            m = m_val
            break
    if C is None:
        raise ValueError("Hilpert: Re hors domaine couvert par les coefficients.")

    Nu = C * (Re ** m) * (Pr ** (1.0 / 3.0))
    return Nu * k / D


h_hilpert_cylinder_crossflow.metadata = _METADATA.copy()

__all__ = ["h_hilpert_cylinder_crossflow"]
