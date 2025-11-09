"""Registry of epsilon-NTU effectiveness relations."""

from __future__ import annotations

from typing import Callable, Dict

from .effectiveness_counterflow import effectiveness_counterflow
from .effectiveness_counterflow_eta_fin import effectiveness_counterflow_eta_fin
from .effectiveness_crossflow_mixed_cmax import effectiveness_crossflow_mixed_cmax
from .effectiveness_crossflow_mixed_cmin import effectiveness_crossflow_mixed_cmin
from .effectiveness_crossflow_unmixed import effectiveness_crossflow_unmixed
from .effectiveness_double_pipe_counterflow import effectiveness_double_pipe_counterflow
from .effectiveness_double_pipe_parallel import effectiveness_double_pipe_parallel
from .effectiveness_parallel import effectiveness_parallel
from .effectiveness_parallel_eta_fin import effectiveness_parallel_eta_fin
from .effectiveness_shell_and_tube_1_2 import effectiveness_shell_and_tube_1_2
from .effectiveness_shell_and_tube_2_4 import effectiveness_shell_and_tube_2_4
from .effectiveness_with_eta_fin import effectiveness_with_eta_fin


EffectivenessFunction = Callable[..., float]

EPSILON_FUNCTIONS: Dict[str, EffectivenessFunction] = {
    "parallel": effectiveness_parallel,
    "counterflow": effectiveness_counterflow,
    "shell_and_tube_1_2": effectiveness_shell_and_tube_1_2,
    "shell_and_tube_2_4": effectiveness_shell_and_tube_2_4,
    "crossflow_both_unmixed": effectiveness_crossflow_unmixed,
    "crossflow_mixed_cmax": effectiveness_crossflow_mixed_cmax,
    "crossflow_mixed_cmin": effectiveness_crossflow_mixed_cmin,
    "double_pipe_counterflow": effectiveness_double_pipe_counterflow,
    "double_pipe_parallel": effectiveness_double_pipe_parallel,
}

EPSILON_WITH_FIN_FUNCTIONS: Dict[str, EffectivenessFunction] = {
    "counterflow_eta_fin": effectiveness_counterflow_eta_fin,
    "parallel_eta_fin": effectiveness_parallel_eta_fin,
}

__all__ = ["EPSILON_FUNCTIONS", "EPSILON_WITH_FIN_FUNCTIONS", "EffectivenessFunction"]
