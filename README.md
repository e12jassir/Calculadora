# 🧮 Scientific Calculator Pro

A high-performance, architecturally sound scientific calculator built with Python and PyQt6. This isn't just a simple calculator; it's a demonstration of software engineering principles applied to a classic problem.

## 🚀 Features

- **Advanced Mathematical Engine**:
  - Full support for trigonometric, logarithmic, and exponential functions.
  - **Recursive Descent Parser**: Custom-built parser that handles operator precedence and associativity (including right-associativity for powers `^`) without using the dangerous `eval()` function.
  - **Implicit Multiplication**: Supports natural mathematical notation, e.g., `2(3 + 4)` is correctly interpreted as `2 * (3 + 4)`.
  - **Right-to-Left Power**: Correctly handles `2^3^2` as `2^(3^2) = 512`.
- **Professional UX**:
  - **MVVM Architecture**: Complete separation between Logic (Model), State Management (ViewModel), and Presentation (View).
  - **2nd Function Mode**: Toggle between primary and inverse functions (e.g., `sin` $\rightarrow$ `asin`).
  - **Smart Display**: Real-time expression preview as you type.
  - **Memory Management**: Full `MC`, `MR`, `M+`, `M-` functionality.
  - **Calculation History**: Persistent history of all previous operations.
  - **Unit Converter**: Integrated tool for common unit conversions.
  - **Theme Support**: Built-in Dark and Light modes.
  - **Keyboard Integration**: Full support for keyboard shortcuts and numeric keypad.
- **Developer-Centric**:
  - **Full Test Suite**: Unit tests for the ViewModel ensuring rock-solid reliability.

## 🛠️ Architect's Corner

### The "No-Eval" Philosophy
Most beginner calculators use Python's `eval()` to process expressions. This is a critical security flaw and a sign of poor engineering. This project implements a **Recursive Descent Parser**, which tokenizes the input and builds an abstract understanding of the mathematical hierarchy. This ensures:
1. **Security**: No arbitrary code execution.
2. **Control**: Precise handling of mathematical rules (like implicit multiplication).

### MVVM Pattern
To avoid the "God Object" anti-pattern, the project follows the **Model-View-ViewModel (MVVM)** pattern:
- **Model**: The `ExpressionParser` and `HistoryManager`. They handle raw data and math.
- **ViewModel**: The `CalculatorViewModel`. It manages the application state, formats data for the UI, and handles business logic.
- **View**: The `CalculatorWindow`. A "dumb" layer that only renders the state provided by the ViewModel and forwards user events.

**Benefit**: This decoupling allows for effortless testing of the logic without launching a GUI and makes the app ready for future migrations (e.g., to a web or mobile interface).

## 💻 Tech Stack

- **Language**: Python 3.12+
- **GUI Framework**: PyQt6
- **Testing**: Pytest
- **Packaging**: PyInstaller

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Quick Start
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/scientific-calculator.git
   cd scientific-calculator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 🧪 Running Tests

The project includes a comprehensive test suite to ensure mathematical accuracy and state stability.

```bash
# Run all tests
python -m pytest
```

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
