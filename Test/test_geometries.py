"""Unit tests for geometric helper classes."""
from __future__ import annotations

import math
import unittest

from Source.geometries import (
    PipeGeometry,
    PipeNetworkGeometry,
    PlateFinGeometry,
    PlateHeatExchangerGeometry,
    TubeFinGeometry,
    TubeFinNetworkGeometry,
)


class TestPipeGeometry(unittest.TestCase):
    def setUp(self) -> None:
        self.pipe = PipeGeometry(
            name="acier",
            density=7800.0,
            inner_diameter=0.01,
            outer_diameter=0.012,
            length=2.0,
        )

    def test_pipe_volumes(self) -> None:
        expected_fluid = math.pi * (0.5 * 0.01) ** 2 * 2.0
        expected_material = math.pi * ((0.5 * 0.012) ** 2 - (0.5 * 0.01) ** 2) * 2.0
        self.assertAlmostEqual(self.pipe.fluid_volume, expected_fluid)
        self.assertAlmostEqual(self.pipe.material_volume, expected_material)
        self.assertAlmostEqual(self.pipe.total_volume, expected_fluid + expected_material)

    def test_invalid_diameters(self) -> None:
        with self.assertRaises(ValueError):
            PipeGeometry(
                name="acier",
                density=7800.0,
                inner_diameter=0.02,
                outer_diameter=0.015,
                length=1.0,
            )


class TestPipeNetworkGeometry(unittest.TestCase):
    def test_network_scaling(self) -> None:
        single = PipeGeometry(
            name="acier",
            density=7800.0,
            inner_diameter=0.01,
            outer_diameter=0.012,
            length=2.0,
        )
        network = PipeNetworkGeometry(
            name="acier",
            density=7800.0,
            inner_diameter=0.01,
            outer_diameter=0.012,
            length=2.0,
            count=5,
        )
        self.assertAlmostEqual(network.fluid_volume, 5 * single.fluid_volume)
        self.assertAlmostEqual(network.material_volume, 5 * single.material_volume)
        self.assertAlmostEqual(network.total_volume, 5 * single.total_volume)

    def test_invalid_count(self) -> None:
        with self.assertRaises(ValueError):
            PipeNetworkGeometry(
                name="acier",
                density=7800.0,
                inner_diameter=0.01,
                outer_diameter=0.012,
                length=2.0,
                count=0,
            )


class TestPlateFinGeometry(unittest.TestCase):
    def setUp(self) -> None:
        self.geometry = PlateFinGeometry(
            name="aluminium",
            density=2700.0,
            length=0.3,
            fin_height=0.02,
            fin_thickness=0.001,
            fin_count=10,
            channel_width=0.002,
            plate_thickness=0.001,
        )

    def test_plate_fin_volumes(self) -> None:
        channel_count = 11
        total_width = 10 * 0.001 + channel_count * 0.002
        expected_fluid = channel_count * 0.3 * 0.02 * 0.002
        base_volume = 0.3 * total_width * 0.001
        fins_volume = 10 * 0.3 * 0.02 * 0.001
        expected_material = base_volume + fins_volume
        self.assertAlmostEqual(self.geometry.channel_count, channel_count)
        self.assertAlmostEqual(self.geometry.total_width, total_width)
        self.assertAlmostEqual(self.geometry.fluid_volume, expected_fluid)
        self.assertAlmostEqual(self.geometry.material_volume, expected_material)
        self.assertAlmostEqual(self.geometry.total_volume, expected_fluid + expected_material)

    def test_plate_fin_invalid(self) -> None:
        with self.assertRaises(ValueError):
            PlateFinGeometry(
                name="aluminium",
                density=2700.0,
                length=0.3,
                fin_height=0.02,
                fin_thickness=0.001,
                fin_count=-1,
                channel_width=0.002,
                plate_thickness=0.001,
            )


class TestPlateHeatExchangerGeometry(unittest.TestCase):
    def setUp(self) -> None:
        self.geometry = PlateHeatExchangerGeometry(
            name="inox",
            density=8000.0,
            length=0.5,
            width=0.2,
            plate_thickness=0.001,
            channel_gap=0.002,
            plate_count=20,
        )

    def test_volumes_and_stack(self) -> None:
        channel_count = 19
        expected_fluid = channel_count * 0.5 * 0.2 * 0.002
        expected_material = 20 * 0.5 * 0.2 * 0.001
        expected_stack = 20 * 0.001 + channel_count * 0.002

        self.assertEqual(self.geometry.channel_count, channel_count)
        self.assertAlmostEqual(self.geometry.fluid_volume, expected_fluid)
        self.assertAlmostEqual(self.geometry.material_volume, expected_material)
        self.assertAlmostEqual(self.geometry.total_volume, expected_fluid + expected_material)
        self.assertAlmostEqual(self.geometry.stack_thickness, expected_stack)

    def test_invalid_plate_count(self) -> None:
        with self.assertRaises(ValueError):
            PlateHeatExchangerGeometry(
                name="inox",
                density=8000.0,
                length=0.5,
                width=0.2,
                plate_thickness=0.001,
                channel_gap=0.002,
                plate_count=1,
            )


class TestTubeFinGeometry(unittest.TestCase):
    def setUp(self) -> None:
        self.geometry = TubeFinGeometry(
            name="cuivre",
            density=8900.0,
            inner_diameter=0.01,
            outer_diameter=0.012,
            length=1.5,
            fin_outer_diameter=0.05,
            fin_thickness=0.001,
            fin_count=20,
        )

    def test_tube_fin_material_volume(self) -> None:
        tube_volume = math.pi * ((0.5 * 0.012) ** 2 - (0.5 * 0.01) ** 2) * 1.5
        annulus_area = 0.25 * math.pi * (0.05 ** 2 - 0.012 ** 2)
        fins_volume = 20 * annulus_area * 0.001
        expected_material = tube_volume + fins_volume
        expected_fluid = math.pi * (0.5 * 0.01) ** 2 * 1.5
        self.assertAlmostEqual(self.geometry.material_volume, expected_material)
        self.assertAlmostEqual(self.geometry.fluid_volume, expected_fluid)
        self.assertAlmostEqual(self.geometry.total_volume, expected_material + expected_fluid)

    def test_invalid_fin_outer(self) -> None:
        with self.assertRaises(ValueError):
            TubeFinGeometry(
                name="cuivre",
                density=8900.0,
                inner_diameter=0.01,
                outer_diameter=0.012,
                length=1.5,
                fin_outer_diameter=0.01,
                fin_thickness=0.001,
                fin_count=20,
            )


class TestTubeFinNetworkGeometry(unittest.TestCase):
    def test_network(self) -> None:
        base_kwargs = dict(
            name="cuivre",
            density=8900.0,
            inner_diameter=0.01,
            outer_diameter=0.012,
            length=1.5,
            fin_outer_diameter=0.05,
            fin_thickness=0.001,
            fin_count=20,
        )
        single = TubeFinGeometry(**base_kwargs)
        network = TubeFinNetworkGeometry(tube_count=3, **base_kwargs)
        self.assertAlmostEqual(network.fluid_volume, 3 * single.fluid_volume)
        self.assertAlmostEqual(network.material_volume, 3 * single.material_volume)
        self.assertAlmostEqual(network.total_volume, 3 * single.total_volume)

    def test_invalid_count(self) -> None:
        with self.assertRaises(ValueError):
            TubeFinNetworkGeometry(
                name="cuivre",
                density=8900.0,
                inner_diameter=0.01,
                outer_diameter=0.012,
                length=1.5,
                fin_outer_diameter=0.05,
                fin_thickness=0.001,
                fin_count=20,
                tube_count=0,
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
