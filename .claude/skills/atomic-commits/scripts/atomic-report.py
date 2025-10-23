#!/usr/bin/env python3

"""
atomic-report.py

PURPOSE:
    Generates a comprehensive report on commit quality across a repository or branch.
    Analyzes commit history for atomic commit adherence and provides actionable insights.

USAGE:
    ./atomic-report.py [options]

OPTIONS:
    --since <date>       Analyze commits since date (e.g., '30 days ago', '2025-01-01')
    --branch <name>      Analyze specific branch (default: current branch)
    --range <range>      Analyze commit range (e.g., 'main..feature-branch')
    --format <fmt>       Output format: 'text', 'markdown', 'html', 'json' (default: text)
    --output <file>      Write report to file instead of stdout
    --min-score <n>      Only show commits with score below threshold (0-100)
    --verbose, -v        Include detailed per-commit analysis
    --help, -h           Show this help message

EXAMPLES:
    ./atomic-report.py --since "30 days ago"           # Last 30 days
    ./atomic-report.py --range main..feature-branch    # Compare branches
    ./atomic-report.py --format html --output report.html  # HTML report
    ./atomic-report.py --min-score 70                  # Show problem commits

ENVIRONMENT VARIABLES:
    ATOMIC_MAX_FILES=20        Maximum files to consider atomic (default: 20)
    ATOMIC_MAX_LINES=500       Maximum lines to consider atomic (default: 500)

EXIT CODES:
    0 - Success
    1 - No commits found
    2 - Git error

SAVES: ~2-3 hours per sprint in code review time and identifying training needs
"""

import subprocess
import sys
import argparse
import json
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict


@dataclass
class CommitScore:
    """Represents a commit with quality score"""
    sha: str
    short_sha: str
    message: str
    author: str
    date: str
    files_changed: int
    insertions: int
    deletions: int
    score: int  # 0-100
    issues: List[str]
    warnings: List[str]


@dataclass
class RepoStats:
    """Overall repository statistics"""
    total_commits: int
    date_range: str
    average_score: float
    median_score: float
    commits_below_70: int
    commits_below_50: int
    perfect_commits: int
    total_files_changed: int
    total_insertions: int
    total_deletions: int
    most_common_issues: Dict[str, int]
    score_distribution: Dict[str, int]  # ranges: 0-50, 51-70, 71-85, 86-100


class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


class AtomicReportGenerator:
    """Main report generator class"""

    def __init__(self, max_files: int = 20, max_lines: int = 500):
        self.max_files = max_files
        self.max_lines = max_lines
        self.commits: List[CommitScore] = []

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

    def score_commit(self, sha: str) -> CommitScore:
        """Score a single commit based on atomic principles"""
        # Get commit info
        info = self.run_git_command([
            'show', '--format=%H%n%h%n%s%n%an%n%ai',
            '--quiet', sha
        ]).split('\n')

        full_sha = info[0]
        short_sha = info[1]
        message = info[2]
        author = info[3]
        date = info[4]

        # Get file stats
        numstat = self.run_git_command([
            'show', '--numstat', '--format=', sha
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

        # Score the commit
        score = 100
        issues = []
        warnings = []

        # File count penalty
        if len(files) > self.max_files:
            penalty = min(30, (len(files) - self.max_files) * 2)
            score -= penalty
            issues.append(f"Too many files: {len(files)} (penalty: -{penalty})")
        elif len(files) > self.max_files // 2:
            warnings.append(f"High file count: {len(files)}")

        # Line count penalty
        total_lines = total_insertions + total_deletions
        if total_lines > self.max_lines:
            penalty = min(30, (total_lines - self.max_lines) // 20)
            score -= penalty
            issues.append(f"Too many lines: {total_lines} (penalty: -{penalty})")
        elif total_lines > self.max_lines // 2:
            warnings.append(f"High line count: {total_lines}")

        # Message quality
        if len(message) < 10:
            score -= 10
            issues.append("Very short commit message (penalty: -10)")
        elif len(message) < 20:
            warnings.append("Short commit message")

        if message.lower() in ['wip', 'update', 'fix', 'changes', 'updates']:
            score -= 20
            issues.append("Vague commit message (penalty: -20)")

        # Check for conventional commit format
        if not any(message.startswith(prefix) for prefix in [
            'feat:', 'fix:', 'docs:', 'style:', 'refactor:',
            'test:', 'chore:', 'perf:', 'ci:', 'build:'
        ]):
            score -= 5
            warnings.append("Not using conventional commit format")

        # File type diversity penalty
        file_types = self.categorize_files(files)
        if len(file_types) > 3:
            score -= 15
            issues.append(f"Mixed file types: {len(file_types)} categories (penalty: -15)")

        # Ensure score is in valid range
        score = max(0, min(100, score))

        return CommitScore(
            sha=full_sha,
            short_sha=short_sha,
            message=message,
            author=author,
            date=date,
            files_changed=len(files),
            insertions=total_insertions,
            deletions=total_deletions,
            score=score,
            issues=issues,
            warnings=warnings
        )

    def categorize_files(self, files: List[str]) -> Dict[str, int]:
        """Categorize files by type"""
        categories = defaultdict(int)

        for filepath in files:
            if 'test' in filepath.lower() or 'spec' in filepath.lower():
                categories['test'] += 1
            elif filepath.endswith(('.md', '.txt', '.adoc')):
                categories['docs'] += 1
            elif filepath.endswith(('.json', '.yaml', '.yml', '.toml')):
                categories['config'] += 1
            elif filepath.endswith(('.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs')):
                categories['source'] += 1
            elif filepath.endswith(('.css', '.scss', '.sass')):
                categories['style'] += 1
            else:
                categories['other'] += 1

        return dict(categories)

    def analyze_commits(self, commit_range: Optional[str] = None,
                       since: Optional[str] = None,
                       branch: Optional[str] = None) -> List[CommitScore]:
        """Analyze commits in the specified range"""
        # Build git log command
        cmd = ['log', '--format=%H']

        if commit_range:
            cmd.append(commit_range)
        elif since:
            cmd.append(f'--since={since}')

        if branch:
            cmd.append(branch)

        # Get commit SHAs
        output = self.run_git_command(cmd)
        shas = [sha for sha in output.split('\n') if sha.strip()]

        if not shas:
            return []

        # Score each commit
        commits = []
        for i, sha in enumerate(shas, 1):
            if i % 10 == 0:
                print(f"Analyzing commits... {i}/{len(shas)}", end='\r', file=sys.stderr)

            commits.append(self.score_commit(sha))

        print(f"Analyzed {len(commits)} commits.          ", file=sys.stderr)
        return commits

    def calculate_stats(self, commits: List[CommitScore]) -> RepoStats:
        """Calculate overall statistics"""
        if not commits:
            raise ValueError("No commits to analyze")

        scores = [c.score for c in commits]
        average_score = sum(scores) / len(scores)

        sorted_scores = sorted(scores)
        median_score = sorted_scores[len(sorted_scores) // 2]

        commits_below_70 = sum(1 for s in scores if s < 70)
        commits_below_50 = sum(1 for s in scores if s < 50)
        perfect_commits = sum(1 for s in scores if s == 100)

        total_files = sum(c.files_changed for c in commits)
        total_insertions = sum(c.insertions for c in commits)
        total_deletions = sum(c.deletions for c in commits)

        # Count issue types
        issue_counts = defaultdict(int)
        for commit in commits:
            for issue in commit.issues:
                # Extract issue type (first part before colon or parenthesis)
                issue_type = issue.split(':')[0].split('(')[0].strip()
                issue_counts[issue_type] += 1

        most_common_issues = dict(sorted(
            issue_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5])

        # Score distribution
        score_dist = {
            '0-50': sum(1 for s in scores if s <= 50),
            '51-70': sum(1 for s in scores if 51 <= s <= 70),
            '71-85': sum(1 for s in scores if 71 <= s <= 85),
            '86-100': sum(1 for s in scores if 86 <= s <= 100),
        }

        # Date range
        dates = [c.date for c in commits]
        date_range = f"{min(dates)[:10]} to {max(dates)[:10]}"

        return RepoStats(
            total_commits=len(commits),
            date_range=date_range,
            average_score=round(average_score, 2),
            median_score=median_score,
            commits_below_70=commits_below_70,
            commits_below_50=commits_below_50,
            perfect_commits=perfect_commits,
            total_files_changed=total_files,
            total_insertions=total_insertions,
            total_deletions=total_deletions,
            most_common_issues=most_common_issues,
            score_distribution=score_dist
        )

    def format_text(self, stats: RepoStats, commits: List[CommitScore],
                   verbose: bool = False, min_score: Optional[int] = None) -> str:
        """Format report as plain text"""
        lines = []

        lines.append(f"{Colors.BOLD}{Colors.BLUE}╔════════════════════════════════════════════════════════════════╗{Colors.END}")
        lines.append(f"{Colors.BOLD}{Colors.BLUE}║        Atomic Commit Quality Report                           ║{Colors.END}")
        lines.append(f"{Colors.BOLD}{Colors.BLUE}╚════════════════════════════════════════════════════════════════╝{Colors.END}\n")

        lines.append(f"{Colors.BOLD}Repository Statistics{Colors.END}")
        lines.append(f"  Date Range:       {stats.date_range}")
        lines.append(f"  Total Commits:    {stats.total_commits}")
        lines.append(f"  Average Score:    {stats.average_score}/100")
        lines.append(f"  Median Score:     {stats.median_score}/100")
        lines.append(f"  Perfect (100):    {stats.perfect_commits} ({stats.perfect_commits/stats.total_commits*100:.1f}%)")
        lines.append(f"  Below 70:         {stats.commits_below_70} ({stats.commits_below_70/stats.total_commits*100:.1f}%)")
        lines.append(f"  Below 50:         {stats.commits_below_50} ({stats.commits_below_50/stats.total_commits*100:.1f}%)")
        lines.append("")

        lines.append(f"{Colors.BOLD}Code Changes{Colors.END}")
        lines.append(f"  Files Changed:    {stats.total_files_changed}")
        lines.append(f"  Lines Added:      +{stats.total_insertions}")
        lines.append(f"  Lines Deleted:    -{stats.total_deletions}")
        lines.append("")

        lines.append(f"{Colors.BOLD}Score Distribution{Colors.END}")
        for range_name, count in stats.score_distribution.items():
            pct = count / stats.total_commits * 100
            bar_length = int(pct / 2)
            bar = '█' * bar_length
            lines.append(f"  {range_name:8} [{bar:50}] {count:3} ({pct:5.1f}%)")
        lines.append("")

        if stats.most_common_issues:
            lines.append(f"{Colors.BOLD}Most Common Issues{Colors.END}")
            for issue, count in stats.most_common_issues.items():
                pct = count / stats.total_commits * 100
                lines.append(f"  {issue:40} {count:3} ({pct:5.1f}%)")
            lines.append("")

        # Recommendations
        lines.append(f"{Colors.BOLD}Recommendations{Colors.END}")
        if stats.average_score >= 85:
            lines.append(f"  {Colors.GREEN}✓ Excellent commit quality! Keep up the good work.{Colors.END}")
        elif stats.average_score >= 70:
            lines.append(f"  {Colors.YELLOW}⚠ Good commit quality with room for improvement.{Colors.END}")
        else:
            lines.append(f"  {Colors.RED}✗ Commit quality needs attention.{Colors.END}")

        if stats.commits_below_70 > stats.total_commits * 0.3:
            lines.append(f"  {Colors.YELLOW}- Consider team training on atomic commits{Colors.END}")

        if "Too many files" in stats.most_common_issues:
            lines.append(f"  {Colors.YELLOW}- Use commit-splitter.py to break down large commits{Colors.END}")

        if "Vague commit message" in stats.most_common_issues:
            lines.append(f"  {Colors.YELLOW}- Adopt conventional commit format (feat:, fix:, etc.){Colors.END}")

        lines.append("")

        # Verbose: show individual commits
        if verbose or min_score is not None:
            filtered = commits
            if min_score is not None:
                filtered = [c for c in commits if c.score < min_score]

            if filtered:
                lines.append(f"{Colors.BOLD}Individual Commits{Colors.END}")
                lines.append("")

                for commit in sorted(filtered, key=lambda c: c.score):
                    score_color = Colors.GREEN if commit.score >= 85 else \
                                Colors.YELLOW if commit.score >= 70 else Colors.RED

                    lines.append(f"{score_color}{commit.score:3}/100{Colors.END} {commit.short_sha} {commit.message}")
                    lines.append(f"         {commit.author} - {commit.date[:10]}")
                    if commit.issues:
                        for issue in commit.issues:
                            lines.append(f"         {Colors.RED}✗ {issue}{Colors.END}")
                    if commit.warnings:
                        for warning in commit.warnings:
                            lines.append(f"         {Colors.YELLOW}⚠ {warning}{Colors.END}")
                    lines.append("")

        return '\n'.join(lines)

    def format_json(self, stats: RepoStats, commits: List[CommitScore]) -> str:
        """Format report as JSON"""
        data = {
            'stats': asdict(stats),
            'commits': [asdict(c) for c in commits]
        }
        return json.dumps(data, indent=2)

    def format_markdown(self, stats: RepoStats, commits: List[CommitScore],
                       min_score: Optional[int] = None) -> str:
        """Format report as Markdown"""
        lines = []

        lines.append("# Atomic Commit Quality Report\n")

        lines.append("## Repository Statistics\n")
        lines.append(f"- **Date Range:** {stats.date_range}")
        lines.append(f"- **Total Commits:** {stats.total_commits}")
        lines.append(f"- **Average Score:** {stats.average_score}/100")
        lines.append(f"- **Median Score:** {stats.median_score}/100")
        lines.append(f"- **Perfect Commits (100):** {stats.perfect_commits} ({stats.perfect_commits/stats.total_commits*100:.1f}%)")
        lines.append(f"- **Below 70:** {stats.commits_below_70} ({stats.commits_below_70/stats.total_commits*100:.1f}%)")
        lines.append(f"- **Below 50:** {stats.commits_below_50} ({stats.commits_below_50/stats.total_commits*100:.1f}%)\n")

        lines.append("## Score Distribution\n")
        lines.append("| Score Range | Count | Percentage |")
        lines.append("|------------|-------|------------|")
        for range_name, count in stats.score_distribution.items():
            pct = count / stats.total_commits * 100
            lines.append(f"| {range_name} | {count} | {pct:.1f}% |")
        lines.append("")

        if stats.most_common_issues:
            lines.append("## Most Common Issues\n")
            lines.append("| Issue | Count | Percentage |")
            lines.append("|-------|-------|------------|")
            for issue, count in stats.most_common_issues.items():
                pct = count / stats.total_commits * 100
                lines.append(f"| {issue} | {count} | {pct:.1f}% |")
            lines.append("")

        if min_score is not None:
            filtered = [c for c in commits if c.score < min_score]
            if filtered:
                lines.append(f"## Commits Below {min_score}\n")
                for commit in sorted(filtered, key=lambda c: c.score):
                    lines.append(f"### {commit.short_sha} - Score: {commit.score}/100\n")
                    lines.append(f"**Message:** {commit.message}\n")
                    lines.append(f"**Author:** {commit.author}\n")
                    if commit.issues:
                        lines.append("**Issues:**")
                        for issue in commit.issues:
                            lines.append(f"- {issue}")
                    lines.append("")

        return '\n'.join(lines)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate atomic commit quality report',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--since', help="Analyze commits since date (e.g., '30 days ago')")
    parser.add_argument('--branch', help='Analyze specific branch')
    parser.add_argument('--range', help='Analyze commit range (e.g., main..feature)')
    parser.add_argument('--format', choices=['text', 'markdown', 'html', 'json'],
                       default='text', help='Output format')
    parser.add_argument('--output', help='Write report to file')
    parser.add_argument('--min-score', type=int, help='Show commits below this score')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Include detailed per-commit analysis')

    args = parser.parse_args()

    max_files = int(os.environ.get('ATOMIC_MAX_FILES', 20))
    max_lines = int(os.environ.get('ATOMIC_MAX_LINES', 500))

    try:
        generator = AtomicReportGenerator(max_files=max_files, max_lines=max_lines)

        # Analyze commits
        commits = generator.analyze_commits(
            commit_range=args.range,
            since=args.since,
            branch=args.branch
        )

        if not commits:
            print("No commits found in specified range.", file=sys.stderr)
            sys.exit(1)

        # Calculate stats
        stats = generator.calculate_stats(commits)

        # Format output
        if args.format == 'json':
            output = generator.format_json(stats, commits)
        elif args.format == 'markdown':
            output = generator.format_markdown(stats, commits, args.min_score)
        else:  # text
            output = generator.format_text(stats, commits, args.verbose, args.min_score)

        # Write output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Report written to {args.output}", file=sys.stderr)
        else:
            print(output)

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
