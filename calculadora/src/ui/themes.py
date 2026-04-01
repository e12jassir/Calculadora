"""
Sistema de temas para la calculadora.
Soporta tema oscuro y claro con personalización completa.
"""

from PyQt6.QtGui import QPalette, QColor


class DarkTheme:
    """Tema oscuro estilo calculadora moderna."""
    
    NAME = "dark"
    
    BACKGROUND = "#1C1C1E"
    SECONDARY_BG = "#2C2C2E"
    TERTIARY_BG = "#3A3A3C"
    
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#8E8E93"
    
    BUTTON_NUMBER = "#3A3A3C"
    BUTTON_NUMBER_HOVER = "#4A4A4C"
    BUTTON_NUMBER_PRESSED = "#5A5A5C"
    
    BUTTON_OPERATOR = "#FF9500"
    BUTTON_OPERATOR_HOVER = "#FFB143"
    BUTTON_OPERATOR_PRESSED = "#CC7700"
    
    BUTTON_FUNCTION = "#2C2C2E"
    BUTTON_FUNCTION_HOVER = "#3C3C3E"
    BUTTON_FUNCTION_PRESSED = "#4C4C4E"
    
    BUTTON_SPECIAL = "#636366"
    BUTTON_SPECIAL_HOVER = "#737376"
    BUTTON_SPECIAL_PRESSED = "#838386"
    
    BUTTON_EQUALS = "#FF9500"
    BUTTON_EQUALS_HOVER = "#FFB143"
    BUTTON_EQUALS_PRESSED = "#CC7700"
    
    BORDER = "#3A3A3C"
    ACCENT = "#0A84FF"
    ERROR = "#FF453A"
    SUCCESS = "#30D158"
    
    @staticmethod
    def get_palette():
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(DarkTheme.BACKGROUND))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(DarkTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Base, QColor(DarkTheme.SECONDARY_BG))
        palette.setColor(QPalette.ColorRole.Text, QColor(DarkTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Button, QColor(DarkTheme.TERTIARY_BG))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(DarkTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(DarkTheme.ACCENT))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(DarkTheme.TEXT_PRIMARY))
        return palette


class LightTheme:
    """Tema claro minimalista."""
    
    NAME = "light"
    
    BACKGROUND = "#F2F2F7"
    SECONDARY_BG = "#FFFFFF"
    TERTIARY_BG = "#E5E5EA"
    
    TEXT_PRIMARY = "#000000"
    TEXT_SECONDARY = "#8E8E93"
    
    BUTTON_NUMBER = "#FFFFFF"
    BUTTON_NUMBER_HOVER = "#F0F0F0"
    BUTTON_NUMBER_PRESSED = "#E0E0E0"
    
    BUTTON_OPERATOR = "#FF9500"
    BUTTON_OPERATOR_HOVER = "#FFB143"
    BUTTON_OPERATOR_PRESSED = "#CC7700"
    
    BUTTON_FUNCTION = "#E5E5EA"
    BUTTON_FUNCTION_HOVER = "#D5D5DA"
    BUTTON_FUNCTION_PRESSED = "#C5C5CA"
    
    BUTTON_SPECIAL = "#D1D1D6"
    BUTTON_SPECIAL_HOVER = "#C1C1C6"
    BUTTON_SPECIAL_PRESSED = "#B1B1B6"
    
    BUTTON_EQUALS = "#FF9500"
    BUTTON_EQUALS_HOVER = "#FFB143"
    BUTTON_EQUALS_PRESSED = "#CC7700"
    
    BORDER = "#D1D1D6"
    ACCENT = "#007AFF"
    ERROR = "#FF3B30"
    SUCCESS = "#34C759"
    
    @staticmethod
    def get_palette():
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(LightTheme.BACKGROUND))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(LightTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Base, QColor(LightTheme.SECONDARY_BG))
        palette.setColor(QPalette.ColorRole.Text, QColor(LightTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Button, QColor(LightTheme.TERTIARY_BG))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(LightTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(LightTheme.ACCENT))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(LightTheme.TEXT_PRIMARY))
        return palette


def get_theme(theme_name: str):
    """Retorna la clase de tema según el nombre."""
    themes = {
        'dark': DarkTheme,
        'light': LightTheme,
    }
    return themes.get(theme_name.lower(), DarkTheme)
