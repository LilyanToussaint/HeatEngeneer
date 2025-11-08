"""Tests for the CoolProp-backed fluid property helper."""

import importlib.util
import math
import unittest

from Source import FluidProperties


COOLPROP_AVAILABLE = importlib.util.find_spec("CoolProp") is not None


@unittest.skipUnless(COOLPROP_AVAILABLE, "CoolProp n'est pas disponible dans l'environnement de test")
class TestFluidProperties(unittest.TestCase):
    def setUp(self) -> None:
        self.water = FluidProperties("Water")

    def test_properties_at_temperature_pressure(self) -> None:
        state = self.water.properties_at(temperature=300.0, pressure=101325.0)
        self.assertAlmostEqual(state.properties["density"], 996.5569, places=3)
        self.assertAlmostEqual(state.properties["cp"], 4180.636, places=3)
        self.assertAlmostEqual(state.properties["thermal_conductivity"], 0.6095, places=4)
        self.assertAlmostEqual(state.properties["dynamic_viscosity"], 8.537e-4, places=7)
        self.assertAlmostEqual(state.properties["prandtl"], 5.8559, places=4)

    def test_single_property_helper(self) -> None:
        viscosity = self.water.get_property("dynamic_viscosity", temperature=300.0, pressure=101325.0)
        self.assertTrue(math.isfinite(viscosity))
        self.assertAlmostEqual(viscosity, 8.537424862859399e-04, places=9)

    def test_requires_two_inputs(self) -> None:
        with self.assertRaises(ValueError):
            self.water.properties_at(temperature=300.0)

    def test_unknown_property(self) -> None:
        with self.assertRaises(ValueError):
            self.water.properties_at(temperature=300.0, pressure=101325.0, outputs=("nonexistent",))


if __name__ == "__main__":
    unittest.main()
