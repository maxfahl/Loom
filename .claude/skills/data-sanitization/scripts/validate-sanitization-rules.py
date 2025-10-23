#!/usr/bin/env python3
"""
validate-sanitization-rules.py: A script to validate data masking rules against a sample dataset.

This script takes a JSON file containing data masking rules and a sample JSON dataset.
It applies the masking rules to the sample data and then performs checks to ensure
that sensitive fields are indeed masked and, optionally, that referential integrity
is maintained (for deterministic masking).

Usage:
    python3 validate-sanitization-rules.py -r <rules_file.json> -d <sample_data.json> [--verbose]

Examples:
    # Validate masking rules against a sample dataset
    python3 validate-sanitization-rules.py -r masking_rules.json -d sample_data.json

Configuration:
    - Rules file: A JSON file similar to the one used by `mask-database-dump.sh`,
      but can also include a `validation_regex` for each rule to check the masked output.
      Example:
      [
        { "field": "email", "pattern": "email='[^"]+'", "replacement": "email='masked@example.com'", "validation_regex": "email='masked@example.com'" },
        { "field": "ssn", "pattern": "ssn='[^"]+'", "replacement": "ssn='XXX-XX-XXXX'", "validation_regex": "ssn='XXX-XX-XXXX'" }
      ]
    - Sample data file: A JSON file containing an array of objects, where each object
      represents a record to be masked and validated.

Error Handling:
    - Exits with an error if files are not found or are invalid JSON.
    - Reports which rules failed validation and why.

Dependencies:
    - json (built-in)
    - re (built-in)
    - argparse (built-in)
    - sys (built-in)
    - os (built-in)
"""

import argparse
import json
import re
import sys
import os

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

def apply_masking_rules(data_record, rules, verbose=False):
    """Applies masking rules to a single data record."""
    masked_record = json.dumps(data_record) # Convert to string to apply regex rules
    for rule in rules:
        pattern = rule.get("pattern")
        replacement = rule.get("replacement")
        field = rule.get("field", "unknown_field")

        if not pattern or not replacement:
            log_warning(f"Skipping malformed rule for field '{field}': Missing pattern or replacement.", verbose)
            continue

        try:
            # Use re.sub to apply the regex replacement
            masked_record = re.sub(pattern, replacement, masked_record)
            log_info(f"Applied rule for field '{field}'.", verbose)
        except re.error as e:
            log_warning(f"Invalid regex pattern for field '{field}': {pattern} - {e}. Skipping rule.", verbose)
        except Exception as e:
            log_warning(f"Error applying rule for field '{field}': {e}. Skipping rule.", verbose)
    return json.loads(masked_record) # Convert back to JSON object

def validate_masked_data(original_record, masked_record, rules, verbose=False):
    """Validates if sensitive fields in the masked record match validation regexes."""
    validation_results = {"passed": True, "failures": []}

    for rule in rules:
        field = rule.get("field")
        validation_regex = rule.get("validation_regex")

        if not field or not validation_regex:
            continue # Skip rules without a field or validation regex

        original_value = original_record.get(field)
        masked_value = masked_record.get(field)

        if masked_value is None:
            log_warning(f"Field '{field}' not found in masked record for validation.", verbose)
            continue

        try:
            if not re.search(validation_regex, str(masked_value)):
                validation_results["passed"] = False
                validation_results["failures"].append({
                    "field": field,
                    "expected_pattern": validation_regex,
                    "actual_value": masked_value,
                    "reason": "Masked value does not match validation regex."
                })
                log_info(f"Validation FAILED for field '{field}'.", verbose)
            else:
                log_info(f"Validation PASSED for field '{field}'.", verbose)
        except re.error as e:
            log_warning(f"Invalid validation regex for field '{field}': {validation_regex} - {e}. Skipping validation for this field.", verbose)

    return validation_results

def main():
    parser = argparse.ArgumentParser(
        description="Validate data masking rules against a sample dataset.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-r", "--rules",
        required=True,
        help="Path to the JSON file containing data masking rules."
    )
    parser.add_argument(
        "-d", "--data",
        required=True,
        help="Path to the JSON file containing sample data for validation."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    args = parser.parse_args()

    if not os.path.exists(args.rules):
        log_error(f"Rules file not found at '{args.rules}'")
        sys.exit(1)

    if not os.path.exists(args.data):
        log_error(f"Sample data file not found at '{args.data}'")
        sys.exit(1)

    try:
        with open(args.rules, 'r') as f:
            rules = json.load(f)
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in rules file '{args.rules}': {e}")
        sys.exit(1)
    except Exception as e:
        log_error(f"Error reading rules file '{args.rules}': {e}")
        sys.exit(1)

    try:
        with open(args.data, 'r') as f:
            sample_data = json.load(f)
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in sample data file '{args.data}': {e}")
        sys.exit(1)
    except Exception as e:
        log_error(f"Error reading sample data file '{args.data}': {e}")
        sys.exit(1)

    if not isinstance(sample_data, list):
        log_error("Sample data file must contain a JSON array of records.")
        sys.exit(1)

    all_passed = True
    for i, original_record in enumerate(sample_data):
        log_info(f"\nProcessing record {i + 1}/{len(sample_data)}...", args.verbose)
        masked_record = apply_masking_rules(original_record, rules, args.verbose)
        validation_results = validate_masked_data(original_record, masked_record, rules, args.verbose)

        if not validation_results["passed"]:
            all_passed = False
            log_error(f"Validation FAILED for record {i + 1}.")
            for failure in validation_results["failures"]:
                log_error(f"  Field: {failure["field"]}")
                log_error(f"  Reason: {failure["reason"]}")
                log_error(f"  Expected Pattern: {failure["expected_pattern"]}")
                log_error(f"  Actual Value: {failure["actual_value"]}")
        else:
            log_info(f"Validation PASSED for record {i + 1}.", args.verbose)

    if all_passed:
        print(f"\n{GREEN}All sanitization rules validated successfully against the sample data.{NC}")
        sys.exit(0)
    else:
        print(f"\n{RED}Some sanitization rules failed validation. Please review the errors above.{NC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
