"""
Arithmetic module — basic arithmetic operations for the Quantum Calculator.
"""


def add(a, b):
    """Return a + b."""
    return a + b


def subtract(a, b):
    """Return a - b."""
    return a - b


def multiply(a, b):
    """Return a * b."""
    return a * b


def divide(a, b):
    """Return a / b.  Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Division by zero is undefined.")
    return a / b


def modulo(a, b):
    """Return a % b.  Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Modulo by zero is undefined.")
    return a % b
