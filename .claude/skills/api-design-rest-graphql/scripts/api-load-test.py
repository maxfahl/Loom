#!/usr/bin/env python3
"""
api-load-test.py: A script to perform basic load testing on a given API endpoint (REST or GraphQL).

This script uses the 'locust' library to simulate user traffic and measure the performance
of an API. It can be configured to target REST or GraphQL endpoints with custom requests.

Usage:
    python3 api-load-test.py -H <host_url> [--users <num_users>] [--spawn-rate <rate>] [--run-time <time>] [--rest] [--graphql] [--verbose]

Examples:
    # Run a load test against a REST API endpoint
    python3 api-load-test.py -H http://localhost:3000 --users 10 --spawn-rate 5 --run-time 60s --rest

    # Run a load test against a GraphQL API endpoint
    python3 api-load-test.py -H http://localhost:4000/graphql --users 20 --spawn-rate 10 --run-time 120s --graphql

    # Run in web UI mode (default if --run-time is not specified)
    locust -f api-load-test.py --host http://localhost:3000

Configuration:
    - The script can be run directly or by calling `locust -f api-load-test.py` for the web UI.
    - Request methods, paths/queries, and headers can be customized within the `UserBehavior` classes.

Error Handling:
    - Reports errors and failures during the load test.
    - Provides clear output on performance metrics.

Dependencies:
    - locust (install with: `pip install locust`)
    - requests (installed as a dependency of locust)
    - argparse (built-in)
    - sys (built-in)
    - os (built-in)
"""

import argparse
import sys
import os
import json
from locust import HttpUser, task, between, run_single_user

# Colors for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
NC = '\033[0m' # No Color

def log_error(message):
    print(f"{RED}ERROR: {message}{NC}", file=sys.stderr)

def log_warning(message):
    print(f"{YELLOW}WARNING: {message}{NC}", file=sys.stderr)

def log_info(message, verbose):
    if verbose:
        print(f"{GREEN}INFO: {message}{NC}")

class RestUser(HttpUser):
    wait_time = between(1, 2) # Users wait between 1 and 2 seconds between tasks
    host = "http://localhost:3000"

    @task(3) # Higher weight means this task is run more often
    def get_users(self):
        self.client.get("/v1/users", name="Get all users")

    @task(1)
    def create_user(self):
        user_data = {
            "name": fake.name(),
            "email": fake.email()
        }
        self.client.post("/v1/users", json=user_data, name="Create user")

    @task(2)
    def get_single_user(self):
        # Assuming some users exist to fetch
        if users_cache:
            user_id = random.choice(users_cache)
            self.client.get(f"/v1/users/{user_id}", name="Get single user")
        else:
            self.client.get("/v1/users/non-existent-id", name="Get single user (not found)")

class GraphQLUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:4000/graphql"

    @task(3)
    def get_users_graphql(self):
        query = """
            query {\n                users {\n                    id\n                    name\n                    email\n                }\n            }
        """
        self.client.post("/graphql", json={'query': query}, name="GraphQL: Get all users")

    @task(1)
    def create_user_graphql(self):
        mutation = """
            mutation ($name: String!, $email: String!) {\n                createUser(input: { name: $name, email: $email }) {\n                    id\n                    name\n                }\n            }
        """
        variables = {
            "name": fake.name(),
            "email": fake.email()
        }
        self.client.post("/graphql", json={'query': mutation, 'variables': variables}, name="GraphQL: Create user")

    @task(2)
    def get_single_user_graphql(self):
        if users_cache:
            user_id = random.choice(users_cache)
            query = """
                query ($id: ID!) {\n                    user(id: $id) {\n                        id\n                        name\n                        email\n                    }\n                }
            """
            variables = {"id": user_id}
            self.client.post("/graphql", json={'query': query, 'variables': variables}, name="GraphQL: Get single user")
        else:
            query = """
                query {\n                    user(id: \"non-existent-id\") {\n                        id\n                    }\n                }
            """
            self.client.post("/graphql", json={'query': query}, name="GraphQL: Get single user (not found)")

# Global Faker instance for synthetic data in tasks
from faker import Faker
fake = Faker()

# Simple cache for user IDs to simulate fetching existing users
users_cache = []

# Hook to populate users_cache (simplified, in a real scenario this would be more robust)
@task
def populate_users_cache(self):
    if not users_cache:
        if isinstance(self, RestUser):
            res = self.client.get("/v1/users")
            if res.status_code == 200:
                for user in res.json():
                    users_cache.append(user['id'])
        elif isinstance(self, GraphQLUser):
            query = """
                query {\n                    users {\n                        id\n                    }\n                }
            """
            res = self.client.post("/graphql", json={'query': query})
            if res.status_code == 200 and 'data' in res.json() and 'users' in res.json()['data']:
                for user in res.json()['data']['users']:
                    users_cache.append(user['id'])

class MixedUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:3000"

    tasks = [RestUser, GraphQLUser]

def main():
    parser = argparse.ArgumentParser(
        description="Perform basic load testing on an API endpoint using Locust.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-H", "--host",
        default="http://localhost:3000",
        help="Host URL to test (e.g., http://localhost:3000 for REST, http://localhost:4000/graphql for GraphQL)."
    )
    parser.add_argument(
        "--users",
        type=int,
        default=1,
        help="Number of concurrent users to simulate."
    )
    parser.add_argument(
        "--spawn-rate",
        type=int,
        default=1,
        help="Rate at which users are spawned (users per second)."
    )
    parser.add_argument(
        "--run-time",
        help="Stop after the specified amount of time, e.g., 300s, 20m, 3h. If not specified, runs in web UI mode."
    )
    parser.add_argument(
        "--rest",
        action="store_true",
        help="Run load test for REST API (default if no --graphql)."
    )
    parser.add_argument(
        "--graphql",
        action="store_true",
        help="Run load test for GraphQL API."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    args = parser.parse_args()

    # Remove --rest and --graphql from sys.argv if present, to prevent Locust from trying to parse them
    if "--rest" in sys.argv:
        sys.argv.remove("--rest")
    if "--graphql" in sys.argv:
        sys.argv.remove("--graphql")
    if "--verbose" in sys.argv:
        sys.argv.remove("--verbose")

    # Set the host for the HttpUser classes dynamically
    HttpUser.host = args.host

    # Determine which User class to run
    if args.graphql:
        user_class = GraphQLUser
        log_info(f"Running GraphQL load test against {args.host}", args.verbose)
    elif args.rest:
        user_class = RestUser
        log_info(f"Running REST load test against {args.host}", args.verbose)
    else:
        # Default to REST if neither is specified
        user_class = RestUser
        log_info(f"Running REST load test against {args.host} (default)", args.verbose)

    # If run_time is not specified, run in web UI mode
    if not args.run_time:
        log_info("Starting Locust in web UI mode. Open your browser to http://localhost:8089", args.verbose)
        # Locust will automatically pick up the HttpUser classes in the file
        # To run in web UI mode, you typically just run `locust -f your_script.py`
        # This `main` function is more for programmatic execution or CLI-only runs.
        # For simplicity, we'll just exit and instruct the user to run locust directly.
        print(f"\n{YELLOW}To start the Locust web UI, please run: locust -f {os.path.basename(__file__)} --host {args.host}{NC}")
        sys.exit(0)

    # Programmatic run for CLI-only execution
    try:
        from locust.env import Environment
        from locust.stats import stats_printer, stats_history
        from locust.log import setup_logging
        import logging
        import time
        import random

        setup_logging("INFO")

        env = Environment(user_classes=[user_class], host=args.host)
        env.create_local_runner()
        env.create_web_ui(host="127.0.0.1", port=8089)

        # Start the test
        env.runner.start(args.users, spawn_rate=args.spawn_rate)

        # Print stats to console
        stats_printer(env.stats)
        # stats_history(env.stats)

        # Stop the test after run_time
        run_time_seconds = parse_run_time(args.run_time)
        log_info(f"Running test for {args.run_time} ({run_time_seconds} seconds)...", args.verbose)
        time.sleep(run_time_seconds)
        env.runner.quit()
        log_info("Load test finished.", args.verbose)

    except ImportError:
        log_error("Locust library not found. Please install it: pip install locust")
        sys.exit(1)
    except Exception as e:
        log_error(f"An error occurred during load testing: {e}")
        sys.exit(1)

def parse_run_time(run_time_str: str) -> int:
    """Parses a run time string (e.g., 60s, 20m, 3h) into seconds."""
    if run_time_str.endswith('s'):
        return int(run_time_str[:-1])
    elif run_time_str.endswith('m'):
        return int(run_time_str[:-1]) * 60
    elif run_time_str.endswith('h'):
        return int(run_time_str[:-1]) * 3600
    else:
        return int(run_time_str) # Assume seconds if no unit

if __name__ == "__main__":
    main()
