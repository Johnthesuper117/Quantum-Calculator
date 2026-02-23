#!/usr/bin/env python3
"""
Quantum Calculator — command-line interface.

Run modes
---------
1. Interactive REPL (no arguments):
       python main.py

2. Single expression (arguments joined):
       python main.py "1 + 2(2/2) * 4 - 1"
       python main.py sqrt 16 + 2 ^ 3

3. Piped / scripted (stdin):
       echo "3^3 - 1" | python main.py
"""

import sys

from quantum_calculator import solve, CalculatorError


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------
_SEPARATOR = "-" * 40


def _display(expression: str) -> None:
    """Evaluate *expression* and print a formatted result with steps."""
    try:
        result, steps = solve(expression)
    except CalculatorError as exc:
        print(f"  Error: {exc}", file=sys.stderr)
        return

    print(f"\nExpression : {expression}")
    if steps:
        print("Steps (PEMDAS order):")
        for i, step in enumerate(steps, start=1):
            print(f"  Step {i}: {step}")
    else:
        print("  (single value — no computation needed)")

    # Format result: show as integer when the answer is a whole number
    if isinstance(result, float) and result.is_integer():
        print(f"Result     : {int(result)}")
    else:
        print(f"Result     : {result:.10g}")
    print()


# ---------------------------------------------------------------------------
# Interactive REPL
# ---------------------------------------------------------------------------
def _interactive() -> None:
    print("╔══════════════════════════════════════╗")
    print("║       Quantum Calculator v1.0        ║")
    print("╠══════════════════════════════════════╣")
    print("║  Operators : + - * / % ^ ( )         ║")
    print("║  Functions : sqrt abs floor ceil      ║")
    print("║              ln log10 log2            ║")
    print("║              sin cos tan              ║")
    print("║              asin acos atan           ║")
    print("║              factorial                ║")
    print("║  Constants : pi  e                   ║")
    print("║  Type 'help' for examples            ║")
    print("║  Type 'quit' or 'exit' to leave      ║")
    print("╚══════════════════════════════════════╝")
    print()

    while True:
        try:
            expression = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not expression:
            continue

        if expression.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if expression.lower() == "help":
            _print_help()
            continue

        _display(expression)


def _print_help() -> None:
    examples = [
        ("Basic arithmetic",     "3 + 4 * 2"),
        ("Parentheses",          "(3 + 4) * 2"),
        ("Implicit multiply",    "2(3 + 1)"),
        ("Exponent",             "2^10"),
        ("Square root",          "sqrt(144)"),
        ("Mixed expression",     "1 + 2(2/2) * 4 - 1"),
        ("Trig (radians)",       "sin(pi / 2)"),
        ("Logarithm",            "log10(1000)"),
        ("Factorial",            "factorial(5)"),
        ("Constants",            "pi * 2"),
    ]
    print()
    print("Examples:")
    print(_SEPARATOR)
    for label, expr in examples:
        print(f"  {label:<22}  {expr}")
    print(_SEPARATOR)
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    if not sys.stdin.isatty():
        # Piped mode: read one expression per line from stdin
        for line in sys.stdin:
            line = line.strip()
            if line:
                _display(line)
    elif len(sys.argv) > 1:
        # Single expression passed as CLI arguments
        expression = " ".join(sys.argv[1:])
        _display(expression)
    else:
        # Interactive REPL
        _interactive()


if __name__ == "__main__":
    main()
