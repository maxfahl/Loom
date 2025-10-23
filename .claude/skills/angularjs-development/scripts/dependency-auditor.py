
import os
import json
import argparse
from datetime import datetime

# Simplified list of known EOL/problematic AngularJS-era libraries for demonstration
# In a real scenario, this would involve API calls to vulnerability databases or package registries.
KNOWN_PROBLEMATIC_DEPS = {
    "angular": {"eol_date": "2021-12-31", "recommendation": "Migrate to Angular 2+ or another modern framework."},
    "jquery": {"eol_date": "2020-05-01", "recommendation": "Consider modern JavaScript alternatives or a newer version."},
    "bootstrap": {"eol_date": "N/A", "recommendation": "Upgrade to Bootstrap 4+ or a modern CSS framework."},
    "bower": {"eol_date": "2017-10-10", "recommendation": "Migrate to npm/yarn for package management."},
    # Add more as needed for demonstration
}

def audit_dependencies(filepath, package_manager):
    """Audits dependencies from a package.json or bower.json file."""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        dependencies = data.get('dependencies', {})
        dev_dependencies = data.get('devDependencies', {})

        all_deps = {**dependencies, **dev_dependencies}

        if not all_deps:
            findings.append(f"No dependencies found in {filepath}.")
            return findings

        findings.append(f"--- Auditing {package_manager} dependencies in {filepath} ---")

        for dep_name, dep_version in all_deps.items():
            status = f"  - {dep_name}@{dep_version}: "
            problematic_info = KNOWN_PROBLEMATIC_DEPS.get(dep_name.lower())

            if problematic_info:
                status += f"POTENTIALLY PROBLEMATIC. "
                if problematic_info.get("eol_date") != "N/A":
                    status += f"EOL Date: {problematic_info['eol_date']}. "
                status += f"Recommendation: {problematic_info['recommendation']}"
            else:
                status += "Consider checking for updates and vulnerabilities."

            findings.append(status)

        findings.append(f"\n  *Recommendation*: For a comprehensive audit, run `npm audit` (for package.json) or `bower outdated` and `bower install --force-latest` (for bower.json) in your project directory. Also, consider using tools like Snyk or Dependabot for continuous vulnerability scanning.")

    except FileNotFoundError:
        findings.append(f"Error: {filepath} not found.")
    except json.JSONDecodeError:
        findings.append(f"Error: Invalid JSON in {filepath}.")
    except Exception as e:
        findings.append(f"An unexpected error occurred while processing {filepath}: {e}")

    return findings

def main():
    parser = argparse.ArgumentParser(description="Audit AngularJS project dependencies for outdated/vulnerable libraries.")
    parser.add_argument('path', type=str, help="Path to the AngularJS project directory.")
    parser.add_argument('--dry-run', action='store_true', help="Perform a dry run (not applicable for this informational script).")
    args = parser.parse_args()

    project_path = args.path
    if not os.path.isdir(project_path):
        print(f"Error: Directory not found at {project_path}")
        return

    print(f"Auditing dependencies in project at: {project_path}\n")

    found_package_json = False
    found_bower_json = False

    for root, _, files in os.walk(project_path):
        if 'package.json' in files:
            filepath = os.path.join(root, 'package.json')
            for finding in audit_dependencies(filepath, 'npm'):
                print(finding)
            found_package_json = True

        if 'bower.json' in files:
            filepath = os.path.join(root, 'bower.json')
            for finding in audit_dependencies(filepath, 'bower'):
                print(finding)
            found_bower_json = True

    if not found_package_json and not found_bower_json:
        print("No package.json or bower.json found in the specified directory.")

    print("\n--- Audit Complete ---")
    print("Remember to manually verify all dependencies and consider using dedicated security scanning tools.")

if __name__ == "__main__":
    main()
