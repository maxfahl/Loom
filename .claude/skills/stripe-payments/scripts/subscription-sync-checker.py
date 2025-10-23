
```
subscription-sync-checker.py

Description:
This Python script compares subscription data between your application's local database
(simulated here with a JSON file) and Stripe. It identifies discrepancies such as
missing subscriptions, status mismatches, or incorrect billing cycles, and reports them.
This helps ensure data consistency and integrity between your system and Stripe.

Usage:
    python subscription-sync-checker.py --local_db_path ./local_subscriptions.json
    python subscription-sync-checker.py --local_db_path ./local_subscriptions.json --dry_run

Dependencies:
    - stripe
    - python-dotenv

Installation:
    pip install stripe python-dotenv

Configuration:
    - Ensure STRIPE_SECRET_KEY is set in your environment variables or a .env file.
      (Use a test secret key, e.g., `sk_test_...`)
    - The local database JSON file should have a structure like:
      [
          {
              "app_user_id": "user_123",
              "stripe_subscription_id": "sub_abc",
              "expected_status": "active",
              "expected_price_id": "price_xyz"
          },
          ...
      ]
```

import os
import argparse
import json
from dotenv import load_dotenv
import stripe
from typing import List, Dict, Any

# Load environment variables from .env file
load_dotenv()

# Configure Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if not stripe.api_key or not stripe.api_key.startswith("sk_test_"):
    print("Error: STRIPE_SECRET_KEY environment variable not set or not a test key (must start with 'sk_test_').")
    exit(1)

def load_local_subscriptions(local_db_path: str) -> List[Dict[str, Any]]:
    """Loads subscription data from a local JSON file."""
    print(f"Loading local subscription data from {local_db_path}...")
    if not os.path.exists(local_db_path):
        print(f"Warning: Local DB file not found at {local_db_path}. Creating a dummy file.")
        dummy_data = [
            {
                "app_user_id": "user_1",
                "stripe_subscription_id": "sub_123",
                "expected_status": "active",
                "expected_price_id": "price_abc"
            },
            {
                "app_user_id": "user_2",
                "stripe_subscription_id": "sub_456",
                "expected_status": "canceled",
                "expected_price_id": "price_def"
            }
        ]
        with open(local_db_path, 'w') as f:
            json.dump(dummy_data, f, indent=2)
        print("Created dummy local_subscriptions.json for demonstration.")

    with open(local_db_path, 'r') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} local subscriptions.")
    return data

def get_stripe_subscription(subscription_id: str) -> stripe.Subscription | None:
    """Fetches a subscription from Stripe."""
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        return subscription
    except stripe.error.StripeError as e:
        print(f"Stripe Error retrieving subscription {subscription_id}: {e}")
        return None

def compare_subscriptions(local_sub: Dict[str, Any], stripe_sub: stripe.Subscription) -> List[str]:
    """Compares a local subscription record with the Stripe record and returns discrepancies."""
    discrepancies = []

    # Status check
    if local_sub.get("expected_status") and local_sub["expected_status"] != stripe_sub.status:
        discrepancies.append(f"Status mismatch: Local expects '{local_sub["expected_status"]}', Stripe is '{stripe_sub.status}'.")
    
    # Price ID check (assuming one item per subscription for simplicity)
    if local_sub.get("expected_price_id"):
        stripe_price_id = stripe_sub.items.data[0].price.id if stripe_sub.items.data else None
        if local_sub["expected_price_id"] != stripe_price_id:
            discrepancies.append(f"Price ID mismatch: Local expects '{local_sub["expected_price_id"]}', Stripe has '{stripe_price_id}'.")

    # Add more checks as needed (e.g., quantity, current_period_end, customer_id)

    return discrepancies

def main():
    parser = argparse.ArgumentParser(
        description="Compare local subscription data with Stripe to find discrepancies.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--local_db_path",
        type=str,
        default="./local_subscriptions.json",
        help="Path to the local JSON file containing subscription data. Default: ./local_subscriptions.json"
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="If set, performs comparison but does not suggest or apply any fixes."
    )

    args = parser.parse_args()

    print("\n--- Starting Subscription Sync Checker ---")
    print(f"Local DB Path: {args.local_db_path}")
    print(f"Dry Run: {args.dry_run}")
    print("----------------------------------------\n")

    try:
        local_subscriptions = load_local_subscriptions(args.local_db_path)
        if not local_subscriptions:
            print("No local subscriptions found to check. Exiting.")
            return

        all_discrepancies = {}

        for local_sub in local_subscriptions:
            app_user_id = local_sub.get("app_user_id", "N/A")
            stripe_sub_id = local_sub.get("stripe_subscription_id")

            if not stripe_sub_id:
                print(f"Warning: Local record for user {app_user_id} is missing stripe_subscription_id. Skipping.")
                continue

            print(f"Checking subscription {stripe_sub_id} for user {app_user_id}...")
            stripe_sub = get_stripe_subscription(stripe_sub_id)

            if stripe_sub is None:
                all_discrepancies[stripe_sub_id] = [f"Subscription {stripe_sub_id} not found in Stripe."]
            else:
                discrepancies = compare_subscriptions(local_sub, stripe_sub)
                if discrepancies:
                    all_discrepancies[stripe_sub_id] = discrepancies

        if all_discrepancies:
            print("\n--- Discrepancies Found ---")
            for sub_id, issues in all_discrepancies.items():
                print(f"Subscription ID: {sub_id}")
                for issue in issues:
                    print(f"  - {issue}")
                if not args.dry_run:
                    print(f"  Suggested fix: Manually review and update local DB or Stripe for {sub_id}.")
                    # In a real system, you might have automated fix logic here.
            print("---------------------------")
        else:
            print("\nNo discrepancies found. Local and Stripe subscription data are in sync.")

        print("\n--- Subscription Sync Checker Completed ---")

    except FileNotFoundError:
        print(f"Error: Local DB file not found at {args.local_db_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {args.local_db_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
