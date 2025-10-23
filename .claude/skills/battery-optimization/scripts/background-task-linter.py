import argparse
import os
import re
import sys

def find_inefficient_background_tasks(filepath):
    """
    Scans a JavaScript/TypeScript file for patterns indicating inefficient background tasks.
    Flags:
    - setInterval with duration <= 5000ms (5 seconds)
    - Large synchronous loops (e.g., for loops iterating > 1000 times)
    - Heavy computations (e.g., complex regex, JSON parsing of very large strings) on the main thread.
    """
    findings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern 1: setInterval with short duration
    # This regex looks for setInterval(..., <duration>) where duration is a number <= 5000
    # It's a heuristic and might have false positives/negatives.
    interval_pattern = re.compile(r'setInterval\s*\(\s*[^,]+,\s*(\d+)\s*\)')
    for match in interval_pattern.finditer(content):
        interval_ms = int(match.group(1))
        if interval_ms <= 5000:
            line_num = content.count('\n', 0, match.start()) + 1
            findings.append(f"  Line {line_num}: Potentially inefficient setInterval with duration {interval_ms}ms. Consider WorkManager/BackgroundTasks for background operations.")

    # Pattern 2: Large synchronous loops (heuristic)
    # This is very hard to do accurately with static analysis.
    # A simple heuristic: look for 'for' or 'while' loops with a high literal upper bound.
    # This is a very basic check and will miss dynamic loops.
    loop_pattern = re.compile(r'(for|while)\s*\(.*(?:<\s*(\d+)|<=\s*(\d+)|>\s*(\d+)|>=\s*(\d+)).*\)\s*{\n')
    for match in loop_pattern.finditer(content):
        upper_bound = 0
        for i in range(2, 6): # Check groups for numbers
            if match.group(i):
                upper_bound = max(upper_bound, int(match.group(i)))
        if upper_bound > 1000: # Arbitrary threshold for a "large" loop
            line_num = content.count('\n', 0, match.start()) + 1
            findings.append(f"  Line {line_num}: Potentially large synchronous loop ({match.group(1)} iterating up to ~{upper_bound} times). Consider offloading heavy computations to a Web Worker or native thread.")

    # Pattern 3: Heavy JSON parsing (heuristic)
    # This looks for JSON.parse calls that might be processing very large strings.
    # Again, a heuristic.
    json_parse_pattern = re.compile(r'JSON\.parse\s*\(([^)]+)\)')
    for match in json_parse_pattern.finditer(content):
        # This is a very weak heuristic. A real linter would need type information.
        # For now, just flag any JSON.parse as a potential area for review if it's on the main thread.
        line_num = content.count('\n', 0, match.start()) + 1
        findings.append(f"  Line {line_num}: `JSON.parse` detected. Ensure large JSON payloads are parsed off the main thread (e.g., using Web Workers) to prevent UI freezes and battery drain.")


    return findings

def main():
    parser = argparse.ArgumentParser(
        description="Lints JavaScript/TypeScript files for inefficient background task patterns.",
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
            findings = find_inefficient_background_tasks(target_path)
            if findings:
                for f in findings:
                    print(f"\033[93m  WARNING: {f}\033[0m")
            else:
                print("  No obvious inefficient background task patterns found.")
        else:
            print(f"Skipping {target_path}: Not a JavaScript/TypeScript file.")
    elif os.path.isdir(target_path):
        print(f"\033[1mScanning directory: {target_path}\033[0m")
        found_any = False
        for root, dirs, files in os.walk(target_path):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in excluded_dirs]

            for file in files:
                if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    filepath = os.path.join(root, file)
                    if args.verbose:
                        print(f"  Checking {filepath}...")
                    findings = find_inefficient_background_tasks(filepath)
                    if findings:
                        found_any = True
                        print(f"\033[1m  File: {filepath}\033[0m")
                        for f in findings:
                            print(f"\033[93m    WARNING: {f}\033[0m")
        if not found_any:
            print("  No obvious inefficient background task patterns found in scanned files.")
    else:
        print(f"\033[91mError: Path '{target_path}' does not exist.\033[0m")
        sys.exit(1)

if __name__ == '__main__':
    main()
