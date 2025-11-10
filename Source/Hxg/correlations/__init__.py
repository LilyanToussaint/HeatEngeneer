"""Placeholder registry for epsilon-NTU correlations."""

from .EpsNTU_CounterFlow import eps_counterflow
from .EpsNTU_CrossFlow_Mixed import eps_crossflow_mixed
from .EpsNTU_CrossFlow_Unmixed import eps_crossflow_unmixed
from .EpsNTU_ParallelFlow import eps_parallel
from .EpsNTU_ShellAndTube import eps_shell_and_tube

__all__ = [
    "eps_counterflow",
    "eps_parallel",
    "eps_crossflow_mixed",
    "eps_crossflow_unmixed",
    "eps_shell_and_tube",
]
