---
name: python-pep8
version: 1.0.0
category: Python / Style Guide
tags: python, pep8, style, linting, code quality, best practices
description: Enforces and guides adherence to the official Python style guide (PEP 8).
---

# Python PEP 8 Style Guide

## 1. Skill Purpose

This skill enables Claude to understand, apply, and enforce the official Python Enhancement Proposal 8 (PEP 8) style guide. Its primary goal is to ensure Python code is consistently readable, maintainable, and aesthetically pleasing, fostering collaboration and reducing cognitive load for developers.

## 2. When to Activate This Skill

Activate this skill whenever:
- Reviewing Python code for style and consistency.
- Writing new Python code or refactoring existing code.
- Setting up a new Python project or contributing to an existing one.
- Debugging style-related issues or warnings from linters.
- Explaining Python coding standards to other developers.

## 3. Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know regarding PEP 8 include:

- **Indentation**: 4 spaces per level, no tabs.
- **Line Length**: Max 79 characters for code, 72 for docstrings/comments. Use implicit line continuation.
- **Blank Lines**:
    - Two blank lines around top-level function/class definitions.
    - One blank line around method definitions inside a class.
    - One blank line to separate logical sections within functions/methods.
- **Imports**:
    - At the top of the file.
    - Grouped: standard library, third-party, local application.
    - Absolute imports preferred.
    - Avoid `from <module> import *`.
- **Whitespace**:
    - Avoid trailing whitespace.
    - Single space around binary operators.
    - No spaces immediately inside parentheses, brackets, or braces.
    - No space before a function call's opening parenthesis.
- **Naming Conventions**:
    - `snake_case` for functions, variables, and methods.
    - `CamelCase` for class names.
    - `ALL_CAPS_WITH_UNDERSCORES` for constants.
    - `_single_leading_underscore`: weak "internal use" indicator.
    - `single_trailing_underscore_`: to avoid conflicts with Python keywords.
    - `__double_leading_underscore`: name mangling for class attributes.
    - `__double_leading_and_trailing_underscore__`: "magic" objects/attributes.
- **Comments and Docstrings**:
    - Comments explain *why*, not *what*.
    - Docstrings for all public modules, functions, classes, and methods (PEP 257).
    - Limit comment/docstring lines to 72 characters.
- **Tooling**: Familiarity with linters (Flake8, Pylint, Ruff) and auto-formatters (Black, Yapf).
- **Flexibility**: Understand that PEP 8 is a guide; sometimes deviations are acceptable for readability or consistency with existing codebases.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

- ✅ Use `Black` as the primary auto-formatter for Python projects to ensure consistent formatting.
- ✅ Integrate `Flake8` or `Ruff` into CI/CD pipelines to automatically check for PEP 8 compliance.
- ✅ Write clear, concise docstrings for all public APIs following PEP 257.
- ✅ Break long lines using parentheses, brackets, or braces for implicit line continuation.
- ✅ Group imports logically and alphabetically within groups.
- ✅ Use type hints (PEP 484) consistently, as they improve readability and maintainability, complementing PEP 8.
- ✅ Prioritize readability over strict adherence if a deviation makes the code clearer.

### Never Recommend (❌ anti-patterns)

- ❌ Using tabs for indentation.
- ❌ Allowing lines to exceed 79 characters without proper continuation.
- ❌ Wildcard imports (`from module import *`).
- ❌ Inconsistent naming conventions within a project.
- ❌ Trailing whitespace.
- ❌ Ignoring linter warnings without a clear justification.
- ❌ Over-commenting obvious code; comments should add value.

### Common Questions & Responses (FAQ format)

**Q: Why is PEP 8 important?**
A: PEP 8 promotes code readability and consistency, making it easier for multiple developers to work on the same codebase and for future self to understand the code. Consistent style reduces cognitive load.

**Q: Should I always strictly follow PEP 8?**
A: PEP 8 is a guide, not a strict rulebook. While adherence is highly recommended, sometimes local consistency (e.g., with an existing codebase) or improved readability might justify minor deviations. Use your best judgment.

**Q: What tools can help me enforce PEP 8?**
A: `Black` is an opinionated auto-formatter that handles most formatting. `Flake8`, `Pylint`, and `Ruff` are linters that check for style violations and potential errors. Integrate these into your development workflow.

**Q: How do I handle long lines of code?**
A: Use Python's implicit line continuation by wrapping expressions in parentheses, brackets, or braces. For example, `my_long_variable = (value1 + value2 + value3 + value4)`.

## 5. Anti-Patterns to Flag

### Bad vs. Good: Indentation

```python
# BAD: Using tabs or inconsistent indentation
def my_function():
	print("Hello")
  if True:
    print("World")

# GOOD: Consistent 4-space indentation
def my_function():
    print("Hello")
    if True:
        print("World")
```

### Bad vs. Good: Line Length

```python
# BAD: Line exceeding 79 characters
def very_long_function_name(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10):
    result = arg1 + arg2 + arg3 + arg4 + arg5 + arg6 + arg7 + arg8 + arg9 + arg10 # This line is also too long

# GOOD: Using implicit line continuation
def very_long_function_name(
    arg1, arg2, arg3, arg4, arg5,
    arg6, arg7, arg8, arg9, arg10
):
    result = (
        arg1 + arg2 + arg3 + arg4 + arg5 +
        arg6 + arg7 + arg8 + arg9 + arg10
    )
```

### Bad vs. Good: Imports

```python
# BAD: Wildcard import and unorganized
from os import *
import sys, math
from my_project.utils import helper_function
import requests

# GOOD: Organized, explicit imports
import math
import sys
from os import path

import requests

from my_project.utils import helper_function
```

### Bad vs. Good: Naming Conventions

```python
# BAD: Inconsistent naming
class Myclass:
    def Get_Data(self, user_id):
        CONSTANT_VALUE = 10
        return f"Data for {user_id} and {CONSTANT_VALUE}"

# GOOD: PEP 8 compliant naming
class MyClass:
    def get_data(self, user_id):
        CONSTANT_VALUE = 10
        return f"Data for {user_id} and {CONSTANT_VALUE}"
```

## 6. Code Review Checklist

- [ ] All code uses 4-space indentation, no tabs.
- [ ] Line length does not exceed 79 characters (72 for comments/docstrings), using implicit continuation where necessary.
- [ ] Two blank lines separate top-level functions/classes.
- [ ] One blank line separates methods within a class.
- [ ] Imports are at the top, grouped (standard, third-party, local), and sorted alphabetically within groups.
- [ ] No wildcard imports (`from module import *`).
- [ ] Consistent naming conventions are used (`snake_case` for functions/variables, `CamelCase` for classes, `ALL_CAPS` for constants).
- [ ] No trailing whitespace.
- [ ] Proper spacing around operators and no unnecessary spaces inside delimiters.
- [ ] Public functions, classes, and methods have docstrings (PEP 257).
- [ ] Comments explain *why*, not *what*, and are concise.
- [ ] Type hints are used consistently where appropriate.

## 7. Related Skills

- `python-type-hints`: For guidance on using type hints effectively.
- `python-docstrings`: For detailed guidance on writing effective docstrings.
- `ci-cd-pipelines-github-actions`: For integrating linting and formatting into automated workflows.

## 8. Examples Directory Structure

```
examples/
├── good_example.py
└── bad_example.py
```

## 9. Custom Scripts Section

This section outlines automation scripts designed to streamline PEP 8 compliance and related development tasks. Each script aims to solve a common pain point, saving significant developer time.

### 1. `format-and-lint.sh` (Shell Script)
**Description**: Automates the process of formatting Python files with Black and then linting them with Ruff, ensuring both style consistency and adherence to best practices. It supports dry-run and fix modes.

### 2. `generate-docstrings.py` (Python Script)
**Description**: A Python script that scans a specified Python file or directory for functions and classes lacking docstrings and generates basic PEP 257 compliant docstring stubs. This helps developers quickly add documentation.

### 3. `check-line-length.py` (Python Script)
**Description**: A Python script to identify and report lines exceeding the PEP 8 recommended length (79 characters for code, 72 for comments/docstrings). It provides detailed output including file, line number, and current length.

### 4. `import-organizer.py` (Python Script)
**Description**: A Python script that automatically reorganizes imports in Python files according to PEP 8 guidelines (standard library, third-party, local, sorted alphabetically). It can operate in dry-run mode or apply changes directly.
