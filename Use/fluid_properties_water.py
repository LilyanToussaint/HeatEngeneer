"""Example usage of the CoolProp-backed :class:`Fluid` helper."""
from __future__ import annotations

from pathlib import Path
import sys


_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


from Source.Fluid import Fluid


def show_water_state() -> None:
    """Evaluate representative water properties and print them."""
    water = Fluid(name="Water", backend="HEOS")
    water.compute("T", 298.15, "P", 101_325.0)

    print("=== Water state at 25°C and 1 atm ===")
    print("Identifier:", water.identifier)
    print("Inputs:")
    print("  - T: 298.15 K")
    print("  - P: 101325.0 Pa")

    print("Properties:")
    print(f"  - density: {water.density_kg_m3} kg/m³")
    print(f"  - enthalpy: {water.enthalpy_J_kg} J/kg")
    print(f"  - entropy: {water.entropy_J_kgK} J/(kg·K)")
    print(f"  - cp: {water.cp_J_kgK} J/(kg·K)")
    print(f"  - cv: {water.cv_J_kgK} J/(kg·K)")
    print(f"  - conductivity: {water.conductivity_W_mK} W/(m·K)")
    print(f"  - dynamic viscosity: {water.dynamic_viscosity_Pa_s} Pa·s")
    print(f"  - Prandtl: {water.prandtl_number}")
    print(f"  - vapor quality: {water.vapor_quality}")


if __name__ == "__main__":
    show_water_state()
