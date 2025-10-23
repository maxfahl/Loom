#!/usr/bin/env python3
"""
Next.js Pages Router to App Router Component Converter

Converts Pages Router pages to App Router structure. Transforms
getServerSideProps/getStaticProps to async Server Components, updates imports,
and generates proper file structure. Handles metadata migration.

Usage:
    python component-converter.py pages/blog/[slug].tsx
    python component-converter.py pages/dashboard.tsx --output app/dashboard
    python component-converter.py --scan pages/ --auto-convert
    python component-converter.py --help

Examples:
    # Convert single file
    python component-converter.py pages/about.tsx

    # Convert with custom output
    python component-converter.py pages/blog.tsx --output app/blog

    # Scan and preview conversions
    python component-converter.py --scan pages/ --dry-run

Time Saved: ~30 minutes per page migration
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional, Dict, List, Tuple

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

class PageConverter:
    def __init__(self, source_file: Path, output_dir: Optional[Path] = None):
        self.source_file = source_file
        self.output_dir = output_dir or self._determine_output_dir()
        self.source_content = source_file.read_text()
        self.metadata = {}
        self.has_client_features = False

    def _determine_output_dir(self) -> Path:
        """Determine output directory from source path"""
        # Convert pages/blog/[slug].tsx -> app/blog/[slug]/page.tsx
        rel_path = self.source_file.relative_to('pages') if 'pages' in str(self.source_file) else self.source_file
        path_parts = rel_path.parts[:-1]  # Remove filename
        return Path('app') / Path(*path_parts)

    def extract_metadata(self) -> Dict[str, str]:
        """Extract metadata from Head component or export"""
        metadata = {}

        # Extract from Head component
        head_match = re.search(r'<Head>(.*?)</Head>', self.source_content, re.DOTALL)
        if head_match:
            head_content = head_match.group(1)

            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', head_content)
            if title_match:
                metadata['title'] = title_match.group(1)

            # Extract description
            desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', head_content)
            if desc_match:
                metadata['description'] = desc_match.group(1)

        return metadata

    def check_client_features(self) -> bool:
        """Check if component uses client-side features"""
        client_patterns = [
            r'useState',
            r'useEffect',
            r'useContext',
            r'useReducer',
            r'onClick',
            r'onChange',
            r'onSubmit',
            r'window\.',
            r'document\.',
            r'localStorage',
            r'sessionStorage',
        ]

        for pattern in client_patterns:
            if re.search(pattern, self.source_content):
                return True
        return False

    def extract_data_fetching(self) -> Tuple[Optional[str], str]:
        """Extract and convert data fetching methods"""
        # Check for getServerSideProps
        gss_match = re.search(
            r'export\s+async\s+function\s+getServerSideProps.*?\{(.*?)\n\}',
            self.source_content,
            re.DOTALL
        )
        if gss_match:
            return ('ssr', gss_match.group(1))

        # Check for getStaticProps
        gsp_match = re.search(
            r'export\s+async\s+function\s+getStaticProps.*?\{(.*?)\n\}',
            self.source_content,
            re.DOTALL
        )
        if gsp_match:
            return ('ssg', gsp_match.group(1))

        return (None, '')

    def convert_to_app_router(self) -> str:
        """Convert component to App Router format"""
        self.has_client_features = self.check_client_features()
        self.metadata = self.extract_metadata()
        fetch_type, fetch_code = self.extract_data_fetching()

        # Extract component name
        component_match = re.search(r'export\s+default\s+function\s+(\w+)', self.source_content)
        component_name = component_match.group(1) if component_match else 'Page'

        # Start building new content
        lines = []

        # Add 'use client' if needed
        if self.has_client_features:
            lines.append("'use client'\n")

        # Add imports
        imports = self._extract_and_update_imports()
        if imports:
            lines.append(imports)

        # Add metadata export if available
        if self.metadata and not self.has_client_features:
            lines.append(self._generate_metadata_export())

        # Add data fetching if exists
        if fetch_code and not self.has_client_features:
            lines.append(self._convert_data_fetching(fetch_code))

        # Extract and convert component
        component_code = self._extract_component_body()
        if fetch_type and not self.has_client_features:
            # Make component async if it had data fetching
            component_code = self._make_component_async(component_code, fetch_type)

        lines.append(component_code)

        return '\n'.join(lines)

    def _extract_and_update_imports(self) -> str:
        """Extract and update imports"""
        import_lines = []

        # Find all imports
        for line in self.source_content.split('\n'):
            if line.strip().startswith('import'):
                # Update Head to metadata
                if 'next/head' in line:
                    continue  # Skip Head import, use metadata instead
                # Update Link import (stays the same)
                elif 'next/link' in line:
                    import_lines.append(line)
                # Update Image import (stays the same)
                elif 'next/image' in line:
                    import_lines.append(line)
                # Update router
                elif 'next/router' in line:
                    import_lines.append("import { useRouter } from 'next/navigation'")
                else:
                    import_lines.append(line)

        return '\n'.join(import_lines) + '\n' if import_lines else ''

    def _generate_metadata_export(self) -> str:
        """Generate metadata export"""
        title = self.metadata.get('title', 'Page')
        description = self.metadata.get('description', '')

        return f"""
import type {{ Metadata }}

export const metadata: Metadata = {{
  title: '{title}',
  description: '{description}',
}}
"""

    def _convert_data_fetching(self, fetch_code: str) -> str:
        """Convert data fetching to async component pattern"""
        # Extract actual fetch logic
        # This is simplified - real implementation would be more robust
        return f"""
async function getData() {{
  {fetch_code.strip()}
}}
"""

    def _extract_component_body(self) -> str:
        """Extract component body"""
        # Find component definition
        match = re.search(
            r'export\s+default\s+function\s+\w+\s*\((.*?)\)\s*\{(.*)\}(?=\s*(?:export|$))',
            self.source_content,
            re.DOTALL
        )

        if match:
            params = match.group(1)
            body = match.group(2)

            # Remove Head component
            body = re.sub(r'<Head>.*?</Head>', '', body, flags=re.DOTALL)

            return f"export default function Page({params}) {{\n{body}}}"

        return self.source_content

    def _make_component_async(self, component_code: str, fetch_type: str) -> str:
        """Make component async and add data fetching call"""
        # Add async keyword
        component_code = component_code.replace('export default function', 'export default async function')

        # Add data fetching call at start of component
        indent = '  '
        fetch_call = f'{indent}const data = await getData()\n\n'

        # Insert after function declaration
        parts = component_code.split('{', 1)
        if len(parts) == 2:
            component_code = parts[0] + '{\n' + fetch_call + parts[1]

        return component_code

    def convert(self, dry_run: bool = False) -> bool:
        """Perform the conversion"""
        try:
            print_info(f"Converting: {self.source_file}")

            # Determine output file
            output_file = self.output_dir / 'page.tsx'

            if dry_run:
                print_info(f"Would create: {output_file}")
                print_info(f"  Client component: {self.has_client_features}")
                print_info(f"  Has metadata: {bool(self.metadata)}")
                return True

            # Generate converted content
            converted_content = self.convert_to_app_router()

            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)

            # Write file
            output_file.write_text(converted_content)

            print_success(f"Created: {output_file}")
            if self.has_client_features:
                print_warning(f"  Marked as Client Component (uses client-side features)")
            if self.metadata:
                print_success(f"  Generated metadata export")

            return True

        except Exception as e:
            print_error(f"Failed to convert {self.source_file}: {str(e)}")
            return False

def scan_directory(directory: Path) -> List[Path]:
    """Scan directory for convertible pages"""
    pages = []
    for file_path in directory.rglob('*.tsx'):
        if file_path.stem not in ['_app', '_document', '_error', '404', '500']:
            pages.append(file_path)
    return pages

def main():
    parser = argparse.ArgumentParser(
        description="Convert Next.js Pages Router to App Router",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s pages/about.tsx
  %(prog)s pages/blog/[slug].tsx --output app/blog/[slug]
  %(prog)s --scan pages/ --dry-run
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        help='Input file to convert'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output directory (auto-detected if not specified)'
    )
    parser.add_argument(
        '--scan',
        help='Scan directory for convertible files'
    )
    parser.add_argument(
        '--auto-convert',
        action='store_true',
        help='Automatically convert all scanned files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview conversion without creating files'
    )

    args = parser.parse_args()

    if args.dry_run:
        print_info("DRY RUN MODE - No files will be created\n")

    # Scan mode
    if args.scan:
        scan_path = Path(args.scan)
        if not scan_path.exists():
            print_error(f"Directory not found: {scan_path}")
            sys.exit(1)

        pages = scan_directory(scan_path)
        print_info(f"Found {len(pages)} convertible pages:\n")

        success_count = 0
        for page in pages:
            print(f"  • {page}")
            if args.auto_convert:
                converter = PageConverter(page)
                if converter.convert(dry_run=args.dry_run):
                    success_count += 1

        if args.auto_convert:
            print(f"\n{Colors.BOLD}Summary:{Colors.END}")
            print(f"  Total: {len(pages)}")
            print(f"  Converted: {success_count}")
            print(f"  Failed: {len(pages) - success_count}")

        return

    # Single file mode
    if not args.input:
        parser.print_help()
        sys.exit(1)

    input_path = Path(args.input)
    if not input_path.exists():
        print_error(f"File not found: {input_path}")
        sys.exit(1)

    output_dir = Path(args.output) if args.output else None
    converter = PageConverter(input_path, output_dir)

    if converter.convert(dry_run=args.dry_run):
        if not args.dry_run:
            print(f"\n{Colors.GREEN}Conversion completed successfully!{Colors.END}")
            print(f"Next steps:")
            print(f"  1. Review the generated code")
            print(f"  2. Update data fetching if needed")
            print(f"  3. Test in development")
    else:
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)
