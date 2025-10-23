#!/usr/bin/env python3
"""
Next.js App Router Route Generator

Generates complete route structures with layout, page, loading, error files
following Next.js conventions. Supports dynamic routes, catch-all routes,
and parallel routes with TypeScript types and common patterns.

Usage:
    python route-generator.py dashboard --with-loading --with-error
    python route-generator.py blog/[slug] --type dynamic
    python route-generator.py photos --parallel analytics,team
    python route-generator.py --help

Examples:
    # Simple route
    python route-generator.py products

    # Dynamic route with loading/error states
    python route-generator.py products/[id] --type dynamic --with-loading --with-error

    # Parallel routes for dashboard
    python route-generator.py dashboard --parallel analytics,team --with-layout

    # Catch-all route
    python route-generator.py docs/[...slug] --type catch-all

Time Saved: ~20 minutes per route structure
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

# Color codes for output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg: str):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def print_error(msg: str):
    print(f"{Colors.RED}✗{Colors.END} {msg}", file=sys.stderr)

def create_page_file(path: Path, route_type: str, route_name: str):
    """Create page.tsx file"""
    is_dynamic = '[' in route_name
    is_catch_all = '[...' in route_name

    if is_catch_all:
        param_name = route_name.split('[...')[1].rstrip(']')
        params_type = f"{{ {param_name}: string[] }}"
    elif is_dynamic:
        param_name = route_name.split('[')[1].rstrip(']')
        params_type = f"{{ {param_name}: string }}"
    else:
        params_type = None

    content = f'''import {{ Suspense }} from 'react'

interface PageProps {{
  params: Promise<{params_type if params_type else "{}"}>
  searchParams: Promise<{{ [key: string]: string | string[] | undefined }}>
}}

export default async function {route_name.replace('[', '').replace(']', '').replace('...', '').replace('/', '').title()}Page({{ params, searchParams }}: PageProps) {{
  {'const { ' + param_name + ' } = await params' if params_type else ''}
  const search = await searchParams

  return (
    <div>
      <h1>{route_name.replace('[', '').replace(']', '').replace('...', '').title()} Page</h1>
      {'{/* Page content */}'}
    </div>
  )
}}
'''

    path.write_text(content)
    print_success(f"Created {path.name}")

def create_layout_file(path: Path, route_name: str, parallel_routes: Optional[List[str]] = None):
    """Create layout.tsx file"""
    parallel_props = ""
    parallel_render = ""

    if parallel_routes:
        parallel_props = "\n  " + "\n  ".join([f"{route}: React.ReactNode" for route in parallel_routes])
        parallel_render = "\n      " + "\n      ".join([f"<div>{{{route}}}</div>" for route in parallel_routes])

    content = f'''export default function Layout({{
  children,{parallel_props}
}}: {{
  children: React.ReactNode{parallel_props}
}}) {{
  return (
    <div>
      {'{/* Layout wrapper */}'}
      <div>{{children}}</div>{parallel_render}
    </div>
  )
}}
'''

    path.write_text(content)
    print_success(f"Created {path.name}")

def create_loading_file(path: Path):
    """Create loading.tsx file"""
    content = '''export default function Loading() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900" />
    </div>
  )
}
'''
    path.write_text(content)
    print_success(f"Created {path.name}")

def create_error_file(path: Path):
    """Create error.tsx file"""
    content = ''''use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
      <p className="text-gray-600 mb-4">{error.message}</p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Try again
      </button>
    </div>
  )
}
'''
    path.write_text(content)
    print_success(f"Created {path.name}")

def create_not_found_file(path: Path):
    """Create not-found.tsx file"""
    content = '''import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-3xl font-bold mb-2">404 - Not Found</h2>
      <p className="text-gray-600 mb-6">Could not find requested resource</p>
      <Link
        href="/"
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Return Home
      </Link>
    </div>
  )
}
'''
    path.write_text(content)
    print_success(f"Created {path.name}")

def create_parallel_route(base_path: Path, route_name: str):
    """Create parallel route slot"""
    slot_path = base_path / f"@{route_name}"
    slot_path.mkdir(exist_ok=True)

    page_file = slot_path / "page.tsx"
    content = f'''export default function {route_name.title()}Slot() {{
  return (
    <div>
      <h2>{route_name.title()} Slot</h2>
      {'{/* Slot content */}'}
    </div>
  )
}}
'''
    page_file.write_text(content)
    print_success(f"Created parallel route @{route_name}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate Next.js App Router route structures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s dashboard
  %(prog)s blog/[slug] --type dynamic --with-loading
  %(prog)s dashboard --parallel analytics,team
  %(prog)s docs/[...slug] --type catch-all --with-error
        """
    )

    parser.add_argument(
        'route',
        help='Route path (e.g., dashboard, blog/[slug], docs/[...slug])'
    )
    parser.add_argument(
        '--base-dir',
        default='./app',
        help='Base directory for routes (default: ./app)'
    )
    parser.add_argument(
        '--type',
        choices=['simple', 'dynamic', 'catch-all'],
        default='simple',
        help='Route type (default: simple)'
    )
    parser.add_argument(
        '--with-layout',
        action='store_true',
        help='Generate layout.tsx'
    )
    parser.add_argument(
        '--with-loading',
        action='store_true',
        help='Generate loading.tsx'
    )
    parser.add_argument(
        '--with-error',
        action='store_true',
        help='Generate error.tsx'
    )
    parser.add_argument(
        '--with-not-found',
        action='store_true',
        help='Generate not-found.tsx'
    )
    parser.add_argument(
        '--parallel',
        help='Comma-separated list of parallel route names (e.g., analytics,team)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be created without creating files'
    )

    args = parser.parse_args()

    # Determine route path
    base_path = Path(args.base_dir)
    route_path = base_path / args.route

    if args.dry_run:
        print_info("DRY RUN MODE - No files will be created\n")

    # Create directory
    if not args.dry_run:
        route_path.mkdir(parents=True, exist_ok=True)
        print_success(f"Created directory: {route_path}")
    else:
        print_info(f"Would create directory: {route_path}")

    # Generate files
    route_name = args.route.split('/')[-1]

    # Page file (always created)
    page_file = route_path / "page.tsx"
    if not args.dry_run:
        create_page_file(page_file, args.type, route_name)
    else:
        print_info(f"Would create: {page_file}")

    # Optional files
    if args.with_layout:
        parallel_routes = args.parallel.split(',') if args.parallel else None
        layout_file = route_path / "layout.tsx"
        if not args.dry_run:
            create_layout_file(layout_file, route_name, parallel_routes)
        else:
            print_info(f"Would create: {layout_file}")

    if args.with_loading:
        loading_file = route_path / "loading.tsx"
        if not args.dry_run:
            create_loading_file(loading_file)
        else:
            print_info(f"Would create: {loading_file}")

    if args.with_error:
        error_file = route_path / "error.tsx"
        if not args.dry_run:
            create_error_file(error_file)
        else:
            print_info(f"Would create: {error_file}")

    if args.with_not_found:
        not_found_file = route_path / "not-found.tsx"
        if not args.dry_run:
            create_not_found_file(not_found_file)
        else:
            print_info(f"Would create: {not_found_file}")

    # Parallel routes
    if args.parallel:
        for parallel_route in args.parallel.split(','):
            if not args.dry_run:
                create_parallel_route(route_path, parallel_route.strip())
            else:
                print_info(f"Would create parallel route: @{parallel_route.strip()}")

    # Summary
    print(f"\n{Colors.BOLD}Summary:{Colors.END}")
    print(f"  Route: {args.route}")
    print(f"  Type: {args.type}")
    print(f"  Location: {route_path}")

    if not args.dry_run:
        print(f"\n{Colors.GREEN}Route structure generated successfully!{Colors.END}")
        print(f"Next steps:")
        print(f"  1. Customize the generated files")
        print(f"  2. Add your business logic")
        print(f"  3. Test the route in development")
    else:
        print(f"\n{Colors.YELLOW}Dry run complete. Use without --dry-run to create files.{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)
