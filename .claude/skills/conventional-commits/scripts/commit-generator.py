#!/usr/bin/env python3

"""
Conventional Commits Generator

Purpose:
    Interactive CLI tool to generate properly formatted commit messages
    following the Conventional Commits v1.0.0 specification

Usage:
    ./commit-generator.py [OPTIONS]

Options:
    -h, --help              Show this help message
    -t, --type TYPE         Commit type (skip interactive selection)
    -s, --scope SCOPE       Commit scope (skip interactive input)
    -d, --desc DESC         Commit description (skip interactive input)
    -b, --body BODY         Commit body (skip interactive input)
    --breaking              Mark as breaking change
    --issue ISSUE           Reference issue number
    --no-color              Disable colored output
    --dry-run               Show the commit message without committing
    --commit                Automatically commit with generated message
    --config FILE           Load configuration from file

Examples:
    # Interactive mode
    ./commit-generator.py

    # Quick commit with arguments
    ./commit-generator.py -t feat -s auth -d "add password reset"

    # Breaking change
    ./commit-generator.py -t feat -s api --breaking -d "remove v1 endpoints"

    # Generate and commit automatically
    ./commit-generator.py --commit

    # Dry run to preview
    ./commit-generator.py --dry-run -t fix -d "resolve race condition"

Exit Codes:
    0 - Success
    1 - User cancelled or validation failed
    2 - Invalid arguments or configuration error
"""

import sys
import os
import argparse
import subprocess
import re
from typing import Optional, List, Dict
from pathlib import Path

# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

    @classmethod
    def disable(cls):
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = ''
        cls.MAGENTA = cls.CYAN = cls.BOLD = cls.NC = ''


# Commit type definitions with descriptions
COMMIT_TYPES = {
    'feat': 'A new feature (MINOR version bump)',
    'fix': 'A bug fix (PATCH version bump)',
    'refactor': 'Code change without altering behavior',
    'perf': 'Performance improvement',
    'style': 'Code style/formatting changes',
    'test': 'Adding or updating tests',
    'docs': 'Documentation changes only',
    'build': 'Build system or dependency changes',
    'ops': 'Operational/infrastructure changes',
    'chore': 'Miscellaneous changes',
    'revert': 'Revert a previous commit',
}


def print_color(color: str, text: str, **kwargs):
    """Print colored text"""
    print(f"{color}{text}{Colors.NC}", **kwargs)


def print_header(text: str):
    """Print a section header"""
    print()
    print_color(Colors.BOLD + Colors.CYAN, f"{'=' * 60}")
    print_color(Colors.BOLD + Colors.CYAN, f"  {text}")
    print_color(Colors.BOLD + Colors.CYAN, f"{'=' * 60}")
    print()


def print_error(text: str):
    """Print error message"""
    print_color(Colors.RED, f"ERROR: {text}", file=sys.stderr)


def print_success(text: str):
    """Print success message"""
    print_color(Colors.GREEN, f"✓ {text}")


def print_warning(text: str):
    """Print warning message"""
    print_color(Colors.YELLOW, f"⚠ {text}")


def print_info(text: str):
    """Print info message"""
    print_color(Colors.BLUE, f"ℹ {text}")


def get_input(prompt: str, default: str = "", required: bool = False) -> str:
    """Get user input with optional default and validation"""
    while True:
        if default:
            display_prompt = f"{prompt} [{default}]: "
        else:
            display_prompt = f"{prompt}: "

        value = input(display_prompt).strip()

        if not value and default:
            return default

        if not value and required:
            print_error("This field is required!")
            continue

        return value


def select_option(prompt: str, options: Dict[str, str], show_descriptions: bool = True) -> str:
    """Display a menu and get user selection"""
    print()
    print_color(Colors.BOLD, prompt)
    print()

    # Display options
    items = list(options.items())
    for i, (key, description) in enumerate(items, 1):
        if show_descriptions:
            print(f"  {Colors.CYAN}{i}.{Colors.NC} {Colors.BOLD}{key}{Colors.NC}")
            print(f"     {Colors.MAGENTA}{description}{Colors.NC}")
        else:
            print(f"  {Colors.CYAN}{i}.{Colors.NC} {key}: {description}")

    print()

    # Get selection
    while True:
        try:
            choice = input("Enter number: ").strip()
            if not choice:
                print_error("Please enter a number")
                continue

            index = int(choice) - 1
            if 0 <= index < len(items):
                return items[index][0]
            else:
                print_error(f"Please enter a number between 1 and {len(items)}")
        except ValueError:
            print_error("Please enter a valid number")
        except (KeyboardInterrupt, EOFError):
            print()
            print_warning("Cancelled by user")
            sys.exit(1)


def validate_scope(scope: str) -> bool:
    """Validate scope format"""
    if not scope:
        return True  # Scope is optional
    return bool(re.match(r'^[a-z0-9-]+$', scope))


def validate_description(description: str) -> tuple[bool, List[str]]:
    """Validate description and return (is_valid, warnings)"""
    warnings = []

    if not description:
        return False, ["Description is required"]

    # Check capitalization
    if description[0].isupper():
        warnings.append("Description should not start with a capital letter")

    # Check for period at end
    if description.endswith('.'):
        warnings.append("Description should not end with a period")

    # Check length
    if len(description) > 100:
        warnings.append(f"Description is long ({len(description)} chars). Consider keeping it under 100 characters")

    # Check for past tense
    past_tense_words = ['added', 'fixed', 'updated', 'changed', 'removed', 'deleted']
    first_word = description.split()[0].lower() if description.split() else ""
    if first_word in past_tense_words:
        imperative = first_word[:-1] if first_word.endswith('ed') else first_word
        warnings.append(f"Use imperative mood: '{imperative}' instead of '{first_word}'")

    return True, warnings


def format_commit_message(
    commit_type: str,
    description: str,
    scope: str = "",
    breaking: bool = False,
    body: str = "",
    footer: str = "",
    issue: str = ""
) -> str:
    """Format the complete commit message"""
    # Build first line
    first_line = commit_type
    if scope:
        first_line += f"({scope})"
    if breaking:
        first_line += "!"
    first_line += f": {description}"

    # Build complete message
    message_parts = [first_line]

    # Add body if present
    if body:
        message_parts.append("")
        message_parts.append(body)

    # Add footer
    footer_parts = []
    if footer:
        footer_parts.append(footer)
    if issue:
        footer_parts.append(f"Refs: #{issue}")

    if footer_parts:
        message_parts.append("")
        message_parts.extend(footer_parts)

    return "\n".join(message_parts)


def preview_commit_message(message: str):
    """Display the formatted commit message"""
    print_header("Generated Commit Message")
    print_color(Colors.GREEN, "┌" + "─" * 78 + "┐")
    for line in message.split("\n"):
        if not line:
            print_color(Colors.GREEN, "│" + " " * 78 + "│")
        else:
            padded_line = line.ljust(78)[:78]
            print_color(Colors.GREEN, f"│{Colors.NC}{padded_line}{Colors.GREEN}│")
    print_color(Colors.GREEN, "└" + "─" * 78 + "┘")
    print()


def commit_message(message: str, dry_run: bool = False) -> bool:
    """Commit the message or print it for dry-run"""
    if dry_run:
        print_info("Dry-run mode: Message generated but not committed")
        print(message)
        return True

    try:
        # Check if there are staged changes
        result = subprocess.run(
            ['git', 'diff', '--cached', '--quiet'],
            capture_output=True
        )

        if result.returncode == 0:
            print_warning("No staged changes to commit")
            print_info("Stage changes first with: git add <files>")
            return False

        # Create commit
        subprocess.run(
            ['git', 'commit', '-m', message],
            check=True
        )
        print_success("Commit created successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create commit: {e}")
        return False
    except FileNotFoundError:
        print_error("Git is not installed or not in PATH")
        return False


def interactive_mode() -> str:
    """Run interactive commit message builder"""
    print_header("Conventional Commit Message Generator")

    # Select type
    commit_type = select_option(
        "Select commit type:",
        COMMIT_TYPES,
        show_descriptions=True
    )

    # Get scope
    print()
    print_color(Colors.BOLD, "Enter scope (optional):")
    print_color(Colors.MAGENTA, "  Scope describes the section of codebase (e.g., api, auth, parser)")
    scope = get_input("Scope", required=False)

    if scope and not validate_scope(scope):
        print_error("Invalid scope format. Use only lowercase letters, numbers, and hyphens")
        sys.exit(1)

    # Get description
    print()
    print_color(Colors.BOLD, "Enter description:")
    print_color(Colors.MAGENTA, "  Use imperative mood: 'add feature' not 'added feature'")
    print_color(Colors.MAGENTA, "  Don't capitalize first letter, don't end with period")

    description = get_input("Description", required=True)
    is_valid, warnings = validate_description(description)

    if warnings:
        print()
        for warning in warnings:
            print_warning(warning)
        print()
        fix = get_input("Continue anyway? (y/n)", default="n")
        if fix.lower() != 'y':
            print_warning("Cancelled. Please fix the description")
            sys.exit(1)

    # Check for breaking change
    print()
    breaking = get_input("Is this a breaking change? (y/n)", default="n").lower() == 'y'

    # Get body
    print()
    print_color(Colors.BOLD, "Enter body (optional):")
    print_color(Colors.MAGENTA, "  Provide additional context about the change")
    print_color(Colors.MAGENTA, "  Press Enter twice to finish (or just Enter to skip)")

    body_lines = []
    while True:
        line = input()
        if not line and (not body_lines or not body_lines[-1]):
            break
        body_lines.append(line)

    body = "\n".join(body_lines).strip()

    # Get footer (for breaking changes)
    footer = ""
    if breaking:
        print()
        print_color(Colors.BOLD, "Enter breaking change description:")
        print_color(Colors.MAGENTA, "  This will be added to the BREAKING CHANGE footer")
        breaking_desc = get_input("Breaking change", required=True)
        footer = f"BREAKING CHANGE: {breaking_desc}"

    # Get issue reference
    print()
    issue = get_input("Issue number (optional, e.g., 123)", required=False)

    # Generate message
    message = format_commit_message(
        commit_type=commit_type,
        description=description,
        scope=scope,
        breaking=breaking,
        body=body,
        footer=footer,
        issue=issue
    )

    return message


def main():
    parser = argparse.ArgumentParser(
        description='Generate Conventional Commit messages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('-t', '--type', choices=list(COMMIT_TYPES.keys()), help='Commit type')
    parser.add_argument('-s', '--scope', help='Commit scope')
    parser.add_argument('-d', '--desc', '--description', dest='description', help='Commit description')
    parser.add_argument('-b', '--body', help='Commit body')
    parser.add_argument('--breaking', action='store_true', help='Mark as breaking change')
    parser.add_argument('--issue', help='Issue number to reference')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    parser.add_argument('--dry-run', action='store_true', help='Show message without committing')
    parser.add_argument('--commit', action='store_true', help='Automatically commit')

    args = parser.parse_args()

    # Disable colors if requested or not a TTY
    if args.no_color or not sys.stdout.isatty():
        Colors.disable()

    # Determine mode
    if args.type and args.description:
        # Non-interactive mode
        footer = ""
        if args.breaking:
            breaking_desc = input("Enter breaking change description: ") if not args.dry_run else "Breaking change"
            footer = f"BREAKING CHANGE: {breaking_desc}"

        message = format_commit_message(
            commit_type=args.type,
            description=args.description,
            scope=args.scope or "",
            breaking=args.breaking,
            body=args.body or "",
            footer=footer,
            issue=args.issue or ""
        )
    else:
        # Interactive mode
        message = interactive_mode()

    # Preview
    preview_commit_message(message)

    # Determine what to do with the message
    if args.dry_run:
        print_info("Dry-run mode: Message generated but not committed")
        print()
        print(message)
        sys.exit(0)
    elif args.commit:
        # Auto-commit
        if commit_message(message):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        # Ask user
        action = get_input("What would you like to do? (c)ommit, (p)rint, (q)uit", default="c").lower()

        if action == 'c':
            if commit_message(message):
                sys.exit(0)
            else:
                sys.exit(1)
        elif action == 'p':
            print()
            print(message)
            sys.exit(0)
        else:
            print_info("Message not committed")
            print()
            print(message)
            sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(2)
