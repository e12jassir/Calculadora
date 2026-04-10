"""ViewModel de la Calculadora Científica.
Sigue el patrón MVVM para desacoplar la lógica de negocio de la interfaz gráfica.
"""

from typing import Any, Callable, Dict, Optional
import math

from .parser import ExpressionParser
from .history import HistoryManager


class CalculatorViewModel:
    """Gestiona el estado y la lógica de la calculadora.

    Este componente actúa como intermediario entre el Modelo (Parser, History)
    y la Vista (UI).
    """

    def __init__(self, parser: ExpressionParser, history: HistoryManager):
        self._parser = parser
        self._history = history

        # --- Estado de la Aplicación ---
        self.current_expression: str = ""
        self.last_result: str = "0"
        self.has_last_result: bool = False
        self.angle_mode: str = parser.angle_mode
        self.second_mode: bool = False
        self.memory: float = 0.0
        self.has_memory: bool = False
        self.variables: Dict[str, float] = {}

        # Callback para notificar a la Vista sobre cambios de estado
        self.on_state_changed: Optional[Callable[[], None]] = None

    def _notify(self) -> None:
        """Notifica a la vista que el estado ha cambiado."""
        if self.on_state_changed:
            self.on_state_changed()

    # --- Propiedades Públicas (Solo lectura para la Vista) ---
    @property
    def display_expression(self) -> str:
        return self.current_expression

    @property
    def display_result(self) -> str:
        return self.last_result

    @property
    def current_angle_mode(self) -> str:
        return self.angle_mode.upper()

    @property
    def is_second_mode(self) -> bool:
        return self.second_mode

    def get_mode_indicator(self) -> str:
        mode = self.angle_mode.upper()
        if self.second_mode:
            mode = f"{mode} · 2ND"
        return mode

    @property
    def history(self) -> HistoryManager:
        return self._history

    # --- Comandos de Entrada ---

    def add_number(self, digit: str) -> None:
        if self.has_last_result and not self.current_expression:
            self.current_expression = ""

        self.current_expression += digit
        self._notify()

    def add_operator(self, op: str) -> None:
        if not self.current_expression:
            if self.has_last_result:
                self.current_expression = self.last_result + op
            elif op == "-":
                self.current_expression = "-"
            self._notify()
            return

        last = self.current_expression[-1]
        if last in "+*/^":
            self.current_expression = self.current_expression[:-1] + op
        elif last == "-":
            if (
                len(self.current_expression) > 1
                and self.current_expression[-2] in "+-*/^("
            ):
                if op != "-":
                    self.current_expression = self.current_expression[:-1] + op
            else:
                self.current_expression = self.current_expression[:-1] + op
        elif last == "(":
            if op == "-":
                self.current_expression += op
        else:
            self.current_expression += op
        self._notify()

    def add_decimal(self) -> None:
        if not self.current_expression:
            self.current_expression = "0."
        elif "." not in self._get_last_number():
            self.current_expression += "."
        self._notify()

    def add_open_paren(self) -> None:
        self._append_with_implicit("(")
        self._notify()

    def add_close_paren(self) -> None:
        if not self.current_expression:
            return
        if self.current_expression[-1] in "+-*/^(":
            return
        if self.current_expression.count("(") > self.current_expression.count(")"):
            self.current_expression += ")"
        self._notify()

    def add_percent(self) -> None:
        self.current_expression += "%"
        self._notify()

    def toggle_negate(self) -> None:
        if not self.current_expression:
            return
        last_num = self._get_last_number()
        if last_num:
            if last_num.startswith("-"):
                new_num = last_num[1:]
            else:
                new_num = "-" + last_num
            self.current_expression = (
                self.current_expression[: -len(last_num)] + new_num
            )
            self._notify()

    def add_square(self) -> None:
        if self.current_expression:
            self.current_expression += "^2"
        elif self.has_last_result:
            self.current_expression = f"({self.last_result})^2"
        self._notify()

    def add_cube(self) -> None:
        if self.current_expression:
            self.current_expression += "^3"
        elif self.has_last_result:
            self.current_expression = f"({self.last_result})^3"
        self._notify()

    def add_power(self) -> None:
        self.current_expression += "^"
        self._notify()

    def add_sqrt(self) -> None:
        if self.current_expression:
            self.current_expression = f"sqrt({self.current_expression})"
        elif self.has_last_result:
            self.current_expression = f"sqrt({self.last_result})"
        self._notify()

    def add_factorial(self) -> None:
        if self.current_expression:
            self.current_expression += "!"
        elif self.has_last_result:
            self.current_expression = f"({self.last_result})!"
        self._notify()

    def add_function(self, func_name: str) -> None:
        self._append_with_implicit(f"{func_name}(")
        self._notify()

    def add_constant(self, const: str) -> None:
        symbol = "π" if const == "pi" else "e"
        self._append_with_implicit(symbol)
        self._notify()

    def add_answer(self) -> None:
        if self.has_last_result:
            value = self.last_result
            if self._needs_implicit_multiplication():
                self.current_expression += "*"
            self.current_expression += f"({value})" if value.startswith("-") else value
            self._notify()

    def toggle_second_mode(self) -> None:
        self.second_mode = not self.second_mode
        self._notify()

    def clear(self) -> None:
        self.current_expression = ""
        self._notify()

    def delete(self) -> None:
        if not self.current_expression:
            return
        func_prefixes = [
            "asin(",
            "acos(",
            "atan(",
            "sinh(",
            "cosh(",
            "tanh(",
            "sin(",
            "cos(",
            "tan(",
            "ln(",
            "log(",
            "sqrt(",
            "exp(",
            "log2(",
            "cbrt(",
            "ceil(",
            "floor(",
            "abs(",
        ]
        for func in func_prefixes:
            if self.current_expression.endswith(func):
                self.current_expression = self.current_expression[: -len(func)]
                self._notify()
                return
        self.current_expression = self.current_expression[:-1]
        self._notify()

    def calculate(self) -> str:
        if not self.current_expression:
            return self.last_result

        # Auto-cerrar paréntesis
        opens = self.current_expression.count("(")
        closes = self.current_expression.count(")")
        if opens > closes:
            self.current_expression += ")" * (opens - closes)

        try:
            result = self._parser.evaluate(self.current_expression, self.variables)
            formatted = self._format_result(result)

            self._history.add(self.current_expression, formatted, self.angle_mode)

            self.last_result = formatted
            self.has_last_result = True
            self.current_expression = ""

            self._notify()
            return formatted
        except Exception as e:
            self.last_result = "Error"
            self.current_expression = ""
            self._notify()
            return f"Error: {e}"

    def set_angle_mode(self, mode: str) -> None:
        self.angle_mode = mode
        self._parser.set_angle_mode(mode)
        self._notify()

    # --- Memoria ---

    def memory_clear(self) -> None:
        self.memory = 0.0
        self.has_memory = False
        self._notify()

    def memory_recall(self) -> str:
        if self.has_memory:
            formatted = self._format_result(self.memory)
            self.add_number(formatted)
            return formatted
        return "0"

    def memory_add(self) -> str:
        try:
            if self.current_expression:
                value = self._parser.evaluate(self.current_expression, self.variables)
            elif self.has_last_result:
                value = float(self.last_result)
            else:
                return "Error"

            self.memory += value
            self.has_memory = True
            self._notify()
            return self._format_result(self.memory)
        except Exception:
            return "Error"

    def memory_subtract(self) -> str:
        try:
            if self.current_expression:
                value = self._parser.evaluate(self.current_expression, self.variables)
            elif self.has_last_result:
                value = float(self.last_result)
            else:
                return "Error"

            self.memory -= value
            self.has_memory = True
            self._notify()
            return self._format_result(self.memory)
        except Exception:
            return "Error"

    def add_power_10(self) -> None:
        if self.current_expression:
            self.current_expression = f"10^({self.current_expression})"
        elif self.has_last_result:
            self.current_expression = f"10^({self.last_result})"
        self._notify()

    def add_exp(self) -> None:
        if self.current_expression:
            self.current_expression = f"exp({self.current_expression})"
        elif self.has_last_result:
            self.current_expression = f"exp({self.last_result})"
        self._notify()

    # --- Helpers Internos ---

    def _get_last_number(self) -> str:
        if not self.current_expression:
            return ""
        i = len(self.current_expression) - 1
        while i >= 0 and (
            self.current_expression[i].isdigit() or self.current_expression[i] == "."
        ):
            i -= 1
        if i >= 0 and self.current_expression[i] == "-":
            if i == 0 or self.current_expression[i - 1] in "+-*/^(":
                i -= 1
        return self.current_expression[i + 1 :]

    def _append_with_implicit(self, token: str) -> None:
        if self._needs_implicit_multiplication():
            self.current_expression += "*"
        self.current_expression += token

    def _needs_implicit_multiplication(self) -> bool:
        if not self.current_expression:
            return False
        last = self.current_expression[-1]
        return last.isdigit() or last in (")", "!", "%", "π", "e")

    def _format_result(self, value: float) -> str:
        if math.isinf(value):
            return "∞" if value > 0 else "-∞"
        if math.isnan(value):
            return "NaN"
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))
        if abs(value) >= 1e10 or (abs(value) < 1e-6 and value != 0):
            return f"{value:.6E}"
        formatted = f"{value:.10g}"
        if "." in formatted:
            formatted = formatted.rstrip("0").rstrip(".")
        return formatted

    def evaluate_preview(self, expression: str) -> Optional[str]:
        """Permite a la vista obtener un preview del resultado sin cambiar el estado."""
        if not expression:
            return None
        try:
            result = self._parser.evaluate(expression, self.variables)
            return self._format_result(result)
        except Exception:
            return None
