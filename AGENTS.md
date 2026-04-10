# AGENTS.md - Calculadora Científica

## Inicio rápido

```bash
# Activar entorno virtual (Windows)
.\.venv\Scripts\Activate.ps1

# Ejecutar la app
python main.py

# Ejecutar tests
python -m pytest -q
```

## Comandos principales

- `python main.py` - Lanzar app GUI
- `python -m pytest -q` - Ejecutar todos los tests
- `pip install -r requirements.txt` - Instalar dependencias

## Arquitectura

- **Punto de entrada**: `main.py` (no `calculadora.py`)
- **Parser**: Recursivo descendente en `src/core/parser.py` - sin `eval`
- **UI**: PyQt6 en `src/ui/calculator_ui.py`
- **Tests**: `tests/test_parser.py`, `tests/test_history.py`, `tests/test_converter.py`

## Detalles importantes

- El operador potencia (`^`) es asociativo a la derecha: `2 ^ 3 ^ 2 == 512`
- Modo angular por defecto es grados (`DEG`) - cambiar con `Ctrl+G`/`Ctrl+R`
- El entorno virtual usa el directorio `.venv` (no `venv`)
- Los tests CI-runner usa Python 3.11 y 3.12

## Atajos de teclado

| Tecla | Acción |
|-------|--------|
| Enter | Calcular |
| Escape | Limpiar expresión |
| Ctrl+G | Modo grados |
| Ctrl+R | Modo radianes |
| Ctrl+H | Historial |
| Ctrl+U | Conversor de unidades |