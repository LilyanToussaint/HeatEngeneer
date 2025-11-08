"""Hausen correlation for thermally developing laminar flow in tubes."""

_METADATA = {
    "domain": "internal",
    "convection": "forced",
    "geometry": "smooth circular tube",
    "regime": "laminar developing",
}


def h_hausen_laminar_developing(
    Re: float,
    Pr: float,
    k: float,
    d_i: float,
    L: float,
) -> float:
    """Return the average convection coefficient from the Hausen correlation.

    The correlation is valid for laminar flow with uniform wall temperature or heat flux.
    """
    if not (0.6 <= Pr <= 500.0):
        raise ValueError("Hausen: Pr hors domaine (Pr).")
    if Re >= 2300.0:
        raise ValueError("Hausen: Re doit être laminaire (<2300).")
    if d_i <= 0.0 or L <= 0.0:
        raise ValueError("Hausen: dimensions doivent être > 0.")

    graetz = Re * Pr * d_i / L
    nu = 3.66 + (0.0668 * graetz) / (1.0 + 0.04 * graetz ** (2.0 / 3.0))
    return nu * k / d_i


h_hausen_laminar_developing.metadata = _METADATA.copy()

__all__ = ["h_hausen_laminar_developing"]
