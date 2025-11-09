"""Fluid property helpers leveraging CoolProp."""
from __future__ import annotations

from .BaseFluid import BaseFluid
from .ConstantFluid import ConstantFluid
from .FluidPropertyError import FluidPropertyError
from .FluidState import FluidState

try:  # pragma: no cover - optional dependency
    from .CoolPropFluid import CoolPropFluid

    FluidProperties = CoolPropFluid
    _COOLPROP_AVAILABLE = True
except ModuleNotFoundError as exc:  # pragma: no cover - environment guard
    if exc.name != "CoolProp":
        raise

    class CoolPropFluid:  # type: ignore[empty-body]
        def __init__(self, *_: object, **__: object) -> None:
            raise ModuleNotFoundError(
                "CoolProp est requis pour CoolPropFluid mais n'est pas installé."
            )

    class FluidProperties(CoolPropFluid):  # type: ignore[misc]
        """Backward-compatible alias raising the same error."""

    _COOLPROP_AVAILABLE = False

__all__ = [
    "BaseFluid",
    "ConstantFluid",
    "CoolPropFluid",
    "FluidProperties",
    "FluidPropertyError",
    "FluidState",
]
