"""Tests for the material property helper."""
from __future__ import annotations

import unittest

from Source import MaterialProperties, SolidMaterial


class TestMaterials(unittest.TestCase):
    def setUp(self) -> None:
        self.db = MaterialProperties()

    def test_known_material(self) -> None:
        copper = self.db.get("copper")
        self.assertIsInstance(copper, SolidMaterial)
        self.assertGreater(copper.thermal_conductivity, 300.0)

    def test_unknown_material(self) -> None:
        with self.assertRaises(KeyError):
            self.db.get("unobtainium")

    def test_add_material(self) -> None:
        titanium = SolidMaterial(
            name="Titanium",
            density=4500.0,
            heat_capacity=522.0,
            thermal_conductivity=21.9,
            emissivity=0.3,
            poisson_ratio=0.34,
        )
        self.db.add_material("titanium", titanium)
        self.assertIn("titanium", self.db.list_materials())
        self.assertEqual(self.db.get("TiTanium").density, titanium.density)


if __name__ == "__main__":
    unittest.main()
