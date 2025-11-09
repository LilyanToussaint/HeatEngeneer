"""Fluid implementation with temperature-independent properties."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping

from .BaseFluid import BaseFluid
from .FluidState import FluidState


@dataclass
class ConstantFluid(BaseFluid):
    """Return pre-defined constant properties regardless of the state."""

    name: str
    properties: Mapping[str, float] = field(default_factory=dict)
    backend: str | None = None

    def __post_init__(self) -> None:
        super().__init__(self.name)
        self._properties = {k: float(v) for k, v in self.properties.items()}

    def properties_at(
        self,
        *,
        outputs: Iterable[str] | None = None,
        **inputs: float,
    ) -> FluidState:
        if inputs:
            raise ValueError(
                "ConstantFluid ne supporte pas de variables d'état (valeurs constantes)."
            )

        if outputs is None:
            data = dict(self._properties)
        else:
            data = {}
            for key in outputs:
                try:
                    data[key] = self._properties[key]
                except KeyError as exc:
                    raise KeyError(f"Propriété '{key}' indisponible pour {self.name}.") from exc

        return FluidState(fluid=self.name, backend=self.backend, inputs={}, properties=data)

    def get_property(self, output: str, **inputs: float) -> float:
        state = self.properties_at(outputs=(output,), **inputs)
        return state[output]


__all__ = ["ConstantFluid"]
