import argparse
import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# clear-test-db.py
#
# Purpose:
#   Connects to a specified MongoDB test database and clears all collections.
#   This script is crucial for ensuring a clean and isolated state before running
#   integration tests, preventing data contamination between test runs.
#
# Usage:
#   python clear-test-db.py [--uri <mongodb_uri>] [--db <database_name>] [--dry-run]
#
# Arguments:
#   --uri <mongodb_uri>:   Optional. The MongoDB connection URI.
#                          Defaults to 'mongodb://localhost:27017/' if not provided.
#                          Can also be set via the MONGODB_URI environment variable.
#   --db <database_name>:  Optional. The name of the database to clear.
#                          Defaults to 'testdb' if not provided.
#                          Can also be set via the MONGODB_DB environment variable.
#   --dry-run:             Optional. If set, the script will only show what would be done
#                          without actually clearing any data.
#
# Examples:
#   python clear-test-db.py
#   python clear-test-db.py --db my_test_api_db
#   python clear-test-db.py --uri "mongodb://user:pass@host:port/"
#   MONGODB_URI="mongodb://localhost:27017/" MONGODB_DB="my_app_test" python clear-test-db.py
#   python clear-test-db.py --dry-run
#
# Features:
#   - Connects to MongoDB using a configurable URI and database name.
#   - Lists and drops all collections in the specified database.
#   - Includes a dry-run mode for safety.
#   - Provides clear console output with color for better readability.
#   - Handles connection errors gracefully.
#   - Supports environment variables for configuration.

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_color(color, message):
    print(f"{color}{message}{Color.END}")

def main():
    parser = argparse.ArgumentParser(
        description="Clears all collections in a specified MongoDB test database."
    )
    parser.add_argument(
        "--uri",
        default=os.environ.get("MONGODB_URI", "mongodb://localhost:27017/"),
        help="MongoDB connection URI (default: mongodb://localhost:27017/). Can be set via MONGODB_URI env var."
    )
    parser.add_argument(
        "--db",
        default=os.environ.get("MONGODB_DB", "testdb"),
        help="Name of the database to clear (default: testdb). Can be set via MONGODB_DB env var."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, only show what would be done without actually clearing data."
    )

    args = parser.parse_args()

    mongo_uri = args.uri
    db_name = args.db
    dry_run = args.dry_run

    print_color(Color.BLUE, f"Attempting to clear MongoDB database: '{db_name}'")
    print_color(Color.BLUE, f"MongoDB URI: '{mongo_uri}'")
    if dry_run:
        print_color(Color.YELLOW, "DRY RUN: No data will be deleted.")

    try:
        client = MongoClient(mongo_uri)
        # The ping command is cheap and does not require auth.
        client.admin.command('ping')
        db = client[db_name]
        print_color(Color.GREEN, "Successfully connected to MongoDB.")

        collection_names = db.list_collection_names()

        if not collection_names:
            print_color(Color.YELLOW, f"Database '{db_name}' is already empty. No collections to clear.")
            return

        print_color(Color.BLUE, f"Found {len(collection_names)} collections in '{db_name}':")
        for col_name in collection_names:
            print_color(Color.BLUE, f"  - {col_name}")

        if not dry_run:
            confirm = input(f"\nAre you sure you want to drop ALL {len(collection_names)} collections in '{db_name}'? (yes/no): ")
            if confirm.lower() != 'yes':
                print_color(Color.YELLOW, "Operation cancelled by user.")
                return

            for col_name in collection_names:
                print_color(Color.YELLOW, f"Dropping collection: {col_name}...")
                db.drop_collection(col_name)
            print_color(Color.GREEN, f"Successfully cleared all collections in database '{db_name}'.")
        else:
            print_color(Color.YELLOW, "Dry run complete. The above collections would have been dropped.")

    except ConnectionFailure as e:
        print_color(Color.RED, f"Error: Could not connect to MongoDB at '{mongo_uri}'. Please check if the server is running and the URI is correct.")
        print_color(Color.RED, f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        print_color(Color.RED, f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.close()
            print_color(Color.BLUE, "MongoDB connection closed.")

if __name__ == "__main__":
    main()
