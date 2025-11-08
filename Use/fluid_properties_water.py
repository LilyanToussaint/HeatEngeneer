"""Example usage of the CoolProp-backed fluid properties helper."""
from __future__ import annotations

from pathlib import Path
import sys


_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


from Source import FluidProperties


def show_water_state() -> None:
    """Evaluate representative water properties and print them."""
    water = FluidProperties("Water")

    state = water.properties_at(T=298.15, P=101_325)

    print("=== Water state at 25°C and 1 atm ===")
    print("Inputs:")
    for key, value in state.inputs.items():
        print(f"  - {key}: {value}")

    print("Properties:")
    for key, value in state.properties.items():
        print(f"  - {key}: {value}")

    cp = water.get_property("cp", T=298.15, P=101_325)
    print(f"\nSpecific heat capacity (cp): {cp} J/(kg·K)")


if __name__ == "__main__":
    show_water_state()
