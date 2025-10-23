import os
import re
import argparse
from collections import defaultdict

def analyze_angularjs_file(filepath):
    """Analyzes a single AngularJS file for common patterns and potential issues."""
    findings = defaultdict(list)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for angular module definition
    if re.search(r'angular.module(["\'].*?["\'])', content):
        findings['module_definitions'].append(f'Found angular.module definition.')

    # Patterns for controllers, services, factories, directives
    if re.search(r'.controller(["\'].*?["\'])', content):
        findings['controllers'].append(f'Found .controller definition.')
    if re.search(r'.service(["\'].*?["\'])', content):
        findings['services'].append(f'Found .service definition.')
    if re.search(r'.factory(["\'].*?["\'])', content):
        findings['factories'].append(f'Found .factory definition.')
    if re.search(r'.directive(["\'].*?["\'])', content):
        findings['directives'].append(f'Found .directive definition.')

    # Pattern for $scope usage
    if re.search(r'$scope', content):
        findings['scope_usage'].append(f'Found $scope usage.')

    # Pattern for direct DOM manipulation (e.g., element.css, element.on)
    if re.search(r'element.(css|on|append|prepend|remove|html|text)', content):
        findings['dom_manipulation'].append(f'Found potential direct DOM manipulation.')

    # Pattern for direct HTTP calls within controllers (simplified)
    if re.search(r'.controller([\s\S]*?(?:$http|fetch|axios).)', content):
        findings['http_in_controller'].append(f'Found potential HTTP call within controller.')

    # Pattern for global variable declarations (simplified, might have false positives)
    if re.search(r'^(var|let|const)\s+\w+\s*=\s*.*?;', content, re.MULTILINE):
        findings['global_variables'].append(f'Found potential global variable declaration.')

    # Check controller complexity (simple line count heuristic)
    controller_matches = re.findall(r'.controller(["\'].*?["\'],\s*function(.*?)\s*{([\s\S]*?)}\))', content)
    for match in controller_matches:
        controller_body = match[1]
        lines = controller_body.strip().split('\n')
        if len(lines) > 50: # Heuristic for complex controller
            findings['complex_controllers'].append(f'Controller might be complex (>{len(lines)} lines).')

    return findings

def main():
    parser = argparse.ArgumentParser(description="Analyze AngularJS codebase for migration insights.")
    parser.add_argument('path', type=str, help="Path to the AngularJS project directory.")
    parser.add_argument('--dry-run', action='store_true', help="Perform a dry run without making changes (not applicable for this analyzer).")
    args = parser.parse_args()

    project_path = args.path
    if not os.path.isdir(project_path):
        print(f"Error: Directory not found at {project_path}")
        return

    print(f"Analyzing AngularJS project at: {project_path}\n")
    total_findings = defaultdict(int)
    file_count = 0

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(('.js', '.ts')):
                filepath = os.path.join(root, file)
                file_count += 1
                file_findings = analyze_angularjs_file(filepath)
                if file_findings:
                    print(f"--- {filepath} ---")
                    for category, messages in file_findings.items():
                        print(f"  {category.replace('_', ' ').title()}:")
                        for msg in messages:
                            print(f"    - {msg}")
                        total_findings[category] += len(messages)
                    print()

    print("\n--- Analysis Summary ---")
    print(f"Total files scanned: {file_count}")
    if not total_findings:
        print("No specific AngularJS patterns or potential issues found.")
    else:
        for category, count in total_findings.items():
            print(f"  {category.replace('_', ' ').title()}: {count} occurrences")

    print("\nRecommendations:")
    print("- Prioritize migration to a modern framework.")
    print("- Refactor complex controllers into services/components.")
    print("- Isolate business logic from controllers and directives.")
    print("- Avoid direct DOM manipulation; use directives or modern component lifecycle hooks.")
    print("- Minimize $scope usage; prefer 'controllerAs' syntax or component-based approaches.")

if __name__ == "__main__":
    main()
