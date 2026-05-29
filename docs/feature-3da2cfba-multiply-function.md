# Feature: Add `multiply(a, b)` to `calculator.py`

## Overview
This feature adds a third arithmetic helper to the tiny calculator module: `multiply(a, b)`. It keeps the project dependency-free and preserves the existing lightweight test workflow.

## What was built
- Added `multiply(a, b)` to `calculator.py`
- Added `test_multiply()` to `test_calculator.py`
- Updated the `__main__` block so `python3 test_calculator.py` runs the new test directly

## Technical implementation
- `multiply(a, b)` returns the native Python product `a * b`
- The test module now imports `multiply` alongside `add` and `subtract`
- `test_multiply()` uses a straightforward assertion to verify expected output:
  - `multiply(2, 3) == 6`
- The direct-run test entrypoint still ends with `print("all tests passed")`

## How to use
### From Python code
```python
from calculator import add, subtract, multiply

print(add(2, 3))       # 5
print(subtract(5, 2))   # 3
print(multiply(2, 3))   # 6
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
No configuration is required. The change is a small standard-library-only update with no new dependencies or environment variables.

## Testing notes
- The direct script runner confirms the module remains usable without pytest
- Pytest still discovers and runs the `test_*` functions normally
- Because the implementation uses native Python multiplication, it inherits standard behavior for zero, negative numbers, large integers, and floats
