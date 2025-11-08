"""Blasius-type laminar flat-plate forced-convection correlation."""

_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "flat plate",
    "regime": "laminar",
}


def h_flatplate_laminar(Re_L: float, Pr: float, k: float, L: float) -> float:
    """Return the average HTC over a flat plate for laminar flow."""
    if Re_L <= 0.0 or L <= 0.0:
        raise ValueError("Flat plate laminaire: Re_L et longueur doivent être > 0.")
    if Re_L >= 5.0e5:
        raise ValueError("Flat plate laminaire: Re_L doit rester < 5e5.")
    if not (0.6 <= Pr <= 60.0):
        raise ValueError("Flat plate laminaire: Pr hors domaine (Pr).")

    Nu = 0.664 * (Re_L ** 0.5) * (Pr ** (1.0 / 3.0))
    return Nu * k / L


h_flatplate_laminar.metadata = _METADATA.copy()

__all__ = ["h_flatplate_laminar"]
