"""Interfaz gráfica principal de la calculadora científica.

Diseño moderno estilo Casio avanzada con soporte completo
para teclado, memoria, conversor de unidades y más.
"""

import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .themes import get_theme


class CalcButton(QPushButton):
    """Botón personalizado con estilos según tipo."""

    TYPES = {
        "number": "number",
        "operator": "operator",
        "function": "function",
        "special": "special",
        "equals": "equals",
        "memory": "memory",
    }

    def __init__(self, text: str, btn_type: str = "number", parent=None):
        super().__init__(text, parent)
        self.btn_type = btn_type
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(54, 54)
        self.setFont(QFont("Segoe UI", 15))
        self._set_shadow()

    def _set_shadow(self) -> None:
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 2)
        shadow.setColor(Qt.GlobalColor.black)
        self.setGraphicsEffect(shadow)

    def apply_theme(self, theme) -> None:
        """Aplica el tema al botón."""
        colors = {
            "number": (
                theme.BUTTON_NUMBER,
                theme.BUTTON_NUMBER_HOVER,
                theme.BUTTON_NUMBER_PRESSED,
            ),
            "operator": (
                theme.BUTTON_OPERATOR,
                theme.BUTTON_OPERATOR_HOVER,
                theme.BUTTON_OPERATOR_PRESSED,
            ),
            "function": (
                theme.BUTTON_FUNCTION,
                theme.BUTTON_FUNCTION_HOVER,
                theme.BUTTON_FUNCTION_PRESSED,
            ),
            "special": (
                theme.BUTTON_SPECIAL,
                theme.BUTTON_SPECIAL_HOVER,
                theme.BUTTON_SPECIAL_PRESSED,
            ),
            "equals": (
                theme.BUTTON_EQUALS,
                theme.BUTTON_EQUALS_HOVER,
                theme.BUTTON_EQUALS_PRESSED,
            ),
            "memory": (
                theme.BUTTON_MEMORY,
                theme.BUTTON_MEMORY_HOVER,
                theme.BUTTON_MEMORY_PRESSED,
            ),
        }

        bg, hover, pressed = colors.get(self.btn_type, colors["number"])
        text_color = (
            "#FFFFFF" if self.btn_type in ("operator", "equals") else theme.TEXT_PRIMARY
        )

        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {bg};
                color: {text_color};
                border: 1px solid {theme.BORDER};
                border-radius: 14px;
                padding: 10px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
            """
        )


class DisplayPanel(QWidget):
    """Panel de display con expresión y resultado."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._set_shadow()

    def _set_shadow(self) -> None:
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 5)
        shadow.setColor(Qt.GlobalColor.black)
        self.setGraphicsEffect(shadow)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(4)

        self.expression_label = QLabel("")
        self.expression_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expression_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.expression_label.setStyleSheet("color: #8E8E93;")
        self.expression_label.setWordWrap(True)
        self.expression_label.setMinimumHeight(20)
        self.expression_label.setMaximumHeight(34)

        self.result_label = QLabel("0")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.result_label.setFont(QFont("Segoe UI", 38, QFont.Weight.Light))
        self.result_label.setWordWrap(True)
        self.result_label.setMinimumHeight(60)

        layout.addWidget(self.result_label)
        layout.addWidget(self.expression_label)

    def set_expression(self, text: str) -> None:
        self.expression_label.setText(text)
        self._fit_expression_font(text)

    def set_preview(self, text: str) -> None:
        self.expression_label.setText(text)
        self._fit_expression_font(text)

    def set_result(self, text: str) -> None:
        self.result_label.setText(text)

    def clear(self) -> None:
        self.expression_label.setText("")
        self.result_label.setText("0")

    def _fit_expression_font(self, text: str) -> None:
        text_len = len(text)
        if text_len <= 12:
            size = 12
        elif text_len <= 22:
            size = 11
        elif text_len <= 32:
            size = 10
        else:
            size = 9

        self.expression_label.setFont(QFont("Segoe UI", size, QFont.Weight.Medium))

    def apply_theme(self, theme) -> None:
        self.expression_label.setStyleSheet(
            f"color: {theme.TEXT_SECONDARY};"
            " background-color: transparent;"
            " border: none;"
            " padding: 0px 6px 2px 6px;"
        )
        self.result_label.setStyleSheet(f"color: {theme.TEXT_PRIMARY};")
        self.setStyleSheet(
            f"background: {theme.PANEL_GRADIENT};"
            f" border: 1px solid {theme.BORDER}; border-radius: 18px;"
        )


class HistoryDialog(QDialog):
    """Diálogo para mostrar el historial completo."""

    def __init__(self, history_manager, theme, parent=None):
        super().__init__(parent)
        self.history = history_manager
        self.theme = theme
        self.setWindowTitle("Historial de Cálculos")
        self.setMinimumSize(450, 400)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("Consolas", 11))

        for record in self.history.get_all():
            item_text = f"{record.expression} = {record.result}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, record.result)
            self.list_widget.addItem(item)

        btn_layout = QHBoxLayout()

        copy_btn = QPushButton("Copiar resultado")
        copy_btn.clicked.connect(self._copy_selected)

        clear_btn = QPushButton("Limpiar historial")
        clear_btn.clicked.connect(self._clear_history)

        export_btn = QPushButton("Exportar")
        export_btn.clicked.connect(self._export_history)

        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.close)

        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(close_btn)

        layout.addWidget(self.list_widget)
        layout.addLayout(btn_layout)

        self.setStyleSheet(
            f"""
            QDialog {{ background-color: {self.theme.BACKGROUND}; }}
            QListWidget {{
                background-color: {self.theme.SECONDARY_BG};
                color: {self.theme.TEXT_PRIMARY};
                border: 1px solid {self.theme.BORDER};
                border-radius: 12px;
            }}
            QListWidget::item {{ padding: 8px; }}
            QListWidget::item:selected {{ background-color: {self.theme.ACCENT}; }}
            QPushButton {{
                background-color: {self.theme.BUTTON_SPECIAL};
                color: {self.theme.TEXT_PRIMARY};
                border: 1px solid {self.theme.BORDER};
                border-radius: 10px;
                padding: 9px 15px;
            }}
            QPushButton:hover {{ background-color: {self.theme.BUTTON_SPECIAL_HOVER}; }}
            """
        )

    def _copy_selected(self) -> None:
        item = self.list_widget.currentItem()
        if item:
            result = item.data(Qt.ItemDataRole.UserRole)
            QApplication.clipboard().setText(str(result))

    def _clear_history(self) -> None:
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "¿Deseas limpiar todo el historial?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.history.clear()
            self.list_widget.clear()

    def _export_history(self) -> None:
        try:
            self.history.export_to_text()
            QMessageBox.information(
                self,
                "Exportado",
                "Historial exportado a ~/calculadora_export.txt",
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {e}")


class ConverterDialog(QDialog):
    """Diálogo para conversión de unidades."""

    def __init__(self, theme, parent=None):
        super().__init__(parent)
        from src.utils.converter import UnitConverter

        self.converter = UnitConverter
        self.theme = theme
        self.setWindowTitle("Conversor de Unidades")
        self.setMinimumSize(400, 350)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.category_combo = self._create_combo(self.converter.get_categories())
        self.category_combo.currentTextChanged.connect(self._update_units)

        row = QHBoxLayout()
        row.addWidget(QLabel("Categoría:"))
        row.addWidget(self.category_combo)
        layout.addLayout(row)

        units = self._get_current_units()
        self.from_combo = self._create_combo(units)
        self.to_combo = self._create_combo(units)

        unit_row = QHBoxLayout()
        unit_row.addWidget(QLabel("De:"))
        unit_row.addWidget(self.from_combo)
        unit_row.addWidget(QLabel("A:"))
        unit_row.addWidget(self.to_combo)
        layout.addLayout(unit_row)

        self.value_input = self._create_line_edit("0")
        self.result_label = QLabel("Resultado: 0")
        self.result_label.setFont(QFont("Segoe UI", 16))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        convert_btn = QPushButton("Convertir")
        convert_btn.clicked.connect(self._convert)

        layout.addWidget(QLabel("Valor:"))
        layout.addWidget(self.value_input)
        layout.addWidget(convert_btn)
        layout.addWidget(self.result_label)

        self.setStyleSheet(
            f"""
            QDialog {{ background-color: {self.theme.BACKGROUND}; }}
            QLabel {{ color: {self.theme.TEXT_PRIMARY}; }}
            QComboBox {{
                background-color: {self.theme.SECONDARY_BG};
                color: {self.theme.TEXT_PRIMARY};
                border: 1px solid {self.theme.BORDER};
                border-radius: 8px;
                padding: 6px;
            }}
            QLineEdit {{
                background-color: {self.theme.SECONDARY_BG};
                color: {self.theme.TEXT_PRIMARY};
                border: 1px solid {self.theme.BORDER};
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
            }}
            QPushButton {{
                background-color: {self.theme.BUTTON_EQUALS};
                color: #FFFFFF;
                border: 1px solid {self.theme.BUTTON_EQUALS};
                border-radius: 10px;
                padding: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {self.theme.BUTTON_EQUALS_HOVER}; }}
            """
        )

    def _create_combo(self, items: list) -> QComboBox:
        combo = QComboBox()
        combo.addItems(items)
        return combo

    def _get_current_units(self) -> list:
        cat = self.category_combo.currentText()
        return list(self.converter.get_units(cat).keys())

    def _update_units(self) -> None:
        units = self._get_current_units()
        self.from_combo.clear()
        self.from_combo.addItems(units)
        self.to_combo.clear()
        self.to_combo.addItems(units)
        if len(units) > 1:
            self.to_combo.setCurrentIndex(1)

    def _create_line_edit(self, text: str) -> QLineEdit:
        edit = QLineEdit(text)
        return edit

    def _convert(self) -> None:
        try:
            value = float(self.value_input.text())
            category = self.category_combo.currentText()
            from_unit = self.from_combo.currentText()
            to_unit = self.to_combo.currentText()

            result = self.converter.convert(value, category, from_unit, to_unit)
            formatted = f"{result:.10g}".rstrip("0").rstrip(".")
            self.result_label.setText(f"Resultado: {formatted}")
        except ValueError as e:
            self.result_label.setText(f"Error: {e}")


class CalculatorWindow(QMainWindow):
    """Ventana principal de la calculadora científica."""

    def __init__(self, view_model, parent=None):
        super().__init__(parent)
        self.view_model = view_model
        self.theme_name = "dark"
        self.theme = get_theme(self.theme_name)

        self.setWindowTitle("Calculadora Científica")
        self.setMinimumSize(420, 700)
        self.resize(420, 750)

        self._setup_ui()
        self._setup_menu()
        self._setup_statusbar()
        self._apply_theme()
        self._setup_shortcuts()

        # Vincular el ViewModel con la actualización de la UI
        self.view_model.on_state_changed = self._update_display
        self._update_display()
        self._update_mode_indicator()

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.display = DisplayPanel()
        main_layout.addWidget(self.display)

        buttons_widget = QWidget()
        self.buttons_layout = QGridLayout(buttons_widget)
        self.buttons_layout.setSpacing(6)

        self.buttons = {}

        button_config = [
            [
                ("MC", "memory", self._on_memory_clear),
                ("MR", "memory", self._on_memory_recall),
                ("M+", "memory", self._on_memory_add),
                ("M-", "memory", self._on_memory_subtract),
                ("AC", "special", self._on_clear),
            ],
            [
                ("2nd", "function", self._on_2nd),
                ("sin", "function", lambda: self._on_function("sin")),
                ("cos", "function", lambda: self._on_function("cos")),
                ("tan", "function", lambda: self._on_function("tan")),
                ("DEL", "special", self._on_delete),
            ],
            [
                ("x²", "function", self._on_square),
                ("x³", "function", self._on_cube),
                ("xⁿ", "function", self._on_power),
                ("√", "function", self._on_sqrt),
                ("/", "operator", lambda: self._on_operator("/")),
            ],
            [
                ("ln", "function", lambda: self._on_function("ln")),
                ("log", "function", lambda: self._on_function("log")),
                ("(", "function", self._on_open_paren),
                (")", "function", self._on_close_paren),
                ("×", "operator", lambda: self._on_operator("*")),
            ],
            [
                ("7", "number", lambda: self._on_number("7")),
                ("8", "number", lambda: self._on_number("8")),
                ("9", "number", lambda: self._on_number("9")),
                ("%", "function", self._on_percent),
                ("-", "operator", lambda: self._on_operator("-")),
            ],
            [
                ("4", "number", lambda: self._on_number("4")),
                ("5", "number", lambda: self._on_number("5")),
                ("6", "number", lambda: self._on_number("6")),
                ("π", "function", lambda: self._on_constant("pi")),
                ("+", "operator", lambda: self._on_operator("+")),
            ],
            [
                ("1", "number", lambda: self._on_number("1")),
                ("2", "number", lambda: self._on_number("2")),
                ("3", "number", lambda: self._on_number("3")),
                ("e", "function", lambda: self._on_constant("e")),
                ("=", "equals", self._on_equals),
            ],
            [
                ("0", "number", lambda: self._on_number("0")),
                (".", "number", self._on_decimal),
                ("+/-", "function", self._on_negate),
                ("n!", "function", self._on_factorial),
                ("Ans", "function", self._on_answer),
            ],
        ]

        for row_idx, row_buttons in enumerate(button_config):
            for col_idx, (text, btn_type, handler) in enumerate(row_buttons):
                btn = CalcButton(text, btn_type)
                btn.clicked.connect(handler)
                self.buttons[text] = btn
                self.buttons_layout.addWidget(btn, row_idx, col_idx)

        main_layout.addWidget(buttons_widget)

    def _setup_menu(self) -> None:
        menubar = self.menuBar()

        view_menu = menubar.addMenu("Ver")

        dark_action = QAction("Tema oscuro", self)
        dark_action.setShortcut("Ctrl+D")
        dark_action.triggered.connect(lambda: self._change_theme("dark"))
        view_menu.addAction(dark_action)

        light_action = QAction("Tema claro", self)
        light_action.setShortcut("Ctrl+L")
        light_action.triggered.connect(lambda: self._change_theme("light"))
        view_menu.addAction(light_action)

        view_menu.addSeparator()

        history_action = QAction("Historial", self)
        history_action.setShortcut("Ctrl+H")
        history_action.triggered.connect(self._show_history)
        view_menu.addAction(history_action)

        converter_action = QAction("Conversor de unidades", self)
        converter_action.setShortcut("Ctrl+U")
        converter_action.triggered.connect(self._show_converter)
        view_menu.addAction(converter_action)

        calc_menu = menubar.addMenu("Calculadora")

        deg_action = QAction("Modo Grados (DEG)", self)
        deg_action.setShortcut("Ctrl+G")
        deg_action.triggered.connect(lambda: self._set_angle_mode("deg"))
        calc_menu.addAction(deg_action)

        rad_action = QAction("Modo Radianes (RAD)", self)
        rad_action.setShortcut("Ctrl+R")
        rad_action.triggered.connect(lambda: self._set_angle_mode("rad"))
        calc_menu.addAction(rad_action)

        calc_menu.addSeparator()

        copy_action = QAction("Copiar resultado", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self._copy_result)
        calc_menu.addAction(copy_action)

        paste_action = QAction("Pegar expresión", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self._paste_expression)
        calc_menu.addAction(paste_action)

        calc_menu.addSeparator()

        exit_action = QAction("Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        calc_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Ayuda")

        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

        shortcuts_action = QAction("Atajos de teclado", self)
        shortcuts_action.setShortcut("F1")
        shortcuts_action.triggered.connect(self._show_shortcuts)
        help_menu.addAction(shortcuts_action)

    def _setup_statusbar(self) -> None:
        self.mode_indicator = QLabel("")
        self.mode_indicator.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.statusBar().addPermanentWidget(self.mode_indicator)
        self.statusBar().showMessage("Listo")

    def _setup_shortcuts(self) -> None:
        shortcuts = [
            ("Ctrl+D", lambda: self._change_theme("dark")),
            ("Ctrl+L", lambda: self._change_theme("light")),
            ("Ctrl+H", self._show_history),
            ("Ctrl+U", self._show_converter),
            ("Ctrl+G", lambda: self._set_angle_mode("deg")),
            ("Ctrl+R", lambda: self._set_angle_mode("rad")),
            ("Ctrl+C", self._copy_result),
            ("Ctrl+V", self._paste_expression),
            ("Ctrl+Q", self.close),
            ("F1", self._show_shortcuts),
            ("Return", self._on_equals),
            ("Enter", self._on_equals),
            ("Backspace", self._on_delete),
            ("Escape", self._on_clear),
            ("Delete", self._on_clear),
        ]

        self._shortcuts = []
        for sequence, handler in shortcuts:
            shortcut = QShortcut(QKeySequence(sequence), self)
            shortcut.activated.connect(handler)
            self._shortcuts.append(shortcut)

    def keyPressEvent(self, event) -> None:
        key = event.key()
        text = event.text()

        if text.isdigit():
            self._on_number(text)
        elif text == "+":
            self._on_operator("+")
        elif text == "-":
            self._on_operator("-")
        elif text == "*":
            self._on_operator("*")
        elif text == "/":
            self._on_operator("/")
        elif text == ".":
            self._on_decimal()
        elif text == "(":
            self._on_open_paren()
        elif text == ")":
            self._on_close_paren()
        elif text == "%":
            self._on_percent()
        elif text == "^":
            self._on_power()
        elif text == "!":
            self._on_factorial()
        elif text == "π":
            self._on_constant("pi")
        elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self._on_equals()
        elif key == Qt.Key.Key_Backspace:
            self._on_delete()
        elif key == Qt.Key.Key_Escape:
            self._on_clear()
        elif key == Qt.Key.Key_Delete:
            self._on_clear()
        else:
            super().keyPressEvent(event)

    def _apply_theme(self) -> None:
        self.theme = get_theme(self.theme_name)
        self.setPalette(self.theme.get_palette())
        self.display.apply_theme(self.theme)

        for btn in self.buttons.values():
            btn.apply_theme(self.theme)

        self.setStyleSheet(
            f"""
            QMainWindow {{
                background: {self.theme.WINDOW_GRADIENT};
            }}
            QMenuBar {{
                background: {self.theme.SECONDARY_BG};
                color: {self.theme.TEXT_PRIMARY};
                border: none;
                padding: 4px;
            }}
            QMenuBar::item:selected {{
                background-color: {self.theme.TERTIARY_BG};
                border-radius: 6px;
            }}
            QMenu {{
                background-color: {self.theme.SECONDARY_BG};
                color: {self.theme.TEXT_PRIMARY};
                border: 1px solid {self.theme.BORDER};
                border-radius: 8px;
            }}
            QMenu::item:selected {{
                background-color: {self.theme.ACCENT};
            }}
            QStatusBar {{
                background-color: {self.theme.SECONDARY_BG};
                color: {self.theme.TEXT_SECONDARY};
                border-top: 1px solid {self.theme.BORDER};
            }}
            """
        )
        self.mode_indicator.setStyleSheet(
            f"background-color: {self.theme.TERTIARY_BG};"
            f" color: {self.theme.TEXT_PRIMARY};"
            f" border: 1px solid {self.theme.BORDER};"
            " border-radius: 7px; padding: 2px 8px;"
        )

    def _change_theme(self, theme_name: str) -> None:
        self.theme_name = theme_name
        self._apply_theme()
        label = "Oscuro" if theme_name == "dark" else "Claro"
        self.statusBar().showMessage(f"Tema: {label}")

    def _set_angle_mode(self, mode: str) -> None:
        self.view_model.set_angle_mode(mode)
        self._update_mode_indicator()
        self.statusBar().showMessage(f"Modo: {mode.upper()}")

    def _on_number(self, digit: str) -> None:
        self.view_model.add_number(digit)

    def _on_operator(self, op: str) -> None:
        self.view_model.add_operator(op)

    def _on_decimal(self) -> None:
        self.view_model.add_decimal()

    def _on_open_paren(self) -> None:
        self.view_model.add_open_paren()

    def _on_close_paren(self) -> None:
        self.view_model.add_close_paren()

    def _on_percent(self) -> None:
        self.view_model.add_percent()

    def _on_negate(self) -> None:
        self.view_model.toggle_negate()

    def _on_square(self) -> None:
        self.view_model.add_square()

    def _on_cube(self) -> None:
        self.view_model.add_cube()

    def _on_power(self) -> None:
        self.view_model.add_power()

    def _on_sqrt(self) -> None:
        self.view_model.add_sqrt()

    def _on_factorial(self) -> None:
        self.view_model.add_factorial()

    def _on_function(self, func_name: str) -> None:
        self.view_model.add_function(func_name)

    def _on_constant(self, const: str) -> None:
        self.view_model.add_constant(const)

    def _on_answer(self) -> None:
        self.view_model.add_answer()

    def _on_2nd(self) -> None:
        self.view_model.toggle_second_mode()

        toggle_map = {
            "sin": ("asin", "sin"),
            "cos": ("acos", "cos"),
            "tan": ("atan", "tan"),
            "ln": ("exp", "ln"),
            "log": ("10^x", "log"),
        }

        for original_key, (second_text, first_text) in toggle_map.items():
            btn = self.buttons.get(original_key)
            if btn:
                if self.view_model.is_second_mode:
                    btn.setText(second_text)
                else:
                    btn.setText(first_text)

                try:
                    btn.clicked.disconnect()
                except (TypeError, RuntimeError):
                    pass

                if self.view_model.is_second_mode:
                    if second_text == "10^x":
                        btn.clicked.connect(self._on_10x)
                    elif second_text == "exp":
                        btn.clicked.connect(self._on_exp)
                    else:
                        btn.clicked.connect(
                            lambda checked=False, f=second_text: self._on_function(f)
                        )
                else:
                    if original_key == "ln":
                        btn.clicked.connect(
                            lambda checked=False: self._on_function("ln")
                        )
                    elif original_key == "log":
                        btn.clicked.connect(
                            lambda checked=False: self._on_function("log")
                        )
                    else:
                        btn.clicked.connect(
                            lambda checked=False, f=original_key: self._on_function(f)
                        )

        self._update_mode_indicator()
        self.statusBar().showMessage(
            f"Modo secundario: {'activado' if self.view_model.is_second_mode else 'desactivado'}"
        )

    def _on_10x(self) -> None:
        self.view_model.add_power_10()

    def _on_exp(self) -> None:
        self.view_model.add_exp()

    def _on_clear(self) -> None:
        self.view_model.clear()
        self.display.clear()
        self.statusBar().showMessage("Limpiado")

    def _on_delete(self) -> None:
        self.view_model.delete()

    def _on_equals(self) -> None:
        if not self.view_model.display_expression:
            return
        result_text = self.view_model.calculate()
        if "Error" in result_text:
            self.display.set_result("Error")
            self.display.set_expression("")
            self.statusBar().showMessage(result_text)
        else:
            self.display.set_expression("")
            self.display.set_result(result_text)
            self.statusBar().showMessage("Calculado")

    def _on_memory_clear(self) -> None:
        self.view_model.memory_clear()
        self.statusBar().showMessage("Memoria limpiada")

    def _on_memory_recall(self) -> None:
        formatted = self.view_model.memory_recall()
        self.statusBar().showMessage(f"Memoria: {formatted}")

    def _on_memory_add(self) -> None:
        res = self.view_model.memory_add()
        self.statusBar().showMessage(f"M+ = {res}")

    def _on_memory_subtract(self) -> None:
        res = self.view_model.memory_subtract()
        self.statusBar().showMessage(f"M- = {res}")

    def _update_mode_indicator(self) -> None:
        self.mode_indicator.setText(self.view_model.get_mode_indicator())

    def _copy_result(self) -> None:
        QApplication.clipboard().setText(self.display.result_label.text())
        self.statusBar().showMessage("Resultado copiado al portapapeles")

    def _paste_expression(self) -> None:
        text = QApplication.clipboard().text()
        if text:
            # No tenemos el método add_text en ViewModel, vamos a agregarlo o usar add_number/operator
            # Para simplificar, permitamos que el ViewModel reciba un string completo
            self.view_model.current_expression += text
            self.view_model._notify()
            self._update_display()
            self.statusBar().showMessage("Expresión pegada")

    def _show_history(self) -> None:
        dialog = HistoryDialog(self.view_model.history, self.theme, self)
        dialog.exec()

    def _show_converter(self) -> None:
        dialog = ConverterDialog(self.theme, self)
        dialog.exec()

    def _show_about(self) -> None:
        QMessageBox.information(
            self,
            "Acerca de",
            "Calculadora Científica v2.1.0\n\n"
            "Parser matemático seguro (sin eval)\n"
            "Funciones trigonométricas, logarítmicas y conversor de unidades\n"
            "Historial persistente y atajos de teclado\n"
            "Temas oscuro y claro, soporte completo de teclado",
        )

    def _show_shortcuts(self) -> None:
        shortcuts_text = (
            "<h3>Atajos de Teclado</h3>"
            "<table>"
            "<tr><td><b>Ctrl+D</b></td><td>Tema oscuro</td></tr>"
            "<tr><td><b>Ctrl+L</b></td><td>Tema claro</td></tr>"
            "<tr><td><b>Ctrl+H</b></td><td>Historial</td></tr>"
            "<tr><td><b>Ctrl+U</b></td><td>Conversor de unidades</td></tr>"
            "<tr><td><b>Ctrl+G</b></td><td>Modo grados</td></tr>"
            "<tr><td><b>Ctrl+R</b></td><td>Modo radianes</td></tr>"
            "<tr><td><b>Ctrl+C</b></td><td>Copiar resultado</td></tr>"
            "<tr><td><b>Ctrl+V</b></td><td>Pegar expresión</td></tr>"
            "<tr><td><b>Ctrl+Q</b></td><td>Salir</td></tr>"
            "<tr><td><b>F1</b></td><td>Esta ayuda</td></tr>"
            "<tr><td><b>Enter</b></td><td>Calcular</td></tr>"
            "<tr><td><b>Backspace</b></td><td>Borrar último carácter</td></tr>"
            "<tr><td><b>Escape</b></td><td>Limpiar todo</td></tr>"
            "<tr><td><b>^</b></td><td>Potencia</td></tr>"
            "<tr><td><b>!</b></td><td>Factorial</td></tr>"
            "</table>"
        )
        msg = QMessageBox(self)
        msg.setWindowTitle("Atajos de Teclado")
        msg.setText(shortcuts_text)
        msg.exec()

    def _update_display(self) -> None:
        """Actualiza el display con el estado del ViewModel."""
        expr = self.view_model.display_expression
        display_text = expr.replace("*", "×").replace("/", "÷")

        self.display.set_result(display_text if display_text else "0")

        if not expr:
            self.display.set_preview("")
            return

        preview = self.view_model.evaluate_preview(expr)
        if preview:
            self.display.set_preview(f"= {preview}")
        else:
            self.display.set_preview("")
