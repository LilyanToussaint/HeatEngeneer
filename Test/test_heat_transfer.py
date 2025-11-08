"""Tests for the heat-transfer coefficient wrapper and registry."""
from __future__ import annotations

import math
import unittest

from Source import HeatTransferCoefficient
from Source.Heat_transfer_coefficient.correlations import h_gnielinski_internal


class TestHeatTransferCoefficient(unittest.TestCase):
    """Ensure the heat-transfer wrapper integrates the registry correctly."""

    def test_available_contains_gnielinski(self) -> None:
        """The Gnielinski correlation should be discoverable."""

        available = HeatTransferCoefficient.available()
        self.assertIn("gnielinski_internal", available)

    def test_compute_matches_direct_call(self) -> None:
        """Wrapper output must match the direct correlation function."""

        params = dict(Re=2.5e4, Pr=7.0, k=0.6, d_i=0.01)
        direct_value = h_gnielinski_internal(**params)

        htc = HeatTransferCoefficient("gnielinski_internal")
        result = htc.compute(**params)

        self.assertTrue(result.valid)
        self.assertTrue(math.isfinite(result.h))
        self.assertAlmostEqual(result.h, direct_value, places=9)
        self.assertEqual(result.correlation_meta.get("domain"), "internal")
        self.assertEqual(result.correlation, "gnielinski_internal")

    def test_compute_handles_domain_error(self) -> None:
        """Out-of-range inputs should be reported as invalid without raising."""

        htc = HeatTransferCoefficient("gnielinski_internal")
        result = htc.compute(Re=100.0, Pr=7.0, k=0.6, d_i=0.01)

        self.assertFalse(result.valid)
        self.assertTrue(math.isnan(result.h))
        self.assertIn("Re hors domaine", result.message)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
