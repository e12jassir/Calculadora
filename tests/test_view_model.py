import pytest
from src.core.parser import ExpressionParser
from src.core.history import HistoryManager
from src.core.view_model import CalculatorViewModel


@pytest.fixture
def calc_setup():
    """Fixture to provide a fresh ViewModel for each test."""
    parser = ExpressionParser(angle_mode="deg")
    history = HistoryManager()
    vm = CalculatorViewModel(parser, history)
    return vm


class TestCalculatorViewModel:
    """Tests for the CalculatorViewModel logic."""

    def test_initial_state(self, calc_setup):
        vm = calc_setup
        assert vm.display_expression == ""
        assert vm.display_result == "0"
        assert vm.current_angle_mode == "DEG"
        assert not vm.is_second_mode

    def test_add_numbers(self, calc_setup):
        vm = calc_setup
        vm.add_number("1")
        vm.add_number("2")
        vm.add_number("3")
        assert vm.display_expression == "123"

    def test_decimal_behavior(self, calc_setup):
        vm = calc_setup
        vm.add_number("1")
        vm.add_decimal()
        vm.add_number("2")
        vm.add_decimal()  # Should be ignored
        assert vm.display_expression == "1.2"

        vm.clear()
        vm.add_decimal()  # Should start with 0.
        assert vm.display_expression == "0."

    def test_operator_behavior(self, calc_setup):
        vm = calc_setup
        vm.add_number("5")
        vm.add_operator("+")
        vm.add_operator("*")  # Replace + with *
        assert vm.display_expression == "5*"

        vm.add_number("2")
        vm.add_operator("-")
        vm.add_operator("-")  # Replace - with -
        assert vm.display_expression == "5*2-"

    def test_basic_calculation(self, calc_setup):
        vm = calc_setup
        vm.add_number("1")
        vm.add_operator("+")
        vm.add_number("2")
        result = vm.calculate()
        assert result == "3"
        assert vm.display_result == "3"
        assert vm.display_expression == ""

    def test_order_of_operations(self, calc_setup):
        vm = calc_setup
        # 2 + 3 * 4 = 14
        vm.add_number("2")
        vm.add_operator("+")
        vm.add_number("3")
        vm.add_operator("*")
        vm.add_number("4")
        assert vm.calculate() == "14"

    def test_power_associativity(self, calc_setup):
        vm = calc_setup
        # 2^3^2 = 2^(3^2) = 2^9 = 512
        vm.add_number("2")
        vm.add_operator("^")
        vm.add_number("3")
        vm.add_operator("^")
        vm.add_number("2")
        assert vm.calculate() == "512"

    def test_parentheses_auto_close(self, calc_setup):
        vm = calc_setup
        vm.add_open_paren()
        vm.add_number("2")
        vm.add_operator("+")
        vm.add_number("3")
        # Missing closing paren
        assert vm.calculate() == "5"

    def test_implicit_multiplication(self, calc_setup):
        vm = calc_setup
        # 2(3) = 6
        vm.add_number("2")
        vm.add_open_paren()
        vm.add_number("3")
        vm.add_close_paren()
        assert vm.calculate() == "6"

    def test_ans_button(self, calc_setup):
        vm = calc_setup
        vm.add_number("1")
        vm.add_operator("+")
        vm.add_number("1")
        vm.calculate()  # result = 2

        vm.add_number("3")
        vm.add_operator("*")
        vm.add_answer()  # 3 * 2
        assert vm.calculate() == "6"

    def test_memory_flow(self, calc_setup):
        vm = calc_setup
        # M+ 10
        vm.add_number("10")
        vm.memory_add()
        assert vm.memory == 10.0

        # Clear before adding next number
        vm.clear()

        # M+ 5
        vm.add_number("5")
        vm.memory_add()
        assert vm.memory == 15.0

        # Clear
        vm.clear()

        # M- 2
        vm.add_number("2")
        vm.memory_subtract()
        assert vm.memory == 13.0

        # MR
        vm.memory_recall()
        assert "13" in vm.display_expression

        # MC
        vm.memory_clear()
        assert vm.memory == 0.0

    def test_division_by_zero(self, calc_setup):
        vm = calc_setup
        vm.add_number("5")
        vm.add_operator("/")
        vm.add_number("0")
        result = vm.calculate()
        assert "Error" in result
        assert vm.display_result == "Error"

    def test_second_mode_toggle(self, calc_setup):
        vm = calc_setup
        assert not vm.is_second_mode
        vm.toggle_second_mode()
        assert vm.is_second_mode
        vm.toggle_second_mode()
        assert not vm.is_second_mode

    def test_constant_addition(self, calc_setup):
        vm = calc_setup
        vm.add_constant("pi")
        assert vm.display_expression == "π"
        vm.add_constant("e")  # Should add implicit *
        assert vm.display_expression == "π*e"
