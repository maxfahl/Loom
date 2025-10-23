import argparse
import os
import re
import sys
from typing import List, Dict, Any

# ANSI escape codes for colored output
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"

def find_anti_patterns(filepath: str, patterns: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()

        for line_num, line in enumerate(content, 1):
            for pattern_name, pattern_info in patterns.items():
                regex = pattern_info["regex"]
                message = pattern_info["message"]
                severity = pattern_info.get("severity", "warning")

                if re.search(regex, line):
                    findings.append({
                        "file": filepath,
                        "line": line_num,
                        "pattern": pattern_name,
                        "message": message,
                        "severity": severity,
                        "code_snippet": line.strip()
                    })
    except Exception as e:
        print(f"{COLOR_RED}Error reading file {filepath}: {e}{COLOR_RESET}", file=sys.stderr)
    return findings

def main():
    parser = argparse.ArgumentParser(
        description="Analyzes TypeScript files for common CQRS anti-patterns.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "path_to_src",
        help="Path to the source directory containing TypeScript files (e.g., 'src')."
    )
    parser.add_argument(
        "--report-file",
        help="Optional: Path to a file to write the analysis report (e.g., 'cqrs_report.txt')."
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path_to_src):
        print(f"{COLOR_RED}Error: Source directory '{args.path_to_src}' not found.{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)

    # Define common CQRS anti-patterns with regex and messages
    cqrs_anti_patterns = {
        "QueryHandlerSideEffect": {
            "regex": r'(async\s+execute\s*\(.*IQuery.*\).*Promise<.*>\s*\{.*(await\s+this\.\w+\.save|this\.\w+\.publish|new\s+Error\(\'User not found\')|this\.\w+\.delete|this\.\w+\.update)', # Simplified regex, might need refinement
            "message": "Query handlers should not modify state or publish events.",
            "severity": "error"
        },
        "CommandHandlerComplexQuery": {
            "regex": r'(async\s+execute\s*\(.*ICommand.*\).*Promise<void>\s*\{.*(await\s+this\.\w+\.find|await\s+this\.\w+\.get|await\s+this\.\w+\.query)', # Simplified regex
            "message": "Command handlers should avoid complex query logic; delegate to query side.",
            "severity": "warning"
        },
        "MissingReadonly": {
            "regex": r'(interface\s+\w+(Command|Query|Event)\s*\{.*\n\s*\w+\s*:\s*\w+;)', # Detects properties without readonly
            "message": "Command, Query, and Event properties should ideally be readonly.",
            "severity": "info"
        }
    }

    all_findings = []
    print(f"{COLOR_BOLD}{COLOR_BLUE}Starting CQRS Anti-Pattern Analysis in '{args.path_to_src}'...{COLOR_RESET}")

    for root, _, files in os.walk(args.path_to_src):
        for file in files:
            if file.endswith('.ts'):
                filepath = os.path.join(root, file)
                findings = find_anti_patterns(filepath, cqrs_anti_patterns)
                if findings:
                    all_findings.extend(findings)

    output_stream = open(args.report_file, 'w', encoding='utf-8') if args.report_file else sys.stdout

    if all_findings:
        print(f"\n{COLOR_BOLD}{COLOR_YELLOW}--- Analysis Report ---\n{COLOR_RESET}", file=output_stream)
        for finding in all_findings:
            color = COLOR_RED if finding["severity"] == "error" else COLOR_YELLOW if finding["severity"] == "warning" else COLOR_BLUE
            print(f"{color}{COLOR_BOLD}[{finding["severity"].upper()}] {finding["file"]}:{finding["line"]}{COLOR_RESET}", file=output_stream)
            print(f"  {finding["message"]}", file=output_stream)
            print(f"  Code: `{finding["code_snippet"]}`\n", file=output_stream)
        print(f"{COLOR_BOLD}{COLOR_YELLOW}--- End of Report ---\n{COLOR_RESET}", file=output_stream)
    else:
        print(f"\n{COLOR_GREEN}{COLOR_BOLD}No CQRS anti-patterns found in '{args.path_to_src}'. Good job!{COLOR_RESET}", file=output_stream)

    if args.report_file:
        output_stream.close()
        print(f"\n{COLOR_BLUE}Analysis report written to '{args.report_file}'.{COLOR_RESET}")

if __name__ == "__main__":
    main()
