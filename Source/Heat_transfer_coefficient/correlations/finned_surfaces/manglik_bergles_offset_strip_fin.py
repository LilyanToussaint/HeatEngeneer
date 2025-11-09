"""Manglik & Bergles correlation for offset strip-fin surfaces."""

from typing import Optional


_METADATA = {
    "domain": "compact heat exchanger",
    "convection": "forced",
    "geometry": "offset strip fin",
}


def h_manglik_bergles_offset_strip_fin(
    Re: float,
    Pr: float,
    k: float,
    D_h: float,
    *,
    Pr_s: Optional[float] = None,
) -> float:
    """Return the Manglik & Bergles correlation for offset strip fins."""
    if Re <= 0.0 or Pr <= 0.0 or k <= 0.0 or D_h <= 0.0:
        raise ValueError("Manglik-Bergles: paramètres doivent être > 0.")

    Pr_s_val = Pr if Pr_s is None else Pr_s
    Nu = 0.0678 * (Re ** 0.718) * (Pr ** 0.333) * ((Pr / Pr_s_val) ** 0.14)
    return Nu * k / D_h


h_manglik_bergles_offset_strip_fin.metadata = _METADATA.copy()

__all__ = ["h_manglik_bergles_offset_strip_fin"]
