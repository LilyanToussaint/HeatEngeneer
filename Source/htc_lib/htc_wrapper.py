"""High-level wrapper around heat-transfer coefficient correlations."""
from dataclasses import dataclass, field
from typing import Any, Dict

from .correlations import HTC_CORRELATIONS


@dataclass
class HTCResult:
    h: float
    correlation: str
    valid: bool = True
    message: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)


class HeatTransferCoefficient:
    """Wrapper pour appeler une corrélation de HTC."""

    def __init__(self, correlation: str):
        if correlation not in HTC_CORRELATIONS:
            raise ValueError(
                f"Corrélation '{correlation}' inconnue. Dispos: {list(HTC_CORRELATIONS.keys())}"
            )
        self.correlation_name = correlation
        self.func = HTC_CORRELATIONS[correlation]

    @staticmethod
    def available() -> list[str]:
        return list(HTC_CORRELATIONS.keys())

    def compute(self, **kwargs: Any) -> HTCResult:
        try:
            h = float(self.func(**kwargs))
            return HTCResult(
                h=h,
                correlation=self.correlation_name,
                valid=True,
                message="OK",
                meta=kwargs,
            )
        except ValueError as exc:
            return HTCResult(
                h=float("nan"),
                correlation=self.correlation_name,
                valid=False,
                message=str(exc),
                meta=kwargs,
            )
        except Exception as exc:  # pylint: disable=broad-except
            return HTCResult(
                h=float("nan"),
                correlation=self.correlation_name,
                valid=False,
                message=f"Erreur interne: {exc}",
                meta=kwargs,
            )


__all__ = ["HeatTransferCoefficient", "HTCResult"]
