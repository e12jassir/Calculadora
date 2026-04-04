"""Constantes matemáticas y configuración de la calculadora científica."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class AppInfo:
    """Información de la aplicación."""
    NAME: str = "Calculadora Científica"
    VERSION: str = "2.0.0"
    ORGANIZATION: str = "ScientificCalc"


@dataclass(frozen=True)
class DisplayLimits:
    """Límites del display."""
    MAX_DIGITS: int = 15
    MAX_DISPLAY_LENGTH: int = 50
    SCIENTIFIC_THRESHOLD: float = 1e10
    MIN_SCIENTIFIC_THRESHOLD: float = 1e-10


@dataclass(frozen=True)
class MathConstants:
    """Constantes matemáticas disponibles."""
    PI: float = math.pi
    E: float = math.e
    TAU: float = math.tau
    PHI: float = (1 + math.sqrt(5)) / 2


CONSTANTS_DISPLAY = {
    'π': MathConstants.PI,
    'e': MathConstants.E,
    'τ': MathConstants.TAU,
    'φ': MathConstants.PHI,
}
