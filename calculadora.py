#!/usr/bin/env python3
"""Calculadora - Punto de entrada alternativo.

Este archivo redirige a la aplicación principal (main.py).

La versión anterior basada en tkinter con eval() fue reemplazada
por la versión segura con PyQt6 y parser propio.

Uso:
    python calculadora.py
    (equivalente a: python main.py)
"""

from main import main

if __name__ == "__main__":
    main()
