"""Tests unitarios para el conversor de unidades."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.converter import UnitConverter


class TestUnitConverter:
    def test_km_to_m(self):
        result = UnitConverter.convert(1, 'Longitud', 'km', 'm')
        assert abs(result - 1000) < 1e-6

    def test_m_to_km(self):
        result = UnitConverter.convert(1000, 'Longitud', 'm', 'km')
        assert abs(result - 1) < 1e-6

    def test_miles_to_km(self):
        result = UnitConverter.convert(1, 'Longitud', 'mi', 'km')
        assert abs(result - 1.609344) < 1e-4

    def test_kg_to_lb(self):
        result = UnitConverter.convert(1, 'Masa', 'kg', 'lb')
        assert abs(result - 2.20462) < 1e-3

    def test_celsius_to_fahrenheit(self):
        result = UnitConverter.convert(100, 'Temperatura', '°C', '°F')
        assert abs(result - 212) < 1e-6

    def test_fahrenheit_to_celsius(self):
        result = UnitConverter.convert(32, 'Temperatura', '°F', '°C')
        assert abs(result - 0) < 1e-6

    def test_degrees_to_radians(self):
        import math
        result = UnitConverter.convert(180, 'Ángulos', 'deg', 'rad')
        assert abs(result - math.pi) < 1e-6

    def test_hours_to_seconds(self):
        result = UnitConverter.convert(1, 'Tiempo', 'h', 's')
        assert abs(result - 3600) < 1e-6

    def test_invalid_category(self):
        try:
            UnitConverter.convert(1, 'Invalid', 'a', 'b')
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_get_categories(self):
        cats = UnitConverter.get_categories()
        assert 'Longitud' in cats
        assert 'Masa' in cats
        assert 'Temperatura' in cats
