#!/usr/bin/env python3
"""
branch-cleanup.py - Safely clean up merged and stale Git Flow branches

Purpose:
    Identifies and removes merged feature/release/hotfix branches to maintain
    repository hygiene. Includes safety checks and dry-run mode.

Usage:
    ./branch-cleanup.py [options]

Options:
    --type <type>           Branch type to clean (feature/release/hotfix/all)
    --merged-only           Only delete branches merged to develop/main
    --stale-days <days>     Consider branches stale after N days (default: 30)
    --include-remote        Also delete remote branches
    --exclude <pattern>     Exclude branches matching pattern
    --force                 Skip confirmation prompts
    --dry-run               Show what would be deleted
    -h, --help              Show this help

Examples:
    ./branch-cleanup.py --type feature --merged-only
    ./branch-cleanup.py --type all --stale-days 60
    ./branch-cleanup.py --dry-run
    ./branch-cleanup.py --type release --include-remote --force

Requirements:
    - Python 3.7+
    - git

Exit Codes:
    0 - Success
    1 - Invalid arguments
    2 - Git errors
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Set

# ANSI colors
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    GRAY = '\033[0;90m'
    NC = '\033[0m'

def log_info(msg: str) -> None:
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

def log_success(msg: str) -> None:
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")

def log_warning(msg: str) -> None:
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")

def log_error(msg: str) -> None:
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}", file=sys.stderr)

def log_debug(msg: str) -> None:
    print(f"{Colors.GRAY}[DEBUG]{Colors.NC} {msg}")

def run_command(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Execute a git command."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        log_error(f"Command failed: {' '.join(cmd)}")
        log_error(f"Error: {e.stderr if e.stderr else str(e)}")
        if check:
            raise
        return e

class BranchInfo:
    """Information about a git branch."""

    def __init__(self, name: str, last_commit_date: datetime, is_merged: bool, remote_exists: bool = False):
        self.name = name
        self.last_commit_date = last_commit_date
        self.is_merged = is_merged
        self.remote_exists = remote_exists
        self.age_days = (datetime.now() - last_commit_date).days

    def __repr__(self):
        return f"Branch({self.name}, {self.age_days}d, merged={self.is_merged})"

class BranchCleaner:
    """Main branch cleanup manager."""

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.main_branch = self._get_main_branch()
        self.develop_branch = "develop"
        self.current_branch = self._get_current_branch()
        self.protected_branches = {self.main_branch, self.develop_branch, self.current_branch}

    def _get_main_branch(self) -> str:
        """Detect main/master branch."""
        result = run_command(["git", "branch", "--list", "main", "master"])
        branches = [b.strip().replace("* ", "") for b in result.stdout.split('\n') if b.strip()]
        return branches[0] if branches else "main"

    def _get_current_branch(self) -> str:
        """Get current branch name."""
        result = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        return result.stdout.strip()

    def get_local_branches(self, branch_type: str) -> List[BranchInfo]:
        """Get all local branches of specified type."""
        if branch_type == "all":
            patterns = ["feature/*", "release/*", "hotfix/*"]
        else:
            patterns = [f"{branch_type}/*"]

        branches = []
        for pattern in patterns:
            result = run_command(["git", "branch", "--list", pattern])
            branch_names = [b.strip().replace("* ", "") for b in result.stdout.split('\n') if b.strip()]

            for name in branch_names:
                # Skip if excluded
                if self.args.exclude and re.search(self.args.exclude, name):
                    log_debug(f"Excluding {name} (matches exclude pattern)")
                    continue

                # Get last commit date
                date_result = run_command([
                    "git", "log", "-1", "--format=%ci", name
                ])
                commit_date = datetime.strptime(
                    date_result.stdout.strip().split()[0],
                    "%Y-%m-%d"
                )

                # Check if merged
                is_merged = self._is_merged(name)

                # Check remote
                remote_exists = self._remote_exists(name)

                branches.append(BranchInfo(name, commit_date, is_merged, remote_exists))

        return branches

    def _is_merged(self, branch_name: str) -> bool:
        """Check if branch is merged to develop or main."""
        # Check develop
        result = run_command([
            "git", "branch", "--merged", self.develop_branch, "--list", branch_name
        ], check=False)

        if result.returncode == 0 and result.stdout.strip():
            return True

        # Check main
        result = run_command([
            "git", "branch", "--merged", self.main_branch, "--list", branch_name
        ], check=False)

        return result.returncode == 0 and result.stdout.strip() != ""

    def _remote_exists(self, branch_name: str) -> bool:
        """Check if branch exists on remote."""
        result = run_command([
            "git", "ls-remote", "--heads", "origin", branch_name
        ], check=False)
        return len(result.stdout.strip()) > 0

    def filter_branches(self, branches: List[BranchInfo]) -> List[BranchInfo]:
        """Filter branches based on criteria."""
        filtered = []

        for branch in branches:
            # Skip protected branches
            if branch.name in self.protected_branches:
                log_debug(f"Skipping protected branch: {branch.name}")
                continue

            # Check merged-only flag
            if self.args.merged_only and not branch.is_merged:
                log_debug(f"Skipping unmerged branch: {branch.name}")
                continue

            # Check staleness
            if branch.age_days < self.args.stale_days:
                log_debug(f"Skipping recent branch: {branch.name} ({branch.age_days}d old)")
                continue

            filtered.append(branch)

        return filtered

    def display_branches(self, branches: List[BranchInfo]) -> None:
        """Display branches in a formatted table."""
        if not branches:
            log_info("No branches to delete")
            return

        print(f"\n{Colors.YELLOW}Branches to delete:{Colors.NC}\n")
        print(f"{'Branch':<50} {'Age':<12} {'Merged':<10} {'Remote':<10}")
        print("-" * 85)

        for branch in branches:
            age_str = f"{branch.age_days} days"
            merged_str = "✓" if branch.is_merged else "✗"
            remote_str = "✓" if branch.remote_exists else "✗"

            color = Colors.GREEN if branch.is_merged else Colors.YELLOW
            print(f"{color}{branch.name:<50}{Colors.NC} {age_str:<12} {merged_str:<10} {remote_str:<10}")

        print()

    def delete_branches(self, branches: List[BranchInfo]) -> Dict[str, int]:
        """Delete branches locally and optionally remotely."""
        stats = {"local_deleted": 0, "local_failed": 0, "remote_deleted": 0, "remote_failed": 0}

        for branch in branches:
            # Delete local branch
            if self.args.dry_run:
                log_info(f"[DRY-RUN] Would delete local: {branch.name}")
                stats["local_deleted"] += 1
            else:
                result = run_command(["git", "branch", "-d", branch.name], check=False)
                if result.returncode == 0:
                    log_success(f"Deleted local: {branch.name}")
                    stats["local_deleted"] += 1
                else:
                    # Try force delete if not merged
                    if not branch.is_merged:
                        result = run_command(["git", "branch", "-D", branch.name], check=False)
                        if result.returncode == 0:
                            log_warning(f"Force deleted local: {branch.name}")
                            stats["local_deleted"] += 1
                        else:
                            log_error(f"Failed to delete: {branch.name}")
                            stats["local_failed"] += 1
                    else:
                        log_error(f"Failed to delete: {branch.name}")
                        stats["local_failed"] += 1

            # Delete remote branch if requested
            if self.args.include_remote and branch.remote_exists:
                if self.args.dry_run:
                    log_info(f"[DRY-RUN] Would delete remote: {branch.name}")
                    stats["remote_deleted"] += 1
                else:
                    result = run_command([
                        "git", "push", "origin", "--delete", branch.name
                    ], check=False)

                    if result.returncode == 0:
                        log_success(f"Deleted remote: {branch.name}")
                        stats["remote_deleted"] += 1
                    else:
                        log_error(f"Failed to delete remote: {branch.name}")
                        stats["remote_failed"] += 1

        return stats

    def run(self) -> int:
        """Execute the cleanup process."""
        log_info("Git Flow Branch Cleanup")
        log_info(f"Main branch: {self.main_branch}")
        log_info(f"Develop branch: {self.develop_branch}")
        log_info(f"Current branch: {self.current_branch}")
        print()

        # Get branches
        log_info(f"Scanning {self.args.type} branches...")
        branches = self.get_local_branches(self.args.type)
        log_info(f"Found {len(branches)} {self.args.type} branches")

        # Filter branches
        to_delete = self.filter_branches(branches)

        if not to_delete:
            log_success("No branches to clean up!")
            return 0

        # Display branches
        self.display_branches(to_delete)

        # Confirm deletion
        if not self.args.force and not self.args.dry_run:
            response = input(f"Delete {len(to_delete)} branches? [y/N]: ")
            if response.lower() != 'y':
                log_warning("Cleanup cancelled")
                return 0

        # Delete branches
        stats = self.delete_branches(to_delete)

        # Show summary
        print()
        log_success("Cleanup complete!")
        print(f"\nSummary:")
        print(f"  Local deleted:   {stats['local_deleted']}")
        print(f"  Local failed:    {stats['local_failed']}")

        if self.args.include_remote:
            print(f"  Remote deleted:  {stats['remote_deleted']}")
            print(f"  Remote failed:   {stats['remote_failed']}")

        if self.args.dry_run:
            print(f"\n{Colors.YELLOW}DRY-RUN mode: No changes were made{Colors.NC}")

        return 0

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Clean up merged and stale Git Flow branches",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--type",
        choices=["feature", "release", "hotfix", "all"],
        default="all",
        help="Branch type to clean (default: all)"
    )
    parser.add_argument(
        "--merged-only",
        action="store_true",
        help="Only delete branches merged to develop/main"
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=30,
        help="Consider branches stale after N days (default: 30)"
    )
    parser.add_argument(
        "--include-remote",
        action="store_true",
        help="Also delete remote branches"
    )
    parser.add_argument(
        "--exclude",
        help="Exclude branches matching regex pattern"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompts"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without deleting"
    )

    args = parser.parse_args()

    # Check if in git repository
    try:
        run_command(["git", "rev-parse", "--git-dir"])
    except subprocess.CalledProcessError:
        log_error("Not a git repository")
        return 2

    try:
        cleaner = BranchCleaner(args)
        return cleaner.run()
    except KeyboardInterrupt:
        log_warning("\nCleanup cancelled by user")
        return 1
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        return 2

if __name__ == "__main__":
    sys.exit(main())
