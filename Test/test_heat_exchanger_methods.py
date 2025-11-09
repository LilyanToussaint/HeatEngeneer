"""Integration tests for the cleaned heat-transfer toolkit."""
from __future__ import annotations

import unittest

from Source import (
    HeatTransferCoefficient,
    PressureLossCorrelation,
    mass_flow_from_velocity,
    prandtl_number,
    reynolds_number,
    velocity_from_mass_flow,
)
from Source.Fluid import ConstantFluid
from Source.materials import MaterialProperties


class TestGenericBuildingBlocks(unittest.TestCase):
    """Ensure the remaining modules cooperate after the refactor."""

    def test_velocity_mass_flow_helpers(self) -> None:
        area = 0.02
        density = 997.0
        velocity = 1.5
        m_dot = mass_flow_from_velocity(velocity=velocity, density=density, area=area)
        self.assertAlmostEqual(velocity, velocity_from_mass_flow(m_dot, density, area))

    def test_dimensionless_helpers(self) -> None:
        Re = reynolds_number(velocity=2.0, characteristic_length=0.01, density=998.0, dynamic_viscosity=1.0e-3)
        Pr = prandtl_number(dynamic_viscosity=1.0e-3, heat_capacity=4182.0, thermal_conductivity=0.6)
        self.assertGreater(Re, 0.0)
        self.assertGreater(Pr, 0.0)

    def test_heat_transfer_wrapper(self) -> None:
        params = dict(Re=2.5e4, Pr=7.0, k=0.6, d_i=0.01)
        f = (0.79 * params["Re"] ** -0.25 - 0.64) ** 2
        nu = (f / 8.0) * (params["Re"] - 1000.0) * params["Pr"] / (
            1.0 + 12.7 * (f / 8.0) ** 0.5 * (params["Pr"] ** (2.0 / 3.0) - 1.0)
        )
        expected = nu * params["k"] / params["d_i"]

        htc = HeatTransferCoefficient("gnielinski_internal")
        result = htc.compute(**params)
        self.assertTrue(result.valid)
        self.assertAlmostEqual(result.h, expected, places=9)

    def test_pressure_loss_wrapper(self) -> None:
        params = dict(friction_factor=0.02, length=5.0, diameter=0.05, density=1000.0, velocity=1.2)
        expected = params["friction_factor"] * params["length"] * params["density"] * params["velocity"]**2 / (
            2.0 * params["diameter"]
        )
        wrapper = PressureLossCorrelation("darcy_weisbach")
        result = wrapper.compute(**params)
        self.assertTrue(result.valid)
        self.assertAlmostEqual(result.delta_p, expected, places=9)

    def test_material_catalog_access(self) -> None:
        catalog = MaterialProperties()
        aluminium = catalog.get("aluminium")
        self.assertGreater(aluminium.thermal_conductivity, 0.0)
        self.assertIn("water", catalog.list_materials())

    def test_constant_fluid_properties(self) -> None:
        water = ConstantFluid(
            name="water",
            properties={"density": 998.0, "cp": 4182.0, "thermal_conductivity": 0.6},
        )
        state = water.properties_at()
        self.assertAlmostEqual(state["density"], 998.0)
        with self.assertRaises(KeyError):
            water.get_property("viscosity")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
