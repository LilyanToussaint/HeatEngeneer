"""Fluid property utilities powered by CoolProp."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Optional

from CoolProp.CoolProp import PropsSI


class FluidPropertyError(RuntimeError):
    """Raised when CoolProp fails to evaluate a requested property."""


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


class FluidProperties:
    """Helper around CoolProp to evaluate thermophysical properties."""

    #: Friendly names mapped to CoolProp input codes
    _INPUT_CODES: Mapping[str, str] = {
        "temperature": "T",
        "t": "T",
        "T": "T",
        "pressure": "P",
        "p": "P",
        "P": "P",
        "density": "D",
        "rho": "D",
        "D": "D",
        "specific_entropy": "S",
        "entropy": "S",
        "S": "S",
        "specific_enthalpy": "H",
        "enthalpy": "H",
        "H": "H",
        "quality": "Q",
        "x": "Q",
        "Q": "Q",
    }

    #: Mapping from CoolProp input codes to canonical friendly names
    _CANONICAL_INPUTS: Mapping[str, str] = {
        "T": "temperature",
        "P": "pressure",
        "D": "density",
        "S": "entropy",
        "H": "enthalpy",
        "Q": "quality",
    }

    #: Friendly names mapped to CoolProp output codes
    _OUTPUT_CODES: Mapping[str, str] = {
        "temperature": "T",
        "T": "T",
        "pressure": "P",
        "P": "P",
        "density": "D",
        "D": "D",
        "enthalpy": "H",
        "H": "H",
        "entropy": "S",
        "S": "S",
        "internal_energy": "U",
        "U": "U",
        "cp": "C",
        "C": "C",
        "cv": "O",
        "O": "O",
        "thermal_conductivity": "L",
        "L": "L",
        "dynamic_viscosity": "V",
        "V": "V",
        "prandtl": "Prandtl",
        "Prandtl": "Prandtl",
        "speed_of_sound": "A",
        "A": "A",
        "quality": "Q",
        "Q": "Q",
        "compressibility_factor": "Z",
        "Z": "Z",
    }

    #: Properties returned by default when querying a state.
    DEFAULT_OUTPUTS = (
        "temperature",
        "pressure",
        "density",
        "enthalpy",
        "entropy",
        "cp",
        "cv",
        "thermal_conductivity",
        "dynamic_viscosity",
        "prandtl",
    )

    def __init__(self, fluid: str, backend: Optional[str] = None) -> None:
        self.fluid = fluid
        self.backend = backend

    @property
    def identifier(self) -> str:
        """Full CoolProp identifier, including backend when provided."""

        if self.backend:
            return f"{self.backend}::{self.fluid}"
        return self.fluid

    @classmethod
    def available_outputs(cls) -> Iterable[str]:
        return cls._OUTPUT_CODES.keys()

    @classmethod
    def _resolve_property_code(cls, name: str, mapping: Mapping[str, str]) -> str:
        try:
            return mapping[name]
        except KeyError as exc:
            raise ValueError(f"Unknown property key '{name}'.") from exc

    @classmethod
    def _normalize_inputs(cls, inputs: Mapping[str, float]) -> Dict[str, float]:
        normalized: Dict[str, float] = {}
        for key, value in inputs.items():
            code = cls._resolve_property_code(key, cls._INPUT_CODES)
            normalized[code] = float(value)
        if len(normalized) != 2:
            raise ValueError(
                "Exactly two independent state variables are required (e.g. T & P)."
            )
        return normalized

    def _evaluate_outputs(
        self,
        input_codes: Mapping[str, float],
        outputs: Iterable[str],
    ) -> Dict[str, float]:
        items = list(input_codes.items())
        (in1, val1), (in2, val2) = items[0], items[1]
        evaluated: Dict[str, float] = {}
        for friendly_name in outputs:
            code = self._resolve_property_code(friendly_name, self._OUTPUT_CODES)
            try:
                evaluated[friendly_name] = float(
                    PropsSI(code, in1, val1, in2, val2, self.identifier)
                )
            except ValueError as exc:
                raise FluidPropertyError(str(exc)) from exc
        return evaluated

    def properties_at(
        self,
        *,
        outputs: Optional[Iterable[str]] = None,
        **inputs: float,
    ) -> FluidState:
        """Evaluate the requested CoolProp properties for the given state."""

        if not inputs:
            raise ValueError("Provide two independent state properties (e.g. T=..., P=...).")
        normalized = self._normalize_inputs(inputs)
        requested_outputs = tuple(outputs) if outputs else self.DEFAULT_OUTPUTS
        evaluated = self._evaluate_outputs(normalized, requested_outputs)
        readable_inputs = {
            self._CANONICAL_INPUTS.get(code, code): value
            for code, value in normalized.items()
        }
        return FluidState(
            fluid=self.fluid,
            backend=self.backend,
            inputs=readable_inputs,
            properties=evaluated,
        )

    def get_property(self, output: str, **inputs: float) -> float:
        """Convenience helper returning a single property value."""

        state = self.properties_at(outputs=(output,), **inputs)
        return state[output]
