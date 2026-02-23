"""
Quantum Calculator — public package API.

Usage as a module
-----------------
>>> from quantum_calculator import solve
>>> result, steps = solve("1 + 2(2/2) * 4 - 1")
>>> print(result)
8.0
>>> for step in steps:
...     print(step)
2 / 2 = 1
2 * 1 = 2  (implicit multiplication)
2 * 4 = 8
1 + 8 = 9
9 - 1 = 8

Usage from another program
--------------------------
>>> import quantum_calculator as qc
>>> qc.solve("sqrt(144) + 3^2")
(21.0, ['sqrt(144) = 12', '3 ^ 2 = 9', '12 + 9 = 21'])
"""

from quantum_calculator.parser import evaluate, CalculatorError   # noqa: F401
from quantum_calculator import arithmetic, advanced                 # noqa: F401


def solve(expression: str):
    """
    Solve a mathematical expression and return the result with step-by-step
    working.

    Parameters
    ----------
    expression : str
        Any valid mathematical expression, e.g. ``"3 + 4 * 2"`` or
        ``"sqrt(9) * (2^3 - 1)"``.

    Returns
    -------
    result : float
        The numeric answer.
    steps : list[str]
        Step-by-step descriptions of each sub-calculation, in the order
        they were performed (PEMDAS).

    Raises
    ------
    CalculatorError
        If the expression is malformed or causes a math error.

    Examples
    --------
    >>> result, steps = solve("2 + 3 * 4")
    >>> result
    14.0
    >>> steps
    ['3 * 4 = 12', '2 + 12 = 14']
    """
    return evaluate(expression)


__all__ = ["solve", "evaluate", "CalculatorError", "arithmetic", "advanced"]
