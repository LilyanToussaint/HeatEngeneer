"""Tests for the CoolProp-backed :class:`Fluid` helper."""
from __future__ import annotations

import unittest
from unittest.mock import patch

from Source.Fluid import Fluid


class TestFluid(unittest.TestCase):
    """Validate the high level behaviour of :class:`Fluid`."""

    def test_identifier_without_backend(self) -> None:
        fluid = Fluid(name="Water")
        self.assertEqual(fluid.identifier, "Water")

    def test_identifier_with_backend(self) -> None:
        fluid = Fluid(name="Water", backend="HEOS")
        self.assertEqual(fluid.identifier, "HEOS::Water")

    def test_compute_populates_state_and_returns_self(self) -> None:
        fluid = Fluid(name="Water", backend="HEOS")

        expected = {
            "T": 300.0,
            "P": 101_325.0,
            "D": 997.0,
            "H": 1.2e5,
            "S": 1.0e3,
            "C": 4180.0,
            "O": 3120.0,
            "L": 0.6,
            "V": 1.0e-3,
            "Prandtl": 6.98,
            "Q": 0.0,
        }

        calls: list[tuple[str, str, float, str, float, str]] = []

        def fake_props_si(code: str, key1: str, val1: float, key2: str, val2: float, identifier: str) -> float:
            calls.append((code, key1, val1, key2, val2, identifier))
            return expected[code]

        with patch("Source.Fluid.Fluid.PropsSI", side_effect=fake_props_si):
            result = fluid.compute("T", 300.0, "P", 101_325.0)

        self.assertIs(result, fluid)
        self.assertEqual(len(calls), len(expected))
        self.assertEqual(fluid.temperature_K, expected["T"])
        self.assertEqual(fluid.pressure_Pa, expected["P"])
        self.assertEqual(fluid.density_kg_m3, expected["D"])
        self.assertEqual(fluid.enthalpy_J_kg, expected["H"])
        self.assertEqual(fluid.entropy_J_kgK, expected["S"])
        self.assertEqual(fluid.cp_J_kgK, expected["C"])
        self.assertEqual(fluid.cv_J_kgK, expected["O"])
        self.assertEqual(fluid.conductivity_W_mK, expected["L"])
        self.assertEqual(fluid.dynamic_viscosity_Pa_s, expected["V"])
        self.assertEqual(fluid.prandtl_number, expected["Prandtl"])
        self.assertEqual(fluid.vapor_quality, expected["Q"])

        # Each PropsSI call should use the fully qualified identifier.
        for call in calls:
            self.assertEqual(call[-1], "HEOS::Water")

    def test_compute_rejects_invalid_keys(self) -> None:
        fluid = Fluid(name="Water")
        with self.assertRaises(ValueError):
            fluid.compute("X", 1.0, "P", 1.0)

    def test_compute_requires_distinct_keys(self) -> None:
        fluid = Fluid(name="Water")
        with self.assertRaises(ValueError):
            fluid.compute("T", 300.0, "T", 350.0)


if __name__ == "__main__":
    unittest.main()
