"""Lookup helper returning common material properties."""
from __future__ import annotations

from typing import Dict, Iterable, Mapping

from .SolidMaterial import SolidMaterial

__all__ = ["MaterialProperties"]


class MaterialProperties:
    """Lookup helper returning common material properties."""

    _DATABASE: Dict[str, SolidMaterial] = {
        "aluminium": SolidMaterial(
            name="Aluminium 6061",
            density=2700.0,
            heat_capacity=896.0,
            thermal_conductivity=167.0,
            emissivity=0.1,
            poisson_ratio=0.33,
        ),
        "copper": SolidMaterial(
            name="Cuivre",
            density=8960.0,
            heat_capacity=385.0,
            thermal_conductivity=401.0,
            emissivity=0.03,
            poisson_ratio=0.34,
        ),
        "stainless_steel": SolidMaterial(
            name="Inox 304",
            density=8030.0,
            heat_capacity=500.0,
            thermal_conductivity=16.2,
            emissivity=0.4,
            poisson_ratio=0.29,
        ),
        "carbon_steel": SolidMaterial(
            name="Acier carbone",
            density=7850.0,
            heat_capacity=480.0,
            thermal_conductivity=54.0,
            emissivity=0.8,
            poisson_ratio=0.27,
        ),
        "water": SolidMaterial(
            name="Eau liquide",
            density=998.0,
            heat_capacity=4182.0,
            thermal_conductivity=0.6,
        ),
    }

    def __init__(self, database: Mapping[str, SolidMaterial] | None = None) -> None:
        self._materials: Dict[str, SolidMaterial] = {
            key.lower(): value for key, value in (database or self._DATABASE).items()
        }

    def get(self, key: str) -> SolidMaterial:
        try:
            return self._materials[key.lower()]
        except KeyError as exc:
            raise KeyError(
                f"Matériau '{key}' inconnu. Disponibles: {', '.join(sorted(self._materials))}"
            ) from exc

    def add_material(self, key: str, material: SolidMaterial) -> None:
        self._materials[key.lower()] = material

    def list_materials(self) -> Iterable[str]:
        return sorted(self._materials)

    def as_dict(self) -> Dict[str, SolidMaterial]:
        return dict(self._materials)
