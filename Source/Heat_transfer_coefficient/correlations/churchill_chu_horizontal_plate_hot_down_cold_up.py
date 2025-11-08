"""Churchill & Chu natural convection for horizontal plates (hot down / cold up)."""

_METADATA = {
    "domain": "external",
    "convection": "natural",
    "geometry": "horizontal plate",
    "orientation": "hot_down_cold_up",
}


def h_churchill_chu_horizontal_plate_hot_down_cold_up(Ra: float, k: float, L: float) -> float:
    """Return HTC for a downward-facing hot surface (or cold upward)."""
    if Ra <= 0.0 or L <= 0.0:
        raise ValueError(
            "Churchill-Chu horizontal (hot down): Ra et longueur doivent être > 0."
        )

    Nu = 0.27 * (Ra ** 0.25)
    return Nu * k / L


h_churchill_chu_horizontal_plate_hot_down_cold_up.metadata = _METADATA.copy()

__all__ = ["h_churchill_chu_horizontal_plate_hot_down_cold_up"]
