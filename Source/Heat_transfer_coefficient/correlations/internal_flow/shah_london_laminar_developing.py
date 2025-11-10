"""Shah & London correlation for simultaneously developing laminar tube flow."""

_METADATA = {
    "domain": "internal",
    "convection": "forced",
    "geometry": "smooth circular tube",
    "regime": "laminar developing",
}


def h_shah_london_laminar_developing(
    Re: float,
    Pr: float,
    k: float,
    d_i: float,
    L: float,
) -> float:
    """Return the Shah & London average convection coefficient.

    Valid for hydrodynamically and thermally developing laminar flow with constant wall
    temperature. Requires Graetz number between roughly 0.1 and 10^4.
    """
    if not (0.6 <= Pr <= 1000.0):
        raise ValueError("Shah & London: Pr hors domaine (Pr).")
    if Re >= 2300.0:
        raise ValueError("Shah & London: Re doit être laminaire (<2300).")
    if d_i <= 0.0 or L <= 0.0:
        raise ValueError("Shah & London: dimensions doivent être > 0.")

    graetz = Re * Pr * d_i / L
    if graetz <= 0.0:
        raise ValueError("Shah & London: nombre de Graetz doit être > 0.")

    term = (0.065 * graetz) / (1.0 + 0.04 * graetz ** (2.0 / 3.0))
    nu = 3.66 + term
    return nu * k / d_i


h_shah_london_laminar_developing.metadata = _METADATA.copy()

__all__ = ["h_shah_london_laminar_developing"]
