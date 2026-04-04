# Calculadora Científica v1.1

Calculadora científica profesional con interfaz gráfica moderna, parser matemático seguro y herramientas avanzadas.

## Características

- **Parser matemático seguro** - Implementación recursiva descendente sin uso de `eval()`
- **Funciones completas** - Trigonométricas, logarítmicas, exponenciales, factorial, potencias
- **Modo 2nd** - Funciones inversas (asin, acos, atan, exp, 10^x)
- **Memoria** - MC, MR, M+, M- con indicador visual
- **Historial persistente** - Guardado en JSON, exportable a texto
- **Conversor de unidades** - Longitud, masa, temperatura, ángulos, tiempo
- **Temas** - Oscuro y claro
- **Teclado físico completo** - Todos los atajos documentados
- **Botón Ans** - Reutiliza el último resultado

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
# o
python calculadora.py
```

## Estructura del Proyecto

```
calculadora/
├── main.py                 # Punto de entrada principal
├── calculadora.py          # Punto de entrada alternativo
├── requirements.txt        # Dependencias
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── parser.py       # Parser matemático seguro
│   │   ├── history.py      # Gestor de historial
│   │   └── constants.py    # Constantes matemáticas
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── calculator_ui.py # Interfaz principal
│   │   └── themes.py       # Sistema de temas
│   └── utils/
│       ├── __init__.py
│       └── converter.py    # Conversor de unidades
├── tests/
│   ├── __init__.py
│   ├── test_parser.py      # Tests del parser
│   ├── test_history.py     # Tests del historial
│   └── test_converter.py   # Tests del conversor
├── docs/                   # Documentación
└── config/                 # Configuración
```

## Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl+D` | Tema oscuro |
| `Ctrl+L` | Tema claro |
| `Ctrl+H` | Historial |
| `Ctrl+U` | Conversor de unidades |
| `Ctrl+G` | Modo grados |
| `Ctrl+R` | Modo radianes |
| `Ctrl+C` | Copiar resultado |
| `Ctrl+V` | Pegar expresión |
| `Ctrl+Q` | Salir |
| `F1` | Ayuda de atajos |
| `Enter` | Calcular |
| `Backspace` | Borrar último carácter |
| `Escape` | Limpiar todo |
| `^` | Potencia |
| `!` | Factorial |

## Funciones Matemáticas

| Función | Descripción |
|---------|-------------|
| `sin`, `cos`, `tan` | Trigonométricas |
| `asin`, `acos`, `atan` | Trigonométricas inversas |
| `sinh`, `cosh`, `tanh` | Hiperbólicas |
| `ln`, `log`, `log2` | Logaritmos |
| `sqrt`, `cbrt` | Raíces |
| `abs`, `ceil`, `floor` | Utilidades |
| `exp` | Exponencial |
| `fact` | Factorial |

## Constantes

| Constante | Valor |
|-----------|-------|
| `π`, `pi` | 3.14159... |
| `e` | 2.71828... |
| `τ`, `tau` | 6.28318... |
| `φ`, `phi` | 1.61803... |

## Tests

```bash
pytest tests/ -v
```

## Licencia

MIT
