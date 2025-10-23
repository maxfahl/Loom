# patterns/test_doubles.py

# This file demonstrates the use of various test doubles (mocks, stubs, fakes, spies)
# in Python using `unittest.mock` (built-in) and conceptual examples.
# Test doubles are crucial for isolating units under test and controlling their dependencies.

import unittest
from unittest.mock import Mock, MagicMock, patch
from typing import List, Dict, Any

# --- Scenario: Testing a service that interacts with a database ---

# Real Database Client (conceptual)
class RealDatabaseClient:
    def fetch_user_data(self, user_id: int) -> Dict[str, Any] | None:
        print(f"[Real DB] Fetching data for user_id: {user_id}")
        if user_id == 1:
            return {"id": 1, "name": "Alice", "email": "alice@example.com"}
        return None

    def save_log(self, message: str) -> None:
        print(f"[Real DB] Saving log: {message}")

# Service to be tested
class UserService:
    def __init__(self, db_client: RealDatabaseClient):
        self.db_client = db_client

    def get_user_profile(self, user_id: int) -> Dict[str, Any] | None:
        user_data = self.db_client.fetch_user_data(user_id)
        if user_data:
            self.db_client.save_log(f"User {user_id} profile fetched.")
            return user_data
        self.db_client.save_log(f"User {user_id} not found.")
        return None

    def update_user_email(self, user_id: int, new_email: str) -> bool:
        # This method would typically interact with the DB to update, but for this example,
        # we'll just simulate success/failure based on user existence.
        user_data = self.db_client.fetch_user_data(user_id)
        if user_data:
            self.db_client.save_log(f"User {user_id} email updated to {new_email}.")
            return True
        self.db_client.save_log(f"Failed to update email for user {user_id}: not found.")
        return False


# --- Test Doubles in Action ---

class TestUserService(unittest.TestCase):

    def test_get_user_profile_found(self):
        # 1. Mock: Replaces an object with a configurable stand-in.
        #    - We create a mock for the database client.
        mock_db_client = Mock(spec=RealDatabaseClient) # spec ensures mock has same methods as real object

        # Configure the mock's behavior
        mock_db_client.fetch_user_data.return_value = {"id": 1, "name": "MockUser", "email": "mock@example.com"}
        mock_db_client.save_log.return_value = None # save_log doesn't return anything

        user_service = UserService(mock_db_client)
        profile = user_service.get_user_profile(1)

        self.assertIsNotNone(profile)
        self.assertEqual(profile["name"], "MockUser")

        # Verify interactions with the mock
        mock_db_client.fetch_user_data.assert_called_once_with(1)
        mock_db_client.save_log.assert_called_once_with("User 1 profile fetched.")

    def test_get_user_profile_not_found(self):
        mock_db_client = Mock(spec=RealDatabaseClient)
        mock_db_client.fetch_user_data.return_value = None
        mock_db_client.save_log.return_value = None

        user_service = UserService(mock_db_client)
        profile = user_service.get_user_profile(999)

        self.assertIsNone(profile)
        mock_db_client.fetch_user_data.assert_called_once_with(999)
        mock_db_client.save_log.assert_called_once_with("User 999 not found.")

    def test_update_user_email_success(self):
        # 2. Stub: Provides canned answers to calls made during the test.
        #    - Similar to a mock, but often implies less behavior verification.
        #    - Here, fetch_user_data is acting as a stub.
        mock_db_client = Mock(spec=RealDatabaseClient)
        mock_db_client.fetch_user_data.return_value = {"id": 1, "name": "MockUser", "email": "old@example.com"}
        mock_db_client.save_log.return_value = None

        user_service = UserService(mock_db_client)
        result = user_service.update_user_email(1, "new@example.com")

        self.assertTrue(result)
        mock_db_client.fetch_user_data.assert_called_once_with(1)
        mock_db_client.save_log.assert_called_once_with("User 1 email updated to new@example.com.")

    def test_update_user_email_failure(self):
        mock_db_client = Mock(spec=RealDatabaseClient)
        mock_db_client.fetch_user_data.return_value = None
        mock_db_client.save_log.return_value = None

        user_service = UserService(mock_db_client)
        result = user_service.update_user_email(999, "new@example.com")

        self.assertFalse(result)
        mock_db_client.fetch_user_data.assert_called_once_with(999)
        mock_db_client.save_log.assert_called_once_with("Failed to update email for user 999: not found.")

    # 3. Spy: A partial mock that records calls to the real object.
    #    - `unittest.mock.patch.object` or `unittest.mock.MagicMock` can be used to spy.
    #    - Here, we'll use `patch` as a context manager to spy on `save_log`.
    def test_get_user_profile_logs_correctly_with_spy(self):
        real_db = RealDatabaseClient()
        user_service = UserService(real_db)

        with patch.object(real_db, 'save_log') as mock_save_log:
            user_service.get_user_profile(1)
            mock_save_log.assert_called_once_with("User 1 profile fetched.")

            user_service.get_user_profile(999)
            # assert_called_once_with would fail here because it was called twice
            mock_save_log.assert_any_call("User 999 not found.")
            self.assertEqual(mock_save_log.call_count, 2)

    # 4. Fake: A simplified, working implementation of a dependency.
    #    - Often used for in-memory versions of databases or file systems.
    #    - Here, a simple in-memory database client.
    class FakeDatabaseClient:
        def __init__(self):
            self._users = {
                1: {"id": 1, "name": "FakeAlice", "email": "fake@example.com"},
                2: {"id": 2, "name": "FakeBob", "email": "fakebob@example.com"},
            }
            self._logs = []

        def fetch_user_data(self, user_id: int) -> Dict[str, Any] | None:
            return self._users.get(user_id)

        def save_log(self, message: str) -> None:
            self._logs.append(message)

        def get_logs(self) -> List[str]:
            return self._logs

    def test_user_service_with_fake_db(self):
        fake_db_client = self.FakeDatabaseClient()
        user_service = UserService(fake_db_client)

        profile = user_service.get_user_profile(1)
        self.assertIsNotNone(profile)
        self.assertEqual(profile["name"], "FakeAlice")
        self.assertIn("User 1 profile fetched.", fake_db_client.get_logs())

        profile_not_found = user_service.get_user_profile(3)
        self.assertIsNone(profile_not_found)
        self.assertIn("User 3 not found.", fake_db_client.get_logs())


if __name__ == '__main__':
    # To run these tests:
    # 1. Save the code above as `test_doubles.py`.
    # 2. Run `python -m unittest test_doubles.py` in your terminal.
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
