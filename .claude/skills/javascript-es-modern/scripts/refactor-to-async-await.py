#!/usr/bin/env python3

# refactor-to-async-await.py
#
# Purpose:
#   Helps identify and suggest refactoring opportunities for Promise-based
#   `.then().catch()` chains into cleaner `async/await` syntax within
#   JavaScript/TypeScript files. It provides a dry-run mode to preview changes.
#
# Usage:
#   python3 refactor-to-async-await.py <file_path> [OPTIONS]
#
# Options:
#   -h, --help        Display this help message.
#   -d, --dry-run     Show suggested changes without modifying the file. (default)
#   -f, --fix         Apply suggested changes directly to the file.
#
# Examples:
#   python3 refactor-to-async-await.py src/service.ts
#   python3 refactor-to-async-await.py src/old_api.js --fix
#
# Requirements:
#   - Python 3.6+
#
# Note: This script uses regex for pattern matching and provides suggestions.
#       For complex cases, manual review and a proper AST parser might be needed.

import argparse
import re
import sys

# --- Colors for output ---
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color

def log_info(message):
    print(f"{BLUE}[INFO]{NC} {message}")

def log_success(message):
    print(f"{GREEN}[SUCCESS]{NC} {message}")

def log_warn(message):
    print(f"{YELLOW}[WARN]{NC} {message}")

def log_error(message):
    print(f"{RED}[ERROR]{NC} {message}", file=sys.stderr)

def find_and_suggest_refactoring(content):
    suggestions = []
    lines = content.splitlines()

    # Regex to find .then() and .catch() patterns
    # This is a simplified regex and might not catch all complex scenarios
    # It looks for a chain starting with a promise, followed by .then() and optionally .catch()
    # It tries to capture the function body within .then() and .catch()
    pattern = re.compile(
        r"(\\w+\\s*=\\s*)?(\\w+\\(?)\\s*|\\w+)\\s*\\.then\\s*\\(\\s*(?:function\\s*\\((\\w+)\\|)\\|(\\(w+)\\|(\\w+))\\s*=>\\s*\{([\\s\\S]*?)\\}\\s*)"
        r"(\\s*\\.catch\\s*\\(\\s*(?:function\\s*\\((\\w+)\\|)\\|(\\(w+)\\|(\\w+))\\s*=>\\s*\{([\\s\\S]*?)\\}\\s*))?",
        re.MULTILINE
    )

    for i, line in enumerate(lines):
        match = pattern.search(line)
        if match:
            # Extract parts of the match
            assignment_prefix = match.group(1) if match.group(1) else ""
            promise_call = match.group(2)
            then_param = match.group(3) or match.group(4) or match.group(5)
            then_body = match.group(6)
            catch_block = match.group(7)
            catch_param = match.group(8) or match.group(9) or match.group(10) if catch_block else None
            catch_body = match.group(11) if catch_block else None

            # Basic attempt to convert to async/await structure
            # This is highly simplified and will need manual adjustment for real code
            refactored_code = []
            refactored_code.append(f"async function refactoredFunction() {{")
            refactored_code.append(f"  try {{")
            if assignment_prefix:
                refactored_code.append(f"    {assignment_prefix}await {promise_call};")
            else:
                refactored_code.append(f"    const {then_param} = await {promise_call};")
            refactored_code.append(f"    {then_body.strip()}")
            if catch_block:
                refactored_code.append(f"  }} catch ({catch_param}) {{")
                refactored_code.append(f"    {catch_body.strip()}")
            refactored_code.append(f"  }}")
            refactored_code.append(f"}}")

            suggestions.append({
                "line_number": i + 1,
                "original": line.strip(),
                "suggested": "\n".join(refactored_code),
                "full_match": match.group(0)
            })
    return suggestions

def main():
    parser = argparse.ArgumentParser(
        description="Helps refactor Promise chains to async/await syntax.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("file_path", help="Path to the JavaScript/TypeScript file.")
    parser.add_argument(
        "-d", "--dry-run", action="store_true", default=True,
        help="Show suggested changes without modifying the file (default)."
    )
    parser.add_argument(
        "-f", "--fix", action="store_true",
        help="Apply suggested changes directly to the file."
    )
    args = parser.parse_args()

    if args.fix:
        args.dry_run = False # If --fix is used, disable dry-run

    file_path = args.file_path

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        log_error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        log_error(f"Error reading file {file_path}: {e}")
        sys.exit(1)

    log_info(f"Analyzing file: {file_path} for Promise chains...")
    suggestions = find_and_suggest_refactoring(content)

    if not suggestions:
        log_success("No Promise chains found that could be easily refactored to async/await.")
        sys.exit(0)

    log_info(f"Found {len(suggestions)} potential refactoring opportunities.")

    if args.dry_run:
        log_info("--- Dry Run: Suggested Changes (file will NOT be modified) ---")
        for s in suggestions:
            log_warn(f"Line {s['line_number']}: Original:")
            print(f"  {s['original']}")
            log_success("Suggested async/await structure:")
            for line in s['suggested'].splitlines():
                print(f"  {line}")
            print("-" * 50)
        log_info("End of Dry Run. Use --fix to apply changes.")
    elif args.fix:
        log_warn("Applying changes to file. Please ensure you have a backup or use version control.")
        modified_content = content
        # This simple replacement strategy is highly prone to errors and should be used with caution.
        # A proper AST-based refactoring tool would be much safer.
        # For this exercise, we'll do a very basic line-by-line replacement if the full match is found.
        # In a real scenario, this would be more sophisticated.
        for s in reversed(suggestions): # Process in reverse to avoid line number shifts
            original_lines = s['full_match'].splitlines()
            suggested_lines = s['suggested'].splitlines()
            
            # Find the start of the match in the current content
            start_index = modified_content.find(s['full_match'])
            if start_index != -1:
                modified_content = modified_content[:start_index] + s['suggested'] + modified_content[start_index + len(s['full_match']):]
            else:
                log_warn(f"Could not find original pattern at line {s['line_number']} for replacement. Skipping.")

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            log_success(f"Successfully applied {len(suggestions)} refactoring suggestions to {file_path}.")
        except Exception as e:
            log_error(f"Error writing to file {file_path}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
