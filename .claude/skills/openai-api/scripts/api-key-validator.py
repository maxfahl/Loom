#!/usr/bin/env python3

# api-key-validator.py
#
# Purpose: A Python script to validate an OpenAI API key by making a minimal, low-cost
#          API call (e.g., a simple embedding request). It reports on the key's validity,
#          potential issues, and can optionally fetch basic account usage information
#          to check for rate limits or spending.
#
# Usage:
#   python3 api-key-validator.py [--key <your_api_key>] [--check-usage] [--verbose]
#
# Examples:
#   python3 api-key-validator.py
#   python3 api-key-validator.py --key sk-YOUR_API_KEY_HERE
#   python3 api-key-validator.py --check-usage --verbose
#
# Options:
#   --key           Optional: Provide the API key directly. If not provided,
#                   it will attempt to read from the OPENAI_API_KEY environment variable.
#   --check-usage   Optional: Attempt to fetch and display basic account usage information.
#                   Requires additional permissions for the API key.
#   --verbose       Optional: Enable verbose output.
#   --help          Display this help message.

import argparse
import os
import sys
import openai
from openai import OpenAI

def colored_print(text, color):
    """Prints text in a specified color."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

async def validate_api_key(api_key, verbose_mode):
    colored_print("\n--- Validating OpenAI API Key ---", "blue")
    if not api_key:
        colored_print("Error: No API key provided. Please use --key or set OPENAI_API_KEY environment variable.", "red")
        return False

    client = OpenAI(api_key=api_key)

    try:
        if verbose_mode:
            colored_print("Attempting a minimal API call (embedding creation)...", "white")
        # Make a minimal, low-cost API call to validate the key
        await client.embeddings.create(
            model="text-embedding-ada-002",
            input="test",
        )
        colored_print("API Key is VALID! ✅", "green")
        return True
    except openai.AuthenticationError:
        colored_print("API Key is INVALID! ❌ (Authentication Error)", "red")
        colored_print("  - Check if the key is correct and has not expired.", "yellow")
        colored_print("  - Ensure there are no leading/trailing spaces.", "yellow")
        return False
    except openai.RateLimitError:
        colored_print("API Key is VALID, but hit a Rate Limit! ⚠️", "yellow")
        colored_print("  - This key is likely valid but currently rate-limited.", "yellow")
        colored_print("  - Try again later or check your usage limits on the OpenAI dashboard.", "yellow")
        return True # Key is valid, just rate-limited
    except openai.APIStatusError as e:
        colored_print(f"API Key is VALID, but encountered an API Status Error: {e.status_code} ❌", "red")
        colored_print(f"  - Message: {e.response}", "yellow")
        colored_print("  - This could indicate a temporary issue with the OpenAI service or a problem with your request.", "yellow")
        return True # Key is valid, but API call failed for other reasons
    except Exception as e:
        colored_print(f"An unexpected error occurred during validation: {e}", "red")
        return False

async def check_usage(api_key, verbose_mode):
    colored_print("\n--- Checking Account Usage (Requires specific permissions) ---", "blue")
    if not api_key:
        colored_print("Error: No API key provided for usage check.", "red")
        return

    client = OpenAI(api_key=api_key)

    try:
        # This endpoint might require specific permissions or be part of a different API
        # The current OpenAI Python client does not directly expose a "usage" endpoint
        # You would typically check usage via the OpenAI dashboard or a billing API if available.
        # For demonstration, we'll simulate or use a placeholder.

        # Placeholder for actual usage check if an API becomes available
        colored_print("Note: Direct API for detailed usage is not publicly exposed via the standard SDK.", "yellow")
        colored_print("Please check your usage dashboard at https://platform.openai.com/usage", "yellow")

        # Example of how you *might* check if a billing API existed (hypothetical)
        # if verbose_mode:
        #     colored_print("Attempting to fetch billing usage...", "white")
        # usage_response = await client.billing.get_usage() # Hypothetical API call
        # colored_print(f"Current usage: {usage_response.total_usage} USD", "green")
        # colored_print(f"Hard limit: {usage_response.hard_limit} USD", "green")

    except openai.AuthenticationError:
        colored_print("Authentication Error for usage check. Your API key might not have permissions for billing data.", "red")
    except openai.APIError as e:
        colored_print(f"OpenAI API Error during usage check: {e.status_code} - {e.response}", "red")
    except Exception as e:
        colored_print(f"An unexpected error occurred during usage check: {e}", "red")

async def main():
    parser = argparse.ArgumentParser(
        description="Validate an OpenAI API key and optionally check usage.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--key",
        help="Provide the API key directly. If not provided, it will attempt to read from the OPENAI_API_KEY environment variable."
    )
    parser.add_argument(
        "--check-usage",
        action="store_true",
        help="Attempt to fetch and display basic account usage information. Requires additional permissions for the API key."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    args = parser.parse_args()

    api_key_to_use = args.key or os.environ.get("OPENAI_API_KEY")

    is_valid = await validate_api_key(api_key_to_use, args.verbose)

    if is_valid and args.check_usage:
        await check_usage(api_key_to_use, args.verbose)

    colored_print("\n--- Validation Complete ---", "blue")
    if not is_valid:
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
