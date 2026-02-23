"""Tests for quantum_calculator.arithmetic"""
import pytest
from quantum_calculator.arithmetic import add, subtract, multiply, divide, modulo


class TestAdd:
    def test_integers(self):
        assert add(2, 3) == 5

    def test_floats(self):
        assert add(1.5, 2.5) == 4.0

    def test_negative(self):
        assert add(-1, 1) == 0

    def test_zero(self):
        assert add(0, 0) == 0


class TestSubtract:
    def test_positive_result(self):
        assert subtract(5, 3) == 2

    def test_negative_result(self):
        assert subtract(3, 5) == -2

    def test_floats(self):
        assert subtract(2.5, 1.5) == 1.0


class TestMultiply:
    def test_integers(self):
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        assert multiply(9999, 0) == 0

    def test_floats(self):
        assert multiply(2.5, 4) == 10.0

    def test_negatives(self):
        assert multiply(-3, -4) == 12


class TestDivide:
    def test_exact(self):
        assert divide(10, 2) == 5.0

    def test_float_result(self):
        assert divide(1, 4) == 0.25

    def test_negative(self):
        assert divide(-8, 2) == -4.0

    def test_zero_divisor(self):
        with pytest.raises(ZeroDivisionError):
            divide(5, 0)


class TestModulo:
    def test_basic(self):
        assert modulo(10, 3) == 1

    def test_exact_divisible(self):
        assert modulo(9, 3) == 0

    def test_zero_divisor(self):
        with pytest.raises(ZeroDivisionError):
            modulo(5, 0)
