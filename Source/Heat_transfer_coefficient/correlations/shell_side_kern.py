"""Kern method correlation for shell-side convection in shell-and-tube exchangers."""

_METADATA = {
    "domain": "shell-and-tube",
    "convection": "forced",
    "geometry": "shell side",
}


def h_shell_side_kern(
    Re_s: float,
    Pr: float,
    k: float,
    D_e: float,
) -> float:
    """Return the shell-side HTC using Kern's simplified correlation."""
    if any(param <= 0.0 for param in (Re_s, Pr, k, D_e)):
        raise ValueError("Kern: paramètres doivent être > 0.")

    j_h = 0.36 / (Re_s ** 0.55)
    Nu = j_h * Re_s * (Pr ** (1.0 / 3.0))
    return Nu * k / D_e


h_shell_side_kern.metadata = _METADATA.copy()

__all__ = ["h_shell_side_kern"]
