#!/usr/bin/env python3
"""
ios-safe-area-linter.py: Analyzes React Native/iOS UI code for Safe Area issues.

This script helps identify common pitfalls where UI elements might be obscured
by device notches, status bars, or home indicators on iOS devices. It scans
TypeScript/JavaScript files for patterns related to `SafeAreaView` usage,
manual padding/margin, and absolute positioning that might conflict with safe areas.

Usage Examples:
  python ios-safe-area-linter.py --path ./src
  python ios-safe-area-linter.py --path ./src --fix
  python ios-safe-area-linter.py --path ./src/components/MyComponent.tsx --dry-run
"""

import argparse
import re
from pathlib import Path
from typing import List, Tuple

def colored_print(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    print(f"{colors.get(color, colors["reset"])}{text}{colors["reset"]}")

def find_safe_area_issues(file_content: str) -> List[Tuple[int, str, str]]:
    issues = []
    lines = file_content.splitlines()

    # Regex patterns for common issues
    # 1. Manual padding/margin at top/bottom that might conflict with SafeAreaView
    #    Looking for `paddingTop`, `marginTop`, `paddingBottom`, `marginBottom` with fixed values
    #    within a component that might also use SafeAreaView or be a root view.
    manual_padding_pattern = re.compile(r'(paddingTop|marginTop|paddingBottom|marginBottom):\s*(\d+)')

    # 2. Absolute positioning at top/bottom that might overlap safe areas
    absolute_position_pattern = re.compile(r'(top|bottom):\s*(\d+)')

    # 3. Missing SafeAreaView for root-level components on iOS
    #    This is harder to detect precisely without AST, but we can look for `Platform.OS === 'ios'`
    #    checks combined with root-level View components that don't wrap in SafeAreaView.
    #    Or simply a root View in an iOS-specific file without SafeAreaView.
    #    For now, we'll focus on explicit style conflicts.

    for i, line in enumerate(lines):
        # Check for manual padding/margin that might conflict
        for match in manual_padding_pattern.finditer(line):
            prop, value = match.groups()
            if int(value) > 0: # Only flag if padding/margin is actually applied
                issues.append((i + 1, "Manual Padding/Margin", f"Potential conflict: `{prop}: {value}`. Consider using `SafeAreaView` or `useSafeAreaInsets` for iOS."))

        # Check for absolute positioning that might conflict
        for match in absolute_position_pattern.finditer(line):
            prop, value = match.groups()
            if int(value) < 50: # Small absolute values at top/bottom are suspicious
                issues.append((i + 1, "Absolute Positioning", f"Potential conflict: `{prop}: {value}`. Absolute positioning near top/bottom can overlap safe areas on iOS."))

    return issues

def apply_fix(file_path: Path, issues: List[Tuple[int, str, str]], dry_run: bool):
    if not issues:
        return

    colored_print(f"\n--- Applying fixes for {file_path} ---", "yellow")
    original_content = file_path.read_text()
    new_content_lines = original_content.splitlines()
    changes_made = False

    # Simple fix: comment out problematic manual padding/margin/absolute positioning
    # This is a very basic fix and often requires manual developer intervention.
    # A more advanced fix would involve replacing with `SafeAreaView` or `useSafeAreaInsets`.
    for line_num, issue_type, description in sorted(issues, reverse=True): # Process in reverse to avoid line number shifts
        line_index = line_num - 1
        if line_index < len(new_content_lines):
            original_line = new_content_lines[line_index]
            if not original_line.strip().startswith('//'): # Avoid commenting already commented lines
                new_content_lines[line_index] = f"// FIX_SAFE_AREA: {original_line} // {issue_type} - {description}"
                colored_print(f"  Line {line_num}: Commented out potential safe area conflict: {original_line.strip()}", "green")
                changes_made = True

    if changes_made:
        if dry_run:
            colored_print("Dry run: The following changes would be applied:", "cyan")
            colored_print("\n".join(new_content_lines), "cyan")
        else:
            file_path.write_text("\n".join(new_content_lines))
            colored_print(f"Successfully applied basic fixes to {file_path}. Please review manually!", "green")
    else:
        colored_print("No automatic fixes applied (or issues already commented out).", "yellow")

def main():
    parser = argparse.ArgumentParser(
        description="Analyzes React Native/iOS UI code for Safe Area issues.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to the file or directory to scan (e.g., ./src or ./src/components/MyComponent.tsx)."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to automatically apply basic fixes (comments out problematic lines)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually modifying files."
    )

    args = parser.parse_args()

    target_path = Path(args.path)

    if not target_path.exists():
        colored_print(f"Error: Path not found at {target_path}", "red")
        exit(1)

    files_to_scan = []
    if target_path.is_file():
        if target_path.suffix in ['.ts', '.tsx', '.js', '.jsx']:
            files_to_scan.append(target_path)
    elif target_path.is_dir():
        for ext in ['.ts', '.tsx', '.js', '.jsx']:
            files_to_scan.extend(target_path.rglob(f'*{ext}'))
    else:
        colored_print(f"Error: Invalid path type for {target_path}. Must be a file or directory.", "red")
        exit(1)

    if not files_to_scan:
        colored_print(f"No relevant files found in {target_path} to scan.", "yellow")
        exit(0)

    all_issues_found = False
    for file_path in files_to_scan:
        colored_print(f"\nScanning {file_path}...", "blue")
        content = file_path.read_text()
        issues = find_safe_area_issues(content)

        if issues:
            all_issues_found = True
            colored_print(f"  Found {len(issues)} potential safe area issues:", "yellow")
            for line_num, issue_type, description in issues:
                colored_print(f"    L{line_num}: [{issue_type}] {description}", "yellow")
            if args.fix:
                apply_fix(file_path, issues, args.dry_run)
            elif args.dry_run:
                colored_print("  (Run with --fix to apply suggested changes)", "cyan")
        else:
            colored_print("  No obvious safe area issues found.", "green")

    if all_issues_found:
        colored_print("\nScan complete. Review flagged issues and consider using `react-native-safe-area-context` or `SafeAreaView`.", "yellow")
    else:
        colored_print("\nScan complete. No potential safe area issues detected in scanned files.", "green")

if __name__ == "__main__":
    main()
