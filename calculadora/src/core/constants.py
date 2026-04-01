"""
Constantes matemáticas y configuración de la calculadora.
"""

import math

# Constantes matemáticas
CONSTANTS = {
    'π': math.pi,
    'e': math.e,
    'τ': math.tau,
    'φ': (1 + math.sqrt(5)) / 2,
}

# Límites del display
MAX_DIGITS = 15
MAX_DISPLAY_LENGTH = 50

# Formato de números
SCIENTIFIC_THRESHOLD = 1e10
MIN_SCIENTIFIC_THRESHOLD = 1e-10
