#!/usr/bin/env python3
"""Calculadora Científica v2.1.0

Aplicación de calculadora científica con interfaz gráfica moderna.
Soporta funciones trigonométricas, logarítmicas, parser seguro,
historial, conversor de unidades y más.

Uso:
    python main.py

Dependencias:
    pip install PyQt6

Características:
    - Parser matemático seguro (sin eval)
    - Soporte para expresiones completas
    - Modo grados/radianes
    - Historial con persistencia en JSON
    - Temas oscuro/claro
    - Soporte completo para teclado físico
    - Memoria de cálculo
    - Conversor de unidades integrado
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication

from src.core.parser import ExpressionParser
from src.core.history import HistoryManager
from src.ui.calculator_ui import CalculatorWindow


def main():
    """Punto de entrada principal de la aplicación."""
    app = QApplication(sys.argv)
    app.setApplicationName("Calculadora Científica")
    app.setApplicationVersion("2.1.0")
    app.setOrganizationName("ScientificCalc")

    parser = ExpressionParser(angle_mode='deg')
    history = HistoryManager()

    window = CalculatorWindow(parser=parser, history=history)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
