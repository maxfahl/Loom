#!/usr/bin/env python3

# ng-standalone-migrator.py
#
# Purpose:
#   Assists in migrating an existing Angular NgModule to a standalone component structure.
#   It analyzes a given NgModule file, identifies its declarations, imports, and exports,
#   and provides guidance on how to convert them to standalone components, directives, or pipes,
#   and how to update their usage.
#
# Usage:
#   python3 ng-standalone-migrator.py <path/to/module.ts>
#
# Arguments:
#   <path/to/module.ts> : The absolute or relative path to the NgModule file to analyze.
#
# Examples:
#   python3 ng-standalone-migrator.py src/app/feature/feature.module.ts
#
# Configuration:
#   None.
#
# Error Handling:
#   - Exits if the provided path is not a valid file or not a TypeScript file.
#   - Reports if the file does not appear to be an NgModule.
#
# Cross-platform:
#   Pure Python, should work on any OS with Python 3 installed.

import os
import re
import argparse
import sys

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

def show_help():
    print("Usage: python3 ng-standalone-migrator.py <path/to/module.ts>")
    print("\nArguments:")
    print("  <path/to/module.ts> : The path to the NgModule file to analyze.")
    print("\nExamples:")
    print("  python3 ng-standalone-migrator.py src/app/feature/feature.module.ts")
    print("\nThis script analyzes an NgModule and provides guidance for migrating to standalone components.")

def extract_ngmodule_info(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"{Colors.FAIL}Error reading file {filepath}: {e}{Colors.ENDC}")
        sys.exit(1)

    if "@NgModule({" not in content:
        print(f"{Colors.FAIL}Error: File {filepath} does not appear to be an NgModule.{Colors.ENDC}")
        sys.exit(1)

    declarations = re.search(r'declarations:\s*\[([^\]]*)(\s*,[^\].*)*\]', content, re.DOTALL)
    imports = re.search(r'imports:\s*\[([^\]]*)(\s*,[^\].*)*\]', content, re.DOTALL)
    exports = re.search(r'exports:\s*\[([^\]]*)(\s*,[^\].*)*\]', content, re.DOTALL)
    providers = re.search(r'providers:\s*\[([^\]]*)(\s*,[^\].*)*\]', content, re.DOTALL)

    info = {
        'declarations': [d.strip() for d in declarations.group(1).split(',') if d.strip()] if declarations else [],
        'imports': [i.strip() for i in imports.group(1).split(',') if i.strip()] if imports else [],
        'exports': [e.strip() for e in exports.group(1).split(',') if e.strip()] if exports else [],
        'providers': [p.strip() for p in providers.group(1).split(',') if p.strip()] if providers else []
    }
    return info, content

def main():
    parser = argparse.ArgumentParser(
        description="Assists in migrating an existing Angular NgModule to a standalone component structure."
    )
    parser.add_argument(
        "module_path",
        help="The path to the NgModule file to analyze."
    )

    args = parser.parse_args()

    module_filepath = args.module_path

    if not os.path.isfile(module_filepath) or not module_filepath.endswith('.ts'):
        print(f"{Colors.FAIL}Error: Invalid module path. Please provide a valid .ts file.{Colors.ENDC}")
        show_help()
        sys.exit(1)

    print(f"{Colors.HEADER}Analyzing NgModule: {module_filepath}{Colors.ENDC}")
    info, original_content = extract_ngmodule_info(module_filepath)

    print(f"{Colors.BOLD}\n--- Migration Guidance ---{Colors.ENDC}")

    if info['declarations']:
        print(f"{Colors.OKBLUE}\n1. Convert Declarations to Standalone:{Colors.ENDC}")
        print("   For each item declared in this NgModule, you should make it standalone.")
        print("   This involves setting `standalone: true` and adding its dependencies to its `imports` array.")
        for declaration in info['declarations']:
            print(f"   - {Colors.OKGREEN}{declaration}{Colors.ENDC}:")
            print(f"     - Open {declaration.replace('Component', '').replace('Directive', '').replace('Pipe', '').lower()}.component.ts (or similar).")
            print(f"     - Add `standalone: true,` to its `@Component`, `@Directive`, or `@Pipe` decorator.")
            print(f"     - Move any modules or standalone entities it depends on from this NgModule's `imports` or `exports` directly into its own `imports` array.")
            print(f"     - Remove {declaration} from this NgModule's `declarations` array.")

    if info['imports']:
        print(f"{Colors.OKBLUE}\n2. Update Imports:{Colors.ENDC}")
        print("   Once declarations are standalone, you will import them directly where needed.")
        print("   For modules imported here, consider if they can be replaced by direct imports of standalone entities.")
        for imported_item in info['imports']:
            print(f"   - {Colors.OKGREEN}{imported_item}{Colors.ENDC}:")
            print(f"     - If {imported_item} is an Angular module (e.g., `CommonModule`, `FormsModule`, `RouterModule.forChild(...)`), it can often be directly imported into standalone components that need it.")
            print(f"     - If {imported_item} is a feature module you've converted to standalone, you'll import its standalone components/directives/pipes directly.")
            print(f"     - Remove {imported_item} from this NgModule's `imports` array.")

    if info['exports']:
        print(f"{Colors.OKBLUE}\n3. Update Exports:{Colors.ENDC}")
        print("   Items exported from this NgModule will now be directly imported by consumers.")
        for exported_item in info['exports']:
            print(f"   - {Colors.OKGREEN}{exported_item}{Colors.ENDC}:")
            print(f"     - Any component, directive, or pipe that was exported from this NgModule will now be directly imported by any standalone component or NgModule that uses it.")
            print(f"     - Remove {exported_item} from this NgModule's `exports` array.")

    if info['providers']:
        print(f"{Colors.OKBLUE}\n4. Handle Providers:{Colors.ENDC}")
        print("   Providers can often be moved to the component level (for standalone components) or provided in `root` for application-wide services.")
        for provider in info['providers']:
            print(f"   - {Colors.OKGREEN}{provider}{Colors.ENDC}:")
            print(f"     - If {provider} is a service, consider making it `providedIn: 'root'` if it's a singleton across the app, or `providedIn: 'platform'` for platform-wide singletons.")
            print(f"     - If {provider} is specific to a standalone component, add it to the `providers` array of that component's `@Component` decorator.")
            print(f"     - Remove {provider} from this NgModule's `providers` array.")

    print(f"{Colors.BOLD}\n--- Final Steps ---{Colors.ENDC}")
    print("5. Once all declarations, imports, exports, and providers have been migrated, you can safely delete the NgModule file itself.")
    print("6. Update any parent NgModules or standalone components that were importing this NgModule to directly import the new standalone entities.")
    print("7. Run your tests and application to ensure everything works as expected.")
    print(f"{Colors.OKGREEN}\nMigration analysis complete. Please follow the guidance to refactor your code.{Colors.ENDC}")

if __name__ == "__main__":
    main()
