def test_create_single_user(user_factory):
    user = user_factory("Alice", "alice@example.com")
    assert user["name"] == "Alice"
    assert user["email"] == "alice@example.com"

def test_create_multiple_users(user_factory):
    user1 = user_factory("Bob", "bob@example.com")
    user2 = user_factory("Charlie", "charlie@example.com")
    assert user1["name"] == "Bob"
    assert user2["name"] == "Charlie"
