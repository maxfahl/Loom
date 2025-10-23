#!/usr/bin/env python3

"""
check_requirement_quality.py

This script analyzes requirement documents (Markdown files) for common quality issues
like ambiguity, subjectivity, and lack of testability using basic NLP techniques.
It flags problematic phrases and provides suggestions for improvement.

Usage:
    python3 check_requirement_quality.py <file_or_dir_path> [--verbose]

Examples:
    # Check a single requirement file
    python3 check_requirement_quality.py ./requirements/user-stories/UserLogin.md

    # Check all requirement files in a directory with verbose output
    python3 check_requirement_quality.py ./requirements/functional --verbose

    # Get help
    python3 check_requirement_quality.py --help
"""

import argparse
import os
import re
import sys

# Keywords and patterns to flag for ambiguity, subjectivity, or lack of testability
AMBIGUITY_KEYWORDS = [
    "as appropriate", "as applicable", "if appropriate", "if applicable",
    "can be", "could be", "may be", "might be", "should be able to",
    "etc.", "and so on", "and/or", "but not limited to",
    "flexible", "robust", "efficient", "fast", "user-friendly", "easy to use",
    "reliable", "scalable", "secure", "high performance", "low latency",
    "minimal", "maximum", "optimum", "sufficient", "adequate", "appropriate",
    "some", "several", "various", "usually", "generally", "typically",
    "support", "handle", "manage", "process", "allow", "enable",
    "quick", "smooth", "seamless", "graceful", "effective", "timely"
]

# Regex to find lines containing these keywords, case-insensitive
AMBIGUITY_PATTERN = re.compile(r'\b(' + '|'.join(AMBIGUITY_KEYWORDS) + r')\b', re.IGNORECASE)

# Patterns for NFRs that should ideally be measurable
NFR_MEASURABLE_PATTERNS = {
    "performance": re.compile(r'\b(load|response time|throughput|latency|speed)\b', re.IGNORECASE),
    "security": re.compile(r'\b(secure|authentication|authorization|encryption|vulnerability)\b', re.IGNORECASE),
    "usability": re.compile(r'\b(easy to use|user-friendly|intuitive|learnable)\b', re.IGNORECASE),
    "scalability": re.compile(r'\b(scale|concurrent users|growth)\b', re.IGNORECASE),
    "reliability": re.compile(r'\b(available|uptime|fault tolerance|recover)\b', re.IGNORECASE),
}

# Suggestions for improvement
SUGGESTIONS = {
    "ambiguity": "Refine with specific, measurable terms. Avoid vague adjectives and adverbs. Quantify where possible.",
    "nfr_measurable": "Quantify this non-functional requirement with specific metrics (e.g., 'within 2 seconds', '99.9% uptime', '100 concurrent users').",
    "subjectivity": "Replace subjective terms with objective, verifiable statements or acceptance criteria."
}

def analyze_requirement_content(file_path, content, verbose=False):
    """Analyzes the content of a requirement file for quality issues."""
    issues = []
    lines = content.splitlines()

    for i, line in enumerate(lines):
        line_num = i + 1
        # Check for ambiguity keywords
        if AMBIGUITY_PATTERN.search(line):
            issues.append({
                "type": "Ambiguity/Subjectivity",
                "line": line_num,
                "text": line.strip(),
                "suggestion": SUGGESTIONS["ambiguity"]
            })

        # Check for NFRs that lack measurable terms
        # This is a heuristic and might need refinement based on actual NFR patterns
        if "non-functional requirement" in line.lower() or "nfr-" in line.lower():
            is_measurable = False
            for nfr_type, pattern in NFR_MEASURABLE_PATTERNS.items():
                if pattern.search(line):
                    # Look for numbers or percentages in the line to indicate measurability
                    if re.search(r'\d+(\.\d+)?(%|ms|s|users|gb|tb)?\b', line):
                        is_measurable = True
                        break
            if not is_measurable:
                issues.append({
                    "type": "NFR Lacks Measurability",
                    "line": line_num,
                    "text": line.strip(),
                    "suggestion": SUGGESTIONS["nfr_measurable"]
                })

    return issues

def process_file(file_path, verbose=False):
    """Reads a file and performs quality analysis."""
    print(f"\nAnalyzing file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        issues = analyze_requirement_content(file_path, content, verbose)
        if issues:
            print(f"  {len(issues)} potential quality issues found:")
            for issue in issues:
                print(f"    - [Line {issue["line"]}] {issue["type"]}: \'{issue["text"]}\'")
                print(f"      Suggestion: {issue["suggestion"]}")
        else:
            print("  No obvious quality issues found. Good job!")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}", file=sys.stderr)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze requirement Markdown files for quality issues.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "path",
        help="Path to a single requirement file or a directory containing requirement files."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show more detailed output."
    )

    args = parser.parse_args()

    if os.path.isfile(args.path):
        process_file(args.path, args.verbose)
    elif os.path.isdir(args.path):
        print(f"Analyzing all Markdown files in directory: {args.path}")
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith(".md"):
                    process_file(os.path.join(root, file), args.verbose)
    else:
        print(f"Error: Path \'{args.path}\' is neither a file nor a directory.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
