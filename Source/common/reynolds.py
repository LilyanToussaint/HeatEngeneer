"""Reynolds number helper."""

from __future__ import annotations

from typing import Optional


def reynolds_number(
    characteristic_length: float,
    dynamic_viscosity: Optional[float] = None,
    *,
    density: Optional[float] = None,
    velocity: Optional[float] = None,
    mass_flow_rate: Optional[float] = None,
    area: Optional[float] = None,
    mass_flux: Optional[float] = None,
    kinematic_viscosity: Optional[float] = None,
) -> float:
    """Compute the Reynolds number.

    The helper supports multiple input combinations commonly encountered in
    heat-transfer calculations:

    - ``density`` + ``velocity`` (classical definition ``ρ V L / μ``)
    - ``mass_flow_rate`` + ``area`` (uses the mass flux ``G = ṁ / A``)
    - ``mass_flux`` directly (already equal to ``ρ V``)
    - ``velocity`` + ``kinematic_viscosity`` (``V L / ν``)

    Parameters
    ----------
    characteristic_length:
        Characteristic length scale (e.g., diameter) in meters.
    dynamic_viscosity:
        Dynamic viscosity in Pa·s. Required unless ``kinematic_viscosity`` is
        provided.
    density, velocity:
        Density [kg/m³] and bulk velocity [m/s]. Both must be supplied
        together when using the classical formula.
    mass_flow_rate, area:
        Mass-flow rate [kg/s] and associated flow area [m²]. Both must be
        supplied together. The helper internally derives the mass flux ``G``.
    mass_flux:
        Directly provide the mass flux ``G`` [kg/(m²·s)] when available.
    kinematic_viscosity:
        Kinematic viscosity ``ν`` [m²/s]. When supplied alongside ``velocity``
        the Reynolds number is computed as ``V L / ν``.

    Returns
    -------
    float
        The dimensionless Reynolds number.
    """

    if characteristic_length <= 0:
        raise ValueError("Characteristic length must be positive.")

    if dynamic_viscosity is not None and dynamic_viscosity <= 0:
        raise ValueError("Dynamic viscosity must be positive when provided.")

    if kinematic_viscosity is not None and kinematic_viscosity <= 0:
        raise ValueError("Kinematic viscosity must be positive when provided.")

    mass_flux_value: Optional[float] = None

    if mass_flux is not None:
        if mass_flux <= 0:
            raise ValueError("Mass flux must be positive.")
        mass_flux_value = mass_flux
    elif mass_flow_rate is not None:
        if mass_flow_rate <= 0:
            raise ValueError("Mass-flow rate must be positive.")
        if area is None:
            raise ValueError("Flow area must be provided with mass-flow rate.")
        if area <= 0:
            raise ValueError("Flow area must be positive.")
        mass_flux_value = mass_flow_rate / area
    elif density is not None and velocity is not None:
        if density <= 0:
            raise ValueError("Density must be positive when provided.")
        if velocity < 0:
            raise ValueError("Velocity must be non-negative when provided.")
        mass_flux_value = density * velocity
    elif velocity is not None and kinematic_viscosity is not None:
        # Velocity combined with kinematic viscosity: Re = V * L / ν
        return velocity * characteristic_length / kinematic_viscosity
    else:
        raise ValueError(
            "Insufficient inputs for Reynolds number: provide either (density and velocity), "
            "(mass_flow_rate and area), mass_flux, or (velocity and kinematic_viscosity)."
        )

    if mass_flux_value is None:
        raise ValueError("Unable to determine mass flux for Reynolds number calculation.")

    if dynamic_viscosity is None:
        raise ValueError(
            "Dynamic viscosity must be provided unless using velocity with kinematic viscosity."
        )

    return mass_flux_value * characteristic_length / dynamic_viscosity


__all__ = ["reynolds_number"]
