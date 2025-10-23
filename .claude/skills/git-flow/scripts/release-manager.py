#!/usr/bin/env python3
"""
release-manager.py - Comprehensive Git Flow release management

Purpose:
    Manages the complete release workflow including creation, version bumping,
    changelog generation, merging to main and develop, tagging, and cleanup.

Usage:
    ./release-manager.py create <version>     Create new release branch
    ./release-manager.py finalize <version>   Finalize and merge release
    ./release-manager.py status               Show current release status
    ./release-manager.py list                 List all release branches

Options:
    --develop <branch>      Develop branch name (default: develop)
    --main <branch>         Main branch name (default: main)
    --remote <name>         Remote name (default: origin)
    --no-changelog          Skip changelog generation
    --no-tag                Skip git tagging
    --dry-run               Show what would be done
    -h, --help              Show this help

Examples:
    ./release-manager.py create 1.2.0
    ./release-manager.py finalize 1.2.0
    ./release-manager.py create 2.0.0-beta.1
    ./release-manager.py finalize 1.1.0 --no-changelog
    ./release-manager.py status

Requirements:
    - Python 3.7+
    - git
    - semver package (pip install semver)

Exit Codes:
    0 - Success
    1 - Invalid arguments
    2 - Git errors
    3 - Validation errors
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import semver
except ImportError:
    print("Error: semver package not found. Install with: pip install semver")
    sys.exit(1)

# Configuration
DEVELOP_BRANCH = os.environ.get("GIT_FLOW_DEVELOP", "develop")
MAIN_BRANCH = os.environ.get("GIT_FLOW_MAIN", "main")
REMOTE = "origin"
DRY_RUN = False

# ANSI colors
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def log_info(msg: str) -> None:
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

def log_success(msg: str) -> None:
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")

def log_warning(msg: str) -> None:
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")

def log_error(msg: str) -> None:
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}", file=sys.stderr)

def run_command(cmd: List[str], capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    """Execute a command, handling dry-run mode."""
    if DRY_RUN:
        print(f"{Colors.YELLOW}[DRY-RUN]{Colors.NC} {' '.join(cmd)}")
        return subprocess.CompletedProcess(cmd, 0, stdout=b"", stderr=b"")

    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        log_error(f"Command failed: {' '.join(cmd)}")
        log_error(f"Error: {e.stderr if e.stderr else str(e)}")
        raise

def validate_version(version: str) -> bool:
    """Validate semantic version format."""
    try:
        # Handle pre-release versions
        if '-' in version:
            base_version, prerelease = version.split('-', 1)
            semver.VersionInfo.parse(f"{base_version}-{prerelease}")
        else:
            semver.VersionInfo.parse(version)
        return True
    except ValueError:
        log_error(f"Invalid semantic version: {version}")
        log_error("Expected format: X.Y.Z or X.Y.Z-prerelease")
        return False

def get_current_branch() -> str:
    """Get the current git branch name."""
    result = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return result.stdout.strip()

def branch_exists(branch_name: str, remote: bool = False) -> bool:
    """Check if a branch exists locally or remotely."""
    if remote:
        result = run_command(
            ["git", "ls-remote", "--heads", REMOTE, branch_name],
            check=False
        )
        return len(result.stdout.strip()) > 0
    else:
        result = run_command(
            ["git", "show-ref", "--verify", f"refs/heads/{branch_name}"],
            check=False
        )
        return result.returncode == 0

def get_release_branches() -> List[str]:
    """Get all release branches."""
    result = run_command(["git", "branch", "--list", "release/*"])
    branches = [b.strip().replace("* ", "") for b in result.stdout.split('\n') if b.strip()]
    return branches

def get_commits_since(base_branch: str, head_branch: str) -> List[str]:
    """Get commit messages since base_branch."""
    result = run_command([
        "git", "log", f"{base_branch}..{head_branch}",
        "--pretty=format:%s", "--no-merges"
    ])
    return [line for line in result.stdout.split('\n') if line.strip()]

def generate_changelog(version: str, commits: List[str]) -> str:
    """Generate changelog from commit messages."""
    features = []
    fixes = []
    breaking = []
    other = []

    for commit in commits:
        if commit.startswith("feat"):
            features.append(commit)
        elif commit.startswith("fix"):
            fixes.append(commit)
        elif "BREAKING CHANGE" in commit or "!" in commit.split(":")[0]:
            breaking.append(commit)
        else:
            other.append(commit)

    changelog = f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n"

    if breaking:
        changelog += "### ⚠️ BREAKING CHANGES\n\n"
        for commit in breaking:
            changelog += f"- {commit}\n"
        changelog += "\n"

    if features:
        changelog += "### ✨ Features\n\n"
        for commit in features:
            changelog += f"- {commit.replace('feat:', '').replace('feat(', '(').strip()}\n"
        changelog += "\n"

    if fixes:
        changelog += "### 🐛 Bug Fixes\n\n"
        for commit in fixes:
            changelog += f"- {commit.replace('fix:', '').replace('fix(', '(').strip()}\n"
        changelog += "\n"

    if other:
        changelog += "### 🔧 Other Changes\n\n"
        for commit in other[:10]:  # Limit other changes
            changelog += f"- {commit}\n"
        changelog += "\n"

    return changelog

def update_changelog_file(version: str, changelog_entry: str) -> None:
    """Update CHANGELOG.md file."""
    changelog_path = Path("CHANGELOG.md")

    if changelog_path.exists():
        content = changelog_path.read_text()
        # Insert after header
        lines = content.split('\n')
        header_end = 0
        for i, line in enumerate(lines):
            if line.startswith("##") and i > 0:
                header_end = i
                break

        lines.insert(header_end, changelog_entry)
        changelog_path.write_text('\n'.join(lines))
        log_success(f"Updated CHANGELOG.md with version {version}")
    else:
        # Create new changelog
        content = f"# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n{changelog_entry}"
        changelog_path.write_text(content)
        log_success("Created CHANGELOG.md")

    if not DRY_RUN:
        run_command(["git", "add", "CHANGELOG.md"])

def update_version_files(version: str) -> None:
    """Update version in common files."""
    updated = []

    # package.json
    package_json = Path("package.json")
    if package_json.exists():
        run_command(["npm", "version", version, "--no-git-tag-version"], check=False)
        updated.append("package.json")

    # pyproject.toml
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        content = pyproject.read_text()
        content = re.sub(r'version = "[^"]*"', f'version = "{version}"', content)
        if not DRY_RUN:
            pyproject.write_text(content)
        updated.append("pyproject.toml")

    # Cargo.toml
    cargo = Path("Cargo.toml")
    if cargo.exists():
        content = cargo.read_text()
        content = re.sub(r'version = "[^"]*"', f'version = "{version}"', content)
        if not DRY_RUN:
            cargo.write_text(content)
        updated.append("Cargo.toml")

    if updated:
        log_success(f"Updated version in: {', '.join(updated)}")
        if not DRY_RUN:
            run_command(["git", "add"] + updated)

def create_release(version: str, args: argparse.Namespace) -> int:
    """Create a new release branch."""
    log_info(f"Creating release branch for version {version}")

    # Validate version
    if not validate_version(version):
        return 3

    # Check if release branch already exists
    release_branch = f"release/{version}"
    if branch_exists(release_branch):
        log_error(f"Release branch already exists: {release_branch}")
        return 2

    # Ensure we're in a git repository
    try:
        run_command(["git", "rev-parse", "--git-dir"])
    except subprocess.CalledProcessError:
        log_error("Not a git repository")
        return 2

    # Checkout and update develop
    log_info(f"Syncing with {args.develop} branch...")
    run_command(["git", "checkout", args.develop])
    run_command(["git", "pull", args.remote, args.develop])

    # Create release branch
    log_info(f"Creating branch: {release_branch}")
    run_command(["git", "checkout", "-b", release_branch, args.develop])

    # Update version files
    update_version_files(version)

    # Generate changelog if requested
    if not args.no_changelog:
        commits = get_commits_since(args.main, release_branch)
        if commits:
            changelog = generate_changelog(version, commits)
            update_changelog_file(version, changelog)

    # Commit version bump
    if not DRY_RUN:
        run_command(["git", "commit", "-m", f"chore: bump version to {version}"])

    # Push to remote
    log_info(f"Pushing {release_branch} to remote...")
    run_command(["git", "push", "-u", args.remote, release_branch])

    log_success(f"Release branch created: {release_branch}")
    print(f"\nNext steps:")
    print(f"  1. Test the release thoroughly")
    print(f"  2. Fix any bugs in the {release_branch} branch")
    print(f"  3. Finalize with: ./release-manager.py finalize {version}")

    return 0

def finalize_release(version: str, args: argparse.Namespace) -> int:
    """Finalize a release by merging to main and develop."""
    log_info(f"Finalizing release {version}")

    release_branch = f"release/{version}"

    # Check if release branch exists
    if not branch_exists(release_branch):
        log_error(f"Release branch does not exist: {release_branch}")
        return 2

    # Checkout release branch
    run_command(["git", "checkout", release_branch])
    run_command(["git", "pull", args.remote, release_branch])

    # Merge to main
    log_info(f"Merging {release_branch} to {args.main}...")
    run_command(["git", "checkout", args.main])
    run_command(["git", "pull", args.remote, args.main])
    run_command(["git", "merge", "--no-ff", release_branch, "-m", f"Release version {version}"])

    # Tag the release
    if not args.no_tag:
        tag_name = f"v{version}"
        log_info(f"Creating tag: {tag_name}")
        run_command(["git", "tag", "-a", tag_name, "-m", f"Release version {version}"])

    # Push main with tags
    log_info(f"Pushing {args.main} with tags...")
    run_command(["git", "push", args.remote, args.main, "--tags"])

    # Merge back to develop
    log_info(f"Merging {release_branch} back to {args.develop}...")
    run_command(["git", "checkout", args.develop])
    run_command(["git", "pull", args.remote, args.develop])
    run_command(["git", "merge", "--no-ff", release_branch])
    run_command(["git", "push", args.remote, args.develop])

    # Delete release branch
    log_info("Cleaning up release branch...")
    run_command(["git", "branch", "-d", release_branch])
    run_command(["git", "push", args.remote, "--delete", release_branch])

    log_success(f"Release {version} finalized successfully!")
    print(f"\nRelease v{version} is now live on {args.main}")
    print(f"Tag: v{version}")

    return 0

def show_status(args: argparse.Namespace) -> int:
    """Show current release status."""
    print(f"\n{Colors.BLUE}Git Flow Release Status{Colors.NC}\n")

    # Current branch
    current = get_current_branch()
    print(f"Current branch: {current}")

    # Release branches
    releases = get_release_branches()
    if releases:
        print(f"\nActive release branches:")
        for branch in releases:
            print(f"  - {branch}")
    else:
        print(f"\n{Colors.GREEN}No active release branches{Colors.NC}")

    # Latest tag
    result = run_command(["git", "describe", "--tags", "--abbrev=0"], check=False)
    if result.returncode == 0:
        latest_tag = result.stdout.strip()
        print(f"\nLatest release tag: {latest_tag}")

    return 0

def list_releases(args: argparse.Namespace) -> int:
    """List all releases."""
    # Get all tags
    result = run_command(["git", "tag", "-l", "v*", "--sort=-version:refname"])
    tags = result.stdout.strip().split('\n')

    print(f"\n{Colors.BLUE}Release History{Colors.NC}\n")

    for tag in tags[:10]:  # Show last 10 releases
        if tag:
            # Get tag date
            date_result = run_command([
                "git", "log", "-1", "--format=%ai", tag
            ])
            date = date_result.stdout.strip().split()[0]
            print(f"  {tag:20} ({date})")

    return 0

def main() -> int:
    global DRY_RUN, DEVELOP_BRANCH, MAIN_BRANCH, REMOTE

    parser = argparse.ArgumentParser(
        description="Git Flow release manager",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Create release
    create_parser = subparsers.add_parser("create", help="Create new release branch")
    create_parser.add_argument("version", help="Semantic version (e.g., 1.2.0)")

    # Finalize release
    finalize_parser = subparsers.add_parser("finalize", help="Finalize and merge release")
    finalize_parser.add_argument("version", help="Version to finalize")

    # Status
    subparsers.add_parser("status", help="Show release status")

    # List
    subparsers.add_parser("list", help="List all releases")

    # Common options
    for p in [create_parser, finalize_parser]:
        p.add_argument("--develop", default=DEVELOP_BRANCH, help="Develop branch name")
        p.add_argument("--main", default=MAIN_BRANCH, help="Main branch name")
        p.add_argument("--remote", default=REMOTE, help="Remote name")
        p.add_argument("--no-changelog", action="store_true", help="Skip changelog generation")
        p.add_argument("--no-tag", action="store_true", help="Skip git tagging")
        p.add_argument("--dry-run", action="store_true", help="Show what would be done")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if hasattr(args, "dry_run") and args.dry_run:
        DRY_RUN = True

    try:
        if args.command == "create":
            return create_release(args.version, args)
        elif args.command == "finalize":
            return finalize_release(args.version, args)
        elif args.command == "status":
            return show_status(args)
        elif args.command == "list":
            return list_releases(args)
    except subprocess.CalledProcessError:
        return 2
    except KeyboardInterrupt:
        log_warning("\nOperation cancelled by user")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
