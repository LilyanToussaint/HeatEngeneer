"""Prandtl number helper."""

from __future__ import annotations

from typing import Optional


def prandtl_number(
    *,
    dynamic_viscosity: Optional[float] = None,
    heat_capacity: Optional[float] = None,
    thermal_conductivity: Optional[float] = None,
    kinematic_viscosity: Optional[float] = None,
    thermal_diffusivity: Optional[float] = None,
) -> float:
    """Compute the Prandtl number.

    Two common formulations are supported:

    - ``μ c_p / k`` using dynamic viscosity, specific heat capacity, and thermal
      conductivity.
    - ``ν / α`` using kinematic viscosity and thermal diffusivity.

    Parameters
    ----------
    dynamic_viscosity:
        Dynamic viscosity in Pa·s. Required together with ``heat_capacity`` and
        ``thermal_conductivity`` when using the ``μ c_p / k`` definition.
    heat_capacity:
        Specific heat capacity at constant pressure in J/(kg·K).
    thermal_conductivity:
        Thermal conductivity in W/(m·K).
    kinematic_viscosity:
        Kinematic viscosity ``ν`` in m²/s.
    thermal_diffusivity:
        Thermal diffusivity ``α`` in m²/s.

    Returns
    -------
    float
        The dimensionless Prandtl number.
    """

    using_mu = dynamic_viscosity is not None
    using_nu = kinematic_viscosity is not None or thermal_diffusivity is not None

    if using_mu and using_nu:
        raise ValueError("Provide either dynamic-viscosity inputs or kinematic/diffusivity inputs, not both.")

    if using_mu:
        if heat_capacity is None or thermal_conductivity is None:
            raise ValueError("Heat capacity and thermal conductivity are required with dynamic viscosity.")
        if dynamic_viscosity <= 0:
            raise ValueError("Dynamic viscosity must be positive.")
        if heat_capacity <= 0:
            raise ValueError("Heat capacity must be positive.")
        if thermal_conductivity <= 0:
            raise ValueError("Thermal conductivity must be positive.")
        return dynamic_viscosity * heat_capacity / thermal_conductivity

    if using_nu:
        if kinematic_viscosity is None or thermal_diffusivity is None:
            raise ValueError("Both kinematic viscosity and thermal diffusivity are required for ν/α formulation.")
        if kinematic_viscosity <= 0:
            raise ValueError("Kinematic viscosity must be positive.")
        if thermal_diffusivity <= 0:
            raise ValueError("Thermal diffusivity must be positive.")
        return kinematic_viscosity / thermal_diffusivity

    raise ValueError(
        "Insufficient inputs for Prandtl number: provide either (dynamic_viscosity, heat_capacity, thermal_conductivity) "
        "or (kinematic_viscosity, thermal_diffusivity)."
    )


__all__ = ["prandtl_number"]
