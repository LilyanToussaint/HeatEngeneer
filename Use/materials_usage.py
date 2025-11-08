"""Example usage of the material property catalogue."""
from __future__ import annotations

import pathlib
import sys


# Ensure the repository root is on sys.path when running the script directly.
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source import MaterialProperties  # noqa: E402  (import after sys.path tweak)


def main() -> None:
    db = MaterialProperties()

    print("Matériaux disponibles (extrait):")
    for name in list(db.list_materials())[:10]:
        mat = db.get(name)
        print(
            f"- {mat.name:>12s} | densité={mat.density:8.1f} kg/m³ | "
            f"cp={mat.heat_capacity:7.1f} J/kg/K | k={mat.thermal_conductivity:6.2f} W/m/K"
        )

    copper = db.get("copper")
    print("\nPropriétés détaillées pour le cuivre:")
    print(copper)

    print("\nAjout d'un matériau personnalisé (alliage aluminium).")
    db.add_material(
        "aluminum_alloy",
        copper.__class__(
            name="Aluminum alloy 6061",
            density=2700.0,
            heat_capacity=896.0,
            thermal_conductivity=167.0,
            emissivity=0.1,
            poisson_ratio=0.33,
        ),
    )
    alloy = db.get("aluminum_alloy")
    print(
        f"Alliage 6061 → densité {alloy.density} kg/m³, cp {alloy.heat_capacity} J/kg/K, k {alloy.thermal_conductivity} W/m/K"
    )


if __name__ == "__main__":
    main()
