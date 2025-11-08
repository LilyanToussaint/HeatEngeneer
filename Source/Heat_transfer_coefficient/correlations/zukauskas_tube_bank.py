"""Zukauskas correlation for cross-flow over tube banks."""

from typing import Optional


_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "tube bank",
    "orientation": "crossflow",
}

_COEFFICIENTS = [
    (0.0, 1.0e2, 0.9, 0.4),
    (1.0e2, 1.0e3, 0.52, 0.5),
    (1.0e3, 2.0e5, 0.27, 0.63),
    (2.0e5, 2.0e6, 0.021, 0.84),
]


def h_zukauskas_tube_bank(
    Re: float,
    Pr: float,
    k: float,
    D: float,
    *,
    Pr_s: Optional[float] = None,
    n_rows: Optional[int] = None,
) -> float:
    """Return the average HTC for a tube bank using Zukauskas correlation."""
    if Re <= 0.0 or D <= 0.0:
        raise ValueError("Zukauskas: Re et diamètre doivent être > 0.")
    if not (0.7 <= Pr <= 500.0):
        raise ValueError("Zukauskas: Pr hors domaine (Pr).")

    C = m = None
    for Re_min, Re_max, c_val, m_val in _COEFFICIENTS:
        if Re_min <= Re < Re_max:
            C = c_val
            m = m_val
            break
    if C is None:
        raise ValueError("Zukauskas: Re hors domaine couvert par les coefficients.")

    Pr_s_val = Pr if Pr_s is None else Pr_s
    Nu = C * (Re ** m) * (Pr ** 0.36) * (Pr / Pr_s_val) ** 0.25

    if n_rows is not None and n_rows > 0 and n_rows < 20:
        Nu *= (n_rows / 20.0) ** 0.2

    return Nu * k / D


h_zukauskas_tube_bank.metadata = _METADATA.copy()

__all__ = ["h_zukauskas_tube_bank"]
