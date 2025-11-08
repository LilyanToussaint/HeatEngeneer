"""Implicit Colebrook-White turbulent friction-factor correlation."""
from __future__ import annotations

from math import isfinite, log10, sqrt

__all__ = ["f_colebrook_white"]


def f_colebrook_white(
    reynolds: float,
    relative_roughness: float,
    initial_guess: float | None = None,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> float:
    """Solve the Colebrook-White equation for the Darcy friction factor."""

    for name, value in {
        "Re": reynolds,
        "eD": relative_roughness,
        "tol": tol,
    }.items():
        if not isfinite(value):
            raise ValueError(f"f_colebrook_white: '{name}' doit être fini.")

    if reynolds <= 0:
        raise ValueError("f_colebrook_white: Re doit être positif.")
    if relative_roughness < 0:
        raise ValueError("f_colebrook_white: e/D doit être positif ou nul.")
    if tol <= 0:
        raise ValueError("f_colebrook_white: la tolérance doit être positive.")
    if max_iter <= 0:
        raise ValueError("f_colebrook_white: max_iter doit être positif.")

    if initial_guess is None:
        from .f_haaland import f_haaland

        initial_guess = f_haaland(max(reynolds, 3.0e3), relative_roughness)

    if not isfinite(initial_guess) or initial_guess <= 0:
        raise ValueError("f_colebrook_white: initial_guess doit être > 0 et fini.")

    friction = initial_guess
    for _ in range(max_iter):
        lhs = -2.0 * log10(
            relative_roughness / 3.7 + 2.51 / (reynolds * sqrt(friction))
        )
        friction_new = 1.0 / (lhs * lhs)
        if abs(friction_new - friction) < tol:
            return friction_new
        friction = 0.5 * (friction + friction_new)

    raise ValueError("f_colebrook_white: convergence non atteinte.")


f_colebrook_white.metadata = {
    "flow_domain": "internal",
    "regime": "turbulent",
    "geometry": "circular_duct",
    "phase": "single-phase",
    "quantity": "darcy_friction_factor",
    "roughness": "general",
    "solver": "colebrook-white",
}
