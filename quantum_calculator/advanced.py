"""
Advanced math module — powers, roots, logarithms, trig, and other
higher-level operations for the Quantum Calculator.
"""
import math


# ---------------------------------------------------------------------------
# Powers & roots
# ---------------------------------------------------------------------------

def power(base, exp):
    """Return base raised to the power exp (base ^ exp)."""
    return base ** exp


def sqrt(x):
    """Return the square root of x.  Raises ValueError for negative x."""
    if x < 0:
        raise ValueError(f"Cannot take the square root of a negative number ({x}).")
    return math.sqrt(x)


def nth_root(x, n):
    """Return the nth root of x (x^(1/n))."""
    if n == 0:
        raise ValueError("Root degree (n) cannot be zero.")
    if x < 0 and n % 2 == 0:
        raise ValueError(f"Cannot take an even root of a negative number ({x}).")
    return math.copysign(abs(x) ** (1.0 / n), x)


# ---------------------------------------------------------------------------
# Logarithms
# ---------------------------------------------------------------------------

def ln(x):
    """Return the natural logarithm of x."""
    if x <= 0:
        raise ValueError(f"Logarithm is undefined for non-positive values ({x}).")
    return math.log(x)


def log10(x):
    """Return the base-10 logarithm of x."""
    if x <= 0:
        raise ValueError(f"Logarithm is undefined for non-positive values ({x}).")
    return math.log10(x)


def log2(x):
    """Return the base-2 logarithm of x."""
    if x <= 0:
        raise ValueError(f"Logarithm is undefined for non-positive values ({x}).")
    return math.log2(x)


# ---------------------------------------------------------------------------
# Trigonometry (arguments in radians)
# ---------------------------------------------------------------------------

def sin(x):
    """Return the sine of x (radians)."""
    return math.sin(x)


def cos(x):
    """Return the cosine of x (radians)."""
    return math.cos(x)


def tan(x):
    """Return the tangent of x (radians)."""
    return math.tan(x)


def asin(x):
    """Return the arc-sine of x (result in radians)."""
    if not (-1 <= x <= 1):
        raise ValueError(f"asin argument must be in [-1, 1]; got {x}.")
    return math.asin(x)


def acos(x):
    """Return the arc-cosine of x (result in radians)."""
    if not (-1 <= x <= 1):
        raise ValueError(f"acos argument must be in [-1, 1]; got {x}.")
    return math.acos(x)


def atan(x):
    """Return the arc-tangent of x (result in radians)."""
    return math.atan(x)


# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------

def absolute(x):
    """Return the absolute value of x."""
    return abs(x)


def floor(x):
    """Return the floor of x."""
    return math.floor(x)


def ceil(x):
    """Return the ceiling of x."""
    return math.ceil(x)


def factorial(n):
    """Return n!  n must be a non-negative integer."""
    if isinstance(n, float) and not n.is_integer():
        raise ValueError(f"Factorial requires a non-negative integer; got {n}.")
    n = int(n)
    if n < 0:
        raise ValueError(f"Factorial is undefined for negative numbers ({n}).")
    return math.factorial(n)
