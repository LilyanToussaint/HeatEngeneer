"""Example script listing available materials."""
from __future__ import annotations

import pathlib
import sys

# Ensure the repository root is on sys.path when running the script directly.
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source import MATERIAL_DATABASE, Material  # noqa: E402  (import after sys.path tweak)


def main() -> None:
    print("Matériaux disponibles (extrait):")
    for name in list(sorted(MATERIAL_DATABASE))[:10]:
        mat = MATERIAL_DATABASE[name]
        print(
            f"- {mat.name:>12s} | densité={mat.density:8.1f} kg/m³ | "
            f"cp={mat.heat_capacity:7.1f} J/kg/K | k={mat.thermal_conductivity:6.2f} W/m/K"
        )

    copper = MATERIAL_DATABASE["copper"]
    print("\nPropriétés détaillées pour le cuivre:")
    print(copper)

    print("\nAjout d'un matériau personnalisé (alliage aluminium).")
    catalog = dict(MATERIAL_DATABASE)
    catalog["aluminum_alloy"] = Material(
        name="Aluminum alloy 6061",
        density=2700.0,
        heat_capacity=896.0,
        thermal_conductivity=167.0,
        emissivity=0.1,
        poisson_ratio=0.33,
    )
    alloy = catalog["aluminum_alloy"]
    print(
        "Alliage 6061 → densité {density} kg/m³, cp {cp} J/kg/K, k {k} W/m/K".format(
            density=alloy.density,
            cp=alloy.heat_capacity,
            k=alloy.thermal_conductivity,
        )
    )


if __name__ == "__main__":
    main()
