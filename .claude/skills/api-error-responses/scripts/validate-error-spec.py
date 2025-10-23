
#!/usr/bin/env python3
import os
import argparse
import textwrap
import json

try:
    import yaml
except ImportError:
    print("PyYAML is not installed. Please install it with: pip install pyyaml")
    exit(1)

# --- Color constants ---
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- RFC 9457 Schema Definition ---
# A simplified schema to check against. We focus on key required fields.
PROBLEM_DETAILS_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "format": "uri"},
        "title": {"type": "string"},
        "status": {"type": "number"},
        "detail": {"type": "string"},
        "instance": {"type": "string", "format": "uri-reference"},
    },
    "required": ["type", "title", "status"],
}

def validate_schema(response_schema, spec_path):
    """Validates a response schema against the Problem Details standard."""
    errors = []
    
    # Resolve $ref if present
    if "$ref" in response_schema:
        # This is a simplified resolver. A real implementation would need to handle complex paths.
        ref_path = response_schema["$ref"].split('/')[1:] # Assumes #/components/schemas/MyError
        with open(spec_path) as f:
            spec = yaml.safe_load(f)
        
        resolved_schema = spec
        for p in ref_path:
            if p in resolved_schema:
                resolved_schema = resolved_schema[p]
            else:
                errors.append(f"Could not resolve reference: {response_schema['$ref']}")
                return errors
        response_schema = resolved_schema

    if response_schema.get("type") != "object":
        errors.append("Schema `type` is not 'object'.")

    # Check for required fields
    for prop in PROBLEM_DETAILS_SCHEMA["required"]:
        if prop not in response_schema.get("properties", {}):
            errors.append(f"Missing required property: '{prop}'.")
        else:
            # Check type of property
            expected_type = PROBLEM_DETAILS_SCHEMA["properties"][prop]["type"]
            actual_type = response_schema["properties"][prop].get("type")
            if actual_type != expected_type:
                errors.append(f"Property '{prop}' has wrong type. Expected '{expected_type}', got '{actual_type}'.")

    return errors

def main():
    parser = argparse.ArgumentParser(
        description=f"{Color.BOLD}Validate API error responses in an OpenAPI specification against RFC 9457.{Color.ENDC}",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent(f"""
        {Color.BOLD}Description:{Color.ENDC}
          This script crawls an OpenAPI v3 specification file (e.g., `openapi.yaml`) and
          validates that all defined error responses (HTTP 4xx and 5xx) conform to the
          `application/problem+json` standard as defined in RFC 9457.

          It checks for:
          - The presence of the `application/problem+json` content type.
          - A schema that matches the Problem Details structure (required fields: `type`, `title`, `status`).
          - Correct types for the standard fields.

        {Color.BOLD}Usage Examples:{Color.ENDC}
          {Color.OKCYAN}# Validate an OpenAPI spec file{Color.ENDC}
          python3 {__file__} openapi.yaml

          {Color.OKCYAN}# Validate a spec and show all responses, not just errors{Color.ENDC}
          python3 {__file__} path/to/my/spec.json --verbose
        """)
    )
    parser.add_argument(
        "spec_file",
        help="Path to the OpenAPI specification file (YAML or JSON).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="If set, shows passing checks in addition to errors.",
    )

    args = parser.parse_args()

    if not os.path.exists(args.spec_file):
        print(f"{Color.FAIL}Error: Specification file not found at '{args.spec_file}'.{Color.ENDC}")
        return

    print(f"{Color.HEADER}{Color.BOLD}Validating OpenAPI Spec: {args.spec_file}{Color.ENDC}")

    error_count = 0
    warning_count = 0

    with open(args.spec_file, 'r') as f:
        spec = yaml.safe_load(f)

    if "paths" not in spec:
        print(f"{Color.FAIL}Error: No 'paths' found in the specification.{Color.ENDC}")
        return

    for path, methods in spec["paths"].items():
        for method, definition in methods.items():
            if "responses" not in definition:
                continue

            for status_code, response in definition["responses"].items():
                # We only care about 4xx and 5xx error codes
                if not (status_code.startswith('4') or status_code.startswith('5')):
                    continue
                
                location = f"{method.upper()} {path} -> {status_code}"

                if "content" not in response or "application/problem+json" not in response["content"]:
                    print(f"{Color.FAIL}[ERROR]{Color.ENDC} {location}: Missing `application/problem+json` content type.")
                    error_count += 1
                    continue
                
                content_schema = response["content"]["application/problem+json"].get("schema")
                if not content_schema:
                    print(f"{Color.FAIL}[ERROR]{Color.ENDC} {location}: `application/problem+json` is missing a schema.")
                    error_count += 1
                    continue

                validation_errors = validate_schema(content_schema, args.spec_file)

                if validation_errors:
                    print(f"{Color.FAIL}[ERROR]{Color.ENDC} {location}: Schema validation failed:")
                    for err in validation_errors:
                        print(f"  - {err}")
                    error_count += len(validation_errors)
                elif args.verbose:
                    print(f"{Color.OKGREEN}[OK]{Color.ENDC} {location}: Schema conforms to RFC 9457.")

    print("\n" + "-"*20 + " Validation Summary " + "-"*20)
    if error_count == 0:
        print(f"{Color.OKGREEN}{Color.BOLD}Success! All error responses conform to RFC 9457.{Color.ENDC}")
    else:
        print(f"{Color.FAIL}{Color.BOLD}Validation failed with {error_count} error(s).{Color.ENDC}")
        exit(1)

if __name__ == "__main__":
    main()
