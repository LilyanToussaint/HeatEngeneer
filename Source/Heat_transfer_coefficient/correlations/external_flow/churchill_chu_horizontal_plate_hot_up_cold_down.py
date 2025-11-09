"""Churchill & Chu natural convection for horizontal plates (hot up / cold down)."""

_METADATA = {
    "domain": "external",
    "convection": "natural",
    "geometry": "horizontal plate",
    "orientation": "hot_up_cold_down",
}


def h_churchill_chu_horizontal_plate_hot_up_cold_down(Ra: float, k: float, L: float) -> float:
    """Return the average HTC for an upward-facing hot plate (or cold downward)."""
    if Ra <= 0.0 or L <= 0.0:
        raise ValueError("Churchill-Chu horizontal (hot up): Ra et longueur doivent être > 0.")

    if Ra < 1.0e7:
        Nu = 0.54 * (Ra ** 0.25)
    else:
        Nu = 0.15 * (Ra ** (1.0 / 3.0))
    return Nu * k / L


h_churchill_chu_horizontal_plate_hot_up_cold_down.metadata = _METADATA.copy()

__all__ = ["h_churchill_chu_horizontal_plate_hot_up_cold_down"]
