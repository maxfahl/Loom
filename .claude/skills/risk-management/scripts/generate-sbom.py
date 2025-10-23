import argparse
import json
import os
import re
import sys
from datetime import datetime

# ANSI escape codes for colored output
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

def print_color(color, message):
    print(f"{color}{message}{COLOR_RESET}")

def parse_package_json(file_path):
    """Parses package.json for dependencies."""
    components = []
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        for dep_type in ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']:
            if dep_type in data:
                for name, version in data[dep_type].items():
                    # Remove common version prefixes like ^, ~, >=, <=
                    clean_version = re.sub(r'[~^<=>]+', '', version).strip()
                    components.append({
                        "name": name,
                        "version": clean_version,
                        "type": "npm",
                        "scope": dep_type.replace('Dependencies', ''),
                        "license": "Unknown" # License info often in package-lock.json or requires lookup
                    })
    except Exception as e:
        print_color(COLOR_RED, f"Error parsing {file_path}: {e}")
    return components

def parse_requirements_txt(file_path):
    """Parses requirements.txt for dependencies."""
    components = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('-r'):
                    continue
                match = re.match(r'^([a-zA-Z0-9_.-]+)(?:[<=>~!]=)([0-9a-zA-Z_.-]+)', line)
                if match:
                    name, version = match.groups()
                    components.append({
                        "name": name,
                        "version": version,
                        "type": "pip",
                        "scope": "required",
                        "license": "Unknown"
                    })
                else:
                    # Handle cases like 'package-name' without a version
                    components.append({
                        "name": line,
                        "version": "Any",
                        "type": "pip",
                        "scope": "required",
                        "license": "Unknown"
                    })
    except Exception as e:
        print_color(COLOR_RED, f"Error parsing {file_path}: {e}")
    return components

def generate_sbom(project_path, output_file, dry_run):
    """Generates a basic SBOM for the given project path."""
    print_color(COLOR_YELLOW, f"Generating SBOM for project: {project_path}")
    all_components = []

    # Scan for Node.js projects
    package_json_path = os.path.join(project_path, 'package.json')
    if os.path.exists(package_json_path):
        print_color(COLOR_BLUE, f"Found {package_json_path}")
        all_components.extend(parse_package_json(package_json_path))

    # Scan for Python projects
    requirements_txt_path = os.path.join(project_path, 'requirements.txt')
    if os.path.exists(requirements_txt_path):
        print_color(COLOR_BLUE, f"Found {requirements_txt_path}")
        all_components.extend(parse_requirements_txt(requirements_txt_path))

    # Basic SBOM structure (CycloneDX or SPDX-lite could be used for more formal output)
    sbom = {
        "SPDXID": "SPDXRef-DOCUMENT",
        "spdxVersion": "SPDX-2.3",
        "creationInfo": {
            "created": datetime.utcnow().isoformat() + "Z",
            "creators": ["Tool: generate-sbom.py", "Organization: Your Organization Name"]
        },
        "name": os.path.basename(project_path),
        "dataLicense": "CC0-1.0",
        "documentNamespace": f"https://spdx.org/spdxdocs/{os.path.basename(project_path)}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "packages": []
    }

    for i, comp in enumerate(all_components):
        package_entry = {
            "SPDXID": f"SPDXRef-Package-{i}",
            "name": comp["name"],
            "versionInfo": comp["version"],
            "supplier": "NOASSERTION", # Could be parsed from lock files or looked up
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "licenseConcluded": comp["license"],
            "licenseDeclared": comp["license"],
            "externalRefs": [
                {
                    "referenceCategory": "PACKAGE_MANAGER",
                    "referenceLocator": f"{comp["type"]}:{comp["name"]}@{comp["version"]}",
                    "referenceType": "purl"
                }
            ]
        }
        sbom["packages"].append(package_entry)

    sbom_content = json.dumps(sbom, indent=2)

    if dry_run:
        print_color(COLOR_YELLOW, "\n--- Dry Run SBOM Output ---")
        print(sbom_content)
        print_color(COLOR_YELLOW, "--- End Dry Run ---")
    else:
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(sbom_content)
                print_color(COLOR_GREEN, f"SBOM successfully written to {output_file}")
            except Exception as e:
                print_color(COLOR_RED, f"Error writing SBOM to {output_file}: {e}")
                sys.exit(1)
        else:
            print_color(COLOR_GREEN, "\n--- Generated SBOM ---")
            print(sbom_content)
            print_color(COLOR_GREEN, "--- End SBOM ---")

    print_color(COLOR_GREEN, "SBOM generation complete.")

def main():
    parser = argparse.ArgumentParser(
        description="Generate a basic Software Bill of Materials (SBOM) for a project.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-p", "--path",
        default=".",
        help="Project root directory (default: current directory)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path for the SBOM (e.g., sbom.json). If not specified, prints to stdout."
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Show the SBOM output without writing to a file."
    )

    args = parser.parse_args()

    project_path = os.path.abspath(args.path)
    if not os.path.isdir(project_path):
        print_color(COLOR_RED, f"Error: Project path '{project_path}' does not exist or is not a directory.")
        sys.exit(1)

    generate_sbom(project_path, args.output, args.dry_run)

if __name__ == "__main__":
    main()
