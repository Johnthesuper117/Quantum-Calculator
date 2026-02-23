"""Tests for quantum_calculator.advanced"""
import math
import pytest
from quantum_calculator.advanced import (
    power, sqrt, nth_root,
    ln, log10, log2,
    sin, cos, tan, asin, acos, atan,
    absolute, floor, ceil, factorial,
)


class TestPower:
    def test_square(self):
        assert power(2, 10) == 1024

    def test_fractional_exp(self):
        assert power(4, 0.5) == pytest.approx(2.0)

    def test_zero_exp(self):
        assert power(99, 0) == 1

    def test_negative_base(self):
        assert power(-2, 3) == -8


class TestSqrt:
    def test_perfect_square(self):
        assert sqrt(144) == 12.0

    def test_zero(self):
        assert sqrt(0) == 0.0

    def test_float(self):
        assert sqrt(2) == pytest.approx(math.sqrt(2))

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            sqrt(-1)


class TestNthRoot:
    def test_cube_root(self):
        assert nth_root(27, 3) == pytest.approx(3.0)

    def test_square_root(self):
        assert nth_root(16, 2) == pytest.approx(4.0)

    def test_negative_odd_root(self):
        assert nth_root(-8, 3) == pytest.approx(-2.0)

    def test_even_root_negative_raises(self):
        with pytest.raises(ValueError):
            nth_root(-4, 2)

    def test_zero_degree_raises(self):
        with pytest.raises(ValueError):
            nth_root(8, 0)


class TestLn:
    def test_e(self):
        assert ln(math.e) == pytest.approx(1.0)

    def test_one(self):
        assert ln(1) == pytest.approx(0.0)

    def test_non_positive_raises(self):
        with pytest.raises(ValueError):
            ln(0)
        with pytest.raises(ValueError):
            ln(-5)


class TestLog10:
    def test_thousand(self):
        assert log10(1000) == pytest.approx(3.0)

    def test_one(self):
        assert log10(1) == pytest.approx(0.0)

    def test_non_positive_raises(self):
        with pytest.raises(ValueError):
            log10(0)


class TestLog2:
    def test_eight(self):
        assert log2(8) == pytest.approx(3.0)

    def test_one(self):
        assert log2(1) == pytest.approx(0.0)


class TestTrig:
    def test_sin_pi_half(self):
        assert sin(math.pi / 2) == pytest.approx(1.0)

    def test_cos_zero(self):
        assert cos(0) == pytest.approx(1.0)

    def test_tan_pi_quarter(self):
        assert tan(math.pi / 4) == pytest.approx(1.0)

    def test_asin_one(self):
        assert asin(1) == pytest.approx(math.pi / 2)

    def test_acos_one(self):
        assert acos(1) == pytest.approx(0.0)

    def test_atan_one(self):
        assert atan(1) == pytest.approx(math.pi / 4)

    def test_asin_out_of_range(self):
        with pytest.raises(ValueError):
            asin(2)

    def test_acos_out_of_range(self):
        with pytest.raises(ValueError):
            acos(-2)


class TestMisc:
    def test_absolute_positive(self):
        assert absolute(5) == 5

    def test_absolute_negative(self):
        assert absolute(-5) == 5

    def test_floor(self):
        assert floor(3.7) == 3
        assert floor(-3.2) == -4

    def test_ceil(self):
        assert ceil(3.1) == 4
        assert ceil(-3.7) == -3

    def test_factorial_zero(self):
        assert factorial(0) == 1

    def test_factorial_five(self):
        assert factorial(5) == 120

    def test_factorial_float_whole(self):
        assert factorial(5.0) == 120

    def test_factorial_negative_raises(self):
        with pytest.raises(ValueError):
            factorial(-1)

    def test_factorial_float_raises(self):
        with pytest.raises(ValueError):
            factorial(2.5)
