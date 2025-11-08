"""High-level wrapper around pressure-loss correlations."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from .correlations import LOSS_PRESSURE_CORRELATIONS


@dataclass
class PressureLossResult:
    delta_p: float
    correlation: str
    valid: bool = True
    message: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)
    correlation_meta: Dict[str, Any] = field(default_factory=dict)


class PressureLossCorrelation:
    """Wrapper to evaluate registered pressure-loss correlations."""

    def __init__(self, correlation: str):
        if correlation not in LOSS_PRESSURE_CORRELATIONS:
            raise ValueError(
                "Corrélation '{}' inconnue. Dispos: {}".format(
                    correlation, list(LOSS_PRESSURE_CORRELATIONS.keys())
                )
            )
        self.correlation_name = correlation
        self.func = LOSS_PRESSURE_CORRELATIONS[correlation]
        self.metadata = dict(getattr(self.func, "metadata", {}))

    @staticmethod
    def available() -> list[str]:
        return list(LOSS_PRESSURE_CORRELATIONS.keys())

    def compute(self, **kwargs: Any) -> PressureLossResult:
        try:
            delta_p = float(self.func(**kwargs))
            return PressureLossResult(
                delta_p=delta_p,
                correlation=self.correlation_name,
                valid=True,
                message="OK",
                meta=kwargs,
                correlation_meta=dict(self.metadata),
            )
        except ValueError as exc:
            return PressureLossResult(
                delta_p=float("nan"),
                correlation=self.correlation_name,
                valid=False,
                message=str(exc),
                meta=kwargs,
                correlation_meta=dict(self.metadata),
            )
        except Exception as exc:  # pylint: disable=broad-except
            return PressureLossResult(
                delta_p=float("nan"),
                correlation=self.correlation_name,
                valid=False,
                message=f"Erreur interne: {exc}",
                meta=kwargs,
                correlation_meta=dict(self.metadata),
            )


__all__ = ["PressureLossCorrelation", "PressureLossResult"]
