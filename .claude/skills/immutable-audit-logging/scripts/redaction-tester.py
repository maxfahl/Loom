#!/usr/bin/env python3
import argparse
import json
import re
import sys

def redact_sensitive_data(log_entry, redaction_rules, dry_run=False, verbose=False):
    """
    Redacts sensitive data from a log entry based on a list of regex patterns.

    Args:
        log_entry (str): The JSON string of the log entry.
        redaction_rules (list): A list of regex patterns for sensitive data.
        dry_run (bool): If True, show what would be redacted without making changes.
        verbose (bool): If True, print detailed information about redactions.

    Returns:
        str: The redacted log entry as a JSON string.
    """
    try:
        data = json.loads(log_entry)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON log entry: {log_entry}", file=sys.stderr)
        return log_entry

    original_data_str = json.dumps(data)
    redacted_data_str = original_data_str
    redactions_made = []

    for rule in redaction_rules:
        try:
            # Use re.sub to replace all occurrences of the pattern
            # The replacement string is '[REDACTED]'
            # We use a lambda function for replacer to capture what was redacted
            def replacer(match):
                redactions_made.append(f"  - Redacted '{match.group(0)}' using rule '{rule}'")
                return '[REDACTED]'

            # Apply redaction to the string representation of the JSON
            # This is a simple approach; for complex nested structures, a recursive walk might be better
            # but for general log lines, string replacement is often sufficient and simpler.
            redacted_data_str = re.sub(rule, replacer, redacted_data_str, flags=re.IGNORECASE)

        except re.error as e:
            print(f"Warning: Invalid regex rule '{rule}': {e}", file=sys.stderr)

    if verbose and redactions_made:
        print("Redactions proposed/made:")
        for r in redactions_made:
            print(r)

    if dry_run:
        print("\n--- Dry Run Output ---")
        print("Original:", original_data_str)
        print("Redacted:", redacted_data_str)
        return original_data_str # Return original for dry run
    else:
        return redacted_data_str

def main():
    parser = argparse.ArgumentParser(
        description="Test sensitive data redaction rules against sample log entries.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-l', '--log-entry',
        required=True,
        help='A sample log entry as a JSON string (e.g., '''{"user": "test", "password": "secret"}''')'
    )
    parser.add_argument(
        '-r', '--rules',
        nargs='+',
        default=[
            '"password"\s*:\s*"[^"]+"',
            '"apiKey"\s*:\s*"[^"]+"',
            '\b(?:ssn|social_security_number)[^\w]*:?\s*\d{3}-\d{2}-\d{4}\b',
            '\b(?:creditCardNumber|ccn)[^\w]*:?\s*\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'email=[^&\s]+'
        ],
        help='List of regex patterns for sensitive data. Default patterns are provided.
              Example: -r 
              Note: Use single quotes for patterns to avoid shell interpretation.'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be redacted without making actual changes.'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed information about redactions.'
    )
    args = parser.parse_args()

    print("\n--- Redaction Tester ---")
    print(f"Input Log Entry: {args.log_entry}")
    print(f"Redaction Rules: {args.rules}")

    redacted_log = redact_sensitive_data(
        args.log_entry,
        args.rules,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    if not args.dry_run:
        print("\n--- Redacted Log Entry ---")
        print(redacted_log)

    print("\n--- End of Redaction Tester ---
")

if __name__ == "__main__":
    main()
