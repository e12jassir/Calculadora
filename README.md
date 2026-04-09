# Calculadora Cientifica v2.1.0

Aplicacion de calculadora cientifica de escritorio en PyQt6, con parser matematico propio (sin `eval`), historial persistente y conversor de unidades.

## Que hace diferente a este proyecto

- Parser recursivo descendente escrito a mano (`src/core/parser.py`), sin ejecucion dinamica insegura.
- Soporte de notacion natural: multiplicacion implicita (`2pi`, `2(3+4)`, `(2)sin(30)`), porcentaje y factorial.
- Modo angular en grados o radianes para trigonometria directa e inversa.
- Interfaz moderna en PyQt6 con temas claro/oscuro, atajos completos y vista previa de resultado mientras escribes.
- Historial en JSON y exportacion a texto plano.
- Conversor integrado para longitud, masa, temperatura, angulos y tiempo.

## Captura funcional de la UX

- Linea principal: expresion actual (grande, legible).
- Linea secundaria: resultado previo en vivo (`= ...`), mas discreto.
- Al pulsar `=`: se confirma el resultado final y se limpia la vista previa.
- Estado de modo (`DEG`, `RAD`, `2ND`) visible en la barra inferior sin invadir el display.

## Instalacion

### Requisitos

- Python 3.11+
- Pip actualizado

### Linux / macOS

```bash
git clone https://github.com/e12jassir/Calculadora.git
cd Calculadora
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Windows (PowerShell)

```powershell
git clone https://github.com/e12jassir/Calculadora.git
cd Calculadora
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Atajos de teclado

| Atajo | Accion |
|---|---|
| `Enter` | Calcular |
| `Backspace` | Borrar ultimo caracter |
| `Escape` o `Delete` | Limpiar expresion |
| `Ctrl+G` | Modo grados |
| `Ctrl+R` | Modo radianes |
| `Ctrl+H` | Abrir historial |
| `Ctrl+U` | Abrir conversor |
| `Ctrl+D` | Tema oscuro |
| `Ctrl+L` | Tema claro |
| `Ctrl+C` | Copiar resultado |
| `Ctrl+V` | Pegar expresion |
| `F1` | Mostrar ayuda de atajos |

## Funciones y constantes soportadas

### Funciones

- Trigonometricas: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- Logaritmicas: `ln`, `log`, `log2`
- Exponenciales y raices: `exp`, `sqrt`, `cbrt`
- Utilidades: `abs`, `ceil`, `floor`
- Operadores especiales: `^`, `!`, `%`

### Constantes

- `pi`, `π`
- `e`
- `tau`, `τ`
- `phi`, `φ`

## Estructura del proyecto

```text
Calculadora/
|- main.py
|- calculadora.py
|- requirements.txt
|- src/
|  |- core/
|  |  |- parser.py
|  |  |- history.py
|  |  |- constants.py
|  |- ui/
|  |  |- calculator_ui.py
|  |  |- themes.py
|  |- utils/
|     |- converter.py
|- tests/
|  |- test_parser.py
|  |- test_history.py
|  |- test_converter.py
|- .github/workflows/ci.yml
```

## Calidad y pruebas

- Tests unitarios con `pytest`.
- CI en GitHub Actions para Python 3.11 y 3.12.

Ejecutar local:

```bash
python3 -m pytest -q
```

## Notas tecnicas

- El parser evita `eval` y valida la expresion con tokens y gramatica formal.
- La potencia es asociativa a la derecha (`2 ^ 3 ^ 2 == 512`).
- La memoria y el historial se manejan fuera del parser para mantener separacion de responsabilidades.

## Licencia

MIT
