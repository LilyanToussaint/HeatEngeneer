"""Chen-type boiling two-phase pressure-drop correlation."""
from __future__ import annotations

from math import isfinite

__all__ = ["dp_hev_chen_boiling"]


def dp_hev_chen_boiling(
    reynolds_liquid: float,
    quality: float,
    dp_liquid_only: float | None = None,
) -> float:
    """Return a simplified Chen boiling multiplier or pressure drop."""

    if not isfinite(reynolds_liquid) or reynolds_liquid <= 0:
        raise ValueError("dp_hev_chen_boiling: Re_l doit être > 0 et fini.")
    if not isfinite(quality) or not 0.0 <= quality <= 1.0:
        raise ValueError("dp_hev_chen_boiling: x doit être dans [0, 1].")

    enhancement = 1.0 + 2.4 * quality**0.8 * reynolds_liquid ** -0.1

    if dp_liquid_only is not None:
        if dp_liquid_only <= 0:
            raise ValueError("dp_hev_chen_boiling: dp_liquid_only doit être > 0.")
        return enhancement * dp_liquid_only

    return enhancement


dp_hev_chen_boiling.metadata = {
    "flow_domain": "two_phase",
    "model": "chen",
    "quantity": "pressure_drop_or_multiplier",
}
