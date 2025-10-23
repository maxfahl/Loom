# examples/simple_calculator_tdd.py

# This file demonstrates the TDD Red-Green-Refactor cycle using a simple calculator example in Python.
# We'll use `pytest` for testing.

# --- Phase 1: Red (Write a failing test) ---
# Goal: Write a test for an `add` function that should fail because the function doesn't exist yet.

# test_calculator.py (create this file first)
"""Test cases for the simple calculator."""

# import pytest
# from calculator import add

# def test_add_two_positive_numbers():
#     assert add(1, 2) == 3

# To run this test and see it fail:
# 1. Create a file named `calculator.py` (can be empty or just `def add(): pass`)
# 2. Create a file named `test_calculator.py` with the content above.
# 3. Run `pytest test_calculator.py` in your terminal.
#    You should see an error like `NameError: name 'add' is not defined` or `TypeError: add() missing 2 required positional arguments`.


# --- Phase 2: Green (Make the test pass) ---
# Goal: Write the minimal production code to make the `test_add_two_positive_numbers` pass.

# calculator.py
def add(a, b):
    return a + b

# test_calculator.py (same as above)

# To run this test and see it pass:
# 1. Ensure `calculator.py` has the `add` function as above.
# 2. Run `pytest test_calculator.py`.
#    You should see the test pass.


# --- Phase 3: Refactor (Improve the code) ---
# Goal: Improve the code's structure, readability, and maintainability without changing its behavior.
#       Add type hints, better variable names, etc.

# calculator.py
def add(num1: int, num2: int) -> int:
    """Adds two integers and returns their sum."""
    return num1 + num2

# test_calculator.py (same as above)

# To run this test and ensure it still passes after refactoring:
# 1. Ensure `calculator.py` has the refactored `add` function.
# 2. Run `pytest test_calculator.py`.
#    All tests should still pass.


# --- Extending the TDD Cycle: New Feature (Subtraction) ---

# --- Phase 1: Red (Write a failing test for subtraction) ---
# test_calculator.py (add this to the existing test file)
# def test_subtract_two_numbers():
#     assert subtract(5, 2) == 3 # This will fail because 'subtract' doesn't exist

# To run this test and see it fail:
# 1. Add the `test_subtract_two_numbers` function to `test_calculator.py`.
# 2. Run `pytest test_calculator.py`.
#    You should see the new test fail, and the `add` test still pass.


# --- Phase 2: Green (Make the subtraction test pass) ---
# calculator.py (add this function)
def subtract(a, b):
    return a - b

# test_calculator.py (same as above)

# To run this test and see it pass:
# 1. Add the `subtract` function to `calculator.py`.
# 2. Run `pytest test_calculator.py`.
#    Both `add` and `subtract` tests should now pass.


# --- Phase 3: Refactor (Improve subtraction code) ---
# calculator.py
def subtract(minuend: int, subtrahend: int) -> int:
    """Subtracts the subtrahend from the minuend and returns the difference."""
    return minuend - subtrahend

# test_calculator.py (same as above)

# To run this test and ensure it still passes after refactoring:
# 1. Ensure `calculator.py` has the refactored `subtract` function.
# 2. Run `pytest test_calculator.py`.
#    All tests should still pass.


# --- Final `calculator.py` and `test_calculator.py` for reference ---

# calculator.py
"""A simple calculator module."""

def add(num1: int, num2: int) -> int:
    """Adds two integers and returns their sum."""
    return num1 + num2

def subtract(minuend: int, subtrahend: int) -> int:
    """Subtracts the subtrahend from the minuend and returns the difference."""
    return minuend - subtrahend


# test_calculator.py
"""Test cases for the simple calculator."""

import pytest
from calculator import add, subtract

def test_add_two_positive_numbers():
    assert add(1, 2) == 3

def test_add_zero():
    assert add(0, 5) == 5

def test_add_negative_numbers():
    assert add(-1, -2) == -3

def test_subtract_two_positive_numbers():
    assert subtract(5, 2) == 3

def test_subtract_from_zero():
    assert subtract(0, 5) == -5

def test_subtract_negative_numbers():
    assert subtract(-5, -2) == -3
