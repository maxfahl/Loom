import pytest

@pytest.fixture
def user_factory():
    """A factory fixture to create user objects dynamically."""
    users_created = []
    def _create_user(name, email):
        user = {"name": name, "email": email}
        users_created.append(user)
        print(f"\nCreated user: {name}")
        return user
    yield _create_user
    print(f"\nCleaning up {len(users_created)} users: {users_created}")

