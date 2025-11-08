"""Prandtl number helper."""


def prandtl_number(dynamic_viscosity: float, heat_capacity: float, thermal_conductivity: float) -> float:
    """Compute the Prandtl number using μ c_p / k.

    Parameters
    ----------
    dynamic_viscosity:
        Dynamic viscosity in Pa·s.
    heat_capacity:
        Specific heat capacity at constant pressure in J/(kg·K).
    thermal_conductivity:
        Thermal conductivity in W/(m·K).

    Returns
    -------
    float
        The dimensionless Prandtl number.
    """
    if thermal_conductivity <= 0:
        raise ValueError("Thermal conductivity must be positive.")
    if heat_capacity <= 0:
        raise ValueError("Heat capacity must be positive.")
    return dynamic_viscosity * heat_capacity / thermal_conductivity


__all__ = ["prandtl_number"]
