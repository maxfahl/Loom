import argparse
import os
import re
import sys

def analyze_network_requests(filepath):
    """
    Analyzes a JavaScript/TypeScript file for network request patterns.
    Flags:
    - Multiple fetch/axios calls in close proximity (potential for batching).
    - Network calls without explicit caching headers (heuristic).
    """
    findings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern 1: Multiple fetch/axios calls in close proximity
    # This is a very basic heuristic. A more advanced tool would need AST parsing.
    # We'll look for multiple 'fetch(' or 'axios.' within a small window of lines.
    network_call_pattern = re.compile(r'(fetch\s*\(|axios\.(get|post|put|delete)\s*\()')
    
    lines = content.splitlines()
    network_call_lines = []
    for i, line in enumerate(lines):
        if network_call_pattern.search(line):
            network_call_lines.append(i + 1) # Store 1-based line number

    # Check for calls in close proximity (e.g., within 5 lines)
    for i in range(len(network_call_lines) - 1):
        if network_call_lines[i+1] - network_call_lines[i] <= 5:
            findings.append(f"  Lines {network_call_lines[i]} and {network_call_lines[i+1]}: Multiple network calls in close proximity. Consider batching these requests to reduce radio wake-ups.")

    # Pattern 2: Network calls without explicit caching headers (very basic heuristic)
    # This is extremely difficult to do accurately with regex.
    # A very weak heuristic: look for 'fetch' or 'axios' calls that don't seem to have 'Cache-Control' in headers.
    # This will have many false positives and negatives.
    # For a real-world scenario, this would require AST analysis and understanding of the network library.
    # For now, I'll just flag any network call as a reminder to check caching.
    for match in network_call_pattern.finditer(content):
        line_num = content.count('\n', 0, match.start()) + 1
        # This is a very general warning, as detecting actual caching headers with regex is unreliable.
        # The intent is to prompt the developer to review caching.
        findings.append(f"  Line {line_num}: Network request detected. Ensure appropriate caching headers (e.g., Cache-Control) are set or data is cached client-side to minimize redundant fetches.")

    return findings

def main():
    parser = argparse.ArgumentParser(
        description="Analyzes JavaScript/TypeScript files for network request patterns that might impact battery life.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('path', nargs='?', default='.',
                        help="Path to a file or directory to scan. Defaults to current directory.")
    parser.add_argument('--dry-run', action='store_true',
                        help="Perform a dry run without making any changes (current script doesn't modify files).")
    parser.add_argument('--exclude', nargs='*', default=['node_modules', 'dist', 'build'],
                        help="Directories to exclude from scanning.")
    parser.add_argument('--verbose', action='store_true',
                        help="Show verbose output.")

    args = parser.parse_args()

    target_path = args.path
    excluded_dirs = set(args.exclude)
    
    if args.dry_run:
        print("Performing a dry run. No files will be modified.")

    if os.path.isfile(target_path):
        if target_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            print(f"\033[1mScanning file: {target_path}\033[0m")
            findings = analyze_network_requests(target_path)
            if findings:
                for f in findings:
                    print(f"\033[93m  WARNING: {f}\033[0m")
            else:
                print("  No obvious network optimization issues found.")
        else:
            print(f"Skipping {target_path}: Not a JavaScript/TypeScript file.")
    elif os.path.isdir(target_path):
        print(f"\033[1mScanning directory: {target_path}\033[0m")
        found_any = False
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]

            for file in files:
                if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    filepath = os.path.join(root, file)
                    if args.verbose:
                        print(f"  Checking {filepath}...")
                    findings = analyze_network_requests(filepath)
                    if findings:
                        found_any = True
                        print(f"\033[1m  File: {filepath}\033[0m")
                        for f in findings:
                            print(f"\033[93m    WARNING: {f}\033[0m")
        if not found_any:
            print("  No obvious network optimization issues found in scanned files.")
    else:
        print(f"\033[91mError: Path '{target_path}' does not exist.\033[0m")
        sys.exit(1)

if __name__ == '__main__':
    main()
