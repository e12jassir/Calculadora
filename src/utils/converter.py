"""Conversor de unidades integrado en la calculadora."""

from dataclasses import dataclass
from typing import Callable, Dict, Tuple


@dataclass
class UnitInfo:
    """Información de una unidad."""
    name: str
    symbol: str
    to_base: Callable[[float], float]
    from_base: Callable[[float], float]


class UnitConverter:
    """Conversor de unidades soportadas."""

    CATEGORIES: Dict[str, Dict[str, UnitInfo]] = {
        'Longitud': {
            'm': UnitInfo('Metro', 'm', lambda x: x, lambda x: x),
            'km': UnitInfo('Kilómetro', 'km', lambda x: x * 1000, lambda x: x / 1000),
            'cm': UnitInfo('Centímetro', 'cm', lambda x: x / 100, lambda x: x * 100),
            'mm': UnitInfo('Milímetro', 'mm', lambda x: x / 1000, lambda x: x * 1000),
            'mi': UnitInfo('Milla', 'mi', lambda x: x * 1609.344, lambda x: x / 1609.344),
            'yd': UnitInfo('Yarda', 'yd', lambda x: x * 0.9144, lambda x: x / 0.9144),
            'ft': UnitInfo('Pie', 'ft', lambda x: x * 0.3048, lambda x: x / 0.3048),
            'in': UnitInfo('Pulgada', 'in', lambda x: x * 0.0254, lambda x: x / 0.0254),
        },
        'Masa': {
            'kg': UnitInfo('Kilogramo', 'kg', lambda x: x, lambda x: x),
            'g': UnitInfo('Gramo', 'g', lambda x: x / 1000, lambda x: x * 1000),
            'mg': UnitInfo('Miligramo', 'mg', lambda x: x / 1e6, lambda x: x * 1e6),
            'lb': UnitInfo('Libra', 'lb', lambda x: x * 0.453592, lambda x: x / 0.453592),
            'oz': UnitInfo('Onza', 'oz', lambda x: x * 0.0283495, lambda x: x / 0.0283495),
            't': UnitInfo('Tonelada', 't', lambda x: x * 1000, lambda x: x / 1000),
        },
        'Temperatura': {
            '°C': UnitInfo('Celsius', '°C', lambda x: x, lambda x: x),
            '°F': UnitInfo('Fahrenheit', '°F', lambda x: (x - 32) * 5 / 9, lambda x: x * 9 / 5 + 32),
            'K': UnitInfo('Kelvin', 'K', lambda x: x - 273.15, lambda x: x + 273.15),
        },
        'Ángulos': {
            'deg': UnitInfo('Grados', '°', lambda x: x, lambda x: x),
            'rad': UnitInfo('Radianes', 'rad',
                            lambda x: x * 180 / 3.141592653589793,
                            lambda x: x * 3.141592653589793 / 180),
            'grad': UnitInfo('Gradianes', 'grad',
                             lambda x: x * 0.9, lambda x: x / 0.9),
        },
        'Tiempo': {
            's': UnitInfo('Segundo', 's', lambda x: x, lambda x: x),
            'min': UnitInfo('Minuto', 'min', lambda x: x * 60, lambda x: x / 60),
            'h': UnitInfo('Hora', 'h', lambda x: x * 3600, lambda x: x / 3600),
            'ms': UnitInfo('Milisegundo', 'ms', lambda x: x / 1000, lambda x: x * 1000),
        },
    }

    @classmethod
    def get_categories(cls) -> list:
        return list(cls.CATEGORIES.keys())

    @classmethod
    def get_units(cls, category: str) -> Dict[str, UnitInfo]:
        return cls.CATEGORIES.get(category, {})

    @classmethod
    def convert(
        cls,
        value: float,
        category: str,
        from_unit: str,
        to_unit: str,
    ) -> float:
        """Convierte un valor entre unidades de la misma categoría."""
        units = cls.CATEGORIES.get(category)
        if not units:
            raise ValueError(f"Categoría '{category}' no encontrada")

        if from_unit not in units or to_unit not in units:
            raise ValueError(f"Unidad no encontrada en '{category}'")

        base_value = units[from_unit].to_base(value)
        return units[to_unit].from_base(base_value)
