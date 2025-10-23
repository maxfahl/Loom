import argparse
import os
import re
import sys
from typing import List, Dict, Any

# ANSI escape codes for colored output
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"

def parse_env_file(filepath: str) -> Dict[str, str]:
    env_vars = {}
    if not os.path.exists(filepath):
        return env_vars
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            match = re.match(r'^([^=]+)=(.*)$', line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                env_vars[key] = value
    return env_vars

def write_env_file(filepath: str, env_vars: Dict[str, str]):
    with open(filepath, 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

def generate_env_example(env_filepath: str, example_filepath: str, dry_run: bool):
    if not os.path.exists(env_filepath):
        print(f"{COLOR_RED}Error: .env file not found at '{env_filepath}'.{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)

    env_vars = parse_env_file(env_filepath)
    example_content = []
    for key in env_vars:
        example_content.append(f"{key}=")
    
    if dry_run:
        print(f"{COLOR_BOLD}{COLOR_BLUE}--- Generated .env.example (Dry Run) ---
{COLOR_RESET}")
        print("\n".join(example_content))
        print(f"{COLOR_BOLD}{COLOR_BLUE}--------------------------------------------------------------------
{COLOR_RESET}")
    else:
        with open(example_filepath, 'w') as f:
            f.write("\n".join(example_content))
        print(f"{COLOR_GREEN}Successfully generated .env.example at '{example_filepath}'.{COLOR_RESET}")

def validate_env_file(filepath: str) -> List[Dict[str, Any]]:
    findings = []
    if not os.path.exists(filepath):
        findings.append({"message": f".env file not found at '{filepath}'.", "severity": "error"})
        return findings

    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '=' not in line:
                findings.append({
                    "line": line_num,
                    "message": "Line does not contain an equals sign. Expected KEY=VALUE format.",
                    "severity": "error",
                    "code_snippet": line
                })
                continue

            key, value = line.split('=', 1)
            if ' ' in value and not (value.startswith("'"') and value.endswith("'"')) and not (value.startswith('"') and value.endswith('"')):
                findings.append({
                    "line": line_num,
                    "message": "Value contains spaces but is not quoted. This might lead to parsing issues.",
                    "severity": "warning",
                    "code_snippet": line
                })
            if re.search(r'[^a-zA-Z0-9_]', key):
                findings.append({
                    "line": line_num,
                    "message": "Environment variable key contains invalid characters. Use alphanumeric characters and underscores.",
                    "severity": "warning",
                    "code_snippet": line
                })
    return findings

def set_env_variable(filepath: str, key: str, value: str, dry_run: bool):
    env_vars = parse_env_file(filepath)
    old_value = env_vars.get(key)
    env_vars[key] = value

    if dry_run:
        print(f"{COLOR_BOLD}{COLOR_BLUE}--- Set Environment Variable (Dry Run) ---
{COLOR_RESET}")
        print(f"Would set/update '{key}' in '{filepath}'.")
        if old_value is not None:
            print(f"Old value: '{old_value}'")
        print(f"New value: '{value}'")
        print(f"{COLOR_BOLD}{COLOR_BLUE}--------------------------------------------------------------------
{COLOR_RESET}")
    else:
        write_env_file(filepath, env_vars)
        print(f"{COLOR_GREEN}Successfully set '{key}={value}' in '{filepath}'.{COLOR_RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Manages .env files for Docker Compose applications.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "action",
        choices=["generate-example", "validate", "set"],
        help="Action to perform: 'generate-example', 'validate', or 'set'."
    )
    parser.add_argument(
        "env_file_path",
        help="Path to the .env file (e.g., './.env')."
    )
    parser.add_argument(
        "--key",
        help="Required for 'set' action: The environment variable key to set."
    )
    parser.add_argument(
        "--value",
        help="Required for 'set' action: The value for the environment variable."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="For 'generate-example' and 'set' actions: Print changes without modifying files."
    )

    args = parser.parse_args()

    if args.action == "generate-example":
        example_filepath = args.env_file_path + ".example"
        generate_env_example(args.env_file_path, example_filepath, args.dry_run)
    elif args.action == "validate":
        findings = validate_env_file(args.env_file_path)
        if findings:
            print(f"{COLOR_BOLD}{COLOR_YELLOW}--- .env Validation Report for '{args.env_file_path}' ---
{COLOR_RESET}")
            for finding in findings:
                color = COLOR_RED if finding["severity"] == "error" else COLOR_YELLOW
                line_info = f"Line {finding['line']}: " if "line" in finding else ""
                code_snippet = f"  Code: `{finding['code_snippet']}`\n" if "code_snippet" in finding else "\n"
                print(f"{color}{COLOR_BOLD}[{finding["severity"].upper()}] {line_info}{finding["message"]}{COLOR_RESET}")
                print(code_snippet)
            print(f"{COLOR_BOLD}{COLOR_YELLOW}--- End of Report ---
{COLOR_RESET}")
            sys.exit(1)
        else:
            print(f"{COLOR_GREEN}No issues found in '{args.env_file_path}'. Looks good!{COLOR_RESET}")
    elif args.action == "set":
        if not args.key or not args.value:
            parser.error("Arguments --key and --value are required for 'set' action.")
        set_env_variable(args.env_file_path, args.key, args.value, args.dry_run)

if __name__ == "__main__":
    main()
