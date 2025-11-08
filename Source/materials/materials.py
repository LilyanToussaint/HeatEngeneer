"""Basic material property catalogue."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Optional


@dataclass(frozen=True)
class Material:
    name: str
    density: float  # kg/m3
    heat_capacity: float  # J/kg/K
    thermal_conductivity: float  # W/m/K
    emissivity: Optional[float] = None
    poisson_ratio: Optional[float] = None


class MaterialProperties:
    """Lookup helper returning common material properties."""

    _DATABASE: Dict[str, Material] = {
        "aluminium": Material(
            name="Aluminium 6061",
            density=2700.0,
            heat_capacity=896.0,
            thermal_conductivity=167.0,
            emissivity=0.1,
            poisson_ratio=0.33,
        ),
        "copper": Material(
            name="Cuivre", density=8960.0, heat_capacity=385.0, thermal_conductivity=401.0, emissivity=0.03, poisson_ratio=0.34
        ),
        "stainless_steel": Material(
            name="Inox 304",
            density=8030.0,
            heat_capacity=500.0,
            thermal_conductivity=16.2,
            emissivity=0.4,
            poisson_ratio=0.29,
        ),
        "carbon_steel": Material(
            name="Acier carbone",
            density=7850.0,
            heat_capacity=480.0,
            thermal_conductivity=54.0,
            emissivity=0.8,
            poisson_ratio=0.27,
        ),
        "water": Material(
            name="Eau liquide",
            density=998.0,
            heat_capacity=4182.0,
            thermal_conductivity=0.6,
            emissivity=None,
            poisson_ratio=None,
        ),
    }

    def __init__(self, database: Mapping[str, Material] | None = None) -> None:
        self._materials: Dict[str, Material] = {k.lower(): v for k, v in (database or self._DATABASE).items()}

    def get(self, key: str) -> Material:
        try:
            return self._materials[key.lower()]
        except KeyError as exc:
            raise KeyError(
                f"Matériau '{key}' inconnu. Disponibles: {', '.join(sorted(self._materials))}"
            ) from exc

    def add_material(self, key: str, material: Material) -> None:
        self._materials[key.lower()] = material

    def list_materials(self) -> Iterable[str]:
        return sorted(self._materials)

    def as_dict(self) -> Dict[str, Material]:
        return dict(self._materials)
