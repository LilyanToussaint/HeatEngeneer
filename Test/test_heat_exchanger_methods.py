"""Tests for the object-oriented heat-exchanger package."""
from __future__ import annotations

import math
import unittest

from Source import (
    DPModel,
    EpsilonNTUSolver,
    FlowArrangement,
    FluidModel,
    Geometry,
    HeatExchanger,
    HXSide,
    HTCModel,
    LMTDResult,
    LMTDSolver,
    NTUResult,
    OneDResult,
    OneDimensionalSolver,
    Wall,
    EPSILON_FUNCTIONS,
    EPSILON_WITH_FIN_FUNCTIONS,
    get_effectiveness_function,
    mass_flow_from_velocity,
    velocity_from_mass_flow,
)
from Source.heat_exchanger.solvers.epsilon_ntu.effectiveness_counterflow import (
    effectiveness_counterflow,
)


class TestHeatExchangerModels(unittest.TestCase):
    def setUp(self) -> None:
        hot_fluid = FluidModel(name="hot", heat_capacity=4100.0)
        cold_fluid = FluidModel(name="cold", heat_capacity=4200.0)

        hot_geometry = Geometry(area=8.0, hydraulic_diameter=0.02)
        cold_geometry = Geometry(area=8.0, hydraulic_diameter=0.02)

        hot_htc = HTCModel(
            correlation="gnielinski_internal",
            parameters={"Re": 5.5e4, "Pr": 4.5, "k": 0.62, "d_i": 0.02},
        )
        cold_htc = HTCModel(
            correlation="gnielinski_internal",
            parameters={"Re": 4.0e4, "Pr": 6.0, "k": 0.6, "d_i": 0.02},
        )

        self.hot = HXSide(
            label="hot",
            fluid=hot_fluid,
            mass_flow=0.45,
            inlet_temp=370.0,
            geometry=hot_geometry,
            htc_model=hot_htc,
            dp_model=DPModel(),
            heat_capacity_override=1845.0,
            velocity=1.5,
        )
        self.cold = HXSide(
            label="cold",
            fluid=cold_fluid,
            mass_flow=0.6,
            inlet_temp=300.0,
            geometry=cold_geometry,
            htc_model=cold_htc,
            dp_model=DPModel(),
            heat_capacity_override=2520.0,
            velocity=1.2,
        )

        arrangement = FlowArrangement("counterflow")
        wall = Wall(thermal_resistance=0.0)
        self.exchanger = HeatExchanger(
            hot=self.hot,
            cold=self.cold,
            arrangement=arrangement,
            wall=wall,
        )
        self.area = 8.0

    def test_heat_capacity_rate(self) -> None:
        self.assertAlmostEqual(self.hot.heat_capacity_rate(), 1845.0)
        self.assertAlmostEqual(self.cold.heat_capacity_rate(), 2520.0)

    def test_velocity_mass_flow_helpers(self) -> None:
        v = velocity_from_mass_flow(m_dot=0.5, density=997.0, area=0.02)
        self.assertAlmostEqual(v, 0.5 / (997.0 * 0.02))
        m_dot = mass_flow_from_velocity(velocity=v, density=997.0, area=0.02)
        self.assertAlmostEqual(m_dot, 0.5)

    def test_compute_overall_u_with_area_mismatch(self) -> None:
        hot_side = HXSide(
            label="hot",
            fluid=FluidModel(name="hot", heat_capacity=4200.0),
            mass_flow=0.3,
            inlet_temp=360.0,
            geometry=Geometry(area=9.0, hydraulic_diameter=0.018),
            htc_model=HTCModel(
                correlation=self.hot.htc_model.correlation,
                parameters=dict(self.hot.htc_model.parameters),
            ),
            dp_model=DPModel(),
        )
        cold_side = HXSide(
            label="cold",
            fluid=FluidModel(name="cold", heat_capacity=4000.0),
            mass_flow=0.5,
            inlet_temp=295.0,
            geometry=Geometry(area=7.5, hydraulic_diameter=0.018),
            htc_model=HTCModel(
                correlation=self.cold.htc_model.correlation,
                parameters=dict(self.cold.htc_model.parameters),
            ),
            dp_model=DPModel(),
        )
        exchanger = HeatExchanger(
            hot=hot_side,
            cold=cold_side,
            arrangement=FlowArrangement("counterflow"),
            wall=Wall(thermal_resistance=5e-5),
        )
        u = exchanger.compute_overall_u(2800.0, 2400.0, area_reference=8.0)
        self.assertGreater(u, 0.0)
        self.assertLess(u, min(2800.0, 2400.0))

    def test_ntu_counterflow(self) -> None:
        solver = EpsilonNTUSolver()
        result = solver.solve(self.exchanger, area=self.area)
        self.assertIsInstance(result, NTUResult)
        self.assertGreater(result.U, 0.0)
        c_min = min(self.hot.heat_capacity_rate(), self.cold.heat_capacity_rate())
        delta_t = self.hot.inlet_temp - self.cold.inlet_temp
        self.assertTrue(math.isclose(result.Q, result.epsilon * c_min * delta_t, rel_tol=1e-6))
        epsilon_expected = effectiveness_counterflow(result.NTU, result.details["capacity_ratio"])
        self.assertAlmostEqual(result.epsilon, epsilon_expected, places=6)
        self.assertTrue(
            math.isclose(
                result.hot_outlet_temp,
                self.hot.inlet_temp - result.Q / self.hot.heat_capacity_rate(),
                rel_tol=1e-6,
            )
        )

    def test_ntu_with_eta_fin_configuration(self) -> None:
        solver = EpsilonNTUSolver()
        result = solver.solve(
            self.exchanger,
            area=self.area,
            configuration="counterflow",
            use_eta_fin_method=True,
            configuration_kwargs={"eta_hot": 0.9, "eta_cold": 0.88},
        )
        self.assertLess(result.epsilon, 1.0)
        self.assertIn("counterflow_eta_fin", EpsilonNTUSolver.available_configurations())
        direct = solver.solve(
            self.exchanger,
            area=self.area,
            configuration="counterflow_eta_fin",
            configuration_kwargs={"eta_hot": 0.9, "eta_cold": 0.88},
        )
        self.assertAlmostEqual(direct.epsilon, result.epsilon, delta=0.05 * result.epsilon)

    def test_lmtd_consistency(self) -> None:
        solver_ntu = EpsilonNTUSolver()
        ntu_result = solver_ntu.solve(self.exchanger, area=self.area)

        solver_lmtd = LMTDSolver()
        lmtd_result = solver_lmtd.solve(
            self.exchanger,
            area=self.area,
            hot_outlet_temp=ntu_result.hot_outlet_temp,
            cold_outlet_temp=ntu_result.cold_outlet_temp,
        )
        self.assertIsInstance(lmtd_result, LMTDResult)
        self.assertAlmostEqual(lmtd_result.Q, ntu_result.Q, delta=0.05 * ntu_result.Q)

    def test_one_dimensional_solver(self) -> None:
        solver = OneDimensionalSolver()
        result = solver.solve(self.exchanger, area=self.area, segments=25)
        self.assertIsInstance(result, OneDResult)
        self.assertGreater(result.heat_duty, 0.0)
        self.assertLess(result.hot_outlet_temp, self.hot.inlet_temp)
        self.assertGreater(result.cold_outlet_temp, self.cold.inlet_temp)

    def test_effectiveness_catalog(self) -> None:
        for name, func in EPSILON_FUNCTIONS.items():
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
