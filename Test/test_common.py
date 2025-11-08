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
            density=1000.0,
            velocity=2.0,
            characteristic_length=0.05,
            dynamic_viscosity=1.0e-3,
        )
        self.assertTrue(math.isfinite(value))
        self.assertAlmostEqual(value, 100000.0, places=6)

    def test_reynolds_number_invalid_viscosity(self) -> None:
        """Zero or negative viscosity must raise a ValueError."""

        with self.assertRaises(ValueError):
            reynolds_number(
                density=1.0,
                velocity=1.0,
                characteristic_length=1.0,
                dynamic_viscosity=0.0,
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
