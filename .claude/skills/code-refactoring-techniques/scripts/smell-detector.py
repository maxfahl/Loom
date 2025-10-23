#!/usr/bin/env python3

import argparse
import os
import re
from collections import defaultdict

# ANSI escape codes for colored output
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_END = "\033[0m"

def find_long_functions(filepath: str, max_lines: int) -> list[tuple[str, int, int]]:
    """
    Identifies functions/methods in a TypeScript file that exceed a specified line count.

    Args:
        filepath: The path to the TypeScript file.
        max_lines: The maximum allowed lines for a function/method.

    Returns:
        A list of tuples, each containing (function_name, start_line, line_count)
        for functions exceeding max_lines.
    """
    long_functions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Regex to find function/method declarations (basic, might need refinement for complex cases)
    # Covers: function funcName(), funcName = () => {}, class Method() {}
    function_pattern = re.compile(
        r'^\s*(?:export\s+|public\s+|private\s+|protected\s+|static\s+)?'  # Modifiers
        r'(?:async\s+)?(?:function\s+)?'  # async and function keyword
        r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?:<.*>)?'  # Function name (and generics)
        r'\(.*\)\s*(?::\s*.*?)?'  # Parameters and return type
        r'(?:\s*=>)?\s*\{
'
    )

    class_method_pattern = re.compile(
        r'^\s*(?:public\s+|private\s+|protected\s+|static\s+)?'  # Modifiers
        r'(?:async\s+)?'  # async keyword
        r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?:<.*>)?'  # Method name (and generics)
        r'\(.*\)\s*(?::\s*.*?)?'  # Parameters and return type
        r'\s*\{
'
    )

    function_stack = [] # Stores (function_name, start_line)
    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check for function/method start
        match = function_pattern.match(line) or class_method_pattern.match(line)
        if match:
            function_name = match.group(1)
            function_stack.append((function_name, i + 1)) # Store name and 1-based line number

        # Check for function/method end
        if stripped_line == '}' and function_stack:
            func_name, start_line = function_stack.pop()
            line_count = (i + 1) - start_line + 1 # +1 to include the closing brace line
            if line_count > max_lines:
                long_functions.append((func_name, start_line, line_count))
    return long_functions

def find_duplicate_lines(filepath: str, min_duplicate_lines: int) -> list[tuple[str, int, int]]:
    """
    Identifies consecutive duplicate lines in a TypeScript file.
    This is a very basic duplicate detection and will only find exact consecutive duplicates.

    Args:
        filepath: The path to the TypeScript file.
        min_duplicate_lines: The minimum number of consecutive duplicate lines to report.

    Returns:
        A list of tuples, each containing (duplicate_text, start_line, count)
        for duplicate blocks.
    """
    duplicates = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        return []

    current_duplicate_block = []
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if not stripped_line: # Ignore empty lines for duplication check
            if len(current_duplicate_block) >= min_duplicate_lines:
                duplicates.append((current_duplicate_block[0], i - len(current_duplicate_block) + 1, len(current_duplicate_block)))
            current_duplicate_block = []
            continue

        if not current_duplicate_block:
            current_duplicate_block.append(stripped_line)
        elif stripped_line == current_duplicate_block[-1]:
            current_duplicate_block.append(stripped_line)
        else:
            if len(current_duplicate_block) >= min_duplicate_lines:
                duplicates.append((current_duplicate_block[0], i - len(current_duplicate_block) + 1, len(current_duplicate_block)))
            current_duplicate_block = [stripped_line]

    # Check for any remaining duplicate block at the end of the file
    if len(current_duplicate_block) >= min_duplicate_lines:
        duplicates.append((current_duplicate_block[0], len(lines) - len(current_duplicate_block) + 1, len(current_duplicate_block)))

    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description=f"{COLOR_BLUE}Code Smell Detector for TypeScript files.{COLOR_END}\n" 
                    "Scans for long functions/methods and consecutive duplicate lines.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Path to the directory or file to scan. Defaults to current directory.'
    )
    parser.add_argument(
        '--max-lines',
        type=int,
        default=50,
        help='Maximum allowed lines for a function/method. Functions exceeding this will be flagged. Default: 50.'
    )
    parser.add_argument(
        '--min-duplicate-lines',
        type=int,
        default=5,
        help='Minimum number of consecutive identical lines to consider as a duplicate block. Default: 5.'
    )
    parser.add_argument(
        '--exclude',
        type=str,
        nargs='*',
        default=['node_modules', '.git', 'dist', 'build'],
        help='List of directory names to exclude from scanning. Default: node_modules .git dist build.'
    )
    parser.add_argument(
        '--file-pattern',
        type=str,
        default=r'.*\\.(ts|tsx)$',
        help='Regex pattern for files to include (e.g., ".*\\.ts$" for .ts files). Default: .*.\\(ts|tsx)$.'
    )

    args = parser.parse_args()

    target_path = args.path
    max_lines = args.max_lines
    min_duplicate_lines = args.min_duplicate_lines
    exclude_dirs = set(args.exclude)
    file_pattern = re.compile(args.file_pattern)

    print(f"{COLOR_BLUE}--- Code Smell Detection Report ---{COLOR_END}")
    print(f"Scanning path: {target_path}")
    print(f"Max function lines: {max_lines}")
    print(f"Min consecutive duplicate lines: {min_duplicate_lines}")
    print(f"Excluded directories: {', '.join(exclude_dirs)}\n")

    files_scanned = 0
    total_long_functions = 0
    total_duplicate_blocks = 0

    if os.path.isfile(target_path):
        if file_pattern.match(os.path.basename(target_path)):
            files_scanned += 1
            print(f"{COLOR_BLUE}Scanning file: {target_path}{COLOR_END}")
            long_funcs = find_long_functions(target_path, max_lines)
            if long_funcs:
                total_long_functions += len(long_funcs)
                print(f"{COLOR_YELLOW}  Long Functions/Methods (>{max_lines} lines):{COLOR_END}")
                for name, start, count in long_funcs:
                    print(f"    - {name} (Lines: {count}) at line {start}")
            
            dupes = find_duplicate_lines(target_path, min_duplicate_lines)
            if dupes:
                total_duplicate_blocks += len(dupes)
                print(f"{COLOR_YELLOW}  Consecutive Duplicate Lines (>{min_duplicate_lines} lines):{COLOR_END}")
                for text, start, count in dupes:
                    print(f"    - {count} lines starting at line {start} (e.g., '{text[:50]}...')")
            if not long_funcs and not dupes:
                print(f"  No significant code smells found.")
        else:
            print(f"{COLOR_YELLOW}Skipping {target_path}: Does not match file pattern.{COLOR_END}")
    elif os.path.isdir(target_path):
        for root, dirs, files in os.walk(target_path):
            # Modify dirs in-place to prune the search
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file_pattern.match(file):
                    filepath = os.path.join(root, file)
                    files_scanned += 1
                    print(f"{COLOR_BLUE}Scanning file: {filepath}{COLOR_END}")
                    
                    long_funcs = find_long_functions(filepath, max_lines)
                    if long_funcs:
                        total_long_functions += len(long_funcs)
                        print(f"{COLOR_YELLOW}  Long Functions/Methods (>{max_lines} lines):{COLOR_END}")
                        for name, start, count in long_funcs:
                            print(f"    - {name} (Lines: {count}) at line {start}")
                    
                    dupes = find_duplicate_lines(filepath, min_duplicate_lines)
                    if dupes:
                        total_duplicate_blocks += len(dupes)
                        print(f"{COLOR_YELLOW}  Consecutive Duplicate Lines (>{min_duplicate_lines} lines):{COLOR_END}")
                        for text, start, count in dupes:
                            print(f"    - {count} lines starting at line {start} (e.g., '{text[:50]}...')")
                    if not long_funcs and not dupes:
                        print(f"  No significant code smells found.")
    else:
        print(f"{COLOR_RED}Error: Path '{target_path}' not found or is not a file/directory.{COLOR_END}")
        exit(1)

    print(f"\n{COLOR_BLUE}--- Summary ---{COLOR_END}")
    print(f"Files scanned: {files_scanned}")
    print(f"Total long functions/methods found: {total_long_functions}")
    print(f"Total consecutive duplicate blocks found: {total_duplicate_blocks}")
    print(f"{COLOR_BLUE}-------------------{COLOR_END}")

if __name__ == '__main__':
    main()
