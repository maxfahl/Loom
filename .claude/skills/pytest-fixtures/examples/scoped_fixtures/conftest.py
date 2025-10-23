import pytest

@pytest.fixture(scope="function")
def function_scope_fixture():
    print("\n  Setting up function_scope_fixture")
    yield "function_resource"
    print("  Teardown for function_scope_fixture")

@pytest.fixture(scope="module")
def module_scope_fixture():
    print("\nSetting up module_scope_fixture")
    yield "module_resource"
    print("Teardown for module_scope_fixture")

@pytest.fixture(scope="session")
def session_scope_fixture():
    print("\n*** Setting up session_scope_fixture ***")
    yield "session_resource"
    print("*** Teardown for session_scope_fixture ***")

