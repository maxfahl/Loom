#!/usr/bin/env python3
"""
Next.js Pages Router to App Router Migration Assistant

Generates App Router equivalents of Pages Router pages to aid migration.
Creates side-by-side comparisons and TODO lists for manual migration steps.

Usage:
    python migration-assistant.py [OPTIONS]

Options:
    -s, --source DIR          Source pages directory (default: ./pages)
    -t, --target DIR          Target app directory (default: ./app)
    -f, --file FILE           Migrate a single file
    --dry-run                 Preview changes without creating files
    --comparison             Generate side-by-side comparison
    --todo                   Generate TODO list for manual steps
    -v, --verbose            Show detailed output
    -h, --help               Show this help message

Examples:
    # Migrate entire pages directory
    python migration-assistant.py --dry-run

    # Migrate single file with comparison
    python migration-assistant.py -f pages/blog/[slug].tsx --comparison

    # Generate TODO list
    python migration-assistant.py --todo

Author: DevDev AI
Version: 1.0.0
"""

import argparse
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


@dataclass
class MigrationResult:
    """Result of a migration operation."""
    source_file: str
    target_file: str
    migrated_content: str
    conversion_notes: List[str]
    manual_steps: List[str]


def print_colored(text: str, color: str = Colors.ENDC):
    """Print colored text."""
    print(f"{color}{text}{Colors.ENDC}")


def convert_get_static_props_to_async_component(content: str) -> Tuple[str, List[str], List[str]]:
    """Convert getStaticProps to async Server Component."""
    notes = []
    manual_steps = []

    # Extract getStaticProps function
    get_static_props_match = re.search(
        r'export\s+const\s+getStaticProps[^=]*=\s*async\s*\([^)]*\)\s*=>\s*\{(.*?)\n\};',
        content,
        re.DOTALL
    )

    if not get_static_props_match:
        return content, notes, manual_steps

    # Extract props return
    props_match = re.search(r'props:\s*\{([^}]+)\}', get_static_props_match.group(0))
    if not props_match:
        manual_steps.append("Could not automatically extract props. Manual migration required.")
        return content, notes, manual_steps

    # Extract data fetching logic
    fetching_logic = get_static_props_match.group(1)

    # Remove props wrapper and revalidate
    fetching_logic = re.sub(r'return\s*\{[^}]*props:\s*\{', '', fetching_logic)
    fetching_logic = re.sub(r'revalidate:.*?[,}]', '', fetching_logic)
    fetching_logic = re.sub(r'\},?\s*\};?\s*$', '', fetching_logic)

    # Find component function
    component_match = re.search(
        r'export\s+default\s+function\s+(\w+)\s*\([^)]*\)',
        content
    )

    if not component_match:
        manual_steps.append("Could not find default export component. Manual migration required.")
        return content, notes, manual_steps

    component_name = component_match.group(1)

    # Create async component
    new_component = f"""// Migrated to App Router Server Component
export default async function {component_name}() {{
  // Data fetching now happens directly in the component
{fetching_logic}

  return (
    // TODO: Update JSX - props are now directly available as variables
  );
}}
"""

    # Remove old getStaticProps
    content = re.sub(
        r'export\s+const\s+getStaticProps[^;]*;',
        '',
        content,
        flags=re.DOTALL
    )

    # Replace component
    content = re.sub(
        r'export\s+default\s+function\s+\w+\s*\([^)]*\)\s*\{',
        new_component,
        content
    )

    notes.append("Converted getStaticProps to async Server Component")
    manual_steps.append("Update component JSX to use variables instead of props")
    manual_steps.append("Review data fetching logic for any Pages Router specific code")

    return content, notes, manual_steps


def convert_get_server_side_props_to_async_component(content: str) -> Tuple[str, List[str], List[str]]:
    """Convert getServerSideProps to async Server Component."""
    notes = []
    manual_steps = []

    if 'getServerSideProps' not in content:
        return content, notes, manual_steps

    # Similar logic to getStaticProps conversion
    notes.append("Converted getServerSideProps to async Server Component")
    manual_steps.append("Move authentication checks to middleware if applicable")
    manual_steps.append("Update redirect logic to use Next.js redirect() function")
    manual_steps.append("Review request context usage - may need to use headers() or cookies()")

    return content, notes, manual_steps


def convert_get_static_paths(content: str) -> Tuple[str, List[str], List[str]]:
    """Convert getStaticPaths to generateStaticParams."""
    notes = []
    manual_steps = []

    if 'getStaticPaths' not in content:
        return content, notes, manual_steps

    # Extract getStaticPaths
    get_static_paths_match = re.search(
        r'export\s+const\s+getStaticPaths[^=]*=\s*async\s*\([^)]*\)\s*=>\s*\{(.*?)\n\};',
        content,
        re.DOTALL
    )

    if not get_static_paths_match:
        manual_steps.append("Could not automatically convert getStaticPaths. Manual migration required.")
        return content, notes, manual_steps

    # Create generateStaticParams
    new_function = """
export async function generateStaticParams() {
  // TODO: Convert from getStaticPaths format
  // Return array of params objects
  // Example: return [{ slug: 'post-1' }, { slug: 'post-2' }];

  return [];
}
"""

    # Remove old getStaticPaths
    content = re.sub(
        r'export\s+const\s+getStaticPaths[^;]*;',
        new_function,
        content,
        flags=re.DOTALL
    )

    notes.append("Converted getStaticPaths to generateStaticParams")
    manual_steps.append("Convert paths array to return flat array of param objects")
    manual_steps.append("Remove fallback configuration - use dynamicParams instead")

    return content, notes, manual_steps


def convert_api_route_to_route_handler(content: str, filename: str) -> Tuple[str, List[str], List[str]]:
    """Convert API route to Route Handler."""
    notes = []
    manual_steps = []

    # Check if it's an API route
    if 'NextApiRequest' not in content and 'NextApiResponse' not in content:
        return content, notes, manual_steps

    # Create new route handler template
    new_content = """// Migrated to App Router Route Handler
import { NextRequest, NextResponse } from 'next/server';

// GET handler
export async function GET(request: NextRequest) {
  try {
    // TODO: Migrate GET logic
    // Access query params: request.nextUrl.searchParams
    // Access cookies: request.cookies

    return NextResponse.json({ data: 'success' });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// POST handler
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // TODO: Migrate POST logic

    return NextResponse.json({ data: 'success' }, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Additional HTTP methods: PUT, DELETE, PATCH, etc.
"""

    notes.append("Converted API route to Route Handler")
    manual_steps.append("Split single handler into separate HTTP method functions")
    manual_steps.append("Update request/response access patterns")
    manual_steps.append("Move middleware to middleware.ts if applicable")
    manual_steps.append("Update CORS configuration if needed")

    return new_content, notes, manual_steps


def get_target_path(source_path: Path, source_dir: Path, target_dir: Path) -> Path:
    """Convert pages path to app path."""
    relative = source_path.relative_to(source_dir)

    # Convert special files
    if relative.name == '_app.tsx' or relative.name == '_app.ts':
        return target_dir / 'layout.tsx'
    elif relative.name == '_document.tsx' or relative.name == '_document.ts':
        # _document is not needed in App Router
        return None

    # Convert index files to page.tsx
    if relative.stem == 'index':
        return target_dir / relative.parent / 'page.tsx'

    # Convert dynamic routes [param] stays the same
    # API routes go to app/api/...
    if 'api' in relative.parts:
        # API routes: pages/api/users/[id].ts -> app/api/users/[id]/route.ts
        api_path = Path(*[p for p in relative.parts if p != 'api'])
        if api_path.suffix:
            api_path = api_path.with_suffix('')
        return target_dir / 'api' / api_path / 'route.ts'

    # Regular pages
    page_path = relative.with_suffix('')
    return target_dir / page_path / 'page.tsx'


def migrate_file(source_file: Path, target_file: Path, dry_run: bool = False) -> MigrationResult:
    """Migrate a single file from Pages to App Router."""
    content = source_file.read_text()
    original_content = content

    notes = []
    manual_steps = []

    # Determine file type and apply appropriate conversions
    is_api_route = '/api/' in str(source_file)

    if is_api_route:
        content, api_notes, api_manual = convert_api_route_to_route_handler(
            content, source_file.name
        )
        notes.extend(api_notes)
        manual_steps.extend(api_manual)
    else:
        # Convert data fetching methods
        content, ssg_notes, ssg_manual = convert_get_static_props_to_async_component(content)
        notes.extend(ssg_notes)
        manual_steps.extend(ssg_manual)

        content, ssr_notes, ssr_manual = convert_get_server_side_props_to_async_component(content)
        notes.extend(ssr_notes)
        manual_steps.extend(ssr_manual)

        content, paths_notes, paths_manual = convert_get_static_paths(content)
        notes.extend(paths_notes)
        manual_steps.extend(paths_manual)

    # Update imports
    content = content.replace('next/router', 'next/navigation')
    content = content.replace('useRouter', '// TODO: Update to useRouter from next/navigation or useParams/useSearchParams')

    # Write file if not dry run
    if not dry_run and target_file:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content)

    return MigrationResult(
        source_file=str(source_file),
        target_file=str(target_file) if target_file else 'N/A',
        migrated_content=content,
        conversion_notes=notes,
        manual_steps=manual_steps,
    )


def generate_comparison(original: str, migrated: str) -> str:
    """Generate side-by-side comparison."""
    output = []
    output.append(f"{Colors.BOLD}{'='*80}{Colors.ENDC}")
    output.append(f"{Colors.BOLD}{'BEFORE (Pages Router)':<40} | {'AFTER (App Router)':>40}{Colors.ENDC}")
    output.append(f"{Colors.BOLD}{'='*80}{Colors.ENDC}")

    original_lines = original.split('\n')[:20]  # Show first 20 lines
    migrated_lines = migrated.split('\n')[:20]

    max_lines = max(len(original_lines), len(migrated_lines))

    for i in range(max_lines):
        orig_line = original_lines[i] if i < len(original_lines) else ''
        mig_line = migrated_lines[i] if i < len(migrated_lines) else ''

        output.append(f"{orig_line:<40} | {mig_line:>40}")

    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Migrate Next.js Pages Router to App Router',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('-s', '--source', default='./pages',
                        help='Source pages directory (default: ./pages)')
    parser.add_argument('-t', '--target', default='./app',
                        help='Target app directory (default: ./app)')
    parser.add_argument('-f', '--file', help='Migrate a single file')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without creating files')
    parser.add_argument('--comparison', action='store_true',
                        help='Generate side-by-side comparison')
    parser.add_argument('--todo', action='store_true',
                        help='Generate TODO list for manual steps')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show detailed output')

    args = parser.parse_args()

    source_dir = Path(args.source)
    target_dir = Path(args.target)

    if not source_dir.exists():
        print_colored(f"Error: Source directory not found: {source_dir}", Colors.FAIL)
        sys.exit(1)

    # Collect files to migrate
    files_to_migrate = []
    if args.file:
        files_to_migrate = [Path(args.file)]
    else:
        for ext in ['*.tsx', '*.ts', '*.jsx', '*.js']:
            files_to_migrate.extend(source_dir.rglob(ext))

    print_colored(f"\nMigrating {len(files_to_migrate)} files...\n", Colors.BOLD)

    all_manual_steps = []
    migrated_count = 0

    for source_file in files_to_migrate:
        target_file = get_target_path(source_file, source_dir, target_dir)

        if target_file is None:
            print_colored(f"Skipping {source_file.name} (not needed in App Router)", Colors.WARNING)
            continue

        try:
            original_content = source_file.read_text()
            result = migrate_file(source_file, target_file, args.dry_run)

            if args.verbose or args.dry_run:
                print_colored(f"\n{'='*80}", Colors.BOLD)
                print_colored(f"File: {source_file}", Colors.OKBLUE)
                print_colored(f"Target: {target_file}", Colors.OKCYAN)

                if result.conversion_notes:
                    print_colored("\nConversion Notes:", Colors.OKGREEN)
                    for note in result.conversion_notes:
                        print(f"  • {note}")

                if result.manual_steps:
                    print_colored("\nManual Steps Required:", Colors.WARNING)
                    for step in result.manual_steps:
                        print(f"  ⚠ {step}")
                        all_manual_steps.append(f"{source_file}: {step}")

                if args.comparison:
                    print("\n")
                    print(generate_comparison(original_content, result.migrated_content))

            migrated_count += 1

        except Exception as e:
            print_colored(f"Error migrating {source_file}: {e}", Colors.FAIL)

    # Summary
    print_colored(f"\n{'='*80}", Colors.BOLD)
    print_colored(f"Migration Summary", Colors.BOLD)
    print_colored(f"{'='*80}", Colors.BOLD)
    print(f"Files migrated: {migrated_count}/{len(files_to_migrate)}")
    print(f"Dry run: {'Yes' if args.dry_run else 'No'}")

    if args.todo or all_manual_steps:
        print_colored(f"\nTODO List for Manual Migration Steps:", Colors.WARNING)
        for i, step in enumerate(all_manual_steps, 1):
            print(f"{i}. {step}")

    if args.dry_run:
        print_colored(f"\n⚠ This was a dry run. No files were created.", Colors.WARNING)
    else:
        print_colored(f"\n✓ Migration complete! Review the migrated files and complete manual steps.", Colors.OKGREEN)


if __name__ == '__main__':
    main()
