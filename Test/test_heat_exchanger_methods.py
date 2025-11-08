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
)
from Source.Heat_exchanger_methods.eps_ntu import effectiveness_counterflow


class TestHeatExchangerMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.hot = StreamConditions(
            m_dot=0.45,
            cp=4100.0,
            inlet_temp=370.0,
            correlation_kwargs={"Re": 5.5e4, "Pr": 4.5, "k": 0.62, "d_i": 0.02},
            fin_efficiency=0.92,
        )
        self.cold = StreamConditions(
            m_dot=0.6,
            cp=4200.0,
            inlet_temp=300.0,
            correlation_kwargs={"Re": 4.0e4, "Pr": 6.0, "k": 0.6, "d_i": 0.02},
            fin_efficiency=0.95,
        )
        self.area = 8.0

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
        )
        self.assertLess(result.epsilon, 1.0)
        self.assertIn("counterflow_eta_fin", MethodeNTU.available_configurations())
        direct = method.compute(
            self.hot,
            self.cold,
            area=self.area,
            configuration="counterflow_eta_fin",
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


if __name__ == "__main__":
    unittest.main()
