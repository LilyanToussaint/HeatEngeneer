"""Custom exception raised when a fluid property cannot be evaluated."""


class FluidPropertyError(RuntimeError):
    """Raised when the property backend fails."""


__all__ = ["FluidPropertyError"]
