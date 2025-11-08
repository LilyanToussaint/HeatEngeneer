"""Convert hydraulic head to pressure drop."""
from __future__ import annotations

from math import isfinite

__all__ = ["convert_head_to_dp"]

_GRAVITY = 9.80665


def convert_head_to_dp(head_m: float, density: float, gravity: float = _GRAVITY) -> float:
    """Return the pressure equivalent of a hydraulic head (m of fluid)."""

    for name, value in {"h": head_m, "rho": density, "g": gravity}.items():
        if not isfinite(value):
            raise ValueError(f"convert_head_to_dp: '{name}' doit être fini.")

    if head_m < 0 or density <= 0 or gravity <= 0:
        raise ValueError("convert_head_to_dp: paramètres physiques invalides.")

    return density * gravity * head_m


convert_head_to_dp.metadata = {
    "quantity": "pressure_drop",
    "type": "conversion",
}
