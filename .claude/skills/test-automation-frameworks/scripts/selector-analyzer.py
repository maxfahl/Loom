import argparse
import os
import re
from collections import defaultdict

# selector-analyzer.py
#
# Description:
#   This script analyzes TypeScript test files (e.g., Playwright or Selenium Page Objects)
#   to identify potentially fragile or problematic selectors. It flags selectors that rely heavily
#   on CSS classes, XPath, or deep nesting, and suggests more robust alternatives like data-testid.
#
# Usage:
#   python selector-analyzer.py <path_to_test_files> [options]
#
# Arguments:
#   <path_to_test_files> : The path to the directory containing your test files (e.g., './src/e2e').
#
# Options:
#   -e, --exclude <pattern> : Glob pattern to exclude files/directories (e.g., '**/node_modules/**').
#   -o, --output <file>     : Output results to a file instead of stdout.
#   -v, --verbose           : Show more detailed output, including all analyzed selectors.
#   -h, --help              : Show this help message and exit.
#
# Examples:
#   python selector-analyzer.py ./src/e2e
#   python selector-analyzer.py ./tests/e2e --exclude '**/temp/**' -o selector_report.txt
#   python selector-analyzer.py ./playwright-typescript/pages -v
#
# Fragility Rules:
#   - CSS classes: Selectors relying solely on generic or multiple CSS classes are often fragile.
#   - XPath: Complex or absolute XPath expressions are generally fragile.
#   - Nth-child/Nth-of-type: Positional selectors are highly susceptible to UI changes.
#   - Deep nesting: Selectors with many parent-child relationships are fragile.
#   - ID: Generally robust, but dynamic IDs can be problematic.
#   - Data-testid: Highly recommended for stability.

class SelectorAnalyzer:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.fragile_selectors = defaultdict(list)
        self.robust_selectors = defaultdict(list)
        self.total_selectors = 0

    def analyze_selector(self, selector_string, file_path, line_num):
        self.total_selectors += 1
        fragility_score = 0
        suggestions = []
        is_fragile = False

        # Rule 1: Nth-child/Nth-of-type
        if re.search(r':nth-child|:nth-of-type', selector_string):
            fragility_score += 3
            suggestions.append("Avoid positional selectors like :nth-child/:nth-of-type. Use data-testid or unique attributes.")
            is_fragile = True

        # Rule 2: Complex XPath (contains / or //, not just simple attribute)
        if re.search(r'^//|\/', selector_string) and not re.match(r'^//\[@\w+=\'.*?\'\]$', selector_string):
            fragility_score += 5
            suggestions.append("Complex XPath expressions are fragile. Prefer CSS selectors or data-testid.")
            is_fragile = True

        # Rule 3: Generic CSS classes (multiple classes, or common class names)
        # This is a heuristic, might need fine-tuning
        if re.search(r'\.\w+\s*\.\w+', selector_string) or re.search(r'\.(btn|button|input|text|item|card|container)', selector_string, re.IGNORECASE):
            # Exclude data-testid attributes that might look like classes
            if not re.search(r'\[data-testid=["\'].*?["\'].*?\.\w+', selector_string):
                fragility_score += 2
                suggestions.append("Selectors based on generic or multiple CSS classes can be fragile. Use data-testid.")
                is_fragile = True

        # Rule 4: Deep nesting (more than 3 levels of > or space combinators)
        if len(re.findall(r'[ >+~]', selector_string)) > 3:
            fragility_score += 2
            suggestions.append("Deeply nested selectors are fragile. Simplify or use data-testid.")
            is_fragile = True

        # Rule 5: ID (check for dynamic IDs - heuristic)
        if re.search(r'#\w+-\d+', selector_string) or re.search(r'#\d+\w+', selector_string):
            fragility_score += 1
            suggestions.append("Dynamic IDs can be fragile. Ensure IDs are static or use data-testid.")
            is_fragile = True

        # Rule 6: Data-testid (considered robust)
        if re.search(r'\[data-testid=["\'].*?["\']\]', selector_string):
            self.robust_selectors[file_path].append({
                "selector": selector_string,
                "line": line_num,
                "score": 0,
                "suggestions": ["Good: Uses data-testid for robustness."]
            })
            return

        if is_fragile:
            self.fragile_selectors[file_path].append({
                "selector": selector_string,
                "line": line_num,
                "score": fragility_score,
                "suggestions": list(set(suggestions)) # Remove duplicates
            })
        else:
            # If not explicitly fragile and no data-testid, consider it neutral/potentially robust
            self.robust_selectors[file_path].append({
                "selector": selector_string,
                "line": line_num,
                "score": 0,
                "suggestions": ["Looks reasonably robust, consider adding data-testid for explicit stability."]
            })

    def process_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                # Regex to find common selector patterns in Playwright/Selenium code
                # e.g., page.locator('selector'), driver.findElement(By.css('selector'))
                # This regex is a heuristic and might need adjustment based on codebase style.
                matches = re.findall(r"(page\.locator|driver\.findElement\(By\.(css|xpath|id|name|className)\)\s*\(\s*|By\.(css|xpath|id|name|className)\s*\(\s*)\\'([^\'\\]*)\\'|\"([^\"\\]*)\"", line)
                for match in matches:
                    # The actual selector string is in the 4th or 5th capturing group
                    selector_string = match[3] or match[4]
                    self.analyze_selector(selector_string, file_path, i)

    def analyze_directory(self, root_dir, exclude_pattern=None):
        for dirpath, _, filenames in os.walk(root_dir):
            if exclude_pattern and re.search(exclude_pattern, dirpath):
                if self.verbose: print(f"Excluding directory: {dirpath}")
                continue

            for filename in filenames:
                if filename.endswith(('.ts', '.js')):
                    file_path = os.path.join(dirpath, filename)
                    if exclude_pattern and re.search(exclude_pattern, file_path):
                        if self.verbose: print(f"Excluding file: {file_path}")
                        continue
                    if self.verbose: print(f"Analyzing file: {file_path}")
                    self.process_file(file_path)

    def generate_report(self):
        report = []
        report.append("--- Selector Analysis Report ---")
        report.append(f"Total selectors analyzed: {self.total_selectors}")
        report.append(f"Fragile selectors identified: {len(self.fragile_selectors)}")
        report.append(f"Robust selectors identified: {len(self.robust_selectors)}")
        report.append("")

        if self.fragile_selectors:
            report.append("### Fragile Selectors (Potential Flakiness Risk) ###")
            for file_path, selectors in self.fragile_selectors.items():
                report.append(f"\nFile: {file_path}")
                for sel in sorted(selectors, key=lambda x: x['line']):
                    report.append(f"  Line {sel['line']}: '{sel['selector']}' (Score: {sel['score']})")
                    for suggestion in sel['suggestions']:
                        report.append(f"    - Suggestion: {suggestion}")
        else:
            report.append("No fragile selectors identified. Great job!")

        if self.verbose and self.robust_selectors:
            report.append("\n### Robust/Neutral Selectors ###")
            for file_path, selectors in self.robust_selectors.items():
                report.append(f"\nFile: {file_path}")
                for sel in sorted(selectors, key=lambda x: x['line']):
                    report.append(f"  Line {sel['line']}: '{sel['selector']}'")
                    for suggestion in sel['suggestions']:
                        report.append(f"    - Note: {suggestion}")

        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze TypeScript test files for fragile selectors.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("path_to_test_files", type=str, help="Path to the directory containing test files.")
    parser.add_argument("-e", "--exclude", type=str, help="Glob pattern to exclude files/directories (e.g., '**/node_modules/**').")
    parser.add_argument("-o", "--output", type=str, help="Output results to a file instead of stdout.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show more detailed output.")

    args = parser.parse_args()

    analyzer = SelectorAnalyzer(verbose=args.verbose)
    analyzer.analyze_directory(args.path_to_test_files, args.exclude)
    report = analyzer.generate_report()

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Selector analysis report saved to {args.output}")
        except IOError as e:
            print(f"Error writing to file {args.output}: {e}")
            exit(1)
    else:
        print(report)

if __name__ == "__main__":
    main()
