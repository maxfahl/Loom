#!/usr/bin/env python3

# convert-to-esm.py
#
# Purpose:
#   Assists in converting CommonJS (`require`/`module.exports`) modules to
#   ES Modules (`import`/`export`) syntax. This is crucial for modernizing
#   Node.js projects and enabling features like top-level `await`.
#   It provides a dry-run mode to preview changes.
#
# Usage:
#   python3 convert-to-esm.py <file_path> [OPTIONS]
#
# Options:
#   -h, --help        Display this help message.
#   -d, --dry-run     Show suggested changes without modifying the file. (default)
#   -f, --fix         Apply suggested changes directly to the file.
#   -e, --extension   Change file extension to .mjs (for Node.js) or .js (for browser).
#                     Requires --fix. (e.g., --extension .mjs)
#
# Examples:
#   python3 convert-to-esm.py src/utils.js
#   python3 convert-to-esm.py src/config.js --fix --extension .mjs
#
# Requirements:
#   - Python 3.6+
#
# Note: This script uses regex for pattern matching and provides suggestions.
#       For complex cases, manual review and a proper AST parser might be needed.

import argparse
import re
import sys
import os

# --- Colors for output ---
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color

def log_info(message):
    print(f"{BLUE}[INFO]{NC} {message}")

def log_success(message):
    print(f"{GREEN}[SUCCESS]{NC} {message}")

def log_warn(message):
    print(f"{YELLOW}[WARN]{NC} {message}")

def log_error(message):
    print(f"{RED}[ERROR]{NC} {message}", file=sys.stderr)

def convert_cjs_to_esm(content):
    converted_content = content
    suggestions = []

    # 1. Convert `require('module')` to `import module from 'module'` or `import { named } from 'module'`
    #    This is a simplified conversion and might need manual adjustment for default vs named imports.
    #    It assumes `const varName = require('module')` -> `import varName from 'module'`
    #    and `const { named } = require('module')` -> `import { named } from 'module'`

    # Pattern for `const varName = require('module')`
    require_pattern_default = re.compile(r"^\s*const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*require\(['\"](.+?)['\"]\);", re.MULTILINE)
    for match in require_pattern_default.finditer(converted_content):
        var_name = match.group(1)
        module_path = match.group(2)
        new_import = f"import {var_name} from '{module_path}';"
        suggestions.append({
            "type": "require_default",
            "original": match.group(0),
            "suggested": new_import,
            "start": match.start(),
            "end": match.end()
        })
        converted_content = converted_content.replace(match.group(0), new_import, 1)

    # Pattern for `const { named } = require('module')`
    require_pattern_named = re.compile(r"^\s*const\s+\{(.+?)\}
\s*=\s*require\(['\"](.+?)['\"]\);", re.MULTILINE)
    for match in require_pattern_named.finditer(converted_content):
        named_imports = match.group(1)
        module_path = match.group(2)
        new_import = f"import {{{named_imports}}} from '{module_path}';"
        suggestions.append({
            "type": "require_named",
            "original": match.group(0),
            "suggested": new_import,
            "start": match.start(),
            "end": match.end()
        })
        converted_content = converted_content.replace(match.group(0), new_import, 1)

    # 2. Convert `module.exports = ...` to `export default ...`
    module_exports_default_pattern = re.compile(r"^\s*module\.exports\s*=\s*(.+?);?$", re.MULTILINE)
    for match in module_exports_default_pattern.finditer(converted_content):
        exported_value = match.group(1)
        new_export = f"export default {exported_value};"
        suggestions.append({
            "type": "module_exports_default",
            "original": match.group(0),
            "suggested": new_export,
            "start": match.start(),
            "end": match.end()
        })
        converted_content = converted_content.replace(match.group(0), new_export, 1)

    # 3. Convert `exports.name = ...` to `export const name = ...`
    exports_named_pattern = re.compile(r"^\s*exports\.([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+?);?$", re.MULTILINE)
    for match in exports_named_pattern.finditer(converted_content):
        export_name = match.group(1)
        exported_value = match.group(2)
        new_export = f"export const {export_name} = {exported_value};"
        suggestions.append({
            "type": "exports_named",
            "original": match.group(0),
            "suggested": new_export,
            "start": match.start(),
            "end": match.end()
        })
        converted_content = converted_content.replace(match.group(0), new_export, 1)

    return converted_content, suggestions

def main():
    parser = argparse.ArgumentParser(
        description="Helps convert CommonJS modules to ES Modules syntax.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("file_path", help="Path to the JavaScript/TypeScript file.")
    parser.add_argument(
        "-d", "--dry-run", action="store_true", default=True,
        help="Show suggested changes without modifying the file (default)."
    )
    parser.add_argument(
        "-f", "--fix", action="store_true",
        help="Apply suggested changes directly to the file."
    )
    parser.add_argument(
        "-e", "--extension", type=str,
        help="Change file extension (e.g., .mjs for Node.js, .js for browser). Requires --fix."
    )
    args = parser.parse_args()

    if args.fix:
        args.dry_run = False # If --fix is used, disable dry-run

    if args.extension and not args.fix:
        log_error("The --extension flag requires --fix to be enabled.")
        sys.exit(1)

    file_path = args.file_path

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        log_error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        log_error(f"Error reading file {file_path}: {e}")
        sys.exit(1)

    log_info(f"Analyzing file: {file_path} for CommonJS patterns...")
    modified_content, suggestions = convert_cjs_to_esm(content)

    if not suggestions:
        log_success("No CommonJS patterns found that could be converted to ES Modules.")
        sys.exit(0)

    log_info(f"Found {len(suggestions)} potential conversion opportunities.")

    if args.dry_run:
        log_info("--- Dry Run: Suggested Changes (file will NOT be modified) ---")
        for s in suggestions:
            log_warn(f"Original ({s['type']}):")
            print(f"  {s['original']}")
            log_success("Suggested ESM:")
            print(f"  {s['suggested']}")
            print("-" * 50)
        log_info("End of Dry Run. Use --fix to apply changes.")
    elif args.fix:
        log_warn("Applying changes to file. Please ensure you have a backup or use version control.")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            log_success(f"Successfully applied {len(suggestions)} conversion suggestions to {file_path}.")

            if args.extension:
                base, _ = os.path.splitext(file_path)
                new_file_path = base + args.extension
                os.rename(file_path, new_file_path)
                log_success(f"Renamed {file_path} to {new_file_path}.")

        except Exception as e:
            log_error(f"Error writing to file {file_path}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
