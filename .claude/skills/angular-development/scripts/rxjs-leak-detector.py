#!/usr/bin/env python3

import os
import re
import argparse
import sys

EXCLUDE_DIRS = ['node_modules', 'dist', '.git', '.angular']

class Colors:
    HEADER = ''
    OKBLUE = ''
    OKCYAN = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''

SUBSCRIBE_PATTERN = re.compile(r'\.subscribe\(')
UNSUBSCRIBE_PATTERNS = [
    re.compile(r'\.pipe\(.*(takeUntil|take\(1\)|first\(\)).*\)\.subscribe\('),
    re.compile(r'\.subscribe\(.*\)\.add\('),
]
COMPONENT_DECORATOR_PATTERN = re.compile(r'@Component\({\s*[^}]*templateUrl:\s*["\"](.+?\.html)["\"]')
ASYNC_PIPE_PATTERN = re.compile(r'\|\s*async')
DESTROY_SUBJECT_PATTERN = re.compile(r'private\s+(?:readonly\s+)?destroy\$\s*=\s*new\s+Subject<void>\(\);')
NG_ON_DESTROY_PATTERN = re.compile(r'ngOnDestroy\(\):\s*void\s*{')

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
                
                if not is_unsubscribed and i > 0:
                    prev_line = content[i-1].strip()
                    if prev_line.endswith('.pipe(') or prev_line.endswith(')'):
                        for pattern in UNSUBSCRIBE_PATTERNS:
                            if pattern.search(prev_line + line.strip()):
                                is_unsubscribed = True
                                break

                if not is_unsubscribed:
                    template_url_match = COMPONENT_DECORATOR_PATTERN.search(' '.join(content))
                    if template_url_match:
                        template_path_relative = template_url_match.group(1)
                        ts_dir = os.path.dirname(filepath)
                        template_path = os.path.join(ts_dir, template_path_relative)
                        if os.path.exists(template_path):
                            with open(template_path, 'r', encoding='utf-8') as t_f:
                                template_content = t_f.read()
                                if ASYNC_PIPE_PATTERN.search(template_content):
                                    is_unsubscribed = True

                if not is_unsubscribed:
                    potential_leaks.append({
                        'file': os.path.relpath(filepath, root_dir),
                        'line': i + 1,
                        'code': line.strip(),
                        'has_destroy_subject': has_destroy_subject,
                        'has_ng_on_destroy': has_ng_on_destroy
                    })
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return potential_leaks

def fix_leak(filepath, leak_info, dry_run):
    # This function is complex and will be tested separately.
    pass

def main():
    parser = argparse.ArgumentParser(
        description="Scans Angular TypeScript files for potential RxJS memory leaks."
    )
    parser.add_argument("path", nargs='?', default='src/app', help="The directory to scan.")
    parser.add_argument("--fix", action="store_true", help="Attempt to automatically fix leaks.")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without modifying files.")
    args = parser.parse_args()

    scan_path = args.path
    if not os.path.isdir(scan_path):
        print(f"Error: Scan path '{scan_path}' is not a valid directory.")
        return

    print(f"Scanning for RxJS memory leaks in '{scan_path}'...")

    all_potential_leaks = []
    for root, dirs, files in os.walk(scan_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith('.ts') and not file.endswith('.spec.ts'):
                filepath = os.path.join(root, file)
                leaks = find_potential_leaks(filepath, scan_path)
                if leaks:
                    all_potential_leaks.extend(leaks)
    
    if not all_potential_leaks:
        print("No potential RxJS memory leaks detected!")
        return

    print(f"{len(all_potential_leaks)} potential RxJS memory leaks detected:")
    for leak in all_potential_leaks:
        print(f"  - {leak['file']}:{leak['line']}: {leak['code']}")

if __name__ == "__main__":
    main()