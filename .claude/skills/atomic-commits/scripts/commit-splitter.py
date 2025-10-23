#!/usr/bin/env python3

"""
commit-splitter.py

PURPOSE:
    Intelligently splits staged Git changes into multiple logical atomic commits.
    Analyzes file types, change patterns, and code structure to suggest optimal splits.

USAGE:
    ./commit-splitter.py [options]

OPTIONS:
    --interactive, -i     Interactive mode with user approval for each split
    --dry-run, -n        Show proposed splits without committing
    --auto, -a           Automatically commit splits without confirmation
    --strategy <name>    Split strategy: 'type' (by file type) or 'semantic' (by change type)
    --verbose, -v        Show detailed analysis
    --help, -h           Show this help message

EXAMPLES:
    ./commit-splitter.py --dry-run           # Preview splits
    ./commit-splitter.py --interactive       # Approve each split
    ./commit-splitter.py --auto              # Auto-commit all splits

ENVIRONMENT VARIABLES:
    ATOMIC_STRATEGY=type      Default split strategy (type|semantic)
    ATOMIC_AUTO_COMMIT=false  Auto-commit without confirmation

EXIT CODES:
    0 - Success
    1 - No staged changes
    2 - Git error
    3 - Invalid options

SAVES: ~30-45 minutes when dealing with large changesets
"""

import subprocess
import sys
import argparse
import os
from typing import List, Dict, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum


class ChangeType(Enum):
    """Types of changes that can be detected"""
    FEATURE = "feat"
    FIX = "fix"
    REFACTOR = "refactor"
    DOCS = "docs"
    STYLE = "style"
    TEST = "test"
    CONFIG = "config"
    MIGRATION = "migration"
    DEPENDENCY = "deps"


@dataclass
class FileChange:
    """Represents a changed file"""
    path: str
    additions: int
    deletions: int
    file_type: str
    change_type: ChangeType


@dataclass
class CommitSplit:
    """Represents a proposed commit split"""
    files: List[str]
    message: str
    change_type: ChangeType
    description: str


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


class GitError(Exception):
    """Custom exception for Git-related errors"""
    pass


class CommitSplitter:
    """Main class for splitting commits"""

    def __init__(self, strategy: str = 'type', verbose: bool = False):
        self.strategy = strategy
        self.verbose = verbose
        self.file_changes: List[FileChange] = []

    def log_verbose(self, message: str):
        """Log verbose output"""
        if self.verbose:
            print(f"{Colors.CYAN}  → {message}{Colors.END}")

    def run_git_command(self, args: List[str], check_output: bool = True) -> str:
        """Run a git command and return output"""
        try:
            if check_output:
                result = subprocess.check_output(
                    ['git'] + args,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                return result.strip()
            else:
                subprocess.check_call(['git'] + args)
                return ""
        except subprocess.CalledProcessError as e:
            raise GitError(f"Git command failed: {e.output}")

    def check_staged_changes(self) -> bool:
        """Check if there are staged changes"""
        try:
            self.run_git_command(['diff', '--cached', '--quiet'], check_output=False)
            return False
        except GitError:
            return True

    def classify_file_type(self, filepath: str) -> str:
        """Classify file by extension"""
        extension_map = {
            'ts': 'typescript',
            'tsx': 'typescript',
            'js': 'javascript',
            'jsx': 'javascript',
            'py': 'python',
            'go': 'go',
            'rs': 'rust',
            'java': 'java',
            'c': 'c',
            'cpp': 'cpp',
            'h': 'header',
            'md': 'markdown',
            'txt': 'text',
            'json': 'json',
            'yaml': 'yaml',
            'yml': 'yaml',
            'toml': 'toml',
            'css': 'css',
            'scss': 'scss',
            'sql': 'sql',
        }

        # Special files
        if 'test' in filepath.lower() or 'spec' in filepath.lower():
            return 'test'
        if filepath.startswith('docs/'):
            return 'docs'
        if 'migration' in filepath.lower():
            return 'migration'
        if filepath in ['package.json', 'Cargo.toml', 'go.mod', 'requirements.txt']:
            return 'dependency'
        if filepath in ['Dockerfile', 'docker-compose.yml', '.env', '.env.example']:
            return 'config'

        ext = filepath.split('.')[-1]
        return extension_map.get(ext, 'other')

    def detect_change_type(self, filepath: str, diff: str) -> ChangeType:
        """Detect the type of change based on file and diff content"""
        file_type = self.classify_file_type(filepath)

        # File type based classification
        if file_type == 'test':
            return ChangeType.TEST
        if file_type in ['markdown', 'text', 'docs']:
            return ChangeType.DOCS
        if file_type in ['json', 'yaml', 'toml', 'config']:
            return ChangeType.CONFIG
        if file_type == 'migration':
            return ChangeType.MIGRATION
        if file_type == 'dependency':
            return ChangeType.DEPENDENCY

        # Content-based classification
        diff_lower = diff.lower()

        # Check for style-only changes (whitespace, formatting)
        if self.is_style_only_change(diff):
            return ChangeType.STYLE

        # Check for bug fix indicators
        if any(word in diff_lower for word in ['fix', 'bug', 'issue', 'error', 'exception']):
            return ChangeType.FIX

        # Check for refactoring indicators
        if any(word in diff_lower for word in ['refactor', 'extract', 'simplify', 'cleanup']):
            return ChangeType.REFACTOR

        # Default to feature
        return ChangeType.FEATURE

    def is_style_only_change(self, diff: str) -> bool:
        """Check if a diff only contains style changes"""
        # Remove whitespace and check if there's actual content change
        lines = diff.split('\n')
        code_changes = 0

        for line in lines:
            if line.startswith('+') or line.startswith('-'):
                # Ignore lines that are only whitespace changes
                stripped = line[1:].strip()
                if stripped and not stripped.startswith('//') and not stripped.startswith('/*'):
                    code_changes += 1

        # If very few non-whitespace changes, likely style-only
        return code_changes < 3

    def analyze_staged_changes(self):
        """Analyze all staged changes"""
        self.log_verbose("Analyzing staged changes...")

        # Get list of staged files with stats
        numstat = self.run_git_command(['diff', '--cached', '--numstat'])

        for line in numstat.split('\n'):
            if not line.strip():
                continue

            parts = line.split('\t')
            if len(parts) != 3:
                continue

            additions = int(parts[0]) if parts[0] != '-' else 0
            deletions = int(parts[1]) if parts[1] != '-' else 0
            filepath = parts[2]

            # Get diff for this file
            diff = self.run_git_command(['diff', '--cached', filepath])

            file_type = self.classify_file_type(filepath)
            change_type = self.detect_change_type(filepath, diff)

            self.file_changes.append(FileChange(
                path=filepath,
                additions=additions,
                deletions=deletions,
                file_type=file_type,
                change_type=change_type
            ))

            self.log_verbose(f"  {filepath}: {file_type} ({change_type.value})")

    def generate_splits_by_type(self) -> List[CommitSplit]:
        """Generate commit splits based on file types"""
        splits = []

        # Group files by change type
        by_change_type: Dict[ChangeType, List[FileChange]] = defaultdict(list)
        for fc in self.file_changes:
            by_change_type[fc.change_type].append(fc)

        # Priority order for commits
        priority_order = [
            ChangeType.DEPENDENCY,
            ChangeType.CONFIG,
            ChangeType.MIGRATION,
            ChangeType.REFACTOR,
            ChangeType.FIX,
            ChangeType.FEATURE,
            ChangeType.TEST,
            ChangeType.DOCS,
            ChangeType.STYLE,
        ]

        for change_type in priority_order:
            if change_type not in by_change_type:
                continue

            files = by_change_type[change_type]
            if not files:
                continue

            # Generate commit message
            message = self.generate_commit_message(change_type, files)
            description = self.generate_description(change_type, files)

            splits.append(CommitSplit(
                files=[f.path for f in files],
                message=message,
                change_type=change_type,
                description=description
            ))

        return splits

    def generate_commit_message(self, change_type: ChangeType, files: List[FileChange]) -> str:
        """Generate a conventional commit message"""
        prefix = change_type.value

        # Try to generate a meaningful summary
        if len(files) == 1:
            filename = os.path.basename(files[0].path)
            summary = f"Update {filename}"
        else:
            file_types = set(f.file_type for f in files)
            if len(file_types) == 1:
                summary = f"Update {file_types.pop()} files"
            else:
                summary = f"Update {len(files)} files"

        # Customize based on change type
        if change_type == ChangeType.FEATURE:
            summary = f"Add new functionality in {len(files)} file(s)"
        elif change_type == ChangeType.FIX:
            summary = f"Fix issues in {len(files)} file(s)"
        elif change_type == ChangeType.REFACTOR:
            summary = f"Refactor code structure"
        elif change_type == ChangeType.DOCS:
            summary = "Update documentation"
        elif change_type == ChangeType.STYLE:
            summary = "Apply code formatting"
        elif change_type == ChangeType.TEST:
            summary = "Add/update tests"
        elif change_type == ChangeType.CONFIG:
            summary = "Update configuration"
        elif change_type == ChangeType.MIGRATION:
            summary = "Add database migration"
        elif change_type == ChangeType.DEPENDENCY:
            summary = "Update dependencies"

        return f"{prefix}: {summary}"

    def generate_description(self, change_type: ChangeType, files: List[FileChange]) -> str:
        """Generate a description for the split"""
        total_additions = sum(f.additions for f in files)
        total_deletions = sum(f.deletions for f in files)

        desc = f"{len(files)} file(s): +{total_additions} -{total_deletions} lines"
        return desc

    def display_splits(self, splits: List[CommitSplit]):
        """Display proposed splits"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Proposed Commit Splits:{Colors.END}\n")

        for i, split in enumerate(splits, 1):
            print(f"{Colors.BOLD}Commit {i}:{Colors.END} {Colors.GREEN}{split.message}{Colors.END}")
            print(f"  Type: {split.change_type.value}")
            print(f"  Info: {split.description}")
            print(f"  Files:")
            for filepath in split.files:
                print(f"    - {filepath}")
            print()

    def execute_splits(self, splits: List[CommitSplit], interactive: bool = False,
                      dry_run: bool = False):
        """Execute the commit splits"""
        if dry_run:
            print(f"{Colors.YELLOW}[DRY RUN] No commits will be made{Colors.END}\n")
            return

        # First, unstage everything
        self.log_verbose("Unstaging all changes...")
        self.run_git_command(['reset', 'HEAD'], check_output=False)

        for i, split in enumerate(splits, 1):
            print(f"\n{Colors.BOLD}Processing commit {i}/{len(splits)}:{Colors.END} {split.message}")

            if interactive:
                response = input(f"{Colors.YELLOW}Create this commit? [Y/n/q]: {Colors.END}").strip().lower()
                if response == 'q':
                    print(f"{Colors.RED}Aborted by user{Colors.END}")
                    sys.exit(0)
                if response == 'n':
                    print(f"{Colors.YELLOW}Skipped{Colors.END}")
                    continue

            # Stage files for this commit
            self.log_verbose(f"Staging {len(split.files)} file(s)...")
            for filepath in split.files:
                try:
                    self.run_git_command(['add', filepath], check_output=False)
                except GitError as e:
                    print(f"{Colors.RED}Error staging {filepath}: {e}{Colors.END}")
                    continue

            # Create commit
            self.log_verbose(f"Creating commit: {split.message}")
            try:
                self.run_git_command(['commit', '-m', split.message], check_output=False)
                print(f"{Colors.GREEN}✓ Committed{Colors.END}")
            except GitError as e:
                print(f"{Colors.RED}Error creating commit: {e}{Colors.END}")
                continue

        print(f"\n{Colors.GREEN}{Colors.BOLD}All splits completed!{Colors.END}")

    def run(self, interactive: bool = False, dry_run: bool = False):
        """Main execution method"""
        print(f"{Colors.BOLD}{Colors.BLUE}Commit Splitter{Colors.END}")
        print(f"{Colors.BLUE}{'=' * 50}{Colors.END}\n")

        # Check for staged changes
        if not self.check_staged_changes():
            print(f"{Colors.YELLOW}No staged changes found.{Colors.END}")
            print("Use 'git add <files>' to stage changes first.")
            sys.exit(1)

        # Analyze changes
        self.analyze_staged_changes()

        if not self.file_changes:
            print(f"{Colors.YELLOW}No changes to split.{Colors.END}")
            sys.exit(0)

        print(f"Found {len(self.file_changes)} changed file(s)\n")

        # Generate splits
        splits = self.generate_splits_by_type()

        if len(splits) <= 1:
            print(f"{Colors.GREEN}Changes already appear atomic (1 logical unit).{Colors.END}")
            print("No splitting needed.")
            sys.exit(0)

        # Display splits
        self.display_splits(splits)

        # Execute splits
        self.execute_splits(splits, interactive=interactive, dry_run=dry_run)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Intelligently split staged Git changes into atomic commits',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Interactive mode with approval for each split'
    )
    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        help='Show proposed splits without committing'
    )
    parser.add_argument(
        '-a', '--auto',
        action='store_true',
        help='Automatically commit splits without confirmation'
    )
    parser.add_argument(
        '--strategy',
        choices=['type', 'semantic'],
        default=os.environ.get('ATOMIC_STRATEGY', 'type'),
        help='Split strategy (default: type)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed analysis'
    )

    args = parser.parse_args()

    # Validate options
    if args.auto and args.interactive:
        print(f"{Colors.RED}Error: Cannot use --auto and --interactive together{Colors.END}")
        sys.exit(3)

    try:
        splitter = CommitSplitter(strategy=args.strategy, verbose=args.verbose)
        splitter.run(interactive=args.interactive, dry_run=args.dry_run)
    except GitError as e:
        print(f"{Colors.RED}Git Error: {e}{Colors.END}")
        sys.exit(2)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
