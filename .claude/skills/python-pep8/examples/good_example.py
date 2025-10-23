# .devdev/skills/python-pep8/examples/good_example.py

"""A good example of Python code adhering to PEP 8 guidelines.

This module demonstrates proper indentation, naming conventions, line length,
and import organization as recommended by PEP 8.
"""

import os
import sys
from typing import List, Optional

import requests

from my_project.utils import calculate_total, format_message


MAX_RETRIES = 3
DEFAULT_TIMEOUT = 10


class UserProfile:
    """Represents a user's profile information.

    Attributes:
        user_id (int): The unique identifier for the user.
        username (str): The user's chosen username.
        email (str): The user's email address.
    """

    def __init__(self, user_id: int, username: str, email: str) -> None:
        """Initializes a new UserProfile instance.

        Args:
            user_id (int): The unique identifier for the user.
            username (str): The user's chosen username.
            email (str): The user's email address.
        """
        self.user_id = user_id
        self.username = username
        self.email = email

    def get_full_info(self) -> str:
        """Returns a formatted string with the user's full information.

        Returns:
            str: A string containing user ID, username, and email.
        """
        return f"ID: {self.user_id}, Username: {self.username}, Email: {self.email}"


def fetch_data_from_api(
    endpoint: str, params: Optional[dict] = None, timeout: int = DEFAULT_TIMEOUT
) -> Optional[dict]:
    """Fetches data from a specified API endpoint with retries.

    Args:
        endpoint (str): The API endpoint to call.
        params (Optional[dict]): Dictionary of query parameters.
        timeout (int): Timeout for the request in seconds.

    Returns:
        Optional[dict]: JSON response data if successful, None otherwise.
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(f"https://api.example.com/{endpoint}",
                                    params=params, timeout=timeout)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}", file=sys.stderr)
            if attempt < MAX_RETRIES - 1:
                # Simple backoff, in a real app use exponential backoff
                import time
                time.sleep(2 ** attempt)
            else:
                print("Max retries reached.", file=sys.stderr)
    return None


def process_user_data(user_profiles: List[UserProfile]) -> None:
    """Processes a list of user profiles.

    Args:
        user_profiles (List[UserProfile]): A list of UserProfile objects.
    """
    print("\nProcessing user data:")
    for profile in user_profiles:
        # Calculate some value using an external utility
        total_value = calculate_total(profile.user_id, len(profile.username))
        message = format_message(profile.username, total_value)
        print(f"- {message}")


if __name__ == "__main__":
    # Example usage
    user1 = UserProfile(1, "john_doe", "john.doe@example.com")
    user2 = UserProfile(2, "jane_smith", "jane.smith@example.com")

    print(user1.get_full_info())

    users = [user1, user2]
    process_user_data(users)

    # Fetch some data
    api_data = fetch_data_from_api("users", {"limit": 1})
    if api_data:
        print("\nFetched API data:")
        print(api_data)
