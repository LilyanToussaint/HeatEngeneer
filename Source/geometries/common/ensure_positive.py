"""Validation helpers shared by geometry classes."""
from __future__ import annotations


def ensure_positive(value: float, name: str) -> None:
    """Raise :class:`ValueError` if *value* is not strictly positive.

    Args:
        value: Numeric value to validate.
        name: Name of the argument being validated for error messages.
    """

    if value <= 0:
        raise ValueError(f"{name} doit être > 0.")
