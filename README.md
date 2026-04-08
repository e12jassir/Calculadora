# Calculadora Científica v1.2

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

### Requisitos

- **Python 3.11+**
- **PyQt6>=6.5.0**

### Windows

1. **Clonar el repositorio:**
   ```powershell
   git clone https://github.com/e12jassir/Calculadora.git
   cd Calculadora
   ```

2. **Crear entorno virtual e instalar dependencias:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. **Ejecutar:**
   ```powershell
   .\venv\Scripts\python.exe main.py
   ```

### Linux / macOS

```bash
git clone https://github.com/e12jassir/Calculadora.git
cd Calculadora
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Estructura del Proyecto

```
Calculadora/
├── main.py                 # Punto de entrada principal
├── calculadora.py          # Punto de entrada alternativo
├── requirements.txt        # Dependencias
├── src/
│   ├── core/
│   │   ├── parser.py       # Parser matemático seguro
│   │   ├── history.py      # Gestor de historial
│   │   └── constants.py    # Constantes matemáticas
│   ├── ui/
│   │   ├── calculator_ui.py # Interfaz principal
│   │   └── themes.py       # Sistema de temas
│   └── utils/
│       └── converter.py    # Conversor de unidades
└── tests/
    ├── test_parser.py      # Tests del parser
    ├── test_history.py     # Tests del historial
    └── test_converter.py   # Tests del conversor
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
pip install pytest
pytest tests/ -v
```

## Licencia

MIT
