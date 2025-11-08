"""Compute the effective HTC of a finned surface."""

_METADATA = {
    "domain": "extended surfaces",
    "convection": "fin",
    "geometry": "finned surface",
}


def h_effective_finned_surface(
    h_local: float,
    eta_fin: float,
    area_fin: float,
    area_unfinned: float,
) -> float:
    """Return the area-averaged HTC of a finned surface."""
    if any(param < 0.0 for param in (h_local, eta_fin, area_fin, area_unfinned)):
        raise ValueError("Surface ailetée: paramètres doivent être >= 0.")
    if h_local <= 0.0:
        raise ValueError("Surface ailetée: h_local doit être > 0.")
    if eta_fin < 0.0 or eta_fin > 1.0:
        raise ValueError("Surface ailetée: eta_fin doit être entre 0 et 1.")

    A_total = area_fin + area_unfinned
    if A_total <= 0.0:
        raise ValueError("Surface ailetée: surface totale doit être > 0.")

    effective_h = h_local * (eta_fin * area_fin + area_unfinned) / A_total
    return effective_h


h_effective_finned_surface.metadata = _METADATA.copy()

__all__ = ["h_effective_finned_surface"]
