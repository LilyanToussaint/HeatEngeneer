"""Flow arrangement definition for a heat exchanger."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class FlowArrangement:
    """Describe the arrangement (co-current, counter-current, cross-flow, etc.)."""

    name: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Le nom d'agencement ne peut pas être vide.")

    def __str__(self) -> str:
        return self.name
