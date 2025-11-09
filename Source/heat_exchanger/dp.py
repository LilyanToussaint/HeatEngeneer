"""Pressure drop correlation model placeholder."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(slots=True)
class DPModel:
    """Represent a pressure-drop model used by a heat-exchanger side."""

    correlation: str | None = None
    parameters: Dict[str, Any] = field(default_factory=dict)

    def compute(self, overrides: Dict[str, Any] | None = None) -> float:
        """Return the predicted pressure drop (if a correlation is configured)."""

        if self.correlation is None:
            raise NotImplementedError("Aucune corrélation de perte de charge définie.")
        kwargs = dict(self.parameters)
        if overrides:
            kwargs.update(overrides)
        # Placeholder: the actual implementation should call the pressure-loss package.
        raise NotImplementedError("Le calcul de la perte de charge n'est pas encore implémenté.")
