"""Stdlib-runnable tests: `python3 test_calculator.py` (also pytest-compatible)."""
from calculator import add, subtract


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 2) == 3


if __name__ == "__main__":
    test_add()
    test_subtract()
    print("all tests passed")
