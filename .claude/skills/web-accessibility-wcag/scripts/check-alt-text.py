# scripts/check-alt-text.py

import argparse
import os
import re
import sys
from bs4 import BeautifulSoup

def check_html_alt_text(file_path):
    """Checks an HTML file for img tags with missing or generic alt text."""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            for img_tag in soup.find_all('img'):
                alt_text = img_tag.get('alt', None)
                if alt_text is None or alt_text.strip() == '':
                    issues.append(f"  - Missing or empty alt text: <img src=\"{img_tag.get('src', 'N/A')}\">")
                elif alt_text.lower() in ["image", "picture", "graphic", "logo"]:
                    issues.append(f"  - Generic alt text '{alt_text}': <img src=\"{img_tag.get('src', 'N/A')}\">")
    except Exception as e:
        issues.append(f"  - Error processing file: {e}")
    return issues

def check_tsx_alt_text(file_path):
    """Checks a TSX file for img tags with missing or generic alt text using regex."""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Regex to find <img> tags and capture their alt attribute
            # This regex is simplified and might not catch all edge cases,
            # but covers common React/TSX usage.
            img_pattern = re.compile(r'<img(?P<attrs>[^>]*?)>')
            alt_pattern = re.compile(r'alt\s*=\s*(?P<quote>["'])(?P<alt_text>.*?)(?P=quote)')

            for match in img_pattern.finditer(content):
                img_tag_full = match.group(0)
                attrs_str = match.group('attrs')
                
                alt_match = alt_pattern.search(attrs_str)
                
                if alt_match:
                    alt_text = alt_match.group('alt_text').strip()
                    if alt_text == '':
                        issues.append(f"  - Missing or empty alt text: {img_tag_full}")
                    elif alt_text.lower() in ["image", "picture", "graphic", "logo"]:
                        issues.append(f"  - Generic alt text '{alt_text}': {img_tag_full}")
                else:
                    # No alt attribute found
                    issues.append(f"  - Missing alt attribute: {img_tag_full}")
    except Exception as e:
        issues.append(f"  - Error processing file: {e}")
    return issues

def main():
    parser = argparse.ArgumentParser(
        description="Scan HTML/TSX files for <img> tags with missing or generic alt text.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("path", nargs='+', help="One or more file paths or directories to scan.")
    parser.add_argument("-e", "--exclude", nargs='*', default=[],
                        help="Optional: List of file/directory patterns to exclude (e.g., 'node_modules', '*.test.tsx').")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulate the scan process without actually performing checks.")

    args = parser.parse_args()

    if args.dry_run:
        print("Dry run: Alt text check simulation.")
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
                issues = check_html_alt_text(entry_path)
                if issues:
                    all_issues[entry_path] = issues
            elif entry_path.endswith(('.tsx', '.jsx')):
                issues = check_tsx_alt_text(entry_path)
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
                        issues = check_html_alt_text(file_path)
                        if issues:
                            all_issues[file_path] = issues
                    elif file_path.endswith(('.tsx', '.jsx')):
                        issues = check_tsx_alt_text(file_path)
                        if issues:
                            all_issues[file_path] = issues

    if all_issues:
        print("\n--- Alt Text Issues Found ---")
        for file_path, issues in all_issues.items():
            print(f"File: {file_path}")
            for issue in issues:
                print(issue)
        sys.exit(1)
    else:
        print("\nNo alt text issues found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
