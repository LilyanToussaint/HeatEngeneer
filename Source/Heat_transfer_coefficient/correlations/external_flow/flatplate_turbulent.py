"""Colburn/Chilton-Colburn correlation for turbulent flat-plate flow."""

_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "flat plate",
    "regime": "turbulent",
}


def h_flatplate_turbulent(Re_L: float, Pr: float, k: float, L: float) -> float:
    """Return the average HTC over a flat plate for turbulent flow."""
    if Re_L <= 5.0e5:
        raise ValueError("Flat plate turbulent: Re_L doit être > 5e5.")
    if L <= 0.0:
        raise ValueError("Flat plate turbulent: longueur doit être > 0.")
    if not (0.6 <= Pr <= 60.0):
        raise ValueError("Flat plate turbulent: Pr hors domaine (Pr).")

    Nu = (0.037 * (Re_L ** 0.8) - 871.0) * (Pr ** (1.0 / 3.0))
    if Nu <= 0.0:
        raise ValueError("Flat plate turbulent: Nu calculé <= 0, vérifier les paramètres.")
    return Nu * k / L


h_flatplate_turbulent.metadata = _METADATA.copy()

__all__ = ["h_flatplate_turbulent"]
