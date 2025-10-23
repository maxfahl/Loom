#!/usr/bin/env python3

# rxjs-leak-detector.py
#
# Purpose:
#   Scans Angular TypeScript files for common RxJS subscription patterns that might lead to memory leaks.
#   It identifies `subscribe()` calls that are not immediately followed by common unsubscription patterns
#   like `takeUntil`, `take(1)`, or `first()`. It also provides a heuristic check for `async` pipe usage
#   in associated HTML templates.
#
# Usage:
#   python3 rxjs-leak-detector.py [path/to/scan] [--fix] [--dry-run]
#
# Arguments:
#   [path/to/scan] : Optional. The directory to scan for Angular files. Defaults to 'src/app'.
#   --fix          : Optional. Attempt to automatically add `takeUntil(this.destroy$)` to detected leaks.
#                    Requires `destroy$` Subject to be present or adds a basic one.
#   --dry-run      : Optional. Show what changes would be made without actually modifying files.
#                    Implied if --fix is not used.
#
# Examples:
#   python3 rxjs-leak-detector.py
#   python3 rxjs-leak-detector.py src/app/my-feature --dry-run
#   python3 rxjs-leak-detector.py --fix
#
# Configuration:
#   - `EXCLUDE_DIRS`: Directories to exclude from scanning (e.g., node_modules, dist).
#
# Error Handling:
#   - Reports files that cannot be read.
#   - Provides clear messages for detected potential leaks.
#
# Cross-platform:
#   Pure Python, should work on any OS with Python 3 installed.

import os
import re
import argparse
import sys

# --- Configuration ---
EXCLUDE_DIRS = ['node_modules', 'dist', '.git', '.angular']

# --- Colors for better readability (optional) ---
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Regex Patterns ---

# Detects `subscribe(` calls
SUBSCRIBE_PATTERN = re.compile(r'\.subscribe\(')

# Detects common unsubscription patterns immediately preceding `subscribe(`
UNSUBSCRIBE_PATTERNS = [
    re.compile(r'\.pipe\(.*(takeUntil|take\(1\)|first\(\)).*\)\.subscribe\('),
    re.compile(r'\.subscribe\(.*\)\.add\('), # For add() method on subscription
]

# Detects component decorator to find associated template
COMPONENT_DECORATOR_PATTERN = re.compile(r'@Component\({\s*[^}]*templateUrl:\s*["\\]([^\"\\]+\.html)["\\]')

# Detects `async` pipe usage in HTML templates
ASYNC_PIPE_PATTERN = re.compile(r'\|\s*async')

# Detects `destroy$` Subject for takeUntil pattern
DESTROY_SUBJECT_PATTERN = re.compile(r'private\s+(?:readonly\s+)?destroy\$\s*=\s*new\s+Subject<void>\(\);')

# Detects `ngOnDestroy` method
NG_ON_DESTROY_PATTERN = re.compile(r'ngOnDestroy\(\):\s*void\s*{')

# --- Main Logic ---

def find_potential_leaks(filepath, root_dir):
    potential_leaks = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()

        has_destroy_subject = any(DESTROY_SUBJECT_PATTERN.search(line) for line in content)
        has_ng_on_destroy = any(NG_ON_DESTROY_PATTERN.search(line) for line in content)

        for i, line in enumerate(content):
            if SUBSCRIBE_PATTERN.search(line):
                is_unsubscribed = False
                for pattern in UNSUBSCRIBE_PATTERNS:
                    if pattern.search(line):
                        is_unsubscribed = True
                        break
                
                # Heuristic: check previous line for pipe operator if subscribe is on a new line
                if not is_unsubscribed and i > 0:
                    prev_line = content[i-1].strip()
                    if prev_line.endswith('.pipe(') or prev_line.endswith(')'):
                        for pattern in UNSUBSCRIBE_PATTERNS:
                            if pattern.search(prev_line + line.strip()): # Check combined line
                                is_unsubscribed = True
                                break

                if not is_unsubscribed:
                    # Check for async pipe in template (heuristic)
                    template_url_match = COMPONENT_DECORATOR_PATTERN.search(' '.join(content[max(0, i-10):i+1])) # Search nearby lines for @Component
                    if template_url_match:
                        template_path_relative = template_url_match.group(1)
                        # Resolve template path relative to the current TS file
                        ts_dir = os.path.dirname(filepath)
                        template_path = os.path.join(ts_dir, template_path_relative)
                        if os.path.exists(template_path):
                            with open(template_path, 'r', encoding='utf-8') as t_f:
                                template_content = t_f.read()
                                if ASYNC_PIPE_PATTERN.search(template_content):
                                    is_unsubscribed = True # Likely handled by async pipe

                if not is_unsubscribed:
                    potential_leaks.append({
                        'file': os.path.relpath(filepath, root_dir),
                        'line': i + 1,
                        'code': line.strip(),
                        'has_destroy_subject': has_destroy_subject,
                        'has_ng_on_destroy': has_ng_on_destroy
                    })
    except Exception as e:
        print(f"{Colors.FAIL}Error reading file {filepath}: {e}{Colors.ENDC}")
    return potential_leaks

def fix_leak(filepath, leak_info, dry_run):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    line_num = leak_info['line'] - 1
    original_line = lines[line_num]

    # Add takeUntil(this.destroy$) to the pipe
    # This is a simplified fix and might need manual adjustment for complex pipes
    if '.pipe(' in original_line:
        new_line = original_line.replace('.pipe(', '.pipe(takeUntil(this.destroy$), ')
    else:
        # If no pipe, add one
        new_line = original_line.replace('.subscribe(', '.pipe(takeUntil(this.destroy$)).subscribe(')
    
    # Add imports if not present
    imports_to_add = []
    if 'takeUntil' not in ''.join(lines):
        imports_to_add.append('import { takeUntil } from \'rxjs/operators\';')
    if 'Subject' not in ''.join(lines) and not leak_info['has_destroy_subject']:
        imports_to_add.append('import { Subject } from \'rxjs\';')

    # Add destroy$ subject if not present
    if not leak_info['has_destroy_subject']:
        # Find the class definition line
        class_line_index = -1
        for i, line in enumerate(lines):
            if re.search(r'export\s+(?:abstract\s+)?class\s+\w+', line):
                class_line_index = i
                break
        if class_line_index != -1:
            # Insert destroy$ after the class definition or after constructor if exists
            insert_index = class_line_index + 1
            for i in range(class_line_index + 1, len(lines)):
                if 'constructor(' in lines[i]:
                    insert_index = i + 1
                    break
            lines.insert(insert_index, '  private destroy$ = new Subject<void>();\n')
            print(f"{Colors.OKBLUE}  Added `destroy$` Subject to {filepath}{Colors.ENDC}")

    # Add ngOnDestroy if not present
    if not leak_info['has_ng_on_destroy']:
        # Find the class definition line
        class_line_index = -1
        for i, line in enumerate(lines):
            if re.search(r'export\s+(?:abstract\s+)?class\s+\w+', line):
                class_line_index = i
                break
        if class_line_index != -1:
            # Insert ngOnDestroy at the end of the class
            insert_index = len(lines) - 1 # Before the last '}'
            for i in range(len(lines) - 1, class_line_index, -1):
                if lines[i].strip() == '}':
                    insert_index = i
                    break
            
            lines.insert(insert_index, '\n  ngOnDestroy(): void {\n    this.destroy$.next();\n    this.destroy$.complete();\n  }\n')
            print(f"{Colors.OKBLUE}  Added `ngOnDestroy` to {filepath}{Colors.ENDC}")

    # Insert new imports at the top
    for imp_line in reversed(imports_to_add):
        lines.insert(0, imp_line + '\n')

    lines[line_num] = new_line

    if dry_run:
        print(f"{Colors.OKCYAN}  (Dry Run) Would modify {filepath} at line {line_num + 1}:{Colors.ENDC}")
        print(f"{Colors.WARNING}    - {original_line.strip()}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}    + {new_line.strip()}{Colors.ENDC}")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"{Colors.OKGREEN}  Fixed {filepath} at line {line_num + 1}{Colors.ENDC}")


def main():
    parser = argparse.ArgumentParser(
        description="Scans Angular TypeScript files for potential RxJS memory leaks."
    )
    parser.add_argument(
        "path",
        nargs='?',
        default='src/app',
        help="The directory to scan for Angular files. Defaults to 'src/app'."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to automatically add `takeUntil(this.destroy$)` to detected leaks."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what changes would be made without actually modifying files. Implied if --fix is not used."
    )

    args = parser.parse_args()

    scan_path = args.path
    fix_mode = args.fix
    dry_run = args.dry_run or not fix_mode # Dry run if --fix is not used

    if not os.path.isdir(scan_path):
        print(f"{Colors.FAIL}Error: Scan path '{scan_path}' is not a valid directory.{Colors.ENDC}")
        sys.exit(1)

    print(f"{Colors.HEADER}Scanning for RxJS memory leaks in '{scan_path}' (Dry Run: {dry_run})...{Colors.ENDC}")

    all_potential_leaks = []
    for root, dirs, files in os.walk(scan_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS] # Exclude specified directories
        for file in files:
            if file.endswith('.ts') and not file.endswith('.spec.ts'): # Exclude test files
                filepath = os.path.join(root, file)
                leaks = find_potential_leaks(filepath, scan_path)
                if leaks:
                    all_potential_leaks.extend(leaks)
    
    if not all_potential_leaks:
        print(f"{Colors.OKGREEN}No potential RxJS memory leaks detected!{Colors.ENDC}")
        sys.exit(0)

    print(f"{Colors.WARNING}{len(all_potential_leaks)} potential RxJS memory leaks detected:{Colors.ENDC}")
    for leak in all_potential_leaks:
        print(f