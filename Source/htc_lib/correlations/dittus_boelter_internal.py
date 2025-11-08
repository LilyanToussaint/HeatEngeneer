"""Dittus-Boelter correlation for turbulent internal flow in smooth tubes."""


def h_dittus_boelter_internal(
    Re: float, Pr: float, k: float, d_i: float, *, heating: bool = True
) -> float:
    """Return the convection coefficient using the Dittus-Boelter correlation."""
    if Re <= 1e4:
        raise ValueError("Dittus-Boelter: Re trop faible.")
    if not (0.7 <= Pr <= 160):
        raise ValueError("Dittus-Boelter: Pr hors domaine (Pr).")

    n = 0.4 if heating else 0.3
    Nu = 0.023 * Re ** 0.8 * Pr ** n
    return Nu * k / d_i


__all__ = ["h_dittus_boelter_internal"]
