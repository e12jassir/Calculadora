"""
Interfaz gráfica principal de la calculadora científica.
Diseño moderno estilo Casio avanzada con soporte completo para teclado.
"""

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QFrame, QSizePolicy,
    QMenu, QMenuBar, QStatusBar, QSplitter, QListWidget,
    QListWidgetItem, QDialog, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QKeySequence, QAction, QClipboard

from .themes import get_theme, DarkTheme, LightTheme


class CalcButton(QPushButton):
    """Botón personalizado con estilos según tipo."""
    
    TYPES = {
        'number': 'number',
        'operator': 'operator',
        'function': 'function',
        'special': 'special',
        'equals': 'equals',
    }
    
    def __init__(self, text, btn_type='number', parent=None):
        super().__init__(text, parent)
        self.btn_type = btn_type
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(50, 50)
        self.setFont(QFont('Segoe UI', 14))
    
    def apply_theme(self, theme):
        """Aplica el tema al botón."""
        colors = {
            'number': (theme.BUTTON_NUMBER, theme.BUTTON_NUMBER_HOVER,
                      theme.BUTTON_NUMBER_PRESSED),
            'operator': (theme.BUTTON_OPERATOR, theme.BUTTON_OPERATOR_HOVER,
                        theme.BUTTON_OPERATOR_PRESSED),
            'function': (theme.BUTTON_FUNCTION, theme.BUTTON_FUNCTION_HOVER,
                        theme.BUTTON_FUNCTION_PRESSED),
            'special': (theme.BUTTON_SPECIAL, theme.BUTTON_SPECIAL_HOVER,
                       theme.BUTTON_SPECIAL_PRESSED),
            'equals': (theme.BUTTON_EQUALS, theme.BUTTON_EQUALS_HOVER,
                      theme.BUTTON_EQUALS_PRESSED),
        }
        
        bg, hover, pressed = colors.get(self.btn_type, colors['number'])
        
        text_color = '#FFFFFF' if self.btn_type in ('operator', 'equals') else theme.TEXT_PRIMARY
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {text_color};
                border: none;
                border-radius: 12px;
                padding: 10px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
        """)


class DisplayPanel(QWidget):
    """Panel de display con expresión y resultado."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)
        
        self.expression_label = QLabel("")
        self.expression_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expression_label.setFont(QFont('Segoe UI', 14))
        self.expression_label.setStyleSheet("color: #8E8E93;")
        self.expression_label.setWordWrap(True)
        
        self.result_label = QLabel("0")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.result_label.setFont(QFont('Segoe UI', 36, QFont.Weight.Light))
        self.result_label.setWordWrap(True)
        self.result_label.setMinimumHeight(60)
        
        layout.addWidget(self.expression_label)
        layout.addWidget(self.result_label)
    
    def set_expression(self, text):
        self.expression_label.setText(text)
    
    def set_result(self, text):
        self.result_label.setText(text)
    
    def clear(self):
        self.expression_label.setText("")
        self.result_label.setText("0")
    
    def apply_theme(self, theme):
        self.expression_label.setStyleSheet(f"color: {theme.TEXT_SECONDARY};")
        self.result_label.setStyleSheet(f"color: {theme.TEXT_PRIMARY};")
        self.setStyleSheet(f"background-color: {theme.BACKGROUND}; border-radius: 15px;")


class HistoryDialog(QDialog):
    """Diálogo para mostrar el historial completo."""
    
    def __init__(self, history_manager, theme, parent=None):
        super().__init__(parent)
        self.history = history_manager
        self.theme = theme
        self.setWindowTitle("Historial de Cálculos")
        self.setMinimumSize(450, 400)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont('Consolas', 11))
        
        for record in self.history.get_all():
            item_text = f"{record.expression} = {record.result}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, record.result)
            self.list_widget.addItem(item)
        
        btn_layout = QHBoxLayout()
        
        copy_btn = QPushButton("Copiar resultado")
        copy_btn.clicked.connect(self.copy_selected)
        
        clear_btn = QPushButton("Limpiar historial")
        clear_btn.clicked.connect(self.clear_history)
        
        export_btn = QPushButton("Exportar")
        export_btn.clicked.connect(self.export_history)
        
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.close)
        
        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(close_btn)
        
        layout.addWidget(self.list_widget)
        layout.addLayout(btn_layout)
        
        self.setStyleSheet(f"""
            QDialog {{ background-color: {self.theme.BACKGROUND}; }}
            QListWidget {{ 
                background-color: {self.theme.SECONDARY_BG}; 
                color: {self.theme.TEXT_PRIMARY};
                border-radius: 8px;
            }}
            QListWidget::item {{ padding: 8px; }}
            QListWidget::item:selected {{ background-color: {self.theme.ACCENT}; }}
            QPushButton {{
                background-color: {self.theme.BUTTON_SPECIAL};
                color: {self.theme.TEXT_PRIMARY};
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
            }}
            QPushButton:hover {{ background-color: {self.theme.BUTTON_SPECIAL_HOVER}; }}
        """)
    
    def copy_selected(self):
        item = self.list_widget.currentItem()
        if item:
            result = item.data(Qt.ItemDataRole.UserRole)
            QApplication.clipboard().setText(str(result))
    
    def clear_history(self):
        reply = QMessageBox.question(
            self, "Confirmar",
            "¿Deseas limpiar todo el historial?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.history.clear()
            self.list_widget.clear()
    
    def export_history(self):
        try:
            content = self.history.export_to_text()
            QMessageBox.information(
                self, "Exportado",
                f"Historial exportado a ~/calculadora_export.txt"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {str(e)}")


class CalculatorWindow(QMainWindow):
    """Ventana principal de la calculadora científica."""
    
    def __init__(self, parser, history, parent=None):
        super().__init__(parent)
        self.parser = parser
        self.history = history
        self.current_expression = ""
        self.last_result = "0"
        self.angle_mode = 'deg'
        self.theme_name = 'dark'
        self.theme = get_theme(self.theme_name)
        self.variables = {}
        self.memory = 0.0
        
        self.setWindowTitle("Calculadora Científica")
        self.setMinimumSize(420, 650)
        self.resize(420, 700)
        
        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()
        self.apply_theme()
        self.setup_shortcuts()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        self.display = DisplayPanel()
        main_layout.addWidget(self.display)
        
        self.mode_label = QLabel("DEG")
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mode_label.setFont(QFont('Segoe UI', 10))
        self.mode_label.setStyleSheet("color: #FF9500; font-weight: bold;")
        
        mode_layout = QHBoxLayout()
        mode_layout.addStretch()
        mode_layout.addWidget(self.mode_label)
        mode_layout.addStretch()
        main_layout.addLayout(mode_layout)
        
        buttons_widget = QWidget()
        self.buttons_layout = QGridLayout(buttons_widget)
        self.buttons_layout.setSpacing(6)
        
        self.buttons = {}
        
        button_config = [
            [('2nd', 'function', self.on_2nd), ('(', 'function', self.on_open_paren),
             (')', 'function', self.on_close_paren), ('%', 'function', self.on_percent),
             ('AC', 'special', self.on_clear)],
            
            [('sin', 'function', lambda: self.on_function('sin')),
             ('cos', 'function', lambda: self.on_function('cos')),
             ('tan', 'function', lambda: self.on_function('tan')),
             ('ln', 'function', lambda: self.on_function('ln')),
             ('DEL', 'special', self.on_delete)],
            
            [('x²', 'function', self.on_square), ('x³', 'function', self.on_cube),
             ('x^n', 'function', self.on_power), ('√', 'function', self.on_sqrt),
             ('/', 'operator', lambda: self.on_operator('/'))],
            
            [('7', 'number', lambda: self.on_number('7')),
             ('8', 'number', lambda: self.on_number('8')),
             ('9', 'number', lambda: self.on_number('9')),
             ('×', 'operator', lambda: self.on_operator('*'))],
            
            [('4', 'number', lambda: self.on_number('4')),
             ('5', 'number', lambda: self.on_number('5')),
             ('6', 'number', lambda: self.on_number('6')),
             ('-', 'operator', lambda: self.on_operator('-'))],
            
            [('1', 'number', lambda: self.on_number('1')),
             ('2', 'number', lambda: self.on_number('2')),
             ('3', 'number', lambda: self.on_number('3')),
             ('+', 'operator', lambda: self.on_operator('+'))],
            
            [('0', 'number', lambda: self.on_number('0')),
             ('.', 'number', self.on_decimal),
             ('+/-', 'function', self.on_negate),
             ('=', 'equals', self.on_equals)],
        ]
        
        for row_idx, row_buttons in enumerate(button_config):
            for col_idx, (text, btn_type, handler) in enumerate(row_buttons):
                btn = CalcButton(text, btn_type)
                btn.clicked.connect(handler)
                self.buttons[text] = btn
                self.buttons_layout.addWidget(btn, row_idx, col_idx)
        
        main_layout.addWidget(buttons_widget)
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        view_menu = menubar.addMenu("Ver")
        
        dark_action = QAction("Tema oscuro", self)
        dark_action.triggered.connect(lambda: self.change_theme('dark'))
        view_menu.addAction(dark_action)
        
        light_action = QAction("Tema claro", self)
        light_action.triggered.connect(lambda: self.change_theme('light'))
        view_menu.addAction(light_action)
        
        view_menu.addSeparator()
        
        history_action = QAction("Historial", self)
        history_action.triggered.connect(self.show_history)
        view_menu.addAction(history_action)
        
        calc_menu = menubar.addMenu("Calculadora")
        
        deg_action = QAction("Modo Grados (DEG)", self)
        deg_action.triggered.connect(lambda: self.set_angle_mode('deg'))
        calc_menu.addAction(deg_action)
        
        rad_action = QAction("Modo Radianes (RAD)", self)
        rad_action.triggered.connect(lambda: self.set_angle_mode('rad'))
        calc_menu.addAction(rad_action)
        
        calc_menu.addSeparator()
        
        copy_action = QAction("Copiar resultado", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_result)
        calc_menu.addAction(copy_action)
        
        calc_menu.addSeparator()
        
        exit_action = QAction("Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        calc_menu.addAction(exit_action)
    
    def setup_statusbar(self):
        self.statusBar().showMessage("Listo")
    
    def setup_shortcuts(self):
        pass
    
    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        
        if text.isdigit():
            self.on_number(text)
        elif text == '+':
            self.on_operator('+')
        elif text == '-':
            self.on_operator('-')
        elif text == '*':
            self.on_operator('*')
        elif text == '/':
            self.on_operator('/')
        elif text == '.':
            self.on_decimal()
        elif text == '(':
            self.on_open_paren()
        elif text == ')':
            self.on_close_paren()
        elif text == '%':
            self.on_percent()
        elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self.on_equals()
        elif key == Qt.Key.Key_Backspace:
            self.on_delete()
        elif key == Qt.Key.Key_Escape:
            self.on_clear()
        elif text == '^':
            self.on_power()
        elif text == '!':
            self.on_factorial()
    
    def apply_theme(self):
        self.theme = get_theme(self.theme_name)
        self.setPalette(self.theme.get_palette())
        self.display.apply_theme(self.theme)
        
        for btn in self.buttons.values():
            btn.apply_theme(self.theme)
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.theme.BACKGROUND};
            }}
            QMenuBar {{
                background-color: {self.theme.SECONDARY_BG};
                color: {self.theme.TEXT_PRIMARY};
            }}
            QMenuBar::item:selected {{
                background-color: {self.theme.TERTIARY_BG};
            }}
            QMenu {{
                background-color: {self.theme.SECONDARY_BG};
                color: {self.theme.TEXT_PRIMARY};
                border: 1px solid {self.theme.BORDER};
            }}
            QMenu::item:selected {{
                background-color: {self.theme.ACCENT};
            }}
            QStatusBar {{
                background-color: {self.theme.SECONDARY_BG};
                color: {self.theme.TEXT_SECONDARY};
            }}
        """)
    
    def change_theme(self, theme_name):
        self.theme_name = theme_name
        self.apply_theme()
        self.statusBar().showMessage(f"Tema: {'Oscuro' if theme_name == 'dark' else 'Claro'}")
    
    def set_angle_mode(self, mode):
        self.angle_mode = mode
        self.parser.set_angle_mode(mode)
        self.mode_label.setText(mode.upper())
        self.statusBar().showMessage(f"Modo: {mode.upper()}")
    
    def on_number(self, digit):
        if self.last_result != "0" and not self.current_expression:
            self.current_expression = ""
        
        self.current_expression += digit
        self.update_display()
    
    def on_operator(self, op):
        if self.current_expression:
            self.current_expression += op
        elif self.last_result != "0":
            self.current_expression = self.last_result + op
        self.update_display()
    
    def on_decimal(self):
        if not self.current_expression:
            self.current_expression = "0."
        elif '.' not in self._get_last_number():
            self.current_expression += '.'
        self.update_display()
    
    def on_open_paren(self):
        if self.current_expression and self.current_expression[-1].isdigit():
            self.current_expression += '*('
        else:
            self.current_expression += '('
        self.update_display()
    
    def on_close_paren(self):
        self.current_expression += ')'
        self.update_display()
    
    def on_percent(self):
        self.current_expression += '%'
        self.update_display()
    
    def on_negate(self):
        if self.current_expression:
            last_num = self._get_last_number()
            if last_num:
                if last_num.startswith('-'):
                    new_num = last_num[1:]
                else:
                    new_num = '-' + last_num
                
                self.current_expression = self.current_expression[:-len(last_num)] + new_num
                self.update_display()
    
    def on_square(self):
        if self.current_expression:
            self.current_expression += '^2'
        elif self.last_result != "0":
            self.current_expression = f"({self.last_result})^2"
        self.update_display()
    
    def on_cube(self):
        if self.current_expression:
            self.current_expression += '^3'
        elif self.last_result != "0":
            self.current_expression = f"({self.last_result})^3"
        self.update_display()
    
    def on_power(self):
        self.current_expression += '^'
        self.update_display()
    
    def on_sqrt(self):
        if self.current_expression:
            self.current_expression = f"sqrt({self.current_expression})"
        elif self.last_result != "0":
            self.current_expression = f"sqrt({self.last_result})"
        self.update_display()
    
    def on_factorial(self):
        if self.current_expression:
            self.current_expression += '!'
        elif self.last_result != "0":
            self.current_expression = f"({self.last_result})!"
        self.update_display()
    
    def on_function(self, func_name):
        self.current_expression += f"{func_name}("
        self.update_display()
    
    def on_2nd(self):
        funcs = {
            'sin': 'asin', 'cos': 'acos', 'tan': 'atan',
            'asin': 'sin', 'acos': 'cos', 'atan': 'tan',
        }
        
        for btn_text, func in [('sin', 'sin'), ('cos', 'cos'), ('tan', 'tan')]:
            btn = self.buttons.get(btn_text)
            if btn:
                new_text = funcs.get(func, func)
                btn.setText(new_text)
                try:
                    btn.clicked.disconnect()
                except:
                    pass
                btn.clicked.connect(lambda checked=False, f=new_text: self.on_function(f))
    
    def on_clear(self):
        self.current_expression = ""
        self.display.clear()
        self.last_result = "0"
        self.statusBar().showMessage("Limpiado")
    
    def on_delete(self):
        if self.current_expression:
            if self.current_expression.endswith('('):
                for func in ['sin(', 'cos(', 'tan(', 'asin(', 'acos(', 'atan(',
                            'ln(', 'log(', 'sqrt(', 'exp(']:
                    if self.current_expression.endswith(func):
                        self.current_expression = self.current_expression[:-len(func)]
                        self.update_display()
                        return
            
            self.current_expression = self.current_expression[:-1]
            self.update_display()
    
    def on_equals(self):
        if not self.current_expression:
            return
        
        try:
            result = self.parser.evaluate(self.current_expression, self.variables)
            
            formatted = self._format_result(result)
            
            self.history.add(self.current_expression, formatted, self.angle_mode)
            
            self.display.set_expression(f"{self.current_expression} =")
            self.display.set_result(formatted)
            
            self.last_result = formatted
            self.current_expression = ""
            
            self.statusBar().showMessage("Calculado ✓")
            
        except Exception as e:
            self.display.set_result("Error")
            self.display.set_expression(str(e))
            self.statusBar().showMessage(f"Error: {str(e)}")
            self.last_result = "0"
    
    def copy_result(self):
        QApplication.clipboard().setText(self.display.result_label.text())
        self.statusBar().showMessage("Resultado copiado al portapapeles")
    
    def show_history(self):
        dialog = HistoryDialog(self.history, self.theme, self)
        dialog.exec()
    
    def _format_result(self, value):
        """Formatea un resultado numérico."""
        if math.isinf(value):
            return "∞" if value > 0 else "-∞"
        if math.isnan(value):
            return "NaN"
        
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))
        
        if abs(value) >= 1e10 or (abs(value) < 1e-6 and value != 0):
            return f"{value:.6E}"
        
        formatted = f"{value:.10g}"
        if '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
        
        return formatted
    
    def _get_last_number(self):
        """Extrae el último número de la expresión actual."""
        if not self.current_expression:
            return ""
        
        i = len(self.current_expression) - 1
        while i >= 0 and (self.current_expression[i].isdigit() or 
                          self.current_expression[i] == '.' or
                          self.current_expression[i] == '-'):
            i -= 1
        
        return self.current_expression[i+1:]
    
    def update_display(self):
        """Actualiza el display con la expresión actual."""
        display_text = self.current_expression
        display_text = display_text.replace('*', '×').replace('/', '÷')
        self.display.set_result(display_text if display_text else "0")
