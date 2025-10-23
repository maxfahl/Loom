#!/usr/bin/env python3

"""
Semantic Version Bumper

Purpose:
    Automatically determine the next semantic version based on conventional commits
    Analyzes commit history and calculates appropriate version bump (MAJOR.MINOR.PATCH)

Usage:
    ./version-bumper.py [OPTIONS]

Options:
    -h, --help              Show this help message
    -c, --current VERSION   Current version (auto-detect from git tags if not specified)
    -r, --range RANGE       Git commit range to analyze (default: last tag..HEAD)
    --from-tag TAG          Start analysis from specific tag
    --dry-run               Show the next version without updating anything
    --update-file FILE      Update version in specified file (package.json, pyproject.toml, etc.)
    --create-tag            Create git tag for new version
    --prefix PREFIX         Version tag prefix (default: 'v')
    --no-prefix             Don't use prefix for tags
    --prerelease TYPE       Add prerelease identifier (alpha, beta, rc)
    --build-metadata META   Add build metadata
    -v, --verbose           Show detailed analysis
    --format FORMAT         Output format: text, json, version-only (default: text)

Examples:
    # Show next version based on commits
    ./version-bumper.py --dry-run

    # Bump version and create tag
    ./version-bumper.py --create-tag

    # Update package.json with new version
    ./version-bumper.py --update-file package.json

    # Create prerelease version
    ./version-bumper.py --prerelease beta --create-tag

    # Analyze specific commit range
    ./version-bumper.py -r v1.0.0..HEAD --dry-run

    # Get version only (for scripts)
    ./version-bumper.py --format version-only

Exit Codes:
    0 - Success
    1 - Error during version calculation or update
    2 - Invalid arguments or no commits to analyze
"""

import sys
import os
import re
import json
import subprocess
import argparse
from typing import Optional, Tuple, List, Dict
from dataclasses import dataclass
from enum import Enum


class BumpType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    NONE = "none"


@dataclass
class Version:
    major: int
    minor: int
    patch: int
    prerelease: str = ""
    build: str = ""

    def __str__(self) -> str:
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version

    @classmethod
    def parse(cls, version_string: str) -> 'Version':
        """Parse a semantic version string"""
        # Remove 'v' prefix if present
        version_string = version_string.lstrip('v')

        # Pattern: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
        pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?$'
        match = re.match(pattern, version_string)

        if not match:
            raise ValueError(f"Invalid semantic version: {version_string}")

        major, minor, patch, prerelease, build = match.groups()
        return cls(
            major=int(major),
            minor=int(minor),
            patch=int(patch),
            prerelease=prerelease or "",
            build=build or ""
        )

    def bump(self, bump_type: BumpType) -> 'Version':
        """Create a new version with the specified bump"""
        if bump_type == BumpType.MAJOR:
            return Version(self.major + 1, 0, 0)
        elif bump_type == BumpType.MINOR:
            return Version(self.major, self.minor + 1, 0)
        elif bump_type == BumpType.PATCH:
            return Version(self.major, self.minor, self.patch + 1)
        else:
            return Version(self.major, self.minor, self.patch)


@dataclass
class CommitAnalysis:
    sha: str
    type: str
    scope: str
    breaking: bool
    description: str


class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'

    @classmethod
    def disable(cls):
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = cls.BOLD = cls.NC = ''


def print_error(text: str):
    print(f"{Colors.RED}ERROR: {text}{Colors.NC}", file=sys.stderr)


def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.NC}")


def print_info(text: str):
    print(f"{Colors.BLUE}ℹ {text}{Colors.NC}")


def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.NC}")


def run_git_command(args: List[str]) -> Tuple[int, str, str]:
    """Run a git command and return (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except FileNotFoundError:
        print_error("Git is not installed or not in PATH")
        sys.exit(2)


def get_current_version() -> Optional[Version]:
    """Get current version from git tags"""
    returncode, stdout, stderr = run_git_command(['describe', '--tags', '--abbrev=0'])

    if returncode != 0:
        return None

    try:
        return Version.parse(stdout)
    except ValueError as e:
        print_warning(f"Could not parse version from tag '{stdout}': {e}")
        return None


def parse_commit_message(message: str) -> Optional[CommitAnalysis]:
    """Parse a conventional commit message"""
    lines = message.split('\n')
    first_line = lines[0].strip()

    # Skip merge commits
    if first_line.startswith('Merge'):
        return None

    # Pattern: type(scope)!: description
    pattern = r'^([a-z]+)(?:\(([a-z0-9-]+)\))?(!)?:\s*(.+)$'
    match = re.match(pattern, first_line)

    if not match:
        return None

    commit_type, scope, breaking_indicator, description = match.groups()

    # Check for BREAKING CHANGE in footer
    has_breaking_footer = any(
        line.startswith('BREAKING CHANGE:') or line.startswith('BREAKING-CHANGE:')
        for line in lines
    )

    breaking = bool(breaking_indicator) or has_breaking_footer

    # Get commit SHA (first 7 chars)
    returncode, sha, _ = run_git_command(['rev-parse', '--short=7', 'HEAD'])
    if returncode != 0:
        sha = "unknown"

    return CommitAnalysis(
        sha=sha,
        type=commit_type,
        scope=scope or "",
        breaking=breaking,
        description=description
    )


def analyze_commits(commit_range: str, verbose: bool = False) -> Tuple[BumpType, List[CommitAnalysis]]:
    """Analyze commits and determine bump type"""
    # Get commits in range
    returncode, stdout, _ = run_git_command(['rev-list', commit_range])

    if returncode != 0 or not stdout:
        print_error(f"No commits found in range: {commit_range}")
        return BumpType.NONE, []

    commit_shas = stdout.split('\n')

    bump_type = BumpType.NONE
    analyzed_commits = []

    for sha in commit_shas:
        returncode, message, _ = run_git_command(['log', '-1', '--format=%B', sha])

        if returncode != 0:
            continue

        analysis = parse_commit_message(message)

        if not analysis:
            continue

        analyzed_commits.append(analysis)

        # Determine bump type
        if analysis.breaking:
            bump_type = BumpType.MAJOR
        elif analysis.type == 'feat' and bump_type != BumpType.MAJOR:
            bump_type = BumpType.MINOR
        elif analysis.type == 'fix' and bump_type == BumpType.NONE:
            bump_type = BumpType.PATCH

    if verbose:
        print_info(f"Analyzed {len(analyzed_commits)} conventional commits")
        print()

        # Group by type
        by_type: Dict[str, List[CommitAnalysis]] = {}
        for commit in analyzed_commits:
            key = commit.type
            if commit.breaking:
                key = "BREAKING"

            if key not in by_type:
                by_type[key] = []
            by_type[key].append(commit)

        # Display summary
        if "BREAKING" in by_type:
            print(f"{Colors.RED}{Colors.BOLD}BREAKING CHANGES:{Colors.NC}")
            for commit in by_type["BREAKING"]:
                scope = f"({commit.scope})" if commit.scope else ""
                print(f"  • {commit.type}{scope}: {commit.description} ({commit.sha})")
            print()

        if "feat" in by_type:
            print(f"{Colors.GREEN}Features:{Colors.NC}")
            for commit in by_type["feat"]:
                scope = f"({commit.scope})" if commit.scope else ""
                print(f"  • {scope}: {commit.description} ({commit.sha})")
            print()

        if "fix" in by_type:
            print(f"{Colors.YELLOW}Bug Fixes:{Colors.NC}")
            for commit in by_type["fix"]:
                scope = f"({commit.scope})" if commit.scope else ""
                print(f"  • {scope}: {commit.description} ({commit.sha})")
            print()

    return bump_type, analyzed_commits


def update_version_in_file(filepath: str, new_version: str, dry_run: bool = False) -> bool:
    """Update version in a file (package.json, pyproject.toml, etc.)"""
    if not os.path.exists(filepath):
        print_error(f"File not found: {filepath}")
        return False

    filename = os.path.basename(filepath)

    try:
        if filename == 'package.json':
            return update_package_json(filepath, new_version, dry_run)
        elif filename == 'pyproject.toml':
            return update_pyproject_toml(filepath, new_version, dry_run)
        elif filename == 'Cargo.toml':
            return update_cargo_toml(filepath, new_version, dry_run)
        else:
            print_warning(f"Unsupported file type: {filename}")
            return False
    except Exception as e:
        print_error(f"Failed to update {filepath}: {e}")
        return False


def update_package_json(filepath: str, new_version: str, dry_run: bool) -> bool:
    """Update version in package.json"""
    with open(filepath, 'r') as f:
        data = json.load(f)

    old_version = data.get('version', 'unknown')
    data['version'] = new_version

    if dry_run:
        print_info(f"Would update {filepath}: {old_version} -> {new_version}")
        return True

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')

    print_success(f"Updated {filepath}: {old_version} -> {new_version}")
    return True


def update_pyproject_toml(filepath: str, new_version: str, dry_run: bool) -> bool:
    """Update version in pyproject.toml"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Find version line
    pattern = r'^version\s*=\s*"([^"]+)"'
    match = re.search(pattern, content, re.MULTILINE)

    if not match:
        print_error("Could not find version in pyproject.toml")
        return False

    old_version = match.group(1)
    new_content = re.sub(pattern, f'version = "{new_version}"', content, flags=re.MULTILINE)

    if dry_run:
        print_info(f"Would update {filepath}: {old_version} -> {new_version}")
        return True

    with open(filepath, 'w') as f:
        f.write(new_content)

    print_success(f"Updated {filepath}: {old_version} -> {new_version}")
    return True


def update_cargo_toml(filepath: str, new_version: str, dry_run: bool) -> bool:
    """Update version in Cargo.toml"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Find version in [package] section
    pattern = r'(\[package\][\s\S]*?version\s*=\s*)"([^"]+)"'
    match = re.search(pattern, content)

    if not match:
        print_error("Could not find version in Cargo.toml")
        return False

    old_version = match.group(2)
    new_content = re.sub(pattern, rf'\1"{new_version}"', content)

    if dry_run:
        print_info(f"Would update {filepath}: {old_version} -> {new_version}")
        return True

    with open(filepath, 'w') as f:
        f.write(new_content)

    print_success(f"Updated {filepath}: {old_version} -> {new_version}")
    return True


def create_git_tag(version: str, prefix: str, dry_run: bool) -> bool:
    """Create a git tag for the new version"""
    tag_name = f"{prefix}{version}"

    if dry_run:
        print_info(f"Would create git tag: {tag_name}")
        return True

    returncode, _, stderr = run_git_command(['tag', '-a', tag_name, '-m', f'Release {version}'])

    if returncode != 0:
        print_error(f"Failed to create tag: {stderr}")
        return False

    print_success(f"Created git tag: {tag_name}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Determine next semantic version from conventional commits',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('-c', '--current', help='Current version')
    parser.add_argument('-r', '--range', help='Git commit range to analyze')
    parser.add_argument('--from-tag', help='Start analysis from specific tag')
    parser.add_argument('--dry-run', action='store_true', help='Show version without updating')
    parser.add_argument('--update-file', help='Update version in file')
    parser.add_argument('--create-tag', action='store_true', help='Create git tag')
    parser.add_argument('--prefix', default='v', help='Version tag prefix (default: v)')
    parser.add_argument('--no-prefix', action='store_true', help='No version tag prefix')
    parser.add_argument('--prerelease', help='Prerelease identifier (alpha, beta, rc)')
    parser.add_argument('--build-metadata', help='Build metadata')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--format', choices=['text', 'json', 'version-only'], default='text', help='Output format')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    args = parser.parse_args()

    # Disable colors if requested or not a TTY
    if args.no_color or not sys.stdout.isatty():
        Colors.disable()

    # Get current version
    if args.current:
        try:
            current_version = Version.parse(args.current)
        except ValueError as e:
            print_error(f"Invalid version format: {e}")
            sys.exit(2)
    else:
        current_version = get_current_version()
        if not current_version:
            current_version = Version(0, 0, 0)
            print_warning("No version tags found, starting from 0.0.0")

    # Determine commit range
    if args.range:
        commit_range = args.range
    elif args.from_tag:
        commit_range = f"{args.from_tag}..HEAD"
    else:
        # Use last tag to HEAD
        returncode, last_tag, _ = run_git_command(['describe', '--tags', '--abbrev=0'])
        if returncode == 0:
            commit_range = f"{last_tag}..HEAD"
        else:
            # No tags, use all commits
            commit_range = "HEAD"

    # Analyze commits
    bump_type, commits = analyze_commits(commit_range, args.verbose)

    if bump_type == BumpType.NONE:
        if args.format == 'version-only':
            print(str(current_version))
        else:
            print_info(f"No version bump needed. Current version: {current_version}")
        sys.exit(0)

    # Calculate new version
    new_version = current_version.bump(bump_type)

    # Add prerelease/build metadata
    if args.prerelease:
        new_version.prerelease = args.prerelease
    if args.build_metadata:
        new_version.build = args.build_metadata

    # Handle prefix
    prefix = "" if args.no_prefix else args.prefix

    # Output
    if args.format == 'version-only':
        print(str(new_version))
    elif args.format == 'json':
        output = {
            'current': str(current_version),
            'next': str(new_version),
            'bump': bump_type.value,
            'commits_analyzed': len(commits)
        }
        print(json.dumps(output, indent=2))
    else:
        # Text format
        print()
        print(f"{Colors.BOLD}Version Bump Analysis{Colors.NC}")
        print("=" * 50)
        print(f"Current version: {Colors.YELLOW}{current_version}{Colors.NC}")
        print(f"Bump type:       {Colors.BLUE}{bump_type.value.upper()}{Colors.NC}")
        print(f"Next version:    {Colors.GREEN}{new_version}{Colors.NC}")
        print()

    # Update file if requested
    if args.update_file:
        if not update_version_in_file(args.update_file, str(new_version), args.dry_run):
            sys.exit(1)

    # Create tag if requested
    if args.create_tag:
        if not create_git_tag(str(new_version), prefix, args.dry_run):
            sys.exit(1)

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
        import traceback
        traceback.print_exc()
        sys.exit(2)
