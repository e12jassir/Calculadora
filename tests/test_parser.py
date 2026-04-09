"""Tests unitarios para el parser matemático."""

import math
import pytest

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.parser import ExpressionParser, MathError, ParseError


@pytest.fixture
def parser():
    return ExpressionParser(angle_mode='deg')


class TestBasicOperations:
    def test_addition(self, parser):
        assert parser.evaluate("2 + 3") == 5.0

    def test_subtraction(self, parser):
        assert parser.evaluate("10 - 4") == 6.0

    def test_multiplication(self, parser):
        assert parser.evaluate("3 * 4") == 12.0

    def test_division(self, parser):
        assert parser.evaluate("15 / 3") == 5.0

    def test_division_by_zero(self, parser):
        with pytest.raises(MathError):
            parser.evaluate("1 / 0")

    def test_power(self, parser):
        assert parser.evaluate("2 ^ 3") == 8.0

    def test_power_right_associative(self, parser):
        assert parser.evaluate("2 ^ 3 ^ 2") == 512.0

    def test_order_of_operations(self, parser):
        assert parser.evaluate("2 + 3 * 4") == 14.0

    def test_parentheses(self, parser):
        assert parser.evaluate("(2 + 3) * 4") == 20.0

    def test_nested_parentheses(self, parser):
        assert parser.evaluate("((2 + 3) * (4 - 1))") == 15.0


class TestTrigonometric:
    def test_sin_deg(self, parser):
        assert abs(parser.evaluate("sin(30)") - 0.5) < 1e-10

    def test_cos_deg(self, parser):
        assert abs(parser.evaluate("cos(60)") - 0.5) < 1e-10

    def test_tan_deg(self, parser):
        assert abs(parser.evaluate("tan(45)") - 1.0) < 1e-10

    def test_asin_deg(self, parser):
        assert abs(parser.evaluate("asin(0.5)") - 30.0) < 1e-10

    def test_sin_rad(self):
        parser = ExpressionParser(angle_mode='rad')
        assert abs(parser.evaluate("sin(1.5707963267948966)") - 1.0) < 1e-10


class TestLogarithmic:
    def test_ln(self, parser):
        assert abs(parser.evaluate("ln(2.718281828459045)") - 1.0) < 1e-10

    def test_log10(self, parser):
        assert abs(parser.evaluate("log(100)") - 2.0) < 1e-10

    def test_log2(self, parser):
        assert abs(parser.evaluate("log2(8)") - 3.0) < 1e-10


class TestFunctions:
    def test_sqrt(self, parser):
        assert parser.evaluate("sqrt(16)") == 4.0

    def test_cbrt(self, parser):
        assert abs(parser.evaluate("cbrt(27)") - 3.0) < 1e-10

    def test_abs(self, parser):
        assert parser.evaluate("abs(-5)") == 5.0

    def test_ceil(self, parser):
        assert parser.evaluate("ceil(3.2)") == 4.0

    def test_floor(self, parser):
        assert parser.evaluate("floor(3.8)") == 3.0

    def test_exp(self, parser):
        assert abs(parser.evaluate("exp(0)") - 1.0) < 1e-10


class TestConstants:
    def test_pi(self, parser):
        assert abs(parser.evaluate("pi") - math.pi) < 1e-10

    def test_e(self, parser):
        assert abs(parser.evaluate("e") - math.e) < 1e-10

    def test_tau(self, parser):
        assert abs(parser.evaluate("tau") - math.tau) < 1e-10


class TestFactorial:
    def test_factorial(self, parser):
        assert parser.evaluate("5!") == 120.0

    def test_factorial_zero(self, parser):
        assert parser.evaluate("0!") == 1.0

    def test_factorial_negative(self, parser):
        with pytest.raises(MathError):
            parser.evaluate("(-1)!")


class TestPercent:
    def test_percent(self, parser):
        assert parser.evaluate("50%") == 0.5

    def test_percent_in_expression(self, parser):
        assert parser.evaluate("200 * 50%") == 100.0


class TestImplicitMultiplication:
    def test_number_paren(self, parser):
        assert parser.evaluate("2(3 + 4)") == 14.0

    def test_number_pi(self, parser):
        assert abs(parser.evaluate("2pi") - 2 * math.pi) < 1e-10

    def test_number_function(self, parser):
        assert parser.evaluate("2sqrt(9)") == 6.0

    def test_paren_constant(self, parser):
        assert abs(parser.evaluate("(2+1)pi") - (3 * math.pi)) < 1e-10

    def test_constant_paren(self, parser):
        assert abs(parser.evaluate("pi(2)") - (2 * math.pi)) < 1e-10

    def test_paren_function(self, parser):
        assert abs(parser.evaluate("(2)sin(30)") - 1.0) < 1e-10


class TestEdgeCases:
    def test_empty_expression(self, parser):
        with pytest.raises(ParseError):
            parser.evaluate("")

    def test_negative_number(self, parser):
        assert parser.evaluate("-5") == -5.0

    def test_double_negative(self, parser):
        assert parser.evaluate("--5") == 5.0

    def test_decimal(self, parser):
        assert parser.evaluate("0.5 + 0.5") == 1.0

    def test_scientific_notation(self, parser):
        assert parser.evaluate("1e3") == 1000.0

    def test_complex_expression(self, parser):
        result = parser.evaluate("2 + 3 * 4 - 6 / 2")
        assert result == 11.0
