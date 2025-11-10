"""Single-phase circular jet impingement correlation."""
from __future__ import annotations


_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "single circular jet impingement",
}


def h_circular_jet_impingement_singlephase(
    Re: float,
    Pr: float,
    k: float,
    d_j: float,
    H: float,
) -> float:
    """Return the average stagnation-region HTC for a circular jet.

    The implementation follows Martin's correlation (1977) with a
    moderate correction for the nozzle-to-target spacing *H*. Valid for
    turbulent jets impinging normally on a flat plate.
    """

    if Re <= 2000:
        raise ValueError("Jet circulaire: la corrélation suppose Re > 2000 (turbulent).")
    if Pr <= 0:
        raise ValueError("Jet circulaire: Pr doit être > 0.")
    if d_j <= 0 or H <= 0:
        raise ValueError("Jet circulaire: d_j et H doivent être > 0.")

    z = H / d_j
    if not (2.0 <= z <= 12.0):
        raise ValueError("Jet circulaire: la corrélation vaut pour 2 <= H/D <= 12.")

    Nu = 0.5 * Re ** 0.5 * Pr ** (1.0 / 3.0) * z ** -0.1
    return Nu * k / d_j


h_circular_jet_impingement_singlephase.metadata = _METADATA.copy()


__all__ = ["h_circular_jet_impingement_singlephase"]
