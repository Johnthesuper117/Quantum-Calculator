"""
Expression parser for the Quantum Calculator.

Implements a tokenizer and a recursive-descent parser that enforces full
PEMDAS order of operations and records every sub-calculation as a human-
readable step.

Supported operators and syntax
-------------------------------
  +  -  *  /  %  ^            – standard binary operators
  (  )                         – grouping (explicit or implicit: 2(3+1))
  -x  +x                       – unary negation / unary plus
  sqrt(x)  abs(x)  floor(x)   – single-argument math functions
  ceil(x)  ln(x)   log10(x)
  log2(x)  sin(x)  cos(x)
  tan(x)   asin(x) acos(x)
  atan(x)  factorial(x)
  pi  e                        – built-in constants

Operator precedence (highest to lowest)
-----------------------------------------
  1. parentheses / function calls
  2. unary -  /  unary +
  3. ^ (right-associative)
  4. *  /  %
  5. +  -
"""

import math
from quantum_calculator import arithmetic, advanced as adv

# ---------------------------------------------------------------------------
# Token types
# ---------------------------------------------------------------------------
_NUMBER   = "NUMBER"
_PLUS     = "PLUS"
_MINUS    = "MINUS"
_STAR     = "STAR"
_SLASH    = "SLASH"
_CARET    = "CARET"
_PERCENT  = "PERCENT"
_LPAREN   = "LPAREN"
_RPAREN   = "RPAREN"
_FUNCTION = "FUNCTION"
_EOF      = "EOF"

# ---------------------------------------------------------------------------
# Built-in functions (name → callable)
# ---------------------------------------------------------------------------
_FUNCTIONS = {
    "sqrt":      adv.sqrt,
    "abs":       adv.absolute,
    "floor":     adv.floor,
    "ceil":      adv.ceil,
    "ln":        adv.ln,
    "log10":     adv.log10,
    "log2":      adv.log2,
    "sin":       adv.sin,
    "cos":       adv.cos,
    "tan":       adv.tan,
    "asin":      adv.asin,
    "acos":      adv.acos,
    "atan":      adv.atan,
    "factorial": adv.factorial,
}

# Built-in constants (name → value)
_CONSTANTS = {
    "pi": math.pi,
    "e":  math.e,
}


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------
class CalculatorError(Exception):
    """Raised for any evaluation or parse error in the calculator."""


# ---------------------------------------------------------------------------
# Token
# ---------------------------------------------------------------------------
class _Token:
    __slots__ = ("type", "value")

    def __init__(self, type_, value):
        self.type  = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------
def _tokenize(expression: str) -> list:
    """Convert *expression* into a flat list of _Token objects."""
    tokens = []
    i = 0
    expr = expression  # work on the raw string (spaces allowed)

    while i < len(expr):
        c = expr[i]

        # Skip whitespace
        if c.isspace():
            i += 1
            continue

        # Number literal (integer or decimal)
        if c.isdigit() or (c == "." and i + 1 < len(expr) and expr[i + 1].isdigit()):
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == "."):
                j += 1
            raw = expr[i:j]
            if raw.count(".") > 1:
                raise CalculatorError(f"Invalid number literal: '{raw}'")
            tokens.append(_Token(_NUMBER, float(raw)))
            i = j
            continue

        # Identifier: function name or constant
        if c.isalpha() or c == "_":
            j = i
            while j < len(expr) and (expr[j].isalnum() or expr[j] == "_"):
                j += 1
            name = expr[i:j]
            if name in _FUNCTIONS:
                tokens.append(_Token(_FUNCTION, name))
            elif name in _CONSTANTS:
                tokens.append(_Token(_NUMBER, _CONSTANTS[name]))
            else:
                raise CalculatorError(f"Unknown function or constant: '{name}'")
            i = j
            continue

        # Single-character operators / punctuation
        _CHAR_MAP = {
            "+": _PLUS,
            "-": _MINUS,
            "*": _STAR,
            "/": _SLASH,
            "^": _CARET,
            "%": _PERCENT,
            "(": _LPAREN,
            ")": _RPAREN,
        }
        if c in _CHAR_MAP:
            tokens.append(_Token(_CHAR_MAP[c], c))
            i += 1
            continue

        raise CalculatorError(f"Unrecognised character: '{c}'")

    tokens.append(_Token(_EOF, None))
    return tokens


# ---------------------------------------------------------------------------
# Number formatter
# ---------------------------------------------------------------------------
def _fmt(value) -> str:
    """Format a numeric value for display in step descriptions."""
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        # Remove floating-point noise beyond 10 significant digits
        return f"{value:.10g}"
    return str(value)


# ---------------------------------------------------------------------------
# Recursive-descent parser
# ---------------------------------------------------------------------------
class _Parser:
    """
    Parse and evaluate a token list, recording every sub-calculation in
    *self.steps* as a human-readable string.

    Grammar (in order of increasing precedence):
        expression   → additive
        additive     → multiplicative ( ('+' | '-') multiplicative )*
        multiplicative → exponent ( ('*' | '/' | '%') exponent )*
        exponent     → unary ( '^' unary )*          # right-associative
        unary        → '-' unary | '+' unary | primary
        primary      → NUMBER [ '(' expression ')' ]
                      | '(' expression ')'
                      | FUNCTION '(' expression ')'
    """

    def __init__(self, tokens: list, steps: list):
        self._tokens = tokens
        self._pos    = 0
        self.steps   = steps   # list that accumulates step descriptions

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _cur(self) -> _Token:
        return self._tokens[self._pos]

    def _consume(self, expected_type=None) -> _Token:
        tok = self._tokens[self._pos]
        if expected_type and tok.type != expected_type:
            raise CalculatorError(
                f"Expected '{expected_type}' but got '{tok.type}' ({tok.value!r})."
            )
        self._pos += 1
        return tok

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------
    def parse(self):
        result = self._parse_additive()
        if self._cur().type != _EOF:
            raise CalculatorError(
                f"Unexpected token '{self._cur().value}' in expression."
            )
        return result

    # ------------------------------------------------------------------
    # Level 1: Addition / Subtraction
    # ------------------------------------------------------------------
    def _parse_additive(self):
        left = self._parse_multiplicative()
        while self._cur().type in (_PLUS, _MINUS):
            op  = self._consume()
            right = self._parse_multiplicative()
            if op.type == _PLUS:
                result = arithmetic.add(left, right)
                self.steps.append(f"{_fmt(left)} + {_fmt(right)} = {_fmt(result)}")
            else:
                result = arithmetic.subtract(left, right)
                self.steps.append(f"{_fmt(left)} - {_fmt(right)} = {_fmt(result)}")
            left = result
        return left

    # ------------------------------------------------------------------
    # Level 2: Multiplication / Division / Modulo
    # ------------------------------------------------------------------
    def _parse_multiplicative(self):
        left = self._parse_exponent()
        while self._cur().type in (_STAR, _SLASH, _PERCENT):
            op  = self._consume()
            right = self._parse_exponent()
            if op.type == _STAR:
                result = arithmetic.multiply(left, right)
                self.steps.append(f"{_fmt(left)} * {_fmt(right)} = {_fmt(result)}")
            elif op.type == _SLASH:
                result = arithmetic.divide(left, right)
                self.steps.append(f"{_fmt(left)} / {_fmt(right)} = {_fmt(result)}")
            else:
                result = arithmetic.modulo(left, right)
                self.steps.append(f"{_fmt(left)} % {_fmt(right)} = {_fmt(result)}")
            left = result
        return left

    # ------------------------------------------------------------------
    # Level 3: Exponentiation (right-associative)
    # ------------------------------------------------------------------
    def _parse_exponent(self):
        base = self._parse_unary()
        if self._cur().type == _CARET:
            self._consume()
            exp    = self._parse_exponent()   # recurse right for right-assoc
            result = adv.power(base, exp)
            self.steps.append(f"{_fmt(base)} ^ {_fmt(exp)} = {_fmt(result)}")
            return result
        return base

    # ------------------------------------------------------------------
    # Level 4: Unary minus / plus
    # ------------------------------------------------------------------
    def _parse_unary(self):
        if self._cur().type == _MINUS:
            self._consume()
            operand = self._parse_unary()
            return -operand  # negation; no separate step needed
        if self._cur().type == _PLUS:
            self._consume()
            return self._parse_unary()
        return self._parse_primary()

    # ------------------------------------------------------------------
    # Level 5: Literals, parentheses, functions, implicit multiplication
    # ------------------------------------------------------------------
    def _parse_primary(self):
        tok = self._cur()

        # FUNCTION ( expression )
        if tok.type == _FUNCTION:
            fname = tok.value
            func  = _FUNCTIONS[fname]
            self._consume()    # eat function name
            self._consume(_LPAREN)
            arg = self._parse_additive()
            self._consume(_RPAREN)
            try:
                result = func(arg)
            except (ValueError, ZeroDivisionError, OverflowError) as exc:
                raise CalculatorError(str(exc)) from exc
            self.steps.append(f"{fname}({_fmt(arg)}) = {_fmt(result)}")
            return result

        # ( expression )
        if tok.type == _LPAREN:
            self._consume()
            result = self._parse_additive()
            self._consume(_RPAREN)
            return result

        # NUMBER  (possibly followed by implicit multiplication)
        if tok.type == _NUMBER:
            self._consume()
            value = tok.value

            # Implicit multiplication: 2(3+1) → 2 * 4
            if self._cur().type == _LPAREN:
                self._consume()
                inner = self._parse_additive()
                self._consume(_RPAREN)
                result = arithmetic.multiply(value, inner)
                self.steps.append(
                    f"{_fmt(value)} * {_fmt(inner)} = {_fmt(result)}"
                    f"  (implicit multiplication)"
                )
                return result

            return value

        raise CalculatorError(
            f"Unexpected token '{tok.value}' — expected a number, "
            f"function, or '('."
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def evaluate(expression: str):
    """
    Evaluate a mathematical expression string and return the result together
    with a list of step-by-step descriptions.

    Parameters
    ----------
    expression : str
        A mathematical expression such as ``"1 + 2(2/2) * 4 - 1"`` or
        ``"sqrt(16) + 2^3"``.

    Returns
    -------
    result : float
        The numeric result of the expression.
    steps : list[str]
        Ordered list of sub-calculation descriptions showing how the
        result was reached (PEMDAS order).

    Raises
    ------
    CalculatorError
        For syntax errors, unknown identifiers, or math domain errors.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise CalculatorError("Expression must be a non-empty string.")

    steps: list = []
    try:
        tokens = _tokenize(expression.strip())
        parser = _Parser(tokens, steps)
        result = parser.parse()
    except CalculatorError:
        raise
    except Exception as exc:
        raise CalculatorError(f"Evaluation error: {exc}") from exc

    return result, steps
