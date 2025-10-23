#!/usr/bin/env python3

"""
ts_build_optimizer.py

Analyzes TypeScript project configuration and compilation diagnostics to identify
and suggest improvements for slow build times. It checks for recommended
`tsconfig.json` settings and highlights potential bottlenecks from `tsc --diagnostics` output.

Usage:
  python3 ts_build_optimizer.py [-p <PROJECT_PATH>] [--dry-run]

Examples:
  python3 ts_build_optimizer.py
  python3 ts_build_optimizer.py -p ./my-monorepo/packages/frontend --dry-run

Requirements:
  - TypeScript (tsc) installed globally or locally in the project.
"""

import argparse
import subprocess
import json
import os
import sys
import re

# --- Configuration / Constants ---
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

TSCONFIG_FILENAME = "tsconfig.json"

# --- Helper Functions ---

def run_command(command, cwd=None, dry_run=False, capture_output=True, text=True, check=False):
    """Runs a shell command."""
    if dry_run:
        print(f"DRY RUN: Would execute: {' '.join(command)}" + (f" in {cwd}" if cwd else ""))
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=capture_output,
            text=text,
            check=check, # Set to False to handle errors manually
            encoding='utf-8',
            errors='ignore'
        )
        return result
    except FileNotFoundError:
        print(f"{COLOR_RED}Error: Command '{command[0]}' not found. "
              "Please ensure TypeScript (tsc) is installed and in your PATH or project node_modules.{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)

def load_tsconfig(project_path):
    """Loads and parses the tsconfig.json file."""
    tsconfig_path = os.path.join(project_path, TSCONFIG_FILENAME)
    if not os.path.exists(tsconfig_path):
        print(f"{COLOR_RED}Error: {TSCONFIG_FILENAME} not found in {project_path}{COLOR_RESET}", file=sys.stderr)
        return None
    try:
        with open(tsconfig_path, 'r', encoding='utf-8') as f:
            # Remove comments before parsing JSON
            content = re.sub(r"//.*|/\*.*?\*/", "", f.read(), flags=re.DOTALL)
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"{COLOR_RED}Error parsing {TSCONFIG_FILENAME}: {e}{COLOR_RESET}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"{COLOR_RED}Error reading {TSCONFIG_FILENAME}: {e}{COLOR_RESET}", file=sys.stderr)
        return None

def analyze_tsconfig(tsconfig_data):
    """Analyzes tsconfig.json for performance-related settings."""
    suggestions = []
    compiler_options = tsconfig_data.get('compilerOptions', {})

    print(f"{COLOR_BLUE}Analyzing {TSCONFIG_FILENAME} for performance settings...{COLOR_RESET}")

    # Check for incremental compilation
    if not compiler_options.get('incremental'):
        suggestions.append(
            f"{COLOR_YELLOW}Suggestion: Enable `incremental: true` in `compilerOptions`.{COLOR_RESET} "
            "This significantly speeds up rebuilds by caching project information."
        )
    
    # Check for composite projects (monorepos)
    if tsconfig_data.get('references') and not compiler_options.get('composite'):
        suggestions.append(
            f"{COLOR_YELLOW}Suggestion: For projects with `references`, set `composite: true` in `compilerOptions`.{COLOR_RESET} "
            "This enables project references, allowing TypeScript to build and type-check only changed parts."
        )

    # Check for skipLibCheck
    if not compiler_options.get('skipLibCheck'):
        suggestions.append(
            f"{COLOR_YELLOW}Suggestion: Consider `skipLibCheck: true` in `compilerOptions`.{COLOR_RESET} "
            "This speeds up compilation by skipping type-checking of declaration files from `node_modules`."
        )

    # Check for isolatedModules
    if not compiler_options.get('isolatedModules'):
        suggestions.append(
            f"{COLOR_YELLOW}Suggestion: Consider `isolatedModules: true` in `compilerOptions`.{COLOR_RESET} "
            "Ensures each file can be compiled independently, beneficial with transpilers like SWC/Babel."
        )

    # Check for exclude
    if not tsconfig_data.get('exclude'):
        suggestions.append(
            f"{COLOR_YELLOW}Suggestion: Add an `exclude` array to `tsconfig.json`.{COLOR_RESET} "
            "Exclude unnecessary files/folders like `node_modules`, `dist`, `build`, or test files if not needed for main compilation."
        )
    elif "node_modules" not in tsconfig_data['exclude']:
        suggestions.append(
            f"{COLOR_YELLOW}Suggestion: Ensure `node_modules` is in the `exclude` array in `tsconfig.json`.{COLOR_RESET} "
            "This prevents TypeScript from processing files that don't need type-checking."
        )

    # Check for noEmit with external transpiler
    # This is harder to detect automatically, so provide a general tip
    if not compiler_options.get('noEmit'):
        suggestions.append(
            f"{COLOR_BLUE}Tip: If using an external transpiler (e.g., SWC, Babel) for JS generation, "
            f"consider setting `noEmit: true` in `compilerOptions`.{COLOR_RESET} "
            "This allows `tsc` to focus solely on type-checking, potentially speeding up builds."
        )

    return suggestions

def analyze_tsc_diagnostics(project_path, dry_run=False):
    """Runs tsc --diagnostics and analyzes its output."""
    print(f"{COLOR_BLUE}Running `tsc --diagnostics` in {project_path}...{COLOR_RESET}")
    command = ["tsc", "--diagnostics"]
    result = run_command(command, cwd=project_path, dry_run=dry_run, check=False)

    if dry_run:
        return []

    if result.returncode != 0 and "error TS" not in result.stderr:
        print(f"{COLOR_YELLOW}Warning: `tsc --diagnostics` exited with code {result.returncode}, but no TypeScript errors were found. "
              "This might indicate a configuration issue or warnings.{COLOR_RESET}", file=sys.stderr)
    
    output_lines = (result.stdout + result.stderr).splitlines()
    diagnostics_suggestions = []

    # Regex to find diagnostic lines related to compilation time
    # Example: "Type checking time: 1234ms" or "File write time: 567ms"
    time_regex = re.compile(r"^(.*?time):\s*(\d+)ms(?:\s+\((\d+)\))?", re.IGNORECASE)
    
    # Look for specific diagnostic messages indicating slow parts
    for line in output_lines:
        if "Type checking time" in line or "Bind time" in line or "Check time" in line or "Emit time" in line:
            match = time_regex.match(line)
            if match:
                diagnostics_suggestions.append(
                    f"{COLOR_YELLOW}Diagnostic: {match.group(1)}: {match.group(2)}ms. "
                    f"Consider optimizing related files/types. {match.group(3) if match.group(3) else ''}{COLOR_RESET}"
                )
        if "Files:" in line and "(total)" in line:
             diagnostics_suggestions.append(f"{COLOR_BLUE}Diagnostic: {line}{COLOR_RESET}")
        if "memory used" in line:
             diagnostics_suggestions.append(f"{COLOR_BLUE}Diagnostic: {line}{COLOR_RESET}")
        # Add more specific diagnostic parsing if needed, e.g., for slow files

    if not diagnostics_suggestions:
        diagnostics_suggestions.append(f"{COLOR_GREEN}No specific performance diagnostics found from `tsc --diagnostics`.{COLOR_RESET}")

    return diagnostics_suggestions

# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(
        description="Analyze TypeScript project for build performance optimization.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-p", "--project-path",
        default=".",
        help="Path to the TypeScript project directory (where tsconfig.json is located). Defaults to current directory."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the analysis without actually running tsc or modifying files."
    )

    args = parser.parse_args()

    project_path = os.path.abspath(args.project_path)
    print(f"{COLOR_BLUE}Starting TypeScript Build Optimization analysis for: {project_path}{COLOR_RESET}\n")

    all_suggestions = []

    # 1. Analyze tsconfig.json
    tsconfig_data = load_tsconfig(project_path)
    if tsconfig_data:
        tsconfig_suggestions = analyze_tsconfig(tsconfig_data)
        all_suggestions.extend(tsconfig_suggestions)
    else:
        print(f"{COLOR_RED}Skipping tsconfig.json analysis due to errors.{COLOR_RESET}", file=sys.stderr)

    print("\n" + "-"*50 + "\n")

    # 2. Analyze tsc --diagnostics output
    diagnostics_suggestions = analyze_tsc_diagnostics(project_path, args.dry_run)
    all_suggestions.extend(diagnostics_suggestions)

    print("\n" + "-"*50 + "\n")

    print(f"{COLOR_BLUE}Summary of TypeScript Build Optimization Suggestions:{COLOR_RESET}")
    if all_suggestions:
        for i, suggestion in enumerate(all_suggestions):
            print(f"  {i+1}. {suggestion}")
    else:
        print(f"  {COLOR_GREEN}No specific optimization suggestions found. Your TypeScript build seems well-optimized!{COLOR_RESET}")

    if args.dry_run:
        print(f"\n{COLOR_YELLOW}Dry run complete. No changes were made.{COLOR_RESET}")

if __name__ == "__main__":
    main()
