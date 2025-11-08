"""Wakao & Kaguei correlation for convection in packed beds."""

_METADATA = {
    "domain": "packed bed",
    "convection": "forced",
    "geometry": "packed particles",
}


def h_packed_bed_wakao(
    Re_p: float,
    Pr: float,
    k: float,
    d_p: float,
) -> float:
    """Return the Wakao & Kaguei HTC for packed beds."""
    if any(param <= 0.0 for param in (Re_p, Pr, k, d_p)):
        raise ValueError("Wakao: paramètres doivent être > 0.")

    Nu = 2.0 + 1.1 * (Re_p ** 0.6) * (Pr ** (1.0 / 3.0))
    return Nu * k / d_p


h_packed_bed_wakao.metadata = _METADATA.copy()

__all__ = ["h_packed_bed_wakao"]
