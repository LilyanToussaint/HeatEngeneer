"""Abstract base class for fluid property providers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable


class BaseFluid(ABC):
    """Define the minimal interface required by the fluid helpers."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def properties_at(
        self,
        *,
        outputs: Iterable[str] | None = None,
        **inputs: float,
    ) -> "FluidState":
        """Return a structured set of properties for the requested state."""

    @abstractmethod
    def get_property(self, output: str, **inputs: float) -> float:
        """Return a single thermophysical property."""


# Local import at bottom to avoid circular dependency in type checkers
from .FluidState import FluidState  # noqa: E402  (circular import guard)
