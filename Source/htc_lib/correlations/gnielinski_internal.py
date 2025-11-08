"""Gnielinski correlation for turbulent internal flow in smooth tubes."""


def h_gnielinski_internal(Re: float, Pr: float, k: float, d_i: float) -> float:
    """Return the convection coefficient using the Gnielinski correlation."""
    if not (3e3 <= Re <= 5e6):
        raise ValueError("Gnielinski: Re hors domaine (Re).")
    if not (0.5 <= Pr <= 2000):
        raise ValueError("Gnielinski: Pr hors domaine (Pr).")

    f = (0.79 * Re ** -0.25 - 0.64) ** 2
    Nu = (f / 8.0) * (Re - 1000.0) * Pr / (
        1.0 + 12.7 * (f / 8.0) ** 0.5 * (Pr ** (2.0 / 3.0) - 1.0)
    )
    return Nu * k / d_i


__all__ = ["h_gnielinski_internal"]
