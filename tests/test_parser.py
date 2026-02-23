"""Tests for quantum_calculator.parser (expression evaluation and steps)."""
import math
import pytest
from quantum_calculator.parser import evaluate, CalculatorError


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def calc(expr):
    """Return just the numeric result."""
    result, _ = evaluate(expr)
    return result


def steps(expr):
    """Return just the steps list."""
    _, s = evaluate(expr)
    return s


# ---------------------------------------------------------------------------
# Basic arithmetic
# ---------------------------------------------------------------------------
class TestBasicArithmetic:
    def test_addition(self):
        assert calc("1 + 2") == pytest.approx(3)

    def test_subtraction(self):
        assert calc("5 - 3") == pytest.approx(2)

    def test_multiplication(self):
        assert calc("3 * 4") == pytest.approx(12)

    def test_division(self):
        assert calc("10 / 4") == pytest.approx(2.5)

    def test_modulo(self):
        assert calc("10 % 3") == pytest.approx(1)

    def test_division_by_zero(self):
        with pytest.raises(CalculatorError):
            calc("5 / 0")


# ---------------------------------------------------------------------------
# PEMDAS / order of operations
# ---------------------------------------------------------------------------
class TestPEMDAS:
    def test_multiply_before_add(self):
        # 2 + 3*4 = 2 + 12 = 14
        assert calc("2 + 3 * 4") == pytest.approx(14)

    def test_parentheses_override(self):
        # (2+3)*4 = 5*4 = 20
        assert calc("(2 + 3) * 4") == pytest.approx(20)

    def test_problem_statement_example(self):
        # 1 + 2(2/2)*4 - 1  = 1 + 2*1*4 - 1 = 8
        assert calc("1 + 2(2/2) * 4 - 1") == pytest.approx(8)

    def test_nested_parentheses(self):
        # ((2+3)*2) / 5 = 10/5 = 2
        assert calc("((2 + 3) * 2) / 5") == pytest.approx(2)

    def test_left_to_right_same_precedence_add(self):
        # 10 - 3 + 2 = 9  (left-to-right)
        assert calc("10 - 3 + 2") == pytest.approx(9)

    def test_left_to_right_same_precedence_mul(self):
        # 12 / 4 * 3 = 9  (left-to-right)
        assert calc("12 / 4 * 3") == pytest.approx(9)


# ---------------------------------------------------------------------------
# Exponentiation
# ---------------------------------------------------------------------------
class TestExponentiation:
    def test_basic_power(self):
        assert calc("2 ^ 8") == pytest.approx(256)

    def test_right_associative(self):
        # 2^3^2 should be 2^(3^2) = 2^9 = 512, not (2^3)^2 = 64
        assert calc("2 ^ 3 ^ 2") == pytest.approx(512)

    def test_zero_exponent(self):
        assert calc("99 ^ 0") == pytest.approx(1)

    def test_fractional_exponent(self):
        assert calc("4 ^ 0.5") == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# Unary minus
# ---------------------------------------------------------------------------
class TestUnary:
    def test_unary_minus_number(self):
        assert calc("-5") == pytest.approx(-5)

    def test_unary_minus_in_expression(self):
        assert calc("10 + -3") == pytest.approx(7)

    def test_double_unary_minus(self):
        assert calc("--5") == pytest.approx(5)

    def test_unary_minus_parentheses(self):
        assert calc("-(3 + 2)") == pytest.approx(-5)


# ---------------------------------------------------------------------------
# Implicit multiplication
# ---------------------------------------------------------------------------
class TestImplicitMultiply:
    def test_number_paren(self):
        assert calc("2(3 + 1)") == pytest.approx(8)

    def test_number_paren_complex(self):
        assert calc("3(2 + 2(1 + 1))") == pytest.approx(18)


# ---------------------------------------------------------------------------
# Built-in functions
# ---------------------------------------------------------------------------
class TestFunctions:
    def test_sqrt(self):
        assert calc("sqrt(16)") == pytest.approx(4)

    def test_sqrt_negative_raises(self):
        with pytest.raises(CalculatorError):
            calc("sqrt(-1)")

    def test_abs_negative(self):
        assert calc("abs(-7)") == pytest.approx(7)

    def test_factorial(self):
        assert calc("factorial(5)") == pytest.approx(120)

    def test_floor(self):
        assert calc("floor(3.9)") == pytest.approx(3)

    def test_ceil(self):
        assert calc("ceil(3.1)") == pytest.approx(4)

    def test_ln(self):
        assert calc("ln(1)") == pytest.approx(0)

    def test_log10(self):
        assert calc("log10(1000)") == pytest.approx(3)

    def test_log2(self):
        assert calc("log2(8)") == pytest.approx(3)

    def test_sin(self):
        assert calc("sin(0)") == pytest.approx(0)

    def test_cos(self):
        assert calc("cos(0)") == pytest.approx(1)

    def test_tan(self):
        assert calc("tan(0)") == pytest.approx(0)

    def test_function_in_expression(self):
        # sqrt(144) + 3^2 = 12 + 9 = 21
        assert calc("sqrt(144) + 3 ^ 2") == pytest.approx(21)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
class TestConstants:
    def test_pi(self):
        assert calc("pi") == pytest.approx(math.pi)

    def test_e(self):
        assert calc("e") == pytest.approx(math.e)

    def test_pi_in_expression(self):
        # 2 * pi ≈ 6.2831...
        assert calc("2 * pi") == pytest.approx(2 * math.pi)


# ---------------------------------------------------------------------------
# Step-by-step output
# ---------------------------------------------------------------------------
class TestSteps:
    def test_no_steps_for_single_number(self):
        assert steps("42") == []

    def test_single_operation(self):
        s = steps("3 + 4")
        assert len(s) == 1
        assert "3 + 4 = 7" in s[0]

    def test_multiply_then_add_order(self):
        # 2 + 3*4 → first step is multiplication, second is addition
        s = steps("2 + 3 * 4")
        assert len(s) == 2
        assert "3 * 4 = 12" in s[0]
        assert "2 + 12 = 14" in s[1]

    def test_pemdas_example_steps(self):
        # 1 + 2(2/2)*4 - 1
        s = steps("1 + 2(2/2) * 4 - 1")
        # First step should be the division inside parens
        assert "2 / 2 = 1" in s[0]
        # Result step should end with 8
        assert "1 = 8" in s[-1]

    def test_power_step(self):
        s = steps("2 ^ 3")
        assert "2 ^ 3 = 8" in s[0]

    def test_sqrt_step(self):
        s = steps("sqrt(9)")
        assert "sqrt(9) = 3" in s[0]


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------
class TestErrors:
    def test_empty_expression(self):
        with pytest.raises(CalculatorError):
            evaluate("")

    def test_unknown_function(self):
        with pytest.raises(CalculatorError):
            calc("foo(3)")

    def test_missing_closing_paren(self):
        with pytest.raises(CalculatorError):
            calc("(3 + 2")

    def test_syntax_error(self):
        with pytest.raises(CalculatorError):
            calc("3 + * 2")
