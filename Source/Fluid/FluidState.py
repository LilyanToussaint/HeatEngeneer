"""Dataclass capturing a fluid state and evaluated properties."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional


@dataclass(frozen=True)
class FluidState:
    """Container for a fluid state and its evaluated properties."""

    fluid: str
    backend: Optional[str]
    inputs: Mapping[str, float] = field(default_factory=dict)
    properties: Mapping[str, float] = field(default_factory=dict)

    def __getitem__(self, key: str) -> float:
        return self.properties[key]

    def get(self, key: str, default: Optional[float] = None) -> Optional[float]:
        return self.properties.get(key, default)
