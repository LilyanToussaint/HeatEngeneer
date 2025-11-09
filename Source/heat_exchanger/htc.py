"""Heat-transfer coefficient correlation model."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from Source.Heat_transfer_coefficient import HeatTransferCoefficient


@dataclass(slots=True)
class HTCModel:
    """Wrap a heat-transfer coefficient correlation for an exchanger side."""

    correlation: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    _wrapper: HeatTransferCoefficient = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._wrapper = HeatTransferCoefficient(self.correlation)

    def compute(self, overrides: Dict[str, Any] | None = None) -> float:
        """Evaluate the correlation and return the convection coefficient."""

        kwargs = dict(self.parameters)
        if overrides:
            kwargs.update(overrides)
        result = self._wrapper.compute(**kwargs)
        if not result.valid:
            raise ValueError(result.message)
        return result.h

    @property
    def metadata(self) -> Dict[str, Any]:
        return {"correlation": self.correlation, "parameters": dict(self.parameters)}
