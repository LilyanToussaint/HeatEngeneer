"""Churchill-Bernstein correlation for cylinders in cross-flow."""
from math import pow

_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "circular cylinder",
    "orientation": "crossflow",
}


def h_churchill_bernstein_cylinder_crossflow(
    Re: float, Pr: float, k: float, D: float
) -> float:
    """Return the average HTC using the Churchill-Bernstein correlation."""
    if Re <= 0.0 or D <= 0.0:
        raise ValueError("Churchill-Bernstein: Re et diamètre doivent être > 0.")
    if not (0.7 <= Pr <= 500.0):
        raise ValueError("Churchill-Bernstein: Pr hors domaine (Pr).")

    Nu = 0.3 + (
        0.62 * pow(Re, 0.5) * pow(Pr, 1.0 / 3.0)
        / pow(1.0 + (0.4 / Pr) ** (2.0 / 3.0), 0.25)
    ) * pow(1.0 + (Re / 282000.0) ** (5.0 / 8.0), 4.0 / 5.0)
    return Nu * k / D


h_churchill_bernstein_cylinder_crossflow.metadata = _METADATA.copy()

__all__ = ["h_churchill_bernstein_cylinder_crossflow"]
