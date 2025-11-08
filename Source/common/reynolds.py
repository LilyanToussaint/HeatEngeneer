"""Reynolds number helper."""


def reynolds_number(density: float, velocity: float, characteristic_length: float, dynamic_viscosity: float) -> float:
    """Compute the Reynolds number.

    Parameters
    ----------
    density:
        Fluid density in kg/m^3.
    velocity:
        Flow velocity in m/s.
    characteristic_length:
        Characteristic length scale (e.g., diameter) in meters.
    dynamic_viscosity:
        Dynamic viscosity in Pa·s.

    Returns
    -------
    float
        The dimensionless Reynolds number.
    """
    if dynamic_viscosity <= 0:
        raise ValueError("Dynamic viscosity must be positive.")
    return density * velocity * characteristic_length / dynamic_viscosity


__all__ = ["reynolds_number"]
