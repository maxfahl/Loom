---
name: python-type-hints
version: 1.0.0
category: Backend Development / Python
tags: Python, type hints, static analysis, mypy, pyright, best practices
description: Using type hints in Python for improved code quality, maintainability, and static analysis.
---

# Python Type Hints Skill

## 1. Skill Purpose

This skill enables Claude to effectively use Python type hints to write more robust, readable, and maintainable Python code. It focuses on leveraging type hints for static analysis, improving IDE support, facilitating collaboration, and enhancing code documentation, ultimately leading to fewer bugs and more scalable applications.

## 2. When to Activate This Skill

Activate this skill when:
- Developing new Python modules, functions, or classes.
- Refactoring existing Python code to improve clarity and reduce bugs.
- Performing code reviews on Python files to ensure adherence to type hinting best practices.
- Integrating with data validation libraries like Pydantic or FastAPI.
- Debugging type-related issues in Python applications.
- Discussing best practices for modern Python development.

## 3. Core Knowledge

The fundamental concepts, patterns, and tools Claude needs to know regarding Python type hints:

### Core Type Hinting Concepts:

-   **Basic Types**: `str`, `int`, `float`, `bool`, `bytes`.
-   **Collections (Python 3.9+ / PEP 585)**: `list[str]`, `dict[str, int]`, `set[float]`, `tuple[str, ...]` (for homogeneous tuples), `tuple[str, int]` (for heterogeneous tuples).
    -   *Legacy (Python < 3.9)*: `typing.List`, `typing.Dict`, `typing.Set`, `typing.Tuple`.
-   **`Union`**: `Union[str, int]` for values that can be either a string or an integer. (Python 3.10+ allows `str | int`).
-   **`Optional`**: `Optional[str]` is syntactic sugar for `Union[str, None]`, indicating a value can be a string or `None`.
-   **`Any`**: Represents a type that can be anything. Use sparingly as it bypasses type checking.
-   **`Callable`**: `Callable[[Arg1Type, Arg2Type], ReturnType]` for type hinting functions.
-   **`NoReturn`**: Indicates a function will never return normally (e.g., always raises an exception or enters an infinite loop).
-   **`TypeVar`**: For defining generic types.
-   **`Protocol`**: For structural subtyping (duck typing).
-   **`TypedDict`**: For dictionaries with a fixed set of keys and specific value types.
-   **`Literal`**: `Literal["red", "green", "blue"]` for values that must be one of a specific set of literal values.
-   **`Annotated`**: (Python 3.9+) For adding context-specific metadata to types.
-   **`NewType`**: For creating distinct types based on existing ones (e.g., `UserId = NewType('UserId', int)`).
-   **`cast`**: A runtime no-op that tells the type checker to treat an expression as a specific type.
-   **`from __future__ import annotations`**: (Python 3.7+) Postpones evaluation of type annotations, enabling forward references and improving startup time. Best practice to include at the top of modules.

### Tools for Type Checking:

-   **Mypy**: The most widely used static type checker for Python.
-   **Pyright**: A fast, modern type checker developed by Microsoft, often integrated with VS Code (Pylance).
-   **TY**: A newer, Rust-based type checker from Astral, promising speed improvements.
-   **Pydantic**: A data validation and settings management library using Python type annotations.

### Integration Points:

-   **IDEs**: Real-time type checking and autocompletion.
-   **Pre-commit Hooks**: Automate type checking before commits (e.g., with `pre-commit`).
-   **CI/CD Pipelines**: Enforce type checking in continuous integration workflows.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

-   ✅ Always use type hints for function parameters, return values, and class attributes in new code.
-   ✅ For Python 3.9+, prefer native generic types (e.g., `list[str]`) over `typing` module equivalents (`typing.List[str]`).
-   ✅ Use `Optional[Type]` or `Type | None` for values that can legitimately be `None`.
-   ✅ Employ `Literal` for parameters or variables that should accept only a specific set of string or numeric values.
-   ✅ Use `TypedDict` for dictionary structures with known keys and types.
-   ✅ Integrate a static type checker (like Mypy or Pyright) into the development workflow and CI/CD pipeline.
-   ✅ Add `from __future__ import annotations` at the top of every module for forward references and performance.
-   ✅ Use `dataclasses` or Pydantic for defining data models with type hints.
-   ✅ Document complex type logic or non-obvious type choices in comments or docstrings.

### Never Recommend (❌ anti-patterns)

-   ❌ Avoid overusing `Any`. If a type is truly unknown, consider if a more specific type or `Union` can be used after runtime checks.
-   ❌ Do not ignore type checker errors without understanding their implications. Address them or use `type: ignore` comments sparingly and with clear justification.
-   ❌ Do not use type hints as a substitute for proper runtime validation, especially for external input (use Pydantic for this).
-   ❌ Avoid overly complex or deeply nested type annotations that hinder readability. Simplify or break them down.
-   ❌ Never let type hints become outdated. Update them as the code evolves.

### Common Questions & Responses (FAQ format)

**Q: My type checker is complaining about `None` values. How do I fix this?**
A: If a variable or parameter can legitimately be `None`, update its type to `Optional[Type]` or `Type | None`. For example, `name: str` becomes `name: Optional[str]` or `name: str | None`. Then, use explicit `if value is not None:` checks or provide default values to handle the `None` case before using the variable.

**Q: When should I use `Any` vs a more specific type?**
A: Use `Any` only when a type cannot be reasonably determined, or when you are working with highly dynamic data where strict type checking is impractical. In most other cases, strive for more specific types. If you're unsure, `Union` with `object` or `str` might be more appropriate, or consider using `TypeVar` for generics.

**Q: How can I gradually add type hints to a large existing codebase?**
A: Start by adding type hints to new code. For existing code, begin with public APIs (functions, class methods) and critical data structures. Enable type checking incrementally, perhaps starting with a less strict configuration and gradually increasing strictness as errors are resolved. Use `type: ignore` comments for temporary suppressions, but aim to remove them.

**Q: What's the difference between `list[str]` and `typing.List[str]`?**
A: `list[str]` is the native generic type hint introduced in Python 3.9 (PEP 585). It's generally preferred for its cleaner syntax and better performance. `typing.List[str]` is from the `typing` module and is used for older Python versions (3.8 and below). For new projects targeting Python 3.9+, always use the native generics.

## 5. Anti-Patterns to Flag

### Example 1: Overusing `Any`

**BAD:**
```python
def process_data(data: Any) -> Any:
    # This function loses all type safety
    return data["value"] * 2
```

**GOOD:**
```python
from typing import TypedDict

class Data(TypedDict):
    value: int

def process_data(data: Data) -> int:
    return data["value"] * 2

# Or, if the structure is truly unknown, use runtime checks:
def process_flexible_data(data: dict) -> int | None:
    if isinstance(data, dict) and "value" in data and isinstance(data["value"], int):
        return data["value"] * 2
    return None
```

### Example 2: Unhandled `None`

**BAD:**
```python
def get_user_email(user_data: dict) -> str:
    # user_data["email"] might be None or not exist
    return user_data.get("email").lower() # Potential AttributeError
```

**GOOD:**
```python
from typing import Optional, TypedDict

class User(TypedDict):
    name: str
    email: Optional[str]

def get_user_email(user: User) -> Optional[str]:
    # Safely access email, it can be None
    return user.get("email")

def display_user_email(user: User) -> None:
    email = get_user_email(user)
    if email is not None: # Explicit check for None
        print(f"User email: {email.lower()}")
    else:
        print("Email not available.")
```

### Example 3: Missing Return Type for Functions That Don't Return

**BAD:**
```python
def log_message(message: str):
    print(message)
    # Implicitly returns None, but not specified
```

**GOOD:**
```python
def log_message(message: str) -> None:
    print(message)
```

## 6. Code Review Checklist

-   [ ] Are all function parameters and return values type-hinted?
-   [ ] Are native generic types (e.g., `list[str]`) used for Python 3.9+?
-   [ ] Is `Optional[Type]` or `Type | None` used for values that can be `None`?
-   [ ] Is `Literal` used for parameters with a fixed set of values?
-   [ ] Is `TypedDict` used for dictionary structures with known keys and types?
-   [ ] Is `from __future__ import annotations` present at the top of modules?
-   [ ] Are `Any` types used sparingly and justified?
-   [ ] Are type checker errors addressed or explicitly ignored with justification?
-   [ ] Is runtime validation (e.g., Pydantic) used for external data where appropriate?
-   [ ] Are complex type annotations simplified or well-documented?

## 7. Related Skills

-   `tdd-red-green-refactor`: Type hints complement TDD by catching errors early and clarifying intent.
-   `clean-code-principles`: Type hints contribute to code clarity and maintainability.
-   `solid-principles`: Type hints can help enforce interface segregation and dependency inversion.

## 8. Examples Directory Structure

```
python-type-hints/
├── examples/
│   ├── basic_types.py              # Demonstrates basic type hints
│   ├── collection_types.py         # Usage of list, dict, set, tuple
│   ├── optional_union_any.py       # Examples of Optional, Union, Any
│   ├── callable_typeddict.py       # Callable and TypedDict examples
│   └── generics_protocols.py       # TypeVar and Protocol usage
├── patterns/
│   ├── data_validation.py          # Pydantic integration
│   └── runtime_type_checking.py    # Example of runtime type checking
├── scripts/
│   ├── type-hint-initializer.py    # Python script for new project setup
│   ├── type-hint-migrator.py       # Python script to assist with type hint migration
│   ├── type-hint-checker.sh        # Shell script to run type checkers (mypy/pyright)
│   └── type-hint-coverage.py       # Python script for type hint coverage analysis
└── README.md
```

## 9. Custom Scripts Section

Here are 4 automation scripts designed to save significant time when working with Python type hints:

1.  **`type-hint-initializer.py`**: Initializes a new Python project with a basic structure and a `pyproject.toml` configured for type checking (e.g., Mypy).
2.  **`type-hint-migrator.py`**: A Python script that analyzes a Python project, identifies missing type hints, and suggests or applies basic type annotations.
3.  **`type-hint-checker.sh`**: A shell script to run a specified static type checker (Mypy or Pyright) on the project, providing a clear report of type errors.
4.  **`type-hint-coverage.py`**: A Python script to calculate and report on the "type hint coverage" of a Python project, helping to track progress in type hint adoption.
