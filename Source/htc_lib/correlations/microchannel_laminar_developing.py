"""Correlation for laminar thermally developing microchannel flows."""
from __future__ import annotations


_METADATA = {
    "domain": "internal",
    "convection": "forced",
    "geometry": "microchannel",
}


def h_microchannel_laminar_developing(
    Re: float,
    Pr: float,
    k: float,
    d_h: float,
    L: float,
) -> float:
    """Return the convection coefficient for laminar, developing flow.

    This is the compact channel adaptation of the Hausen expression,
    often used for laminar flow with thermal development in small
    hydraulic-diameter passages.
    """

    if Re <= 0 or Pr <= 0:
        raise ValueError("Microchannel laminaire: Re et Pr doivent être > 0.")
    if d_h <= 0 or L <= 0:
        raise ValueError("Microchannel laminaire: d_h et L doivent être > 0.")
    if Re >= 2300:
        raise ValueError("Microchannel laminaire: la corrélation suppose Re < 2300.")

    gdz = Re * Pr * d_h / L
    Nu = 3.66 + (0.0668 * gdz) / (1.0 + 0.04 * gdz ** (2.0 / 3.0))
    return Nu * k / d_h


h_microchannel_laminar_developing.metadata = _METADATA.copy()


__all__ = ["h_microchannel_laminar_developing"]
