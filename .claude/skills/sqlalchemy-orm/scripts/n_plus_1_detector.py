import argparse
import os
import re

def detect_n_plus_1(file_path: str) -> list[str]:
    """
    Detects potential N+1 query patterns in a given Python file.
    This is a heuristic-based detector and may produce false positives/negatives.
    It looks for lazy-loaded relationship access within loops.

    Args:
        file_path: The path to the Python file to analyze.

    Returns:
        A list of strings, each describing a potential N+1 issue found.
    """
    issues = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Regex to find relationship definitions (lazy="select" or no lazy specified)
    # This is a simplification; a full AST parser would be more accurate.
    relationship_pattern = re.compile(r'(\w+)\s*=\s*relationship\(.*?lazy\s*=\s*("select"|'''select''')\s*.*\)')
    # Also consider default lazy loading if not specified
    relationship_pattern_default = re.compile(r'(\w+)\s*=\s*relationship\((?!.*?lazy\s*=).*\)')

    # Regex to find loops
    loop_pattern = re.compile(r'^\s*(for|while)\s+.*:')

    lazy_relationships = {}
    for i, line in enumerate(lines):
        match = relationship_pattern.search(line)
        if match:
            rel_name = match.group(1)
            lazy_relationships[rel_name] = True # Mark as potentially lazy
        else:
            match_default = relationship_pattern_default.search(line)
            if match_default:
                rel_name = match_default.group(1)
                lazy_relationships[rel_name] = True # Default is lazy="select"

    in_loop = False
    loop_start_line = -1
    loop_indentation = -1

    for i, line in enumerate(lines):
        current_line_num = i + 1

        loop_match = loop_pattern.match(line)
        if loop_match:
            in_loop = True
            loop_start_line = current_line_num
            loop_indentation = len(line) - len(line.lstrip())
            continue

        if in_loop:
            current_indentation = len(line) - len(line.lstrip())
            if not line.strip() or current_indentation <= loop_indentation and not loop_match: # Loop ended or blank line
                in_loop = False
                loop_start_line = -1
                loop_indentation = -1
                continue

            # Check for access to lazy-loaded relationships within the loop
            for rel_name in lazy_relationships:
                # Simple heuristic: look for `obj.relationship_name` access
                if re.search(r'\b\w+\.\b' + re.escape(rel_name) + r'\b', line):
                    issues.append(
                        f"Potential N+1 query detected in {file_path} at line {current_line_num}: "
                        f"Accessing lazy-loaded relationship '{rel_name}' inside a loop starting at line {loop_start_line}. "
                        f"Consider using eager loading (e.g., .options(selectinload({rel_name}))) for the query that fetches the parent objects."
                    )

    return issues

def main():
    parser = argparse.ArgumentParser(
        description="Detect potential N+1 query patterns in SQLAlchemy ORM code."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Path to a Python file or a directory to scan."
    )
    parser.add_argument(
        "--exclude",
        type=str,
        nargs='*',
        default=[],
        help="List of file/directory patterns to exclude (e.g., 'tests/*', 'venv/')."
    )

    args = parser.parse_args()

    target_path = args.path
    exclude_patterns = args.exclude

    if os.path.isfile(target_path):
        if target_path.endswith(".py"):
            found_issues = detect_n_plus_1(target_path)
            for issue in found_issues:
                print(f"\033[0;33m[WARNING]\033[0m {issue}")
            if not found_issues:
                print(f"\033[0;32m[INFO]\033[0m No potential N+1 issues found in {target_path}.")
        else:
            print(f"\033[0;31m[ERROR]\033[0m Provided path is not a Python file: {target_path}")
    elif os.path.isdir(target_path):
        print(f"\033[0;34m[INFO]\033[0m Scanning directory: {target_path} for N+1 issues...")
        total_issues = []
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    # Check for exclusion patterns
                    if any(re.fullmatch(pattern, full_path) for pattern in exclude_patterns):
                        continue
                    found_issues = detect_n_plus_1(full_path)
                    total_issues.extend(found_issues)

        if total_issues:
            for issue in total_issues:
                print(f"\033[0;33m[WARNING]\033[0m {issue}")
            print(f"\033[0;31m[SUMMARY]\033[0m Found {len(total_issues)} potential N+1 issues.")
        else:
            print(f"\033[0;32m[INFO]\033[0m No potential N+1 issues found in {target_path}.")
    else:
        print(f"\033[0;31m[ERROR]\033[0m Path does not exist or is not a file/directory: {target_path}")

if __name__ == "__main__":
    main()
