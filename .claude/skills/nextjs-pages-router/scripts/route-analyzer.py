#!/usr/bin/env python3
"""
Next.js Pages Router Route Analyzer

Analyzes your routing structure and suggests optimizations for build time,
performance, and proper fallback strategies.

Usage:
    python route-analyzer.py [OPTIONS]

Options:
    -d, --directory DIR       Pages directory to analyze (default: ./pages)
    -o, --output FILE         Output file for analysis report (default: stdout)
    --format FORMAT           Output format: text, json, html, markdown (default: text)
    --visualize               Generate route tree visualization
    --estimate-build-time     Estimate build time for SSG routes
    -v, --verbose             Show detailed analysis
    -h, --help                Show this help message

Examples:
    # Analyze pages directory with visualization
    python route-analyzer.py -d pages --visualize

    # Generate JSON report
    python route-analyzer.py --format json -o route-analysis.json

    # Estimate build time
    python route-analyzer.py --estimate-build-time

Author: DevDev AI
Version: 1.0.0
"""

import argparse
import os
import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@dataclass
class RouteInfo:
    """Information about a single route."""
    path: str
    file_path: str
    is_dynamic: bool = False
    is_catch_all: bool = False
    is_optional_catch_all: bool = False
    params: List[str] = field(default_factory=list)
    has_get_static_props: bool = False
    has_get_server_side_props: bool = False
    has_get_static_paths: bool = False
    has_api_route: bool = False
    fallback_mode: Optional[str] = None
    revalidate_time: Optional[int] = None
    estimated_paths: int = 0
    file_size_kb: float = 0.0
    line_count: int = 0

@dataclass
class AnalysisReport:
    """Complete analysis report."""
    total_routes: int = 0
    static_routes: int = 0
    dynamic_routes: int = 0
    ssr_routes: int = 0
    api_routes: int = 0
    isr_routes: int = 0
    routes: List[RouteInfo] = field(default_factory=list)
    issues: List[Dict] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    estimated_build_time_seconds: float = 0.0


def print_colored(text: str, color: str = Colors.ENDC):
    """Print colored text."""
    print(f"{color}{text}{Colors.ENDC}")


def analyze_file_content(file_path: Path) -> Dict:
    """Analyze the content of a page file."""
    try:
        content = file_path.read_text()
    except Exception as e:
        return {}

    analysis = {
        'has_get_static_props': 'getStaticProps' in content,
        'has_get_server_side_props': 'getServerSideProps' in content,
        'has_get_static_paths': 'getStaticPaths' in content,
        'fallback_mode': None,
        'revalidate_time': None,
        'estimated_paths': 0,
        'line_count': content.count('\n'),
        'file_size_kb': file_path.stat().st_size / 1024,
    }

    # Extract fallback mode
    fallback_match = re.search(r'fallback:\s*[\'"]?(\w+)[\'"]?', content)
    if fallback_match:
        analysis['fallback_mode'] = fallback_match.group(1)

    # Extract revalidate time
    revalidate_match = re.search(r'revalidate:\s*(\d+)', content)
    if revalidate_match:
        analysis['revalidate_time'] = int(revalidate_match.group(1))

    # Estimate number of paths from getStaticPaths
    if analysis['has_get_static_paths']:
        # Look for array/map operations that might indicate number of paths
        limit_match = re.search(r'limit[:\s=]+(\d+)', content, re.IGNORECASE)
        if limit_match:
            analysis['estimated_paths'] = int(limit_match.group(1))
        else:
            # Default estimate if we can't find a limit
            analysis['estimated_paths'] = 100

    return analysis


def get_route_path(file_path: Path, pages_dir: Path) -> str:
    """Convert file path to route path."""
    relative = file_path.relative_to(pages_dir)

    # Remove extension
    route = str(relative.with_suffix(''))

    # Handle index files
    if route.endswith('/index'):
        route = route[:-6] or '/'
    elif route == 'index':
        route = '/'

    # Convert [param] to :param for display
    route = re.sub(r'\[([^\]]+)\]', r':\1', route)

    # Add leading slash if not present
    if not route.startswith('/'):
        route = '/' + route

    return route


def analyze_route(file_path: Path, pages_dir: Path) -> RouteInfo:
    """Analyze a single route file."""
    route_path = get_route_path(file_path, pages_dir)

    # Detect dynamic parameters
    params = re.findall(r'\[([^\]]+)\]', str(file_path))
    is_dynamic = bool(params)
    is_catch_all = any('...' in p for p in params)
    is_optional_catch_all = any('[[' in str(file_path))

    # Analyze file content
    content_analysis = analyze_file_content(file_path)

    return RouteInfo(
        path=route_path,
        file_path=str(file_path),
        is_dynamic=is_dynamic,
        is_catch_all=is_catch_all,
        is_optional_catch_all=is_optional_catch_all,
        params=params,
        has_get_static_props=content_analysis.get('has_get_static_props', False),
        has_get_server_side_props=content_analysis.get('has_get_server_side_props', False),
        has_get_static_paths=content_analysis.get('has_get_static_paths', False),
        has_api_route='/api/' in route_path,
        fallback_mode=content_analysis.get('fallback_mode'),
        revalidate_time=content_analysis.get('revalidate_time'),
        estimated_paths=content_analysis.get('estimated_paths', 0),
        file_size_kb=content_analysis.get('file_size_kb', 0.0),
        line_count=content_analysis.get('line_count', 0),
    )


def find_issues(route: RouteInfo, report: AnalysisReport):
    """Find issues and add recommendations for a route."""

    # Issue: Dynamic route missing getStaticPaths
    if route.is_dynamic and route.has_get_static_props and not route.has_get_static_paths:
        report.issues.append({
            'severity': 'error',
            'route': route.path,
            'message': 'Dynamic route with getStaticProps must export getStaticPaths',
            'file': route.file_path,
        })

    # Issue: Mixed data fetching methods
    if route.has_get_static_props and route.has_get_server_side_props:
        report.issues.append({
            'severity': 'error',
            'route': route.path,
            'message': 'Cannot use both getStaticProps and getServerSideProps',
            'file': route.file_path,
        })

    # Issue: Missing fallback configuration
    if route.has_get_static_paths and not route.fallback_mode:
        report.issues.append({
            'severity': 'warning',
            'route': route.path,
            'message': 'getStaticPaths should specify a fallback strategy',
            'file': route.file_path,
        })

    # Issue: Excessive path pre-rendering
    if route.estimated_paths > 1000:
        report.issues.append({
            'severity': 'warning',
            'route': route.path,
            'message': f'Pre-rendering {route.estimated_paths} paths may increase build time significantly. Consider using fallback: "blocking"',
            'file': route.file_path,
        })

    # Issue: Very aggressive ISR
    if route.revalidate_time and route.revalidate_time < 10:
        report.issues.append({
            'severity': 'warning',
            'route': route.path,
            'message': f'Very aggressive ISR revalidation ({route.revalidate_time}s). Consider increasing to reduce server load',
            'file': route.file_path,
        })

    # Recommendation: Use ISR instead of SSR for semi-static content
    if route.has_get_server_side_props and not route.has_api_route:
        if route.path.startswith('/blog') or route.path.startswith('/docs') or route.path.startswith('/products'):
            report.recommendations.append(
                f"{route.path}: Consider using getStaticProps with ISR instead of getServerSideProps for better performance"
            )

    # Recommendation: Use fallback: 'blocking' for large datasets
    if route.has_get_static_paths and route.fallback_mode == 'false' and route.estimated_paths > 100:
        report.recommendations.append(
            f"{route.path}: Consider using fallback: 'blocking' instead of 'false' to avoid long build times"
        )


def estimate_build_time(report: AnalysisReport) -> float:
    """Estimate total build time based on routes."""
    total_seconds = 0.0

    for route in report.routes:
        if route.has_get_static_props and not route.has_api_route:
            # Base time per page: 0.5 seconds
            base_time = 0.5

            # Add time based on number of paths
            if route.has_get_static_paths:
                # Assume 0.1 seconds per path
                total_seconds += route.estimated_paths * 0.1
            else:
                total_seconds += base_time

    return total_seconds


def generate_route_tree(routes: List[RouteInfo]) -> str:
    """Generate a text-based route tree visualization."""
    tree_dict = defaultdict(list)

    for route in routes:
        parts = [p for p in route.path.split('/') if p]
        if not parts:
            tree_dict['root'].append(route)
        else:
            tree_dict[parts[0]].append(route)

    output = []
    output.append("Route Tree:")
    output.append("└── / (root)")

    for key in sorted(tree_dict.keys()):
        if key == 'root':
            continue

        routes_in_dir = tree_dict[key]
        output.append(f"    ├── /{key}/")

        for route in sorted(routes_in_dir, key=lambda r: r.path):
            method = ""
            if route.has_get_static_props:
                method = " [SSG"
                if route.revalidate_time:
                    method += f", ISR {route.revalidate_time}s"
                method += "]"
            elif route.has_get_server_side_props:
                method = " [SSR]"
            elif route.has_api_route:
                method = " [API]"

            dynamic_marker = " (dynamic)" if route.is_dynamic else ""

            output.append(f"    │   └── {route.path}{method}{dynamic_marker}")

    return '\n'.join(output)


def format_text_report(report: AnalysisReport, visualize: bool = False) -> str:
    """Format the report as text."""
    output = []

    output.append(f"{Colors.BOLD}{Colors.HEADER}Next.js Route Analysis Report{Colors.ENDC}\n")

    # Summary
    output.append(f"{Colors.BOLD}Summary:{Colors.ENDC}")
    output.append(f"  Total routes: {report.total_routes}")
    output.append(f"  Static routes (SSG): {report.static_routes}")
    output.append(f"  Dynamic routes: {report.dynamic_routes}")
    output.append(f"  Server-side routes (SSR): {report.ssr_routes}")
    output.append(f"  API routes: {report.api_routes}")
    output.append(f"  ISR enabled routes: {report.isr_routes}")

    if report.estimated_build_time_seconds > 0:
        minutes = int(report.estimated_build_time_seconds // 60)
        seconds = int(report.estimated_build_time_seconds % 60)
        output.append(f"  Estimated build time: {minutes}m {seconds}s")

    output.append("")

    # Issues
    if report.issues:
        output.append(f"{Colors.FAIL}{Colors.BOLD}Issues Found:{Colors.ENDC}")
        for issue in report.issues:
            severity_color = Colors.FAIL if issue['severity'] == 'error' else Colors.WARNING
            output.append(f"  {severity_color}[{issue['severity'].upper()}] {issue['route']}{Colors.ENDC}")
            output.append(f"    {issue['message']}")
            output.append(f"    File: {issue['file']}")
        output.append("")
    else:
        output.append(f"{Colors.OKGREEN}No issues found!{Colors.ENDC}\n")

    # Recommendations
    if report.recommendations:
        output.append(f"{Colors.OKCYAN}{Colors.BOLD}Recommendations:{Colors.ENDC}")
        for rec in report.recommendations:
            output.append(f"  • {rec}")
        output.append("")

    # Route tree visualization
    if visualize:
        output.append(f"{Colors.BOLD}Route Structure:{Colors.ENDC}")
        output.append(generate_route_tree(report.routes))
        output.append("")

    return '\n'.join(output)


def format_json_report(report: AnalysisReport) -> str:
    """Format the report as JSON."""
    return json.dumps(asdict(report), indent=2)


def format_markdown_report(report: AnalysisReport) -> str:
    """Format the report as Markdown."""
    output = []

    output.append("# Next.js Route Analysis Report\n")

    # Summary
    output.append("## Summary\n")
    output.append(f"- **Total routes:** {report.total_routes}")
    output.append(f"- **Static routes (SSG):** {report.static_routes}")
    output.append(f"- **Dynamic routes:** {report.dynamic_routes}")
    output.append(f"- **Server-side routes (SSR):** {report.ssr_routes}")
    output.append(f"- **API routes:** {report.api_routes}")
    output.append(f"- **ISR enabled routes:** {report.isr_routes}")

    if report.estimated_build_time_seconds > 0:
        minutes = int(report.estimated_build_time_seconds // 60)
        seconds = int(report.estimated_build_time_seconds % 60)
        output.append(f"- **Estimated build time:** {minutes}m {seconds}s")

    output.append("")

    # Issues
    if report.issues:
        output.append("## Issues Found\n")
        for issue in report.issues:
            output.append(f"### {issue['severity'].upper()}: {issue['route']}\n")
            output.append(f"{issue['message']}\n")
            output.append(f"**File:** `{issue['file']}`\n")
    else:
        output.append("## No Issues Found\n")

    # Recommendations
    if report.recommendations:
        output.append("## Recommendations\n")
        for rec in report.recommendations:
            output.append(f"- {rec}")
        output.append("")

    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze Next.js Pages Router routing structure and suggest optimizations.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('-d', '--directory', default='./pages',
                        help='Pages directory to analyze (default: ./pages)')
    parser.add_argument('-o', '--output', help='Output file for analysis report')
    parser.add_argument('--format', choices=['text', 'json', 'markdown'],
                        default='text', help='Output format (default: text)')
    parser.add_argument('--visualize', action='store_true',
                        help='Generate route tree visualization')
    parser.add_argument('--estimate-build-time', action='store_true',
                        help='Estimate build time for SSG routes')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show detailed analysis')

    args = parser.parse_args()

    pages_dir = Path(args.directory)

    if not pages_dir.exists():
        print_colored(f"Error: Pages directory not found: {pages_dir}", Colors.FAIL)
        sys.exit(1)

    # Initialize report
    report = AnalysisReport()

    # Find all page files
    page_files = []
    for ext in ['*.tsx', '*.ts', '*.jsx', '*.js']:
        page_files.extend(pages_dir.rglob(ext))

    # Analyze each route
    for file_path in page_files:
        # Skip non-page files
        if file_path.name.startswith('_') and file_path.name not in ['_app.tsx', '_app.ts', '_document.tsx', '_document.ts', '_error.tsx', '_error.ts']:
            continue

        route = analyze_route(file_path, pages_dir)
        report.routes.append(route)

        # Update counters
        report.total_routes += 1
        if route.has_get_static_props:
            report.static_routes += 1
        if route.is_dynamic:
            report.dynamic_routes += 1
        if route.has_get_server_side_props:
            report.ssr_routes += 1
        if route.has_api_route:
            report.api_routes += 1
        if route.revalidate_time:
            report.isr_routes += 1

        # Find issues
        find_issues(route, report)

    # Estimate build time if requested
    if args.estimate_build_time:
        report.estimated_build_time_seconds = estimate_build_time(report)

    # Format output
    if args.format == 'json':
        output = format_json_report(report)
    elif args.format == 'markdown':
        output = format_markdown_report(report)
    else:  # text
        output = format_text_report(report, args.visualize)

    # Write output
    if args.output:
        Path(args.output).write_text(output)
        print_colored(f"Analysis report written to: {args.output}", Colors.OKGREEN)
    else:
        print(output)

    # Exit code
    error_count = sum(1 for issue in report.issues if issue['severity'] == 'error')
    sys.exit(1 if error_count > 0 else 0)


if __name__ == '__main__':
    main()
