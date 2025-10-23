# .devdev/skills/python-pep8/examples/bad_example.py

# BAD example of Python code violating PEP 8 guidelines.

from os import *
import sys, math
from my_project.utils import helper_function
import requests


MAX_RETRIES=3
default_timeout=10

class myclass:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

    def Get_Full_Info(self):
        return "ID: "+str(self.user_id)+", Username: "+self.username+", Email: "+self.email

def fetch_data_from_api(endpoint, params=None, timeout=default_timeout):
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get("https://api.example.com/"+endpoint, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}", file=sys.stderr)
            if attempt < MAX_RETRIES - 1:
                import time
                time.sleep(2**attempt)
            else:
                print("Max retries reached.", file=sys.stderr)
    return None

def process_user_data(user_profiles):
    print("\nProcessing user data:")
    for profile in user_profiles:
        total_value = helper_function(profile.user_id, len(profile.username))
        message = f"User {profile.username} processed with value {total_value}"
        print(f"- {message}")

if __name__ == "__main__":
    user1 = myclass(1, "john_doe", "john.doe@example.com")
    user2 = myclass(2, "jane_smith", "jane.smith@example.com")

    print(user1.Get_Full_Info())

    users = [user1, user2]
    process_user_data(users)

    api_data = fetch_data_from_api("users", {"limit":1})
    if api_data:
        print("\nFetched API data:")
        print(api_data)
