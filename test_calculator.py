"""Stdlib-runnable tests: `python3 test_calculator.py` (also pytest-compatible)."""
from calculator import add, multiply, subtract


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 2) == 3


def test_multiply():
    assert multiply(2, 3) == 6


if __name__ == "__main__":
    test_add()
    test_subtract()
    test_multiply()
    print("all tests passed")