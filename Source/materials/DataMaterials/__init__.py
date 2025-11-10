"""Static material property database."""
from __future__ import annotations

from typing import Dict

from ..Material import Material

MATERIAL_DATABASE: Dict[str, Material] = {
    "aluminium": Material(
        name="Aluminium 6061",
        density=2700.0,
        heat_capacity=896.0,
        thermal_conductivity=167.0,
        emissivity=0.1,
        poisson_ratio=0.33,
    ),
    "copper": Material(
        name="Cuivre",
        density=8960.0,
        heat_capacity=385.0,
        thermal_conductivity=401.0,
        emissivity=0.03,
        poisson_ratio=0.34,
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
    ),
}

__all__ = ["MATERIAL_DATABASE"]
