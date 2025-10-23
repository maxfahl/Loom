# scripts/aria-linter.py

import argparse
import os
import re
import sys
from bs4 import BeautifulSoup

def check_html_aria(file_path):
    """Checks an HTML file for common ARIA issues."""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

            # Rule 1: role="button" without tabindex="0" on non-focusable elements
            for el in soup.find_all(attrs={"role": "button"}):
                if el.name not in ['button', 'a', 'input', 'select', 'textarea'] and el.get('tabindex') != '0':
                    issues.append(f"  - Element with role='button' is not natively focusable and missing tabindex='0': <{el.name} {el.attrs}>")

            # Rule 2 & 3: role="checkbox" or "radio" without aria-checked
            for el in soup.find_all(attrs={"role": ["checkbox", "radio"]}):
                if not el.has_attr('aria-checked'):
                    issues.append(f"  - Element with role='{el['role']}' is missing aria-checked attribute: <{el.name} {el.attrs}>")

            # Rule 4: role="img" without aria-label/labelledby or alt
            for el in soup.find_all(attrs={"role": "img"}):
                if not (el.has_attr('aria-label') or el.has_attr('aria-labelledby') or el.has_attr('alt')):
                    issues.append(f"  - Element with role='img' is missing a text alternative (aria-label, aria-labelledby, or alt): <{el.name} {el.attrs}>")

            # Rule 5: Empty aria-label or aria-labelledby
            for el in soup.find_all(attrs={"aria-label": True}):
                if not el['aria-label'].strip():
                    issues.append(f"  - Element has an empty aria-label: <{el.name} {el.attrs}>")
            for el in soup.find_all(attrs={"aria-labelledby": True}):
                if not el['aria-labelledby'].strip():
                    issues.append(f"  - Element has an empty aria-labelledby: <{el.name} {el.attrs}>")

    except Exception as e:
        issues.append(f"  - Error processing file: {e}")
    return issues

def check_tsx_aria(file_path):
    """Checks a TSX file for common ARIA issues using regex."""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # Regex to find elements with role attribute
            element_with_role_pattern = re.compile(r'<(\w+)([^>]*?)role\s*=\s*["'](button|checkbox|radio|img)["']([^>]*?)>')
            
            for match in element_with_role_pattern.finditer(content):
                tag_name = match.group(1)
                attrs_before_role = match.group(2)
                role = match.group(3)
                attrs_after_role = match.group(4)
                full_element_str = match.group(0)

                all_attrs = attrs_before_role + attrs_after_role

                # Rule 1: role="button" without tabindex="0" on non-focusable elements
                if role == "button" and tag_name not in ['button', 'a', 'input', 'select', 'textarea']:
                    if not re.search(r'tabIndex\s*=\s*["']?0["']?', all_attrs, re.IGNORECASE):
                        issues.append(f"  - Element with role='button' is not natively focusable and missing tabIndex='0': {full_element_str}")

                # Rule 2 & 3: role="checkbox" or "radio" without aria-checked
                if role in ["checkbox", "radio"]:
                    if not re.search(r'aria-checked\s*=', all_attrs, re.IGNORECASE):
                        issues.append(f"  - Element with role='{role}' is missing aria-checked attribute: {full_element_str}")

                # Rule 4: role="img" without aria-label/labelledby or alt
                if role == "img":
                    if not (re.search(r'aria-label\s*=', all_attrs, re.IGNORECASE) or
                            re.search(r'aria-labelledby\s*=', all_attrs, re.IGNORECASE) or
                            re.search(r'alt\s*=', all_attrs, re.IGNORECASE)):
                        issues.append(f"  - Element with role='img' is missing a text alternative (aria-label, aria-labelledby, or alt): {full_element_str}")

            # Rule 5: Empty aria-label or aria-labelledby
            aria_label_pattern = re.compile(r'aria-label\s*=\s*["']\s*["']')
            for match in aria_label_pattern.finditer(content):
                issues.append(f"  - Element has an empty aria-label: {match.group(0)}")

            aria_labelledby_pattern = re.compile(r'aria-labelledby\s*=\s*["']\s*["']')
            for match in aria_labelledby_pattern.finditer(content):
                issues.append(f"  - Element has an empty aria-labelledby: {match.group(0)}")

    except Exception as e:
        issues.append(f"  - Error processing file: {e}")
    return issues

def main():
    parser = argparse.ArgumentParser(
        description="Scan HTML/TSX files for common ARIA attribute misuses or missing attributes.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("path", nargs='+', help="One or more file paths or directories to scan.")
    parser.add_argument("-e", "--exclude", nargs='*', default=[],
                        help="Optional: List of file/directory patterns to exclude (e.g., 'node_modules', '*.test.tsx').")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulate the scan process without actually performing checks.")

    args = parser.parse_args()

    if args.dry_run:
        print("Dry run: ARIA linter simulation.")
        print(f"Would scan paths: {', '.join(args.path)}")
        if args.exclude:
            print(f"Would exclude patterns: {', '.join(args.exclude)}")
        sys.exit(0)

    all_issues = {}
    for entry_path in args.path:
        if os.path.isfile(entry_path):
            if any(re.search(pattern, entry_path) for pattern in args.exclude):
                continue
            if entry_path.endswith(('.html', '.htm')):
                issues = check_html_aria(entry_path)
                if issues:
                    all_issues[entry_path] = issues
            elif entry_path.endswith(('.tsx', '.jsx')):
                issues = check_tsx_aria(entry_path)
                if issues:
                    all_issues[entry_path] = issues
        elif os.path.isdir(entry_path):
            for root, _, files in os.walk(entry_path):
                if any(re.search(pattern, root) for pattern in args.exclude):
                    continue
                for file_name in files:
                    if any(re.search(pattern, file_name) for pattern in args.exclude):
                        continue
                    file_path = os.path.join(root, file_name)
                    if file_path.endswith(('.html', '.htm')):
                        issues = check_html_aria(file_path)
                        if issues:
                            all_issues[file_path] = issues
                    elif file_path.endswith(('.tsx', '.jsx')):
                        issues = check_tsx_aria(file_path)
                        if issues:
                            all_issues[file_path] = issues

    if all_issues:
        print("\n--- ARIA Linter Issues Found ---")
        for file_path, issues in all_issues.items():
            print(f"File: {file_path}")
            for issue in issues:
                print(issue)
        sys.exit(1)
    else:
        print("\nNo ARIA linter issues found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
