"""Tests for the heat-exchanger method package."""
from __future__ import annotations

import math
import unittest

from Source import (
    HeatExchangerResult,
    Methode1D,
    MethodeLMTD,
    MethodeNTU,
    StreamConditions,
    mass_flow_from_velocity,
    velocity_from_mass_flow,
)
from Source.Heat_exchanger_methods.eps_ntu.effectiveness_counterflow import (
    effectiveness_counterflow,
)
from Source.Heat_exchanger_methods.eps_ntu.get_effectiveness_function import (
    get_effectiveness_function,
)
from Source.Heat_exchanger_methods.eps_ntu.registry import (
    EPSILON_FUNCTIONS,
    EPSILON_WITH_FIN_FUNCTIONS,
)
from Source.Heat_exchanger_methods.utils import compute_overall_u


class TestHeatExchangerMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.hot = StreamConditions(
            fluid={"name": "hot"},
            m_dot=0.45,
            cp=4100.0,
            inlet_temp=370.0,
            correlation_kwargs={"Re": 5.5e4, "Pr": 4.5, "k": 0.62, "d_i": 0.02},
            C=1845.0,
            area=8.0,
            velocity=1.5,
        )
        self.cold = StreamConditions(
            fluid={"name": "cold"},
            m_dot=0.6,
            cp=4200.0,
            inlet_temp=300.0,
            correlation_kwargs={"Re": 4.0e4, "Pr": 6.0, "k": 0.6, "d_i": 0.02},
            C=2520.0,
            area=8.0,
            velocity=1.2,
        )
        self.area = 8.0

    def test_stream_conditions_capacity_rate(self) -> None:
        self.assertAlmostEqual(self.hot.heat_capacity_rate(), 1845.0)
        self.assertAlmostEqual(self.cold.heat_capacity_rate(), 2520.0)

    def test_velocity_mass_flow_helpers(self) -> None:
        v = velocity_from_mass_flow(m_dot=0.5, density=997.0, area=0.02)
        self.assertAlmostEqual(v, 0.5 / (997.0 * 0.02))
        m_dot = mass_flow_from_velocity(velocity=v, density=997.0, area=0.02)
        self.assertAlmostEqual(m_dot, 0.5)

    def test_compute_overall_u_with_area_mismatch(self) -> None:
        hot = StreamConditions(
            fluid={"name": "hot"},
            m_dot=0.3,
            cp=4200.0,
            inlet_temp=360.0,
            correlation_kwargs={"Re": 3.2e4, "Pr": 5.3, "k": 0.62, "d_i": 0.018},
            area=9.0,
            velocity=1.1,
        )
        cold = StreamConditions(
            fluid={"name": "cold"},
            m_dot=0.5,
            cp=4000.0,
            inlet_temp=295.0,
            correlation_kwargs={"Re": 2.4e4, "Pr": 6.5, "k": 0.58, "d_i": 0.018},
            area=7.5,
            velocity=0.9,
        )
        u = compute_overall_u(2800.0, 2400.0, area_total=8.0, hot=hot, cold=cold, wall_resistance=5e-5)
        self.assertGreater(u, 0.0)
        self.assertLess(u, min(2800.0, 2400.0))

    def test_compute_overall_u_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            compute_overall_u(-1.0, 100.0, 5.0, self.hot, self.cold)
        with self.assertRaises(ValueError):
            compute_overall_u(100.0, 100.0, -1.0, self.hot, self.cold)

    def test_ntu_counterflow(self) -> None:
        method = MethodeNTU("gnielinski_internal")
        result = method.compute(self.hot, self.cold, area=self.area, configuration="counterflow")
        self.assertIsInstance(result, HeatExchangerResult)
        self.assertGreater(result.U, 0.0)
        c_min = min(self.hot.heat_capacity_rate(), self.cold.heat_capacity_rate())
        delta_t = self.hot.inlet_temp - self.cold.inlet_temp
        self.assertTrue(math.isclose(result.Q, result.epsilon * c_min * delta_t, rel_tol=1e-6))
        # verify epsilon via reference function
        epsilon_expected = effectiveness_counterflow(result.NTU, result.details["capacity_ratio"])
        self.assertAlmostEqual(result.epsilon, epsilon_expected, places=6)
        # outlet temperatures consistent
        self.assertTrue(
            math.isclose(
                result.hot_outlet_temp,
                self.hot.inlet_temp - result.Q / self.hot.heat_capacity_rate(),
                rel_tol=1e-6,
            )
        )

    def test_ntu_with_eta_fin_configuration(self) -> None:
        method = MethodeNTU("gnielinski_internal")
        result = method.compute(
            self.hot,
            self.cold,
            area=self.area,
            configuration="counterflow",
            use_eta_fin_method=True,
            configuration_kwargs={"eta_hot": 0.9, "eta_cold": 0.88},
        )
        self.assertLess(result.epsilon, 1.0)
        self.assertIn("counterflow_eta_fin", MethodeNTU.available_configurations())
        direct = method.compute(
            self.hot,
            self.cold,
            area=self.area,
            configuration="counterflow_eta_fin",
            configuration_kwargs={"eta_hot": 0.9, "eta_cold": 0.88},
        )
        self.assertAlmostEqual(direct.epsilon, result.epsilon, delta=0.05 * result.epsilon)

    def test_lmtd_consistency(self) -> None:
        method_ntu = MethodeNTU("gnielinski_internal")
        ntu_result = method_ntu.compute(self.hot, self.cold, area=self.area)

        method_lmtd = MethodeLMTD("gnielinski_internal")
        lmtd_result = method_lmtd.compute(
            self.hot,
            self.cold,
            area=self.area,
            hot_outlet_temp=ntu_result.hot_outlet_temp,
            cold_outlet_temp=ntu_result.cold_outlet_temp,
        )
        self.assertAlmostEqual(lmtd_result.Q, ntu_result.Q, delta=0.05 * ntu_result.Q)

    def test_one_dimensional_solver(self) -> None:
        method = Methode1D("gnielinski_internal")
        result = method.compute(self.hot, self.cold, area=self.area, segments=25)
        self.assertGreater(result.heat_duty, 0.0)
        self.assertLess(result.hot_outlet_temp, self.hot.inlet_temp)
        self.assertGreater(result.cold_outlet_temp, self.cold.inlet_temp)

    def test_effectiveness_catalog(self) -> None:
        for name, func in EPSILON_FUNCTIONS.items():
            # Ensure all registered functions are callable and yield values between 0 and 1
            eps = func(NTU=1.2, capacity_ratio=0.4)
            self.assertIsInstance(eps, float)
            self.assertGreaterEqual(eps, 0.0, msg=name)
            self.assertLessEqual(eps, 1.0 + 1e-9, msg=name)

        for name, func in EPSILON_WITH_FIN_FUNCTIONS.items():
            eps = func(NTU=1.2, capacity_ratio=0.6, eta_hot=0.9, eta_cold=0.85)
            self.assertGreaterEqual(eps, 0.0, msg=name)
            self.assertLessEqual(eps, 1.0 + 1e-9, msg=name)

        func, needs_eta = get_effectiveness_function("counterflow")
        self.assertFalse(needs_eta)
        self.assertIs(func, effectiveness_counterflow)

        func, needs_eta = get_effectiveness_function("counterflow_eta_fin")
        self.assertTrue(needs_eta)
        with self.assertRaises(ValueError):
            get_effectiveness_function("unknown-config")


if __name__ == "__main__":
    unittest.main()
