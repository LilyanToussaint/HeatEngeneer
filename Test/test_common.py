"""Unit tests for common dimensionless-number helpers."""
from __future__ import annotations

import math
import unittest

from Source import prandtl_number, reynolds_number


class TestReynoldsNumber(unittest.TestCase):
    """Validate the Reynolds number helper."""

    def test_reynolds_number_nominal(self) -> None:
        """A typical liquid-water case should match the analytical formula."""

        value = reynolds_number(
            characteristic_length=0.05,
            dynamic_viscosity=1.0e-3,
            density=1000.0,
            velocity=2.0,
        )
        self.assertTrue(math.isfinite(value))
        self.assertAlmostEqual(value, 100000.0, places=6)

    def test_reynolds_number_from_mass_flow(self) -> None:
        """Mass-flow data with area should produce the correct Reynolds number."""

        mass_flow = 2.0  # kg/s
        area = 0.01  # m²
        hydraulic_diameter = 0.05  # m
        mu = 1.0e-3  # Pa·s

        value = reynolds_number(
            characteristic_length=hydraulic_diameter,
            dynamic_viscosity=mu,
            mass_flow_rate=mass_flow,
            area=area,
        )

        # Equivalent density * velocity: mass_flux = 200 kg/(m²·s)
        expected = (mass_flow / area) * hydraulic_diameter / mu
        self.assertAlmostEqual(value, expected, places=9)

    def test_reynolds_number_with_kinematic_viscosity(self) -> None:
        """Velocity and kinematic viscosity inputs should be accepted."""

        value = reynolds_number(
            characteristic_length=0.02,
            velocity=3.0,
            kinematic_viscosity=1.5e-6,
        )
        self.assertAlmostEqual(value, 40000.0, places=6)

    def test_reynolds_number_invalid_viscosity(self) -> None:
        """Zero or negative viscosity must raise a ValueError."""

        with self.assertRaises(ValueError):
            reynolds_number(
                characteristic_length=1.0,
                dynamic_viscosity=0.0,
                density=1.0,
                velocity=1.0,
            )


class TestPrandtlNumber(unittest.TestCase):
    """Validate the Prandtl number helper."""

    def test_prandtl_number_nominal(self) -> None:
        """Verify the textbook relation μ c_p / k."""

        value = prandtl_number(
            dynamic_viscosity=1.0e-3,
            heat_capacity=4184.0,
            thermal_conductivity=0.6,
        )
        self.assertTrue(math.isfinite(value))
        self.assertAlmostEqual(value, 6.9733333333, places=7)

    def test_prandtl_number_from_kinematic_viscosity(self) -> None:
        """The ν/α form should match the classical definition."""

        nu = 1.5e-6
        alpha = 7.5e-7
        value = prandtl_number(
            kinematic_viscosity=nu,
            thermal_diffusivity=alpha,
        )
        self.assertAlmostEqual(value, nu / alpha, places=9)

    def test_prandtl_number_invalid_parameters(self) -> None:
        """Non-positive properties must be rejected."""

        with self.assertRaises(ValueError):
            prandtl_number(
                dynamic_viscosity=1.0e-3,
                heat_capacity=0.0,
                thermal_conductivity=0.6,
            )

        with self.assertRaises(ValueError):
            prandtl_number(
                dynamic_viscosity=1.0e-3,
                heat_capacity=4184.0,
                thermal_conductivity=0.0,
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
