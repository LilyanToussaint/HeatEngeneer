"""Abstract solver base for heat exchangers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .heat_exchanger import HeatExchanger


class SolverResult(Protocol):
    epsilon: float
    Q: float


@dataclass(slots=True)
class HeatExchangerSolver:
    """Base solver class."""

    name: str

    def solve(self, exchanger: HeatExchanger, area: float, **kwargs: Any) -> SolverResult:
        raise NotImplementedError
