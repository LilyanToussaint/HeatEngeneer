"""Array jet impingement correlation for single-phase cooling."""
from __future__ import annotations


_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "jet array impingement",
}


def h_array_jet_impingement(
    Re: float,
    Pr: float,
    k: float,
    d_j: float,
    H: float,
    s: float,
    configuration: str = "inline",
) -> float:
    """Return the area-averaged HTC for an array of impinging jets.

    The expression is adapted from the Florschuetz & Truman (1985)
    formulation. *configuration* is either ``"inline"`` or
    ``"staggered"``.
    """

    if Re <= 2000:
        raise ValueError("Jet array: la corrélation suppose Re > 2000.")
    if Pr <= 0:
        raise ValueError("Jet array: Pr doit être > 0.")
    if min(d_j, H, s) <= 0:
        raise ValueError("Jet array: dimensions doivent être > 0.")

    phi_h = (H / d_j) ** -0.2
    phi_s = (s / d_j) ** -0.3

    if configuration not in {"inline", "staggered"}:
        raise ValueError("Jet array: configuration doit être 'inline' ou 'staggered'.")

    c = 0.6 if configuration == "inline" else 0.65
    Nu = c * Re ** 0.7 * Pr ** (1.0 / 3.0) * phi_h * phi_s
    return Nu * k / d_j


h_array_jet_impingement.metadata = _METADATA.copy()


__all__ = ["h_array_jet_impingement"]
