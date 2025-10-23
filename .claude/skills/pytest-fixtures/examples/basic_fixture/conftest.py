import pytest

@pytest.fixture
def basic_resource():
    """A basic fixture providing a simple string resource."""
    print("\nSetting up basic_resource")
    resource = "Hello from basic_resource!"
    yield resource
    print("\nTeardown for basic_resource")

