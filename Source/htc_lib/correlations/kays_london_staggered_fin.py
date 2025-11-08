"""Kays & London style correlation for staggered fin surfaces."""

_METADATA = {
    "domain": "compact heat exchanger",
    "convection": "forced",
    "geometry": "staggered fin",
}


def h_kays_london_staggered_fin(
    Re: float,
    Pr: float,
    k: float,
    D_h: float,
    *,
    Pr_s: float | None = None,
) -> float:
    """Return an approximate HTC for staggered fins using Kays & London data."""
    if Re <= 0.0 or Pr <= 0.0 or k <= 0.0 or D_h <= 0.0:
        raise ValueError("Kays-London: paramètres doivent être > 0.")

    Pr_s_val = Pr if Pr_s is None else Pr_s
    Nu = 0.086 * (Re ** 0.8) * (Pr ** 0.3) * ((Pr / Pr_s_val) ** 0.25)
    return Nu * k / D_h


h_kays_london_staggered_fin.metadata = _METADATA.copy()

__all__ = ["h_kays_london_staggered_fin"]
