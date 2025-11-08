"""Tests for the pressure-loss wrapper and correlations."""
from __future__ import annotations

import math
import unittest

from Source import PressureLossCorrelation
from Source.loss_pressure.correlations import dp_darcy_weisbach


class TestPressureLossCorrelation(unittest.TestCase):
    """Validate the pressure-loss correlation wrapper."""

    def test_available_contains_darcy_weisbach(self) -> None:
        """The Darcy-Weisbach correlation must be discoverable."""

        available = PressureLossCorrelation.available()
        self.assertIn("darcy_weisbach", available)

    def test_compute_matches_direct_call(self) -> None:
        """Wrapper output should align with the direct correlation."""

        params = dict(
            friction_factor=0.02,
            length=10.0,
            diameter=0.1,
            density=1000.0,
            velocity=2.0,
        )
        direct_value = dp_darcy_weisbach(**params)

        wrapper = PressureLossCorrelation("darcy_weisbach")
        result = wrapper.compute(**params)

        self.assertTrue(result.valid)
        self.assertTrue(math.isfinite(result.delta_p))
        self.assertAlmostEqual(result.delta_p, direct_value, places=9)
        self.assertEqual(result.correlation_meta.get("geometry"), "circular_duct")
        self.assertEqual(result.correlation, "darcy_weisbach")

    def test_compute_handles_invalid_parameters(self) -> None:
        """Invalid inputs should set the result as invalid without exceptions."""

        wrapper = PressureLossCorrelation("darcy_weisbach")
        result = wrapper.compute(
            friction_factor=-1.0,
            length=10.0,
            diameter=0.1,
            density=1000.0,
            velocity=2.0,
        )

        self.assertFalse(result.valid)
        self.assertTrue(math.isnan(result.delta_p))
        self.assertIn("doit être positif", result.message)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
