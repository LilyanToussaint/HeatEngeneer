"""Kandlikar correlation for single-phase flow in microchannels."""
from __future__ import annotations


_METADATA = {
    "domain": "internal",  # flow inside channels
    "convection": "forced",  # single-phase forced convection
    "geometry": "microchannel",  # compact hydraulic diameter
}


def h_kandlikar_singlephase_microchannel(
    Re: float,
    Pr: float,
    k: float,
    d_h: float,
    L: float,
) -> float:
    """Return the convection coefficient for single-phase microchannels.

    The expression follows the widely used Kandlikar & Balasubramanian
    correlation for thermally and hydrodynamically developing laminar
    flows inside rectangular microchannels. *Re* is based on the
    hydraulic diameter *d_h* and mass-averaged velocity, *Pr* is the
    liquid Prandtl number, *k* the thermal conductivity of the fluid,
    and *L* the heated length.
    """

    if Re <= 0 or Pr <= 0:
        raise ValueError("Kandlikar microchannel (single-phase): Re et Pr doivent être > 0.")
    if d_h <= 0 or L <= 0:
        raise ValueError("Kandlikar microchannel (single-phase): d_h et L doivent être > 0.")

    if Re > 3000:
        raise ValueError("Kandlikar microchannel (single-phase): corrélation valable pour Re <= 3000.")

    gdz = Re * Pr * d_h / L
    Nu = 7.541 + (0.024 * gdz) / (1.0 + 0.035 * gdz ** 0.6666666667)
    return Nu * k / d_h


h_kandlikar_singlephase_microchannel.metadata = _METADATA.copy()


__all__ = ["h_kandlikar_singlephase_microchannel"]
