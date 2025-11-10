from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict
from CoolProp.CoolProp import PropsSI


@dataclass
class Fluid:
    """
    Représente un fluide + son état thermodynamique courant (CoolProp).

    Attributs (tous en SI) mis à jour par compute():

      temperature_K              [K]
      pressure_Pa                [Pa]
      density_kg_m3              [kg/m3]
      enthalpy_J_kg              [J/kg]
      entropy_J_kgK              [J/kg/K]
      cp_J_kgK                   [J/kg/K]
      cv_J_kgK                   [J/kg/K]
      conductivity_W_mK          [W/m/K]
      dynamic_viscosity_Pa_s     [Pa·s]
      prandtl_number             [-]
      vapor_quality              [-] (titre vapeur, si diphasique)
    """

    name: str                      # ex: "Water", "HEOS::Water"
    backend: Optional[str] = None  # optionnel si tu veux séparer backend/fluide

    # État courant
    temperature_K: Optional[float] = None
    pressure_Pa: Optional[float] = None
    density_kg_m3: Optional[float] = None
    enthalpy_J_kg: Optional[float] = None
    entropy_J_kgK: Optional[float] = None
    cp_J_kgK: Optional[float] = None
    cv_J_kgK: Optional[float] = None
    conductivity_W_mK: Optional[float] = None
    dynamic_viscosity_Pa_s: Optional[float] = None
    prandtl_number: Optional[float] = None
    vapor_quality: Optional[float] = None

    @property
    def identifier(self) -> str:
        """Identifiant CoolProp complet."""
        if self.backend and "::" not in self.name:
            return f"{self.backend}::{self.name}"
        return self.name

    def compute(self, key1: str, val1: float, key2: str, val2: float) -> "Fluide":
        """
        Met à jour l'état à partir de 2 grandeurs indépendantes CoolProp.

        Exemples:
            f.compute("T", 300.0, "P", 1e5)
            f.compute("P", 5e5, "H", 1e5)

        Clés autorisées (codes CoolProp):
            "T", "P", "H", "S", "D", "Q"
        """

        allowed = {"T", "P", "H", "S", "D", "Q"}
        if key1 not in allowed or key2 not in allowed:
            raise ValueError(f"Clés invalides: '{key1}', '{key2}'. Autorisées: {allowed}")
        if key1 == key2:
            raise ValueError("Les 2 clés doivent être différentes.")

        props = {
            "T":  "T",
            "P":  "P",
            "D":  "D",
            "H":  "H",
            "S":  "S",
            "C":  "C",        # Cp
            "O":  "O",        # Cv
            "L":  "L",        # k
            "V":  "V",        # mu
            "Pr": "Prandtl",  # Pr
            "Q":  "Q",        # titre
        }

        values: Dict[str, float] = {}
        for attr, cp_code in props.items():
            values[attr] = PropsSI(cp_code, key1, float(val1), key2, float(val2), self.identifier)

        # Mapping explicite vers des noms propres
        self.temperature_K          = values["T"]
        self.pressure_Pa            = values["P"]
        self.density_kg_m3          = values["D"]
        self.enthalpy_J_kg          = values["H"]
        self.entropy_J_kgK          = values["S"]
        self.cp_J_kgK               = values["C"]
        self.cv_J_kgK               = values["O"]
        self.conductivity_W_mK      = values["L"]
        self.dynamic_viscosity_Pa_s = values["V"]
        self.prandtl_number         = values["Pr"]
        self.vapor_quality          = values["Q"]

        return self