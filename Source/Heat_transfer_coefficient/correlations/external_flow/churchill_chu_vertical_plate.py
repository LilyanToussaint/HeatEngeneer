"""Churchill & Chu correlation for natural convection on vertical plates."""

_METADATA = {
    "domain": "external",
    "convection": "natural",
    "geometry": "vertical plate",
}


def h_churchill_chu_vertical_plate(Ra: float, Pr: float, k: float, L: float) -> float:
    """Return the average HTC using Churchill & Chu's vertical-plate correlation."""
    if Ra <= 0.0 or L <= 0.0:
        raise ValueError("Churchill-Chu vertical: Ra et longueur doivent être > 0.")
    if Pr <= 0.0:
        raise ValueError("Churchill-Chu vertical: Pr doit être > 0.")

    Nu = (
        0.825
        + 0.387 * Ra ** (1.0 / 6.0)
        / (1.0 + (0.492 / Pr) ** (9.0 / 16.0)) ** (8.0 / 27.0)
    ) ** 2
    return Nu * k / L


h_churchill_chu_vertical_plate.metadata = _METADATA.copy()

__all__ = ["h_churchill_chu_vertical_plate"]
