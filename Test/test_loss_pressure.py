from __future__ import annotations

import math
import unittest

from Source import PressureLossCorrelation
from Source.common import reynolds_number
from Source.loss_pressure.correlations import (
    convert_head_to_dp,
    dp_darcy_weisbach,
    dp_friedel,
    dp_laminar_fully_developed,
    dp_minor,
    dp_total_channel,
    f_to_dp,
    fanning_factor_moody,
    re_pipe_flow,
    select_friction_model,
)


class TestPressureLossCorrelation(unittest.TestCase):
    """Validate the pressure-loss correlation wrapper."""

    def test_available_contains_core_entries(self) -> None:
        """Ensure the registry exposes the newly-added correlations."""

        available = set(PressureLossCorrelation.available())
        self.assertIn("darcy_weisbach", available)
        self.assertIn("laminar_fully_developed", available)
        self.assertIn("minor", available)
        self.assertIn("friedel", available)

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

    def test_laminar_poisseuille_matches_expectation(self) -> None:
        """Compare Poiseuille drop with analytic expression."""

        re_laminar = 1200.0
        mu = 1.0e-3
        diameter = 0.01
        length = 2.0
        density = 998.0
        velocity = re_laminar * mu / (density * diameter)
        expected = 32.0 * mu * velocity * length / diameter**2
        actual = dp_laminar_fully_developed(re_laminar, length, diameter, mu, velocity)
        self.assertAlmostEqual(expected, actual, places=9)

    def test_minor_loss_utility(self) -> None:
        """The minor-loss helper should recover the standard relation."""

        k = 1.5
        rho = 997.0
        velocity = 1.2
        expected = 0.5 * k * rho * velocity**2
        self.assertAlmostEqual(expected, dp_minor(k, rho, velocity))

    def test_total_channel_combines_minor_losses(self) -> None:
        """Verify combination of linear and minor contributions."""

        velocity = 1.5
        rho = 1000.0
        diameter = 0.05
        dp_linear = f_to_dp(0.02, length=5.0, diameter=diameter, density=rho, velocity=velocity)
        dp_total = dp_total_channel(
            friction_factor=0.02,
            mass_flux=rho * velocity,
            length=5.0,
            hydraulic_diameter=diameter,
            density=rho,
            minor_losses=0.6,
        )
        self.assertGreater(dp_total, dp_linear)

    def test_fanning_factor_selector(self) -> None:
        """Moody helper should fall back to expected correlations."""

        f_laminar = fanning_factor_moody(500.0)
        f_selected = select_friction_model(5.0e5, 1e-4)
        self.assertAlmostEqual(f_laminar, 16.0 / 500.0)
        self.assertGreater(f_selected, 0.0)

    def test_re_pipe_flow_matches_common_helper(self) -> None:
        """Mass-flow Reynolds helper should mirror the shared computation."""

        m_dot = 0.2
        diameter = 0.02
        rho = 998.0
        mu = 1.0e-3
        area = math.pi * diameter**2 / 4.0
        velocity = m_dot / (rho * area)
        expected = reynolds_number(
            velocity=velocity,
            characteristic_length=diameter,
            density=rho,
            dynamic_viscosity=mu,
        )
        self.assertAlmostEqual(expected, re_pipe_flow(m_dot, diameter, mu, rho))

    def test_two_phase_multiplier_returns_phi_sq(self) -> None:
        """Friedel correlation should return a multiplier when dp is absent."""

        phi_sq = dp_friedel(
            reynolds_liquid=5.0e4,
            reynolds_gas=1.0e5,
            quality=0.3,
            density_liquid=950.0,
            density_gas=30.0,
            viscosity_liquid=0.001,
            viscosity_gas=1.5e-5,
            surface_tension=0.06,
            diameter=0.02,
        )
        self.assertGreater(phi_sq, 1.0)

    def test_convert_head_to_dp(self) -> None:
        """Hydraulic head conversion should match ρ·g·h."""

        rho = 1000.0
        head = 3.0
        expected = rho * 9.80665 * head
        self.assertAlmostEqual(expected, convert_head_to_dp(head, rho))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
