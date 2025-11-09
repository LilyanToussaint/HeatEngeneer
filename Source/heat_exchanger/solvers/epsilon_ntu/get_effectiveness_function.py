"""Lookup helper for epsilon-NTU effectiveness relations."""
from __future__ import annotations

from typing import Callable, Tuple

from .registry import EPSILON_FUNCTIONS, EPSILON_WITH_FIN_FUNCTIONS

EffectivenessLookup = Tuple[Callable[..., float], bool]


def get_effectiveness_function(name: str) -> EffectivenessLookup:
    """Return the effectiveness function associated with the provided name."""

    if name in EPSILON_FUNCTIONS:
        return EPSILON_FUNCTIONS[name], False
    if name in EPSILON_WITH_FIN_FUNCTIONS:
        return EPSILON_WITH_FIN_FUNCTIONS[name], True
    raise ValueError(
        "Configuration epsilon-NTU inconnue '%s'. Dispos: %s" % (
            name,
            list(EPSILON_FUNCTIONS) + list(EPSILON_WITH_FIN_FUNCTIONS),
        )
    )


__all__ = ["get_effectiveness_function", "EffectivenessLookup"]
