"""Demonstrate the three heat-exchanger calculation approaches."""
from __future__ import annotations

import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Source import (  # noqa: E402  (import after sys.path tweaks)
    Methode1D,
    MethodeLMTD,
    MethodeNTU,
    StreamConditions,
)


HOT_STREAM = StreamConditions(
    m_dot=0.35,
    cp=3900.0,
    inlet_temp=380.0,
    correlation_kwargs={"Re": 4.8e4, "Pr": 5.5, "k": 0.63, "d_i": 0.018},
    fin_efficiency=0.93,
)

COLD_STREAM = StreamConditions(
    m_dot=0.5,
    cp=4180.0,
    inlet_temp=295.0,
    correlation_kwargs={"Re": 3.2e4, "Pr": 6.4, "k": 0.58, "d_i": 0.018},
    fin_efficiency=0.9,
)

AREA = 7.5


def run_ntu() -> None:
    method = MethodeNTU("gnielinski_internal")
    result = method.compute(HOT_STREAM, COLD_STREAM, area=AREA, configuration="counterflow")
    print("=== Méthode epsilon-NTU ===")
    print(f"NTU       : {result.NTU:.3f}")
    print(f"epsilon   : {result.epsilon:.3f}")
    print(f"Q (kW)    : {result.Q / 1000:.2f}")
    print(f"U global  : {result.U:.1f} W/m²/K")
    print(f"T_hot_out : {result.hot_outlet_temp:.1f} K")
    print(f"T_cold_out: {result.cold_outlet_temp:.1f} K\n")


def run_lmtd() -> None:
    method = MethodeLMTD("gnielinski_internal")
    ntu = MethodeNTU("gnielinski_internal").compute(
        HOT_STREAM, COLD_STREAM, area=AREA, configuration="counterflow"
    )
    result = method.compute(
        HOT_STREAM,
        COLD_STREAM,
        area=AREA,
        hot_outlet_temp=ntu.hot_outlet_temp,
        cold_outlet_temp=ntu.cold_outlet_temp,
    )
    print("=== Méthode LMTD ===")
    print(f"LMTD corr : {result.lmtd_corrected:.2f} K")
    print(f"Q (kW)    : {result.Q / 1000:.2f}")
    print(f"Facteur F : {result.correction_factor:.3f}\n")


def run_1d() -> None:
    method = Methode1D("gnielinski_internal")
    result = method.compute(HOT_STREAM, COLD_STREAM, area=AREA, segments=30)
    print("=== Modèle 1D segmenté ===")
    print(f"Segments : {len(result.temperature_profile_hot)}")
    print(f"Q (kW)   : {result.heat_duty / 1000:.2f}")
    print(f"T_hot_out: {result.hot_outlet_temp:.1f} K")
    print(f"T_cold_out: {result.cold_outlet_temp:.1f} K")


if __name__ == "__main__":
    run_ntu()
    run_lmtd()
    run_1d()
