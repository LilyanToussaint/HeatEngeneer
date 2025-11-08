"""Empirical correlation for sinusoidal wavy fins."""
from __future__ import annotations


_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "compact exchanger wavy fin",
}


def h_wavy_fin_correlation(
    Re: float,
    Pr: float,
    k: float,
    D_h: float,
    wave_amplitude_ratio: float = 0.1,
    wave_length_ratio: float = 1.0,
) -> float:
    """Return the HTC for wavy fins using a Manglik & Bergles style fit."""

    if Re <= 0 or Pr <= 0:
        raise ValueError("Wavy fin: Re et Pr doivent être > 0.")
    if D_h <= 0 or wave_amplitude_ratio <= 0 or wave_length_ratio <= 0:
        raise ValueError("Wavy fin: paramètres géométriques doivent être > 0.")

    phi = (wave_amplitude_ratio / wave_length_ratio) ** 0.2
    Nu = 0.086 * Re ** 0.7 * Pr ** (1.0 / 3.0) * phi
    return Nu * k / D_h


h_wavy_fin_correlation.metadata = _METADATA.copy()


__all__ = ["h_wavy_fin_correlation"]
