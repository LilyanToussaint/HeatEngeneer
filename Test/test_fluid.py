# test_fluid.py
# Tests unitaires pour la classe Fluid sans utiliser "assert"
# Exécution : python -m unittest test_fluid.py

import math
import unittest

from fluid import Fluid


class TestFluid(unittest.TestCase):

    def test_init_valid_fluid(self):
        f = Fluid(name="Water", rho=1000.0, mu=1e-3, k=0.6, cp=4180.0)
        self.assertEqual(f.name, "Water")
        self.assertAlmostEqual(f.rho, 1000.0)
        self.assertAlmostEqual(f.mu, 1e-3)
        self.assertAlmostEqual(f.k, 0.6)
        self.assertAlmostEqual(f.cp, 4180.0)

    def test_init_invalid_physical_values(self):
        base = dict(name="X", rho=1000.0, mu=1e-3, k=0.6, cp=4180.0)

        cases = [
            ("rho", -1.0),
            ("rho", 0.0),
            ("mu", -1e-3),
            ("mu", 0.0),
            ("k", -0.1),
            ("k", 0.0),
            ("cp", -10.0),
            ("cp", 0.0),
        ]

        for field, value in cases:
            kwargs = base.copy()
            kwargs[field] = value
            with self.subTest(field=field, value=value):
                with self.assertRaises((ValueError, TypeError)):
                    Fluid(**kwargs)

    def test_prandtl_number_computation(self):
        rho = 997.0
        mu = 8.9e-4
        k = 0.6
        cp = 4180.0

        f = Fluid(name="Water", rho=rho, mu=mu, k=k, cp=cp)
        expected_Pr = cp * mu / k

        self.assertAlmostEqual(f.Pr, expected_Pr, delta=abs(expected_Pr) * 1e-6)

    def test_prandtl_is_read_only(self):
        """On ne doit pas pouvoir définir Pr directement si c'est une @property."""
        f = Fluid(name="Water", rho=1000.0, mu=1e-3, k=0.6, cp=4180.0)

        with self.assertRaises(AttributeError):
            # type: ignore[attr-defined]
            f.Pr = 1.0

    def test_repr_contains_useful_info(self):
        f = Fluid(name="Water", rho=1000.0, mu=1e-3, k=0.6, cp=4180.0)
        r = repr(f).lower()

        self.assertIn("water", r)
        # On ne fige pas le format exact, on vérifie juste des mots clés utiles
        self.assertTrue(("rho" in r) or ("density" in r))
        self.assertTrue(("mu" in r) or ("viscos" in r))

    def test_from_dict_valid(self):
        if not hasattr(Fluid, "from_dict"):
            self.skipTest("from_dict non implémenté dans Fluid")

        data = {
            "name": "Water",
            "rho": 1000.0,
            "mu": 1e-3,
            "k": 0.6,
            "cp": 4180.0,
        }

        f = Fluid.from_dict(data)
        self.assertIsInstance(f, Fluid)
        self.assertEqual(f.name, "Water")
        self.assertAlmostEqual(f.rho, 1000.0)
        self.assertAlmostEqual(f.mu, 1e-3)
        self.assertAlmostEqual(f.k, 0.6)
        self.assertAlmostEqual(f.cp, 4180.0)

    def test_with_updated_state_returns_new_instance(self):
        if not hasattr(Fluid, "with_updated_state"):
            self.skipTest("with_updated_state non implémenté dans Fluid")

        f1 = Fluid(name="Water", rho=1000.0, mu=1e-3, k=0.6, cp=4180.0)
        f2 = f1.with_updated_state(mu=2e-3)

        self.assertIsInstance(f2, Fluid)
        self.assertIsNot(f1, f2)
        self.assertAlmostEqual(f2.mu, 2e-3)
        self.assertAlmostEqual(f2.rho, f1.rho)
        self.assertAlmostEqual(f2.k, f1.k)
        self.assertAlmostEqual(f2.cp, f1.cp)

        expected_Pr = f2.cp * f2.mu / f2.k
        self.assertAlmostEqual(f2.Pr, expected_Pr, delta=abs(expected_Pr) * 1e-6)

    def test_numerical_stability_prandtl(self):
        f = Fluid(name="Oil", rho=850.0, mu=0.02, k=0.13, cp=2000.0)
        self.assertGreater(f.Pr, 0.0)
        self.assertTrue(math.isfinite(f.Pr))


if __name__ == "__main__":
    unittest.main()