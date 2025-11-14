from __future__ import annotations

import unittest

from Source import (
    Fluid,
    HeatTransferCoefficient,
    MATERIAL_DATABASE,
    PressureLossCorrelation,
    _COOLPROP_AVAILABLE,
    mass_flow_from_velocity,
    prandtl_number,
    reynolds_number,
    velocity_from_mass_flow,
)


class TestGenericBuildingBlocks(unittest.TestCase):
    """Ensure the remaining modules cooperate after the refactor."""

    def test_velocity_mass_flow_helpers(self) -> None:
        area = 0.02
        density = 997.0
        velocity = 1.5
        m_dot = mass_flow_from_velocity(velocity=velocity, density=density, area=area)
        self.assertAlmostEqual(velocity, velocity_from_mass_flow(m_dot, density, area))

    def test_dimensionless_helpers(self) -> None:
        Re = reynolds_number(
            velocity=2.0,
            characteristic_length=0.01,
            density=998.0,
            dynamic_viscosity=1.0e-3,
        )
        Pr = prandtl_number(
            dynamic_viscosity=1.0e-3,
            heat_capacity=4182.0,
            thermal_conductivity=0.6,
        )
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
        params = dict(
            friction_factor=0.02,
            length=5.0,
            diameter=0.05,
            density=1000.0,
            velocity=1.2,
        )
        expected = (
            params["friction_factor"]
            * params["length"]
            * params["density"]
            * params["velocity"]**2
            / (2.0 * params["diameter"])
        )
        wrapper = PressureLossCorrelation("darcy_weisbach")
        result = wrapper.compute(**params)
        self.assertTrue(result.valid)
        self.assertAlmostEqual(result.delta_p, expected, places=9)

    def test_material_database_access(self) -> None:
        aluminium = MATERIAL_DATABASE["aluminium"]
        self.assertGreater(aluminium.thermal_conductivity or 0.0, 0.0)
        self.assertIn("water", MATERIAL_DATABASE)

    def test_coolprop_backend_availability(self) -> None:
        fluid = Fluid(name="Water", backend="HEOS")
        if not _COOLPROP_AVAILABLE:
            with self.assertRaises(ModuleNotFoundError):
                fluid.compute("T", 300.0, "P", 101325.0)
        else:  # pragma: no cover - requires CoolProp
            fluid.compute("T", 300.0, "P", 101325.0)
            self.assertIsNotNone(fluid.density_kg_m3)
            self.assertGreater(fluid.density_kg_m3 or 0.0, 0.0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
