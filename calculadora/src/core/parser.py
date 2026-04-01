"""
Parser matemático seguro para la calculadora científica.
Implementa un parser recursivo descendente que NO usa eval().
Soporta expresiones completas con funciones trigonométricas, logarítmicas, etc.
"""

import math
import re
from enum import Enum, auto
from typing import List, Optional, Tuple, Callable, Dict
from dataclasses import dataclass


class TokenType(Enum):
    """Tipos de tokens para el lexer."""
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    LPAREN = auto()
    RPAREN = auto()
    FUNC = auto()
    FACTORIAL = auto()
    PERCENT = auto()
    PI = auto()
    E_CONST = auto()
    VARIABLE = auto()
    CONSTANT = auto()
    COMMA = auto()
    EOF = auto()


@dataclass
class Token:
    """Representa un token con su tipo y valor."""
    type: TokenType
    value: any
    position: int


class MathError(Exception):
    """Excepción para errores matemáticos."""
    pass


class ParseError(Exception):
    """Excepción para errores de parsing."""
    pass


class Lexer:
    """
    Analizador léxico que convierte texto en tokens.
    Maneja números, operadores, funciones y constantes.
    """
    
    FUNCTIONS = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        'log': math.log10, 'ln': math.log, 'log2': math.log2,
        'sqrt': math.sqrt, 'cbrt': lambda x: x ** (1/3),
        'abs': abs, 'ceil': math.ceil, 'floor': math.floor,
        'exp': math.exp,
    }
    
    CONSTANTS = {
        'pi': math.pi, 'π': math.pi,
        'e': math.e,
        'tau': math.tau,
        'inf': math.inf,
    }
    
    def __init__(self, angle_mode: str = 'deg'):
        """
        Args:
            angle_mode: 'deg' para grados, 'rad' para radianes
        """
        self.angle_mode = angle_mode
        self.text = ""
        self.pos = 0
        self.tokens: List[Token] = []
    
    def tokenize(self, text: str) -> List[Token]:
        """Convierte texto en lista de tokens."""
        self.text = text.lower().strip()
        self.pos = 0
        self.tokens = []
        
        while self.pos < len(self.text):
            self._skip_whitespace()
            if self.pos >= len(self.text):
                break
            
            ch = self.text[self.pos]
            
            if ch.isdigit() or ch == '.':
                self._read_number()
            elif ch == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.pos))
                self.pos += 1
            elif ch == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.pos))
                self.pos += 1
            elif ch in '×*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', self.pos))
                self.pos += 1
            elif ch in '÷/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', self.pos))
                self.pos += 1
            elif ch == '^':
                self.tokens.append(Token(TokenType.POWER, '^', self.pos))
                self.pos += 1
            elif ch == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.pos))
                self.pos += 1
            elif ch == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.pos))
                self.pos += 1
            elif ch == '!':
                self.tokens.append(Token(TokenType.FACTORIAL, '!', self.pos))
                self.pos += 1
            elif ch == '%':
                self.tokens.append(Token(TokenType.PERCENT, '%', self.pos))
                self.pos += 1
            elif ch == 'π':
                self.tokens.append(Token(TokenType.PI, math.pi, self.pos))
                self.pos += 1
            elif ch == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.pos))
                self.pos += 1
            elif ch.isalpha() or ch == '_':
                self._read_identifier()
            else:
                raise ParseError(f"Carácter inesperado '{ch}' en posición {self.pos}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.pos))
        return self.tokens
    
    def _skip_whitespace(self):
        """Salta espacios en blanco."""
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1
    
    def _read_number(self):
        """Lee un número (entero, decimal o notación científica)."""
        start = self.pos
        has_dot = False
        has_e = False
        
        while self.pos < len(self.text):
            ch = self.text[self.pos]
            if ch.isdigit():
                self.pos += 1
            elif ch == '.' and not has_dot and not has_e:
                has_dot = True
                self.pos += 1
            elif ch == 'e' and not has_e and self.pos > start:
                has_e = True
                self.pos += 1
                if self.pos < len(self.text) and self.text[self.pos] in '+-':
                    self.pos += 1
            else:
                break
        
        num_str = self.text[start:self.pos]
        try:
            value = float(num_str)
        except ValueError:
            raise ParseError(f"Número inválido '{num_str}' en posición {start}")
        
        self.tokens.append(Token(TokenType.NUMBER, value, start))
    
    def _read_identifier(self):
        """Lee un identificador (función o constante)."""
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            self.pos += 1
        
        name = self.text[start:self.pos]
        
        if name in self.FUNCTIONS:
            self.tokens.append(Token(TokenType.FUNC, name, start))
        elif name in self.CONSTANTS:
            self.tokens.append(Token(TokenType.CONSTANT if name != 'pi' else TokenType.PI,
                                     self.CONSTANTS[name], start))
        else:
            self.tokens.append(Token(TokenType.VARIABLE, name, start))


class Parser:
    """
    Parser recursivo descendente que respeta la jerarquía de operaciones.
    Convierte tokens en un árbol de expresiones y lo evalúa.
    
    Gramática:
        expr   : term ((+|-) term)*
        term   : power ((*|/) power)*
        power  : unary (^ unary)*
        unary  : -unary | +unary | postfix
        postfix: primary (! | %)*
        primary: NUMBER | CONST | FUNC(expr) | (expr)
    """
    
    def __init__(self, lexer: Lexer, variables: Optional[Dict[str, float]] = None):
        self.lexer = lexer
        self.tokens: List[Token] = []
        self.pos = 0
        self.variables = variables or {}
    
    def parse(self, text: str) -> float:
        """Parsea y evalúa una expresión matemática."""
        self.tokens = self.lexer.tokenize(text)
        self.pos = 0
        result = self._expr()
        
        if self._current().type != TokenType.EOF:
            raise ParseError(f"Token inesperado en posición {self._current().position}")
        
        if math.isnan(result):
            raise MathError("Resultado indefinido (NaN)")
        if math.isinf(result) and result > 0:
            return math.inf
        if math.isinf(result):
            return -math.inf
        
        return result
    
    def _current(self) -> Token:
        """Retorna el token actual."""
        return self.tokens[self.pos]
    
    def _consume(self, expected: Optional[TokenType] = None) -> Token:
        """Consume y retorna el token actual."""
        token = self._current()
        if expected and token.type != expected:
            raise ParseError(
                f"Se esperaba {expected.name}, se obtuvo {token.type.name} "
                f"en posición {token.position}"
            )
        self.pos += 1
        return token
    
    def _peek(self, offset: int = 1) -> Token:
        """Mira el siguiente token sin consumirlo."""
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else Token(TokenType.EOF, None, 0)
    
    def _expr(self) -> float:
        """Regla para expresiones: term ((+|-) term)*"""
        result = self._term()
        
        while self._current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self._consume()
            right = self._term()
            if op.type == TokenType.PLUS:
                result += right
            else:
                result -= right
        
        return result
    
    def _term(self) -> float:
        """Regla para términos: power ((*|/) power)*"""
        result = self._power()
        
        while self._current().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self._consume()
            right = self._power()
            if op.type == TokenType.MULTIPLY:
                result *= right
            else:
                if right == 0:
                    raise MathError("División por cero")
                result /= right
        
        return result
    
    def _power(self) -> float:
        """Regla para potencias: unary (^ unary)*"""
        result = self._unary()
        
        while self._current().type == TokenType.POWER:
            self._consume()
            exponent = self._unary()
            try:
                result = result ** exponent
            except OverflowError:
                raise MathError("Resultado demasiado grande")
        
        return result
    
    def _unary(self) -> float:
        """Regla para unarios: -unary | +unary | postfix"""
        if self._current().type == TokenType.MINUS:
            self._consume()
            return -self._unary()
        elif self._current().type == TokenType.PLUS:
            self._consume()
            return self._unary()
        return self._postfix()
    
    def _postfix(self) -> float:
        """Regla para operadores postfijos: primary (! | %)*"""
        result = self._primary()
        
        while self._current().type in (TokenType.FACTORIAL, TokenType.PERCENT):
            op = self._consume()
            if op.type == TokenType.FACTORIAL:
                result = self._factorial(result)
            elif op.type == TokenType.PERCENT:
                result /= 100
        
        return result
    
    def _primary(self) -> float:
        """Regla para primarios: NUMBER | CONST | FUNC(expr) | (expr)"""
        token = self._current()
        
        if token.type == TokenType.NUMBER:
            self._consume()
            return token.value
        
        elif token.type in (TokenType.PI, TokenType.CONSTANT):
            self._consume()
            return token.value
        
        elif token.type == TokenType.VARIABLE:
            self._consume()
            name = token.value
            if name in self.variables:
                return self.variables[name]
            raise ParseError(f"Variable '{name}' no definida")
        
        elif token.type == TokenType.FUNC:
            func_name = token.value
            self._consume()
            
            args = []
            if self._current().type == TokenType.LPAREN:
                self._consume(TokenType.LPAREN)
                
                if self._current().type != TokenType.RPAREN:
                    args.append(self._expr())
                    while self._current().type == TokenType.COMMA:
                        self._consume()
                        args.append(self._expr())
                
                self._consume(TokenType.RPAREN)
            
            return self._call_function(func_name, args)
        
        elif token.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            result = self._expr()
            self._consume(TokenType.RPAREN)
            return result
        
        else:
            raise ParseError(
                f"Token inesperado '{token.value}' en posición {token.position}"
            )
    
    def _call_function(self, name: str, args: List[float]) -> float:
        """Llama a una función matemática con conversión de ángulos."""
        if name not in self.lexer.FUNCTIONS:
            raise ParseError(f"Función '{name}' no reconocida")
        
        if not args:
            raise ParseError(f"Función '{name}' requiere al menos un argumento")
        
        func = self.lexer.FUNCTIONS[name]
        x = args[0]
        
        trig_funcs = {'sin', 'cos', 'tan', 'asin', 'acos', 'atan'}
        if name in trig_funcs and self.lexer.angle_mode == 'deg':
            if name in ('sin', 'cos', 'tan'):
                x = math.radians(x)
            else:
                result = func(x)
                return math.degrees(result)
        
        try:
            result = func(x)
        except (ValueError, ZeroDivisionError) as e:
            raise MathError(f"Error en {name}({x}): {str(e)}")
        
        return result
    
    def _factorial(self, n: float) -> float:
        """Calcula el factorial de un número."""
        if n < 0:
            raise MathError("Factorial no definido para negativos")
        if n != int(n):
            raise MathError("Factorial solo definido para enteros")
        if n > 170:
            raise MathError("Factorial demasiado grande (overflow)")
        return math.factorial(int(n))


class ExpressionParser:
    """
    Interfaz principal para parsear expresiones matemáticas.
    Facilita el uso del lexer y parser.
    """
    
    def __init__(self, angle_mode: str = 'deg'):
        self.lexer = Lexer(angle_mode)
        self.parser = Parser(self.lexer)
        self.angle_mode = angle_mode
    
    def evaluate(self, expression: str, variables: Optional[Dict[str, float]] = None) -> float:
        """
        Evalúa una expresión matemática de forma segura.
        
        Args:
            expression: Expresión matemática como string
            variables: Diccionario de variables definidas por el usuario
        
        Returns:
            Resultado numérico de la expresión
        
        Raises:
            ParseError: Si la expresión tiene errores de sintaxis
            MathError: Si hay errores matemáticos
        """
        self.parser.variables = variables or {}
        cleaned = self._preprocess(expression)
        
        if not cleaned:
            raise ParseError("Expresión vacía")
        
        return self.parser.parse(cleaned)
    
    def set_angle_mode(self, mode: str):
        """Cambia el modo de ángulos."""
        if mode not in ('deg', 'rad'):
            raise ValueError("Modo debe ser 'deg' o 'rad'")
        self.angle_mode = mode
        self.lexer.angle_mode = mode
    
    def _preprocess(self, expression: str) -> str:
        """
        Preprocesa la expresión para facilitar el parsing.
        Maneja notación implícita de multiplicación.
        """
        expr = expression.strip()
        
        expr = expr.replace('×', '*').replace('÷', '/')
        expr = expr.replace('−', '-').replace('＋', '+')
        
        patterns = [
            (r'(\d)(\()', r'\1*\2'),
            (r'(\))(\d)', r'\1*\2'),
            (r'(\))(\()', r'\1*\2'),
            (r'(\d)(pi|π|e|tau)', r'\1*\2'),
            (r'(pi|π|e|tau)(\d)', r'\1*\2'),
            (r'(\d)(sin|cos|tan|asin|acos|atan|log|ln|sqrt|exp)', r'\1*\2'),
        ]
        
        for pattern, replacement in patterns:
            expr = re.sub(pattern, replacement, expr)
        
        return expr
    
    def get_supported_functions(self) -> List[str]:
        """Retorna lista de funciones soportadas."""
        return sorted(self.lexer.FUNCTIONS.keys())
    
    def get_constants(self) -> Dict[str, float]:
        """Retorna diccionario de constantes disponibles."""
        return dict(self.lexer.CONSTANTS)
