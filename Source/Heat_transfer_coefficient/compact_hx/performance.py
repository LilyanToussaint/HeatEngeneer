"""Helper to evaluate compact heat-exchanger performance from j/f correlations."""
from __future__ import annotations

from typing import Callable, Dict, Mapping

from ..correlations.j_colburn_to_h import j_colburn_to_h
from ..correlations.fanning_f_to_dp import fanning_f_to_dp
from ...common import reynolds_number


GeometryMapping = Mapping[str, float]
FluidMapping = Mapping[str, float]


def hx_compact_performance(
    geometry: GeometryMapping,
    fluid: FluidMapping,
    mass_flow: float,
    j_correlation: Callable[[float], float],
    f_correlation: Callable[[float], float],
) -> Dict[str, float]:
    """Return key performance indicators for a compact heat exchanger.

    Parameters
    ----------
    geometry:
        Mapping containing at least ``flow_area`` [m²], ``surface_area`` [m²],
        ``hydraulic_diameter`` [m] and ``length`` [m].
    fluid:
        Mapping containing ``rho`` [kg/m³], ``mu`` [Pa·s], ``cp`` [J/kg/K],
        ``k`` [W/m/K] and ``Pr`` [-].
    mass_flow:
        Mass-flow rate through the core [kg/s].
    j_correlation, f_correlation:
        Callables returning the Colburn *j* factor and the Fanning friction
        factor given a Reynolds number.
    """

    required_geom = {"flow_area", "surface_area", "hydraulic_diameter", "length"}
    missing_geom = required_geom - geometry.keys()
    if missing_geom:
        raise ValueError(f"hx_compact_performance: géométrie incomplète: {missing_geom}.")

    required_fluid = {"rho", "mu", "cp", "k", "Pr"}
    missing_fluid = required_fluid - fluid.keys()
    if missing_fluid:
        raise ValueError(f"hx_compact_performance: propriétés fluides manquantes: {missing_fluid}.")

    flow_area = geometry["flow_area"]
    hydraulic_diameter = geometry["hydraulic_diameter"]

    if mass_flow <= 0:
        raise ValueError("hx_compact_performance: débit massique doit être > 0.")
    if flow_area <= 0:
        raise ValueError("hx_compact_performance: surface d'écoulement doit être > 0.")
    if hydraulic_diameter <= 0:
        raise ValueError("hx_compact_performance: diamètre hydraulique doit être > 0.")

    G = mass_flow / flow_area
    Re = reynolds_number(
        characteristic_length=hydraulic_diameter,
        dynamic_viscosity=fluid["mu"],
        mass_flux=G,
    )
    if Re <= 0:
        raise ValueError("hx_compact_performance: Reynolds calculé <= 0.")

    j = j_correlation(Re)
    f = f_correlation(Re)
    h = j_colburn_to_h(j, G, fluid["cp"], fluid["Pr"])
    delta_p = fanning_f_to_dp(f, G, geometry["length"], hydraulic_diameter, fluid["rho"])

    effectiveness = h * geometry["surface_area"] / (mass_flow * fluid["cp"])

    return {
        "Re": Re,
        "j": j,
        "f": f,
        "h": h,
        "delta_p": delta_p,
        "effectiveness": effectiveness,
    }


__all__ = ["hx_compact_performance"]
