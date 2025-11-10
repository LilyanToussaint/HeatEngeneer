"""Churchill & Chu correlation for natural convection over horizontal cylinders."""

_METADATA = {
    "domain": "external",
    "convection": "natural",
    "geometry": "horizontal cylinder",
}


def h_churchill_chu_horizontal_cylinder(
    Ra: float, Pr: float, k: float, D: float
) -> float:
    """Return the average HTC using Churchill & Chu's horizontal-cylinder correlation."""
    if Ra <= 0.0 or D <= 0.0:
        raise ValueError("Churchill-Chu cylindre: Ra et diamètre doivent être > 0.")
    if Pr <= 0.0:
        raise ValueError("Churchill-Chu cylindre: Pr doit être > 0.")

    Nu = (
        0.60
        + 0.387 * Ra ** (1.0 / 6.0)
        / (1.0 + (0.559 / Pr) ** (9.0 / 16.0)) ** (8.0 / 27.0)
    ) ** 2
    return Nu * k / D


h_churchill_chu_horizontal_cylinder.metadata = _METADATA.copy()

__all__ = ["h_churchill_chu_horizontal_cylinder"]
