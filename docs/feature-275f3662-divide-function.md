# Feature: Add `divide(a, b)` to `calculator.py`

## Overview
This feature adds division support to the tiny calculator module while keeping the project dependency-free and easy to run from the command line.

## What was built
- Added `divide(a, b)` to `calculator.py`
- Added `test_divide()` to `test_calculator.py`
- Updated the `__main__` block so `python3 test_calculator.py` runs the full calculator test set directly

## Technical implementation
- `divide(a, b)` returns the native Python quotient `a / b`
- The function performs an explicit zero check and raises `ValueError` when the divisor is `0`
- The test module imports `divide` alongside the other calculator helpers
- `test_divide()` covers both expected behavior and the zero-divisor failure case
- The direct-run entrypoint still ends with `print("all tests passed")`

## How to use
### From Python code
```python
from calculator import add, subtract, divide

print(add(2, 3))       # 5
print(subtract(5, 2))  # 3
print(divide(8, 2))    # 4.0
```

### Run the tests directly
```bash
python3 test_calculator.py
```

### Run the pytest suite
```bash
python -m pytest
```

## Configuration
No configuration is required. The change uses only the Python standard library and does not add environment variables or external dependencies.

## Testing notes
- `python3 test_calculator.py` validates the new division behavior without requiring pytest
- `test_divide()` checks a normal division case and confirms division by zero raises `ValueError`
- The repository remains pytest-compatible, so the same tests can also be run with `python -m pytest`
- The explicit zero check prevents Python’s built-in `ZeroDivisionError` from leaking through the calculator API
