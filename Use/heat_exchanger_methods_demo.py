"""Demonstration script for the generic heat-transfer utilities."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source import (  # noqa: E402  (import after sys.path tweaks)
    HeatTransferCoefficient,
    MATERIAL_DATABASE,
    PressureLossCorrelation,
    _COOLPROP_AVAILABLE,
    CoolPropFluid,
    mass_flow_from_velocity,
    prandtl_number,
    reynolds_number,
    velocity_from_mass_flow,
)


def demo_htc() -> None:
    params = dict(Re=3.0e4, Pr=7.0, k=0.62, d_i=0.018)
    htc = HeatTransferCoefficient("gnielinski_internal")
    result = htc.compute(**params)
    print("=== Coefficient de convection (Gnielinski) ===")
    print(f"h = {result.h:.1f} W/m²/K")
    print(f"validité: {result.valid}\n")


def demo_pressure_drop() -> None:
    wrapper = PressureLossCorrelation("darcy_weisbach")
    params = dict(friction_factor=0.018, length=5.0, diameter=0.02, density=998.0, velocity=1.3)
    result = wrapper.compute(**params)
    print("=== Pertes de charge (Darcy-Weisbach) ===")
    print(f"Δp = {result.delta_p:.1f} Pa")
    print(f"message: {result.message or 'ok'}\n")


def demo_flow_helpers() -> None:
    area = 0.0005
    density = 997.0
    velocity = 1.8
    m_dot = mass_flow_from_velocity(velocity=velocity, density=density, area=area)
    recovered_v = velocity_from_mass_flow(m_dot, density, area)
    Re = reynolds_number(
        velocity=velocity,
        characteristic_length=0.02,
        density=density,
        dynamic_viscosity=1.0e-3,
    )
    Pr = prandtl_number(
        dynamic_viscosity=1.0e-3,
        heat_capacity=4182.0,
        thermal_conductivity=0.6,
    )
    print("=== Outils de débit et grandeurs sans dimension ===")
    print(f"m_dot = {m_dot:.4f} kg/s, vitesse retrouvée = {recovered_v:.2f} m/s")
    print(f"Re = {Re:.0f}, Pr = {Pr:.2f}\n")


def demo_materials_and_fluids() -> None:
    copper = MATERIAL_DATABASE["copper"]
    print("=== Matériaux et fluides ===")
    print(f"Cuivre: k = {copper.thermal_conductivity:.1f} W/m/K")
    if not _COOLPROP_AVAILABLE:
        print("CoolProp indisponible: impossible de démontrer les fluides dynamiques.\n")
        return

    water = CoolPropFluid("Water")
    state = water.properties_at(T=298.15, P=101325.0, outputs=("cp", "density"))
    print(
        "Eau: cp = {cp:.1f} J/kg/K, rho = {rho:.1f} kg/m³\n".format(
            cp=state["cp"],
            rho=state["density"],
        )
    )


if __name__ == "__main__":
    demo_htc()
    demo_pressure_drop()
    demo_flow_helpers()
    demo_materials_and_fluids()
