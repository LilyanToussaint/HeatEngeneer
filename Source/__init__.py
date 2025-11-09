"""Heat transfer computation utilities."""

from .common import (
    mass_flow_from_velocity,
    prandtl_number,
    reynolds_number,
    velocity_from_mass_flow,
)
try:
    from .Fluid import FluidProperties, FluidPropertyError, FluidState
    _COOLPROP_AVAILABLE = True
except ModuleNotFoundError as exc:  # pragma: no cover - environment guard
    if exc.name != "CoolProp":
        raise

    class FluidPropertyError(RuntimeError):
        """Raised when CoolProp is unavailable."""

    class FluidState:  # type: ignore[empty-body]
        pass

    class FluidProperties:  # type: ignore[empty-body]
        def __init__(self, *_: object, **__: object) -> None:
            raise ModuleNotFoundError(
                "CoolProp est requis pour FluidProperties mais n'est pas installé."
            )

    _COOLPROP_AVAILABLE = False
from .heat_exchanger import (
    DPModel,
    EpsilonNTUSolver,
    FlowArrangement,
    FluidModel,
    Geometry,
    HeatExchanger,
    HeatExchangerSolver,
    HTCModel,
    HXSide,
    LMTDResult,
    LMTDSolver,
    NTUResult,
    OneDResult,
    OneDimensionalSolver,
    Wall,
    EPSILON_FUNCTIONS,
    EPSILON_WITH_FIN_FUNCTIONS,
    get_effectiveness_function,
)
from .Heat_transfer_coefficient import (
    HeatTransferCoefficient,
    HTCResult,
    hx_compact_performance,
)
from .loss_pressure import PressureLossCorrelation, PressureLossResult
from .materials import Material, MaterialProperties

__all__ = [
    "FluidProperties",
    "FluidPropertyError",
    "FluidState",
    "HeatExchanger",
    "FlowArrangement",
    "HXSide",
    "FluidModel",
    "Geometry",
    "HTCModel",
    "DPModel",
    "Wall",
    "HeatExchangerSolver",
    "EpsilonNTUSolver",
    "NTUResult",
    "LMTDSolver",
    "LMTDResult",
    "OneDimensionalSolver",
    "OneDResult",
    "EPSILON_FUNCTIONS",
    "EPSILON_WITH_FIN_FUNCTIONS",
    "get_effectiveness_function",
    "HeatTransferCoefficient",
    "HTCResult",
    "hx_compact_performance",
    "PressureLossCorrelation",
    "PressureLossResult",
    "Material",
    "MaterialProperties",
    "reynolds_number",
    "prandtl_number",
    "velocity_from_mass_flow",
    "mass_flow_from_velocity",
]
