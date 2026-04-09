"""Sistema de temas para la calculadora."""

from PyQt6.QtGui import QColor, QPalette


class DarkTheme:
    """Tema oscuro estilo calculadora moderna."""

    NAME = "dark"

    BACKGROUND = "#121826"
    SECONDARY_BG = "#1B2333"
    TERTIARY_BG = "#273449"
    WINDOW_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #101624, stop:1 #1A2540)"
    PANEL_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #172033, stop:1 #1D2940)"

    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#9BA9C1"

    BUTTON_NUMBER = "#2C3A52"
    BUTTON_NUMBER_HOVER = "#354863"
    BUTTON_NUMBER_PRESSED = "#425874"

    BUTTON_OPERATOR = "#F39C3D"
    BUTTON_OPERATOR_HOVER = "#FFB35C"
    BUTTON_OPERATOR_PRESSED = "#D1842F"

    BUTTON_FUNCTION = "#233048"
    BUTTON_FUNCTION_HOVER = "#2E3D58"
    BUTTON_FUNCTION_PRESSED = "#3A4B69"

    BUTTON_SPECIAL = "#3B4A62"
    BUTTON_SPECIAL_HOVER = "#485A76"
    BUTTON_SPECIAL_PRESSED = "#526687"

    BUTTON_EQUALS = "#1F8FFF"
    BUTTON_EQUALS_HOVER = "#4CA7FF"
    BUTTON_EQUALS_PRESSED = "#1976D2"

    BUTTON_MEMORY = "#243246"
    BUTTON_MEMORY_HOVER = "#2F3F56"
    BUTTON_MEMORY_PRESSED = "#3A4C66"

    BORDER = "#2D3D56"
    ACCENT = "#2EA8FF"
    ERROR = "#FF453A"
    SUCCESS = "#30D158"

    @staticmethod
    def get_palette() -> QPalette:
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(DarkTheme.BACKGROUND))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(DarkTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Base, QColor(DarkTheme.SECONDARY_BG))
        palette.setColor(QPalette.ColorRole.Text, QColor(DarkTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Button, QColor(DarkTheme.TERTIARY_BG))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(DarkTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(DarkTheme.ACCENT))
        palette.setColor(
            QPalette.ColorRole.HighlightedText, QColor(DarkTheme.TEXT_PRIMARY)
        )
        return palette


class LightTheme:
    """Tema claro minimalista."""

    NAME = "light"

    BACKGROUND = "#F4F7FB"
    SECONDARY_BG = "#FFFFFF"
    TERTIARY_BG = "#E7EEF8"
    WINDOW_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F7FAFF, stop:1 #E9F0FC)"
    PANEL_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #F1F6FF)"

    TEXT_PRIMARY = "#1E293B"
    TEXT_SECONDARY = "#64748B"

    BUTTON_NUMBER = "#FFFFFF"
    BUTTON_NUMBER_HOVER = "#F3F7FF"
    BUTTON_NUMBER_PRESSED = "#E7EEFA"

    BUTTON_OPERATOR = "#EE9A40"
    BUTTON_OPERATOR_HOVER = "#F6B168"
    BUTTON_OPERATOR_PRESSED = "#D88836"

    BUTTON_FUNCTION = "#EAF1FB"
    BUTTON_FUNCTION_HOVER = "#DBE7F8"
    BUTTON_FUNCTION_PRESSED = "#CBDCF4"

    BUTTON_SPECIAL = "#DEE8F5"
    BUTTON_SPECIAL_HOVER = "#D0DDF0"
    BUTTON_SPECIAL_PRESSED = "#C1D2EA"

    BUTTON_EQUALS = "#2E8BFF"
    BUTTON_EQUALS_HOVER = "#57A2FF"
    BUTTON_EQUALS_PRESSED = "#2173D8"

    BUTTON_MEMORY = "#E7EEF8"
    BUTTON_MEMORY_HOVER = "#D9E4F4"
    BUTTON_MEMORY_PRESSED = "#CBD9EE"

    BORDER = "#D4E0F2"
    ACCENT = "#2E8BFF"
    ERROR = "#FF3B30"
    SUCCESS = "#34C759"

    @staticmethod
    def get_palette() -> QPalette:
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(LightTheme.BACKGROUND))
        palette.setColor(
            QPalette.ColorRole.WindowText, QColor(LightTheme.TEXT_PRIMARY)
        )
        palette.setColor(QPalette.ColorRole.Base, QColor(LightTheme.SECONDARY_BG))
        palette.setColor(QPalette.ColorRole.Text, QColor(LightTheme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Button, QColor(LightTheme.TERTIARY_BG))
        palette.setColor(
            QPalette.ColorRole.ButtonText, QColor(LightTheme.TEXT_PRIMARY)
        )
        palette.setColor(QPalette.ColorRole.Highlight, QColor(LightTheme.ACCENT))
        palette.setColor(
            QPalette.ColorRole.HighlightedText, QColor(LightTheme.TEXT_PRIMARY)
        )
        return palette


def get_theme(theme_name: str):
    """Retorna la clase de tema según el nombre."""
    themes = {
        'dark': DarkTheme,
        'light': LightTheme,
    }
    return themes.get(theme_name.lower(), DarkTheme)
