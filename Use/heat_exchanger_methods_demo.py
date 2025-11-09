"""Demonstration script for the refactored heat-exchanger API."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source import (  # noqa: E402  (import after sys.path tweaks)
    EpsilonNTUSolver,
    FlowArrangement,
    FluidModel,
    Geometry,
    HeatExchanger,
    HXSide,
    HTCModel,
    LMTDSolver,
    OneDimensionalSolver,
    Wall,
)

hot_side = HXSide(
    label="hot",
    fluid=FluidModel(name="huile", heat_capacity=3900.0),
    mass_flow=0.35,
    inlet_temp=380.0,
    geometry=Geometry(area=7.5, hydraulic_diameter=0.018),
    htc_model=HTCModel(
        correlation="gnielinski_internal",
        parameters={"Re": 4.8e4, "Pr": 5.5, "k": 0.63, "d_i": 0.018},
    ),
)

cold_side = HXSide(
    label="cold",
    fluid=FluidModel(name="eau", heat_capacity=4180.0),
    mass_flow=0.5,
    inlet_temp=295.0,
    geometry=Geometry(area=7.5, hydraulic_diameter=0.018),
    htc_model=HTCModel(
        correlation="gnielinski_internal",
        parameters={"Re": 3.2e4, "Pr": 6.4, "k": 0.58, "d_i": 0.018},
    ),
)

EXCHANGER = HeatExchanger(
    hot=hot_side,
    cold=cold_side,
    arrangement=FlowArrangement("counterflow"),
    wall=Wall(thermal_resistance=0.0),
)
AREA = 7.5


def run_ntu() -> None:
    solver = EpsilonNTUSolver()
    result = solver.solve(EXCHANGER, area=AREA)
    print("=== Méthode epsilon-NTU ===")
    print(f"NTU       : {result.NTU:.3f}")
    print(f"epsilon   : {result.epsilon:.3f}")
    print(f"Q (kW)    : {result.Q / 1000:.2f}")
    print(f"U global  : {result.U:.1f} W/m²/K")
    print(f"T_hot_out : {result.hot_outlet_temp:.1f} K")
    print(f"T_cold_out: {result.cold_outlet_temp:.1f} K\n")


def run_lmtd() -> None:
    ntu_result = EpsilonNTUSolver().solve(EXCHANGER, area=AREA)
    solver = LMTDSolver()
    result = solver.solve(
        EXCHANGER,
        area=AREA,
        hot_outlet_temp=ntu_result.hot_outlet_temp,
        cold_outlet_temp=ntu_result.cold_outlet_temp,
    )
    print("=== Méthode LMTD ===")
    print(f"LMTD corr : {result.delta_t_lm:.2f} K")
    print(f"Q (kW)    : {result.Q / 1000:.2f}")
    print(f"Facteur F : {result.correction_factor:.3f}\n")


def run_1d() -> None:
    solver = OneDimensionalSolver()
    result = solver.solve(EXCHANGER, area=AREA, segments=30)
    print("=== Modèle 1D segmenté ===")
    print(f"Segments : {result.segments}")
    print(f"Q (kW)   : {result.heat_duty / 1000:.2f}")
    print(f"T_hot_out: {result.hot_outlet_temp:.1f} K")
    print(f"T_cold_out: {result.cold_outlet_temp:.1f} K")


if __name__ == "__main__":
    run_ntu()
    run_lmtd()
    run_1d()
