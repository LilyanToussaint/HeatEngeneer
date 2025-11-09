"""Tests for the material property helpers."""
from __future__ import annotations

import unittest

from Source import MATERIAL_DATABASE, Material


class TestMaterials(unittest.TestCase):
    def test_known_material(self) -> None:
        copper = MATERIAL_DATABASE["copper"]
        self.assertIsInstance(copper, Material)
        self.assertGreater(copper.thermal_conductivity or 0.0, 300.0)

    def test_unknown_material_key(self) -> None:
        self.assertNotIn("unobtainium", MATERIAL_DATABASE)

    def test_extend_database(self) -> None:
        catalog = dict(MATERIAL_DATABASE)
        catalog["titanium"] = Material(
            name="Titanium",
            density=4500.0,
            heat_capacity=522.0,
            thermal_conductivity=21.9,
            emissivity=0.3,
            poisson_ratio=0.34,
        )
        self.assertIn("titanium", catalog)
        self.assertEqual(catalog["titanium"].density, 4500.0)


if __name__ == "__main__":
    unittest.main()
