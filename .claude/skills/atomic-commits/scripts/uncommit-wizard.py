#!/usr/bin/env python3

"""
uncommit-wizard.py

PURPOSE:
    Interactive tool to split existing commits that should have been atomic.
    Helps clean up commit history before creating pull requests.

USAGE:
    ./uncommit-wizard.py [options]

OPTIONS:
    --count <n>          Number of recent commits to analyze (default: 5)
    --commit <sha>       Analyze specific commit by SHA
    --auto-detect        Automatically detect non-atomic commits
    --no-safety-check    Skip safety checks (dangerous!)
    --help, -h           Show this help message

EXAMPLES:
    ./uncommit-wizard.py                      # Analyze last 5 commits
    ./uncommit-wizard.py --count 10           # Analyze last 10 commits
    ./uncommit-wizard.py --commit abc123      # Analyze specific commit
    ./uncommit-wizard.py --auto-detect        # Find problematic commits

ENVIRONMENT VARIABLES:
    ATOMIC_MAX_FILES=20        Maximum files to consider atomic (default: 20)
    ATOMIC_MAX_LINES=500       Maximum lines to consider atomic (default: 500)

EXIT CODES:
    0 - Success
    1 - No commits to process
    2 - Git error or unsafe operation
    3 - Invalid options

SAVES: ~20-30 minutes when cleaning up history before pull requests
"""

import subprocess
import sys
import argparse
import os
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CommitInfo:
    """Represents a Git commit"""
    sha: str
    short_sha: str
    message: str
    author: str
    date: str
    files_changed: int
    insertions: int
    deletions: int
    file_list: List[str]
    is_atomic: bool
    issues: List[str]


class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class UncommitWizard:
    """Main class for uncommit wizard"""

    def __init__(self, max_files: int = 20, max_lines: int = 500):
        self.max_files = max_files
        self.max_lines = max_lines

    def run_git_command(self, args: List[str]) -> str:
        """Run a git command and return output"""
        try:
            result = subprocess.check_output(
                ['git'] + args,
                stderr=subprocess.STDOUT,
                text=True
            )
            return result.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"Git command failed: {e.output}")

    def check_repo_safety(self) -> Tuple[bool, str]:
        """Check if it's safe to rewrite history"""
        # Check if on a branch
        try:
            branch = self.run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'])
        except:
            return False, "Not on a valid branch"

        if branch in ['main', 'master', 'develop', 'production']:
            return False, f"Cannot rewrite history on protected branch: {branch}"

        # Check if there are unpushed commits
        try:
            unpushed = self.run_git_command(['log', '@{u}..HEAD', '--oneline'])
            if not unpushed:
                return False, "No unpushed commits. Already pushed to remote - rewriting history is unsafe!"
        except:
            # No upstream, which is fine for local branches
            pass

        # Check for uncommitted changes
        try:
            status = self.run_git_command(['status', '--porcelain'])
            if status:
                return False, "You have uncommitted changes. Commit or stash them first."
        except:
            pass

        return True, "Safe to proceed"

    def get_commit_info(self, commit_sha: str = 'HEAD') -> CommitInfo:
        """Get detailed information about a commit"""
        # Get basic info
        info = self.run_git_command([
            'show', '--format=%H%n%h%n%s%n%an%n%ar',
            '--quiet', commit_sha
        ]).split('\n')

        sha = info[0]
        short_sha = info[1]
        message = info[2]
        author = info[3]
        date = info[4]

        # Get file stats
        numstat = self.run_git_command([
            'show', '--numstat', '--format=', commit_sha
        ])

        files = []
        total_insertions = 0
        total_deletions = 0

        for line in numstat.split('\n'):
            if not line.strip():
                continue

            parts = line.split('\t')
            if len(parts) != 3:
                continue

            insertions = int(parts[0]) if parts[0] != '-' else 0
            deletions = int(parts[1]) if parts[1] != '-' else 0
            filepath = parts[2]

            files.append(filepath)
            total_insertions += insertions
            total_deletions += deletions

        # Analyze if commit is atomic
        is_atomic, issues = self.analyze_atomicity(
            len(files), total_insertions, total_deletions, files
        )

        return CommitInfo(
            sha=sha,
            short_sha=short_sha,
            message=message,
            author=author,
            date=date,
            files_changed=len(files),
            insertions=total_insertions,
            deletions=total_deletions,
            file_list=files,
            is_atomic=is_atomic,
            issues=issues
        )

    def analyze_atomicity(self, file_count: int, insertions: int,
                         deletions: int, files: List[str]) -> Tuple[bool, List[str]]:
        """Analyze if a commit is atomic"""
        issues = []
        total_lines = insertions + deletions

        # Check file count
        if file_count > self.max_files:
            issues.append(f"Too many files: {file_count} > {self.max_files}")

        # Check line count
        if total_lines > self.max_lines:
            issues.append(f"Too many lines: {total_lines} > {self.max_lines}")

        # Check for mixed file types
        file_types = set()
        for filepath in files:
            if 'test' in filepath.lower() or 'spec' in filepath.lower():
                file_types.add('test')
            elif filepath.endswith(('.md', '.txt')):
                file_types.add('docs')
            elif filepath.endswith(('.json', '.yaml', '.yml', '.toml')):
                file_types.add('config')
            elif filepath.endswith(('.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs')):
                file_types.add('source')
            elif filepath.endswith(('.css', '.scss', '.sass')):
                file_types.add('style')
            else:
                file_types.add('other')

        if len(file_types) > 3:
            issues.append(f"Mixed file types: {', '.join(file_types)}")

        is_atomic = len(issues) == 0
        return is_atomic, issues

    def display_commit(self, commit: CommitInfo, index: int = None):
        """Display commit information"""
        header = f"Commit {index}" if index is not None else "Commit"

        print(f"\n{Colors.BOLD}{Colors.BLUE}{header}:{Colors.END}")
        print(f"  SHA:     {Colors.YELLOW}{commit.short_sha}{Colors.END}")
        print(f"  Message: {commit.message}")
        print(f"  Author:  {commit.author}")
        print(f"  Date:    {commit.date}")
        print(f"  Files:   {commit.files_changed}")
        print(f"  Changes: +{commit.insertions} -{commit.deletions}")

        if commit.is_atomic:
            print(f"  Status:  {Colors.GREEN}✓ Appears atomic{Colors.END}")
        else:
            print(f"  Status:  {Colors.RED}✗ Non-atomic{Colors.END}")
            print(f"  Issues:")
            for issue in commit.issues:
                print(f"    - {Colors.RED}{issue}{Colors.END}")

        if commit.files_changed <= 10:
            print(f"  Files changed:")
            for filepath in commit.file_list:
                print(f"    - {filepath}")

    def get_recent_commits(self, count: int) -> List[CommitInfo]:
        """Get recent commits"""
        commits = []
        commit_shas = self.run_git_command([
            'log', f'-{count}', '--format=%H'
        ]).split('\n')

        for sha in commit_shas:
            if sha.strip():
                commits.append(self.get_commit_info(sha))

        return commits

    def interactive_split(self, commit: CommitInfo):
        """Interactively split a commit"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Splitting commit: {commit.short_sha}{Colors.END}")
        print(f"{Colors.YELLOW}This will use interactive rebase to split the commit.{Colors.END}\n")

        print("Steps:")
        print("1. Git will start interactive rebase")
        print("2. The commit will be marked for 'edit'")
        print("3. You'll be dropped into a shell to re-stage changes")
        print("4. Use 'git add -p' to stage changes in chunks")
        print("5. Create multiple atomic commits")
        print("6. Continue with 'git rebase --continue'\n")

        response = input(f"{Colors.YELLOW}Proceed with split? [y/N]: {Colors.END}").strip().lower()
        if response != 'y':
            print(f"{Colors.YELLOW}Cancelled{Colors.END}")
            return

        # Start interactive rebase
        print(f"\n{Colors.BLUE}Starting interactive rebase...{Colors.END}\n")

        # Set up git sequence editor to mark commit for edit
        commit_position = self.run_git_command(['rev-list', '--count', f'{commit.sha}..HEAD'])
        rebase_count = int(commit_position) + 1

        print(f"{Colors.CYAN}Instructions for splitting:{Colors.END}")
        print(f"1. The editor will open with the commit list")
        print(f"2. Change 'pick' to 'edit' for commit {commit.short_sha}")
        print(f"3. Save and close the editor")
        print(f"4. Git will pause at that commit")
        print(f"5. Run these commands:")
        print(f"   {Colors.GREEN}git reset HEAD^{Colors.END}          # Unstage the commit")
        print(f"   {Colors.GREEN}git add -p file.ts{Colors.END}      # Stage changes interactively")
        print(f"   {Colors.GREEN}git commit -m 'msg'{Colors.END}     # Commit first chunk")
        print(f"   {Colors.GREEN}git add -p file.ts{Colors.END}      # Stage more changes")
        print(f"   {Colors.GREEN}git commit -m 'msg'{Colors.END}     # Commit second chunk")
        print(f"   {Colors.GREEN}git rebase --continue{Colors.END}   # Finish rebase")
        print()

        input(f"{Colors.YELLOW}Press Enter to open rebase editor...{Colors.END}")

        try:
            # Launch interactive rebase
            subprocess.run(['git', 'rebase', '-i', f'HEAD~{rebase_count}'])
            print(f"\n{Colors.GREEN}Rebase completed!{Colors.END}")
        except:
            print(f"\n{Colors.RED}Rebase was cancelled or encountered an error{Colors.END}")
            print(f"If rebase is in progress, use:")
            print(f"  {Colors.GREEN}git rebase --continue{Colors.END}  # Continue after fixing")
            print(f"  {Colors.YELLOW}git rebase --abort{Colors.END}     # Cancel rebase")

    def auto_detect_mode(self, count: int):
        """Automatically detect non-atomic commits"""
        print(f"{Colors.BOLD}{Colors.BLUE}Auto-detecting non-atomic commits...{Colors.END}\n")

        commits = self.get_recent_commits(count)
        non_atomic = [c for c in commits if not c.is_atomic]

        if not non_atomic:
            print(f"{Colors.GREEN}✓ All recent commits appear atomic!{Colors.END}")
            return

        print(f"{Colors.YELLOW}Found {len(non_atomic)} non-atomic commit(s):{Colors.END}\n")

        for i, commit in enumerate(non_atomic, 1):
            self.display_commit(commit, i)

        print(f"\n{Colors.BOLD}What would you like to do?{Colors.END}")
        print("1. Split a specific commit")
        print("2. View all commits")
        print("3. Exit")

        choice = input(f"\n{Colors.YELLOW}Choice [1-3]: {Colors.END}").strip()

        if choice == '1':
            commit_num = input(f"{Colors.YELLOW}Enter commit number to split [1-{len(non_atomic)}]: {Colors.END}").strip()
            try:
                idx = int(commit_num) - 1
                if 0 <= idx < len(non_atomic):
                    self.interactive_split(non_atomic[idx])
                else:
                    print(f"{Colors.RED}Invalid commit number{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}Invalid input{Colors.END}")
        elif choice == '2':
            for i, commit in enumerate(commits, 1):
                self.display_commit(commit, i)
        else:
            print(f"{Colors.YELLOW}Exiting{Colors.END}")

    def run(self, count: int = 5, commit_sha: Optional[str] = None,
           auto_detect: bool = False, skip_safety: bool = False):
        """Main execution method"""
        print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}  Uncommit Wizard - Interactive Commit Splitter{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}\n")

        # Safety checks
        if not skip_safety:
            safe, message = self.check_repo_safety()
            if not safe:
                print(f"{Colors.RED}Safety check failed: {message}{Colors.END}")
                print(f"\nUse --no-safety-check to skip (not recommended)")
                sys.exit(2)
            print(f"{Colors.GREEN}✓ Safety check passed: {message}{Colors.END}\n")

        # Handle specific commit
        if commit_sha:
            commit = self.get_commit_info(commit_sha)
            self.display_commit(commit)

            if not commit.is_atomic:
                print(f"\n{Colors.YELLOW}This commit should be split.{Colors.END}")
                self.interactive_split(commit)
            else:
                print(f"\n{Colors.GREEN}This commit appears atomic. No action needed.{Colors.END}")
            return

        # Auto-detect mode
        if auto_detect:
            self.auto_detect_mode(count)
            return

        # Manual mode - show recent commits
        commits = self.get_recent_commits(count)

        print(f"Analyzing last {count} commit(s)...\n")

        for i, commit in enumerate(commits, 1):
            self.display_commit(commit, i)

        # Summary
        atomic_count = sum(1 for c in commits if c.is_atomic)
        non_atomic_count = len(commits) - atomic_count

        print(f"\n{Colors.BOLD}Summary:{Colors.END}")
        print(f"  {Colors.GREEN}✓ Atomic commits: {atomic_count}{Colors.END}")
        print(f"  {Colors.RED}✗ Non-atomic commits: {non_atomic_count}{Colors.END}")

        if non_atomic_count == 0:
            print(f"\n{Colors.GREEN}All commits look good!{Colors.END}")
            return

        # Offer to split
        print(f"\n{Colors.YELLOW}Would you like to split a commit?{Colors.END}")
        response = input(f"Enter commit number to split [1-{len(commits)}], or 'q' to quit: ").strip()

        if response.lower() == 'q':
            print(f"{Colors.YELLOW}Exiting{Colors.END}")
            return

        try:
            idx = int(response) - 1
            if 0 <= idx < len(commits):
                self.interactive_split(commits[idx])
            else:
                print(f"{Colors.RED}Invalid commit number{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}Invalid input{Colors.END}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Interactive tool to split non-atomic commits',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--count',
        type=int,
        default=5,
        help='Number of recent commits to analyze (default: 5)'
    )
    parser.add_argument(
        '--commit',
        help='Analyze specific commit by SHA'
    )
    parser.add_argument(
        '--auto-detect',
        action='store_true',
        help='Automatically detect non-atomic commits'
    )
    parser.add_argument(
        '--no-safety-check',
        action='store_true',
        help='Skip safety checks (dangerous!)'
    )

    args = parser.parse_args()

    max_files = int(os.environ.get('ATOMIC_MAX_FILES', 20))
    max_lines = int(os.environ.get('ATOMIC_MAX_LINES', 500))

    try:
        wizard = UncommitWizard(max_files=max_files, max_lines=max_lines)
        wizard.run(
            count=args.count,
            commit_sha=args.commit,
            auto_detect=args.auto_detect,
            skip_safety=args.no_safety_check
        )
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
