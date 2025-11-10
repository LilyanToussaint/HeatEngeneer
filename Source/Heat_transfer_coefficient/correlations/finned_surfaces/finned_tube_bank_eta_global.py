"""Global HTC for finned tube banks from fin efficiency."""
from __future__ import annotations


_METADATA = {
    "domain": "external",
    "convection": "forced",
    "geometry": "finned tube bank",
}


def h_finned_tube_bank_eta_global(
    h_external: float,
    eta_fin: float,
    A_fin: float,
    A_primary: float,
) -> float:
    """Combine fin efficiency and area fractions into an effective HTC."""

    if h_external <= 0:
        raise ValueError("Finned tube bank: h_external doit être > 0.")
    if not (0 <= eta_fin <= 1):
        raise ValueError("Finned tube bank: eta_fin doit être dans [0, 1].")
    if A_fin < 0 or A_primary <= 0:
        raise ValueError("Finned tube bank: surfaces doivent être positives.")

    A_total = A_fin + A_primary
    if A_total <= 0:
        raise ValueError("Finned tube bank: surface totale nulle.")

    effectiveness = (eta_fin * A_fin + A_primary) / A_total
    return h_external * effectiveness


h_finned_tube_bank_eta_global.metadata = _METADATA.copy()


__all__ = ["h_finned_tube_bank_eta_global"]
