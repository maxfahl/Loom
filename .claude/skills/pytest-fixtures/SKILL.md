---
name: pytest-fixtures
version: 1.0.0
category: Testing / Python
tags: pytest, fixtures, python, testing, unit testing, integration testing
description: Mastering pytest fixtures for efficient and maintainable Python test setups.
---

# Pytest Fixtures: Efficient Test Setup and Teardown

## 2. Skill Purpose

This skill enables Claude to effectively design, implement, and utilize `pytest` fixtures for Python testing. It covers best practices for managing test dependencies, setting up test environments, and ensuring proper teardown, leading to more robust, readable, and maintainable test suites.

## 3. When to Activate This Skill

Activate this skill when:
*   Writing new Python tests using `pytest`.
*   Refactoring existing `pytest` test suites to improve readability, reduce duplication, or enhance maintainability.
*   Debugging test failures related to setup, teardown, or test environment inconsistencies.
*   Designing shared test resources (e.g., database connections, API clients, temporary files).
*   When encountering repetitive setup/teardown logic across multiple tests.

## 4. Core Knowledge

### Fundamental Concepts
*   **What are Fixtures?** Functions that provide a fixed baseline for tests, managing dependencies and handling setup/teardown.
*   **Dependency Injection:** Fixtures are injected into test functions by name.
*   **Scopes:** Control how often a fixture is run and torn down (`function`, `class`, `module`, `package`, `session`).
*   **`conftest.py`:** Special files for sharing fixtures across multiple test files or directories.
*   **`yield` for Teardown:** Ensures resources are properly released after tests.
*   **Parametrization:** Running tests or fixtures with different sets of parameters.
*   **Factory Fixtures:** Functions returned by fixtures for dynamic object creation.

### Key APIs and Decorators
*   `@pytest.fixture`: Decorator to define a fixture.
*   `@pytest.mark.parametrize`: Decorator for parametrizing tests and fixtures.
*   `pytest.raises`: Context manager for asserting expected exceptions.
*   Built-in fixtures: `tmp_path`, `monkeypatch`, `capsys`, `mocker` (from `pytest-mock`), `request`.

## 5. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
*   ✅ **Keep Fixtures Simple and Focused:** Each fixture should have a single, clear responsibility. Avoid complex logic within fixtures; delegate to helper functions if necessary.
*   ✅ **Choose the Correct Fixture Scope:**
    *   `function` (default): For isolated, test-specific resources (e.g., temporary files, database transactions).
    *   `class`: For resources shared across methods in a test class.
    *   `module`: For resources shared across all tests in a module (e.g., database connections, API clients).
    *   `session`: For resources shared across the entire test run (e.g., starting a test server once).
*   ✅ **Use `conftest.py` for Reusability:** Place shared fixtures in `conftest.py` files at appropriate levels in the test directory hierarchy.
*   ✅ **Employ `yield` for Teardown:** Always use `yield` in fixtures that acquire resources to ensure they are released, even if tests fail.
*   ✅ **Parametrize Tests and Fixtures:** Use `@pytest.mark.parametrize` to test various scenarios with minimal code duplication.
*   ✅ **Use Factory Fixtures for Dynamic Data:** When tests need to create multiple instances of an object with varying configurations, use a fixture that returns a factory function.
*   ✅ **Leverage Built-in Fixtures:** Utilize `tmp_path` for temporary files/directories, `monkeypatch` for mocking, and `capsys` for capturing stdout/stderr.
*   ✅ **Organize Fixtures Logically:** Group related fixtures. For large projects, consider a `fixtures/` directory for common fixtures and `conftest.py` for module-specific ones.
*   ✅ **Document Fixtures:** Add clear docstrings to fixtures explaining their purpose, parameters, and what they provide.

### Never Recommend (❌ Anti-Patterns)
*   ❌ **Global Variables for Test State:** Avoid using global variables to share state between tests; use fixtures instead.
*   ❌ **Complex Logic in Fixtures:** Fixtures should primarily set up and tear down. If a fixture becomes too complex, it might be doing too much.
*   ❌ **Incorrect Fixture Scopes:** Using a `function`-scoped fixture for an expensive, `session`-scoped resource will lead to slow tests.
*   ❌ **Forgetting Teardown:** Not using `yield` or `addfinalizer` for resources that need explicit cleanup can lead to resource leaks or test interference.
*   ❌ **Overloading `conftest.py`:** A single, massive `conftest.py` can become a maintenance burden. Distribute fixtures logically.
*   ❌ **Hardcoding Test Data:** Generate or provide test data via fixtures to make tests more flexible and maintainable.

### Common Questions & Responses

*   **Q: How do I share a database connection across all my tests?**
    *   **A:** Define a fixture in your top-level `conftest.py` with `scope="session"` that establishes and tears down the database connection.
    ```python
    # conftest.py
    import pytest
    import sqlite3

    @pytest.fixture(scope="session")
    def db_connection():
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        yield conn
        conn.close()
    ```

*   **Q: I need to create multiple users for different tests. How can I do this efficiently?**
    *   **A:** Use a factory fixture that returns a function to create users dynamically.
    ```python
    # conftest.py
    import pytest

    @pytest.fixture
    def user_factory(db_connection):
        def _user_factory(name):
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            db_connection.commit()
            return {"id": cursor.lastrowid, "name": name}
        return _user_factory

    # test_users.py
    def test_create_user(user_factory):
        user = user_factory("Alice")
        assert user["name"] == "Alice"
    ```

*   **Q: How do I mock an external API call in my tests?**
    *   **A:** Use the `monkeypatch` built-in fixture or `pytest-mock`'s `mocker` fixture.
    ```python
    # my_module.py
    import requests

    def fetch_data(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    # test_my_module.py
    import pytest
    from my_module import fetch_data

    def test_fetch_data(monkeypatch):
        def mock_get(*args, **kwargs):
            class MockResponse:
                def __init__(self):
                    self.status_code = 200
                def json(self):
                    return {"data": "mocked"}
                def raise_for_status(self):
                    pass
            return MockResponse()

        monkeypatch.setattr("requests.get", mock_get)
        data = fetch_data("http://example.com/api/data")
        assert data == {"data": "mocked"}
    ```

## 6. Anti-Patterns to Flag

### Anti-Pattern: Global State Modification
**BAD:** Modifying a global variable directly in a test or setup function without proper cleanup.
```python
# BAD: global_state.py
GLOBAL_COUNTER = 0

def increment():
    global GLOBAL_COUNTER
    GLOBAL_COUNTER += 1

# BAD: test_global_state.py
def test_increment_one():
    increment()
    assert GLOBAL_COUNTER == 1

def test_increment_two(): # Fails if test_increment_one runs first
    increment()
    assert GLOBAL_COUNTER == 1
```

**GOOD:** Using a fixture to manage state and ensure isolation.
```python
# GOOD: conftest.py
import pytest

@pytest.fixture
def counter():
    value = 0
    yield value
    # No explicit teardown needed for simple integer, but demonstrates pattern

# GOOD: test_isolated_state.py
def test_increment_one(counter):
    counter += 1
    assert counter == 1

def test_increment_two(counter):
    counter += 1
    assert counter == 1
```

### Anti-Pattern: Repetitive Setup Code
**BAD:** Duplicating setup logic in multiple test functions.
```python
# BAD: test_data_setup.py
def setup_database():
    # ... complex database setup ...
    return db_connection

def teardown_database(db_connection):
    # ... complex database teardown ...
    db_connection.close()

def test_query_users():
    db = setup_database()
    # ... test logic ...
    teardown_database(db)

def test_add_user():
    db = setup_database()
    # ... test logic ...
    teardown_database(db)
```

**GOOD:** Encapsulating setup/teardown in a fixture.
```python
# GOOD: conftest.py
import pytest
# Assume db_connection fixture from above

# GOOD: test_data_setup_fixture.py
def test_query_users(db_connection):
    # ... test logic using db_connection ...
    pass

def test_add_user(db_connection):
    # ... test logic using db_connection ...
    pass
```

## 7. Code Review Checklist

When reviewing code that uses `pytest-fixtures`:
*   [ ] Are fixtures named clearly and descriptively?
*   [ ] Is the correct scope (`function`, `class`, `module`, `session`) used for each fixture?
*   [ ] Do fixtures that acquire resources use `yield` for proper teardown?
*   [ ] Are `conftest.py` files used appropriately for shared fixtures, avoiding a single monolithic file?
*   [ ] Is `@pytest.mark.parametrize` used to reduce test duplication for varying inputs?
*   [ ] Are factory fixtures used for dynamic test data generation?
*   [ ] Is global state avoided in favor of fixture-managed state?
*   [ ] Are built-in fixtures (`tmp_path`, `monkeypatch`, `capsys`) utilized where appropriate?
*   [ ] Are fixtures well-documented with docstrings?
*   [ ] Are complex setup steps delegated to helper functions outside the fixture if the fixture itself becomes too long?

## 8. Related Skills

*   `python-testing`: General Python testing principles and frameworks.
*   `python-mocking`: Advanced mocking techniques for isolating dependencies.
*   `python-docstrings`: Best practices for documenting Python code, including fixtures.

## 9. Examples Directory Structure

```
examples/
├── basic_fixture/
│   ├── conftest.py
│   └── test_example.py
├── factory_fixture/
│   ├── conftest.py
│   └── test_factory.py
├── scoped_fixtures/
│   ├── conftest.py
│   ├── test_function_scope.py
│   ├── test_module_scope.py
│   └── test_session_scope.py
└── mocking_with_monkeypatch/
    ├── my_module.py
    └── test_mocking.py
```

## 10. Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for developers working with `pytest-fixtures`.

### Script 1: `generate_fixture_boilerplate.py` (Python)
**Purpose:** Generates a basic `pytest` fixture boilerplate in `conftest.py` with a chosen scope and optional teardown.
**Pain Point:** Manually writing the basic structure of a new fixture, especially remembering the `yield` pattern and scope.

### Script 2: `find_unused_fixtures.py` (Python)
**Purpose:** Scans a test directory to identify and list `pytest` fixtures that are defined but never used.
**Pain Point:** Accumulation of dead code (unused fixtures) in large test suites, leading to confusion and maintenance overhead.

### Script 3: `fixture_dependency_graph.sh` (Shell)
**Purpose:** Generates a simple text-based dependency graph for fixtures within a specified test file or directory.
**Pain Point:** Understanding complex fixture dependencies, especially when fixtures depend on other fixtures.
