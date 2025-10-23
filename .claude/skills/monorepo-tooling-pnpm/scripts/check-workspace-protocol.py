#!/usr/bin/env python3
import argparse
import json
import os
import sys
import yaml # For pnpm-workspace.yaml

# ANSI escape codes for colored output
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

def get_workspace_packages(root_dir):
    """
    Reads pnpm-workspace.yaml and returns a list of package paths.
    """
    workspace_file = os.path.join(root_dir, 'pnpm-workspace.yaml')
    if not os.path.exists(workspace_file):
        print(f"{Colors.FAIL}Error: pnpm-workspace.yaml not found at {workspace_file}{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)

    with open(workspace_file, 'r') as f:
        workspace_config = yaml.safe_load(f)

    package_globs = workspace_config.get('packages', [])
    package_paths = set()

    for glob_pattern in package_globs:
        # Convert glob pattern to regex for os.walk filtering
        # This is a simplified conversion and might not cover all glob nuances
        regex_pattern = glob_pattern.replace('.', '\.').replace('*', '[^/]*').replace('**', '.*')
        for root, dirs, files in os.walk(root_dir):
            relative_root = os.path.relpath(root, root_dir)
            if re.fullmatch(regex_pattern, relative_root) and 'package.json' in files:
                package_paths.add(os.path.join(root_dir, relative_root))
            # Also check subdirectories if glob_pattern contains /**/
            elif '**' in glob_pattern:
                if re.fullmatch(regex_pattern, relative_root + '/') and 'package.json' in files:
                    package_paths.add(os.path.join(root_dir, relative_root))

    # Filter to ensure only actual package directories (containing package.json) are included
    final_package_paths = [p for p in package_paths if os.path.exists(os.path.join(p, 'package.json'))]
    return sorted(final_package_paths)

def get_internal_package_names(workspace_paths):
    """
    Extracts package names from all package.json files in the workspace.
    """
    internal_names = set()
    for path in workspace_paths:
        package_json_path = os.path.join(path, 'package.json')
        try:
            with open(package_json_path, 'r') as f:
                pkg_json = json.load(f)
                if 'name' in pkg_json:
                    internal_names.add(pkg_json['name'])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"{Colors.WARNING}Warning: Could not read or parse {package_json_path}: {e}{Colors.ENDC}", file=sys.stderr)
    return internal_names

def check_workspace_protocol(root_dir, dry_run=False):
    """
    Audits package.json files for correct workspace: protocol usage.
    """
    workspace_paths = get_workspace_packages(root_dir)
    internal_package_names = get_internal_package_names(workspace_paths)

    issues_found = 0
    for package_path in workspace_paths:
        package_json_path = os.path.join(package_path, 'package.json')
        package_name = os.path.basename(package_path)

        try:
            with open(package_json_path, 'r') as f:
                pkg_json = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"{Colors.FAIL}Error: Could not read or parse {package_json_path}: {e}{Colors.ENDC}", file=sys.stderr)
            issues_found += 1
            continue

        deps_sections = ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']
        for section in deps_sections:
            if section in pkg_json:
                for dep, version in pkg_json[section].items():
                    if dep in internal_package_names:
                        if not version.startswith('workspace:'):
                            issues_found += 1
                            print(f"{Colors.FAIL}  ❌ Package '{package_name}' ({section}): Internal dependency '{dep}' does not use 'workspace:' protocol. Found: '{version}'{Colors.ENDC}")
                            if not dry_run:
                                print(f"{Colors.OKBLUE}    Consider changing to: \"workspace:^\" or \"workspace:*\"{Colors.ENDC}")
                        else:
                            print(f"{Colors.OKGREEN}  ✅ Package '{package_name}' ({section}): Internal dependency '{dep}' uses 'workspace:' protocol. Found: '{version}'{Colors.ENDC}")

    return issues_found

def main():
    parser = argparse.ArgumentParser(
        description="Audit pnpm monorepo package.json files for correct 'workspace:' protocol usage.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show issues without suggesting changes.'
    )
    args = parser.parse_args()

    root_dir = os.getcwd() # Assume script is run from monorepo root or sub-directory
    try:
        # Find git root to ensure we are at the monorepo root
        git_root = os.popen('git rev-parse --show-toplevel').read().strip()
        if git_root:
            root_dir = git_root
    except Exception:
        pass # Not a git repo, use current working directory

    print(f"{Colors.HEADER}{Colors.BOLD}--- Workspace Protocol Auditor Started ---{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Scanning monorepo at: {root_dir}{Colors.ENDC}")

    issues = check_workspace_protocol(root_dir, args.dry_run)

    print(f"{Colors.HEADER}{Colors.BOLD}--- Audit Summary ---{Colors.ENDC}")
    if issues == 0:
        print(f"{Colors.OKGREEN}All internal dependencies use the 'workspace:' protocol correctly! ✅{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}{issues} issue(s) found regarding 'workspace:' protocol usage. ❌{Colors.ENDC}")
        if not args.dry_run:
            print(f"{Colors.WARNING}Please review the output and update the affected package.json files.{Colors.ENDC}")

    print(f"{Colors.HEADER}{Colors.BOLD}--- Workspace Protocol Auditor Finished ---{Colors.ENDC}")

    if issues > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
