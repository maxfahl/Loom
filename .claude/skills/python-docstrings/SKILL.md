---
name: python-docstrings
version: 1.0.0
category: Documentation / Python
tags: python, docstrings, documentation, pep257, sphinx, numpy, google, type hints
description: Guiding Claude to write effective Python docstrings for clear and maintainable code.
---

# Python Docstrings: Crafting Clear and Comprehensive Code Documentation

## 2. Skill Purpose

This skill enables Claude to effectively write, understand, and leverage Python docstrings for documenting Python code. It focuses on adhering to PEP 257, utilizing popular styles like Google and NumPy, and integrating with type hints to improve code readability, maintainability, and facilitate automatic documentation generation.

## 3. When to Activate This Skill

Activate this skill when:
*   Writing new Python code (modules, functions, classes, methods) that requires clear documentation.
*   Refactoring existing Python code to add or improve docstrings.
*   Ensuring compliance with PEP 257 and chosen docstring style guides (e.g., Google, NumPy).
*   Preparing a Python project for documentation generation using tools like Sphinx.
*   When needing to quickly generate a standard docstring structure for a given Python entity.

## 4. Core Knowledge

### Fundamental Concepts
*   **PEP 257:** The official Python Enhancement Proposal outlining docstring conventions.
*   **Placement:** Docstrings are placed immediately after the `def` or `class` line.
*   **Purpose:** Explain what the code does, how to use it, its parameters, return values, and any exceptions it might raise.
*   **Readability:** Docstrings are for humans first, then for tools.
*   **Consistency:** Adhere to a single style throughout a project.

### Popular Docstring Styles
1.  **Google Style:**
    *   **Summary:** One-line summary.
    *   **Extended Description:** Detailed explanation.
    *   **Args:**
        ```
        Args:
            param_name (param_type): Description of the parameter.
        ```
    *   **Returns:**
        ```
        Returns:
            return_type: Description of the return value.
        ```
    *   **Raises:**
        ```
        Raises:
            ExceptionType: Description of when this exception is raised.
        ```
    *   **Example:**
        ```python
        def add(a, b):
            """Adds two numbers.

            Args:
                a (int): The first number.
                b (int): The second number.

            Returns:
                int: The sum of a and b.

            Examples:
                >>> add(1, 2)
                3
            """
            return a + b
        ```

2.  **NumPy Style:**
    *   **Summary:** One-line summary.
    *   **Extended Description:** Detailed explanation.
    *   **Parameters:**
        ```
        Parameters
        ----------
        param_name : param_type
            Description of the parameter.
        ```
    *   **Returns:**
        ```
        Returns
        -------
        return_type
            Description of the return value.
        ```
    *   **Raises:**
        ```
        Raises
        ------
        ExceptionType
            Description of when this exception is raised.
        ```
    *   **Example:**
        ```python
        def subtract(a, b):
            """Subtracts two numbers.

            Parameters
            ----------
            a : int
                The first number.
            b : int
                The second number.

            Returns
            -------
            int
                The difference of a and b.
            """
            return a - b
        ```

### Key Components of a Docstring
*   **Summary Line:** Concise, imperative, ends with a period.
*   **Extended Summary:** More detail, if needed, separated by a blank line.
*   **Parameters:** Name, type (with type hints if available), description.
*   **Returns:** Type, description.
*   **Yields:** For generator functions.
*   **Raises:** Exceptions and conditions.
*   **Examples:** Usage snippets.
*   **See Also:** References to related functions/classes.
*   **Notes:** Additional important information.

## 5. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
*   ✅ **Adhere to PEP 257:** Ensure docstrings are correctly placed and formatted.
*   ✅ **Choose a Consistent Style:** Recommend sticking to either Google or NumPy style throughout a project.
*   ✅ **Start with a Concise Summary:** The first line should be a brief, imperative summary of the entity's purpose.
*   ✅ **Document All Public APIs:** Every module, public function, class, and method should have a docstring.
*   ✅ **Use Type Hints:** Integrate PEP 484 type hints in function signatures; this can make docstrings more concise regarding types.
*   ✅ **Clearly Document Parameters:** For each parameter, specify its name, type, and a clear description of its role.
*   ✅ **Explain Return Values:** Describe what the function returns, its type, and any special conditions.
*   ✅ **Document Exceptions:** List any exceptions that can be raised and the circumstances under which they occur.
*   ✅ **Provide Examples:** Include simple usage examples, especially for complex functions or classes.
*   ✅ **Keep Docstrings Up-to-Date:** Ensure docstrings reflect the current behavior and signature of the code.
*   ✅ **Use Tools:** Recommend using linters (e.g., `flake8-docstrings`) and documentation generators (e.g., Sphinx with `napoleon` extension for Google/NumPy styles).

### Never Recommend (❌ Anti-Patterns)
*   ❌ **Missing Docstrings:** Leaving public APIs undocumented.
*   ❌ **Vague Descriptions:** Docstrings like `"A function"` or `"Does stuff"` are unhelpful.
*   ❌ **Inconsistent Styles:** Mixing Google, NumPy, and reST styles within the same project.
*   ❌ **Outdated Docstrings:** Docstrings that do not match the current function signature or behavior.
*   ❌ **Redundant Information:** Repeating information already clear from the function name or type hints without adding value.
*   ❌ **Overly Complex Docstrings for Simple Code:** Don't over-document trivial, self-explanatory code.
*   ❌ **Incorrect Placement:** Docstrings not immediately following the definition line.

### Common Questions & Responses

*   **Q: Which docstring style should I use?**
    *   **A:** For general Python projects, Google style is very popular and readable. For scientific computing or data analysis projects, NumPy style is preferred. Consistency within a project is key.
*   **Q: How do I document a class?**
    *   **A:** The class docstring should describe its purpose, main attributes, and any important methods.
    ```python
    class MyClass:
        """A brief description of MyClass.

        This class handles the processing of various data types.

        Attributes:
            data (list): The list of data items.
            config (dict): Configuration settings for the class.
        """
        def __init__(self, data, config):
            self.data = data
            self.config = config
    ```

*   **Q: How do I document a generator function?**
    *   **A:** Use the `Yields` section instead of `Returns`.
    ```python
    def generate_numbers(n):
        """Generates numbers from 0 up to n-1.

        Args:
            n (int): The upper limit (exclusive).

        Yields:
            int: The next number in the sequence.
        """
        for i in range(n):
            yield i
    ```

## 6. Anti-Patterns to Flag

### Anti-Pattern: Vague Summary and Missing Details
**BAD:**
```python
def calculate_average(numbers):
    """Calculates average."""
    return sum(numbers) / len(numbers)
```
**GOOD (Google Style):**
```python
def calculate_average(numbers: list[float]) -> float:
    """Calculates the average of a list of numbers.

    This function takes a list of floating-point numbers and returns their arithmetic mean.

    Args:
        numbers (list[float]): A list of numbers.

    Returns:
        float: The calculated average.

    Raises:
        ValueError: If the input list `numbers` is empty.
    """
    if not numbers:
        raise ValueError("Input list cannot be empty.")
    return sum(numbers) / len(numbers)
```

### Anti-Pattern: Inconsistent Formatting (Mixing Styles)
**BAD:**
```python
def process_data(data):
    """Processes input data.

    :param data: The data to process.
    :type data: list
    :returns: Processed data.
    :rtype: list
    """
    # ... some processing ...
    return data
```
(Mixes reST with a simple summary)

**GOOD (NumPy Style):**
```python
def process_data(data: list) -> list:
    """Processes input data.

    Parameters
    ----------
    data : list
        The list of data items to be processed.

    Returns
    -------
    list
        The processed list of data items.
    """
    # ... some processing ...
    return data
```

## 7. Code Review Checklist

When reviewing Python code with docstrings:
*   [ ] Does every public module, function, class, and method have a docstring?
*   [ ] Does the docstring adhere to PEP 257 (placement, quotes)?
*   [ ] Is a consistent docstring style (Google, NumPy, reST) used throughout the project?
*   [ ] Does the docstring start with a concise, imperative summary line?
*   [ ] Are all parameters correctly documented with name, type (if not in type hints), and description?
*   [ ] Is the return value (or yielded value for generators) clearly described with its type?
*   [ ] Are all exceptions that can be raised documented with their conditions?
*   [ ] Are usage examples provided for complex or non-obvious entities?
*   [ ] Is the docstring up-to-date with the current code logic and signature?
*   [ ] Is the language clear, concise, and free of jargon?
*   [ ] Are type hints (PEP 484) used in function signatures where appropriate?
*   [ ] Are there any redundant or overly verbose docstrings for simple code?

## 8. Related Skills

*   `python-type-hints`: For a deeper understanding of Python's type system.
*   `clean-code-principles`: General principles for writing readable and maintainable code.
*   `api-design`: For designing clear and well-documented APIs.
*   `sphinx-documentation`: For generating comprehensive project documentation.

## 9. Examples Directory Structure

```
examples/
├── google_style/
│   └── my_module.py
├── numpy_style/
│   └── data_utils.py
├── class_docstrings/
│   └── models.py
└── generator_docstrings/
    └── iterators.py
```

## 10. Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for developers working with Python docstrings.

### Script 1: `generate_docstring_boilerplate.py` (Python)
**Purpose:** Generates docstring boilerplate (Google or NumPy style) for a given Python function or class.
**Pain Point:** Manually writing out docstring blocks, especially for functions with many parameters or complex return types, and ensuring style consistency.

### Script 2: `check_docstring_coverage.py` (Python)
**Purpose:** Scans Python files and reports on the percentage of functions/classes that have docstrings.
**Pain Point:** Ensuring consistent documentation coverage across a codebase and identifying undocumented public APIs.

### Script 3: `convert_docstring_style.py` (Python)
**Purpose:** Converts docstrings from one style (e.g., reST) to another (e.g., Google or NumPy).
**Pain Point:** Migrating existing docstrings to a new project standard or preferred style.
