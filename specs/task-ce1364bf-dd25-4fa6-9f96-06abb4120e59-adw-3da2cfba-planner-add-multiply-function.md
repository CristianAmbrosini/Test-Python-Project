# Feature: Add multiply(a, b) to calculator.py

## Metadata
task_id: `ce1364bf-dd25-4fa6-9f96-06abb4120e59`
adw_id: `3da2cfba`
project_id: `prj_6efcfced-a176-4e4c-a989-9767c16fddf7`

## Feature Description
Add a new `multiply(a, b)` function to the calculator module so the application can perform basic multiplication alongside the existing `add(a, b)` and `subtract(a, b)` helpers. The feature should include direct test coverage in `test_calculator.py` and preserve the current stdlib-friendly test entrypoint so the suite can be run with `python3 test_calculator.py`.

## User Story
As a developer using the calculator module
I want to multiply two numbers with the same lightweight API style as the other arithmetic helpers
So that the module supports a complete basic arithmetic operation set without adding complexity.

## Problem Statement
The calculator module currently supports addition and subtraction only. Consumers and regression tests have no built-in way to verify multiplication behavior, which leaves the arithmetic helper set incomplete and the test harness unable to validate a third core operation.

## Solution Statement
Extend `calculator.py` with a simple `multiply(a, b)` function that returns `a * b`. Add a matching `test_multiply()` in `test_calculator.py`, import the new function, and invoke the test from the `__main__` block so the existing direct execution workflow remains intact. Keep the implementation minimal and consistent with the current module style.

## Relevant Files
Use these files to implement the feature:

- `calculator.py`
  - Add the new `multiply(a, b)` function next to the existing arithmetic helpers.
  - Keep the module style consistent with the current tiny, dependency-free design.

- `test_calculator.py`
  - Import `multiply` from `calculator`.
  - Add `test_multiply()` with straightforward assertions that verify the new function returns the expected product.
  - Update the `__main__` block so `python3 test_calculator.py` executes the new test.

- `README.md`
  - Confirm the project’s current test workflow and ensure the plan stays aligned with the documented lightweight setup.

### New Files
- None required for this feature.

## Implementation Plan
### Phase 1: Foundation
Confirm the current arithmetic API and test runner structure in `calculator.py` and `test_calculator.py`, then identify the smallest safe change needed to add multiplication without introducing new dependencies or altering the existing execution model.

### Phase 2: Core Implementation
Implement `multiply(a, b)` in `calculator.py`. Update `test_calculator.py` to import the new function, add `test_multiply()`, and call it from the `__main__` block so the stdlib-runnable test file exercises all arithmetic helpers.

### Phase 3: Integration
Run the direct test command and the repository’s pytest command to verify the new helper behaves correctly and that the project remains compatible with both execution styles.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Verify the current calculator/test structure
- Review `calculator.py` and `test_calculator.py` to confirm the existing function signatures, import style, and `__main__` test runner pattern.
- Keep the implementation intentionally simple to match the repository’s minimal Python footprint.

### 2. Implement multiplication in the calculator module
- Add `multiply(a, b)` to `calculator.py`.
- Return the direct arithmetic product `a * b` with no extra branching or helper abstractions.
- Preserve the module’s current docstring and lightweight structure.

### 3. Extend the test module
- Import `multiply` in `test_calculator.py` alongside `add` and `subtract`.
- Create `test_multiply()` with a clear assertion, such as verifying a positive integer case.
- Call `test_multiply()` from the `if __name__ == "__main__":` block after the existing tests so direct execution validates the new behavior.

### 4. Validate the feature end-to-end
- Run `python3 test_calculator.py` to confirm the stdlib test entrypoint passes and prints the expected success message.
- Run `python -m pytest` to confirm the new test remains compatible with pytest collection and execution.
- If either command fails, fix the implementation or test update and rerun both commands until they pass cleanly.

## Testing Strategy
### Unit Tests
- Verify `multiply(2, 3) == 6` in a new `test_multiply()` unit test.
- Keep the test style consistent with the existing direct `assert`-based tests.
- Ensure the `__main__` block includes the new test so the file remains self-validating when executed directly.

### Edge Cases
- Multiplication by zero should return zero.
- Multiplication with negative numbers should preserve sign correctly.
- Large integer multiplication should behave like standard Python arithmetic.
- If future floating-point tests are added, the implementation should continue to rely on native Python multiplication semantics.

## Acceptance Criteria
- `calculator.py` exports a `multiply(a, b)` function that returns `a * b`.
- `test_calculator.py` includes `test_multiply()` with at least one assertion covering the new function.
- The `__main__` block in `test_calculator.py` calls `test_multiply()`.
- `python3 test_calculator.py` runs successfully from the repository root and reports all tests passed.
- `python -m pytest` also passes without regressions to the existing tests.

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `python3 test_calculator.py` - Run the stdlib test entrypoint required by the task.
- `python -m pytest` - Verify pytest compatibility and ensure all tests still pass under the project’s documented workflow.

## Notes
- This is a minimal Python-only change; no package manager, build step, or type-check command is defined in the repository.
- The feature should stay dependency-free and preserve the current low-friction test workflow.
