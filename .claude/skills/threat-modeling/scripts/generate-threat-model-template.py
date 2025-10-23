#!/usr/bin/env python3

import argparse
import os
import datetime
import yaml

def generate_markdown_template(project_name, author, date, components, output_file):
    """Generates a basic threat model in Markdown format."""
    template = f"""# Threat Model for {project_name}

## 1. Project Information
*   **Project Name:** {project_name}
*   **Author:** {author}
*   **Date:** {date}
*   **Version:** 1.0
*   **Description:** Initial threat model for the {project_name} project.

## 2. System Overview
Describe the system's purpose, key functionalities, and overall architecture.

## 3. Scope
Define what is in scope and out of scope for this threat model.

## 4. Data Flow Diagram (DFD) Overview
Provide a high-level description or reference to the DFD.

## 5. Assets
Identify critical assets that need protection (e.g., sensitive data, user accounts, intellectual property).

## 6. Entry Points / Trust Boundaries
List all external interfaces, APIs, and trust boundaries.

## 7. Identified Threats (STRIDE per component)

### Component: {", ".join(components) if components else "Core System"}
*   **Spoofing (S):**
    *   Threat:
    *   Countermeasure:
*   **Tampering (T):**
    *   Threat:
    *   Countermeasure:
*   **Repudiation (R):**
    *   Threat:
    *   Countermeasure:
*   **Information Disclosure (I):**
    *   Threat:
    *   Countermeasure:
*   **Denial of Service (D):**
    *   Threat:
    *   Countermeasure:
*   **Elevation of Privilege (E):**
    *   Threat:
    *   Countermeasure:

## 8. Risk Assessment
Prioritize identified threats based on likelihood and impact.

## 9. Remediation Plan
Outline actions to mitigate identified risks.

## 10. Review and Approval
*   **Reviewers:**
*   **Approval Date:**
"""
    with open(output_file, 'w') as f:
        f.write(template)
    print(f"Markdown threat model template generated at: {output_file}")

def generate_yaml_template(project_name, author, date, components, output_file):
    """Generates a basic threat model in YAML format."""
    threat_model_data = {
        "project_info": {
            "name": project_name,
            "author": author,
            "date": date,
            "version": "1.0",
            "description": f"Initial threat model for the {project_name} project."
        },
        "system_overview": "Describe the system's purpose, key functionalities, and overall architecture.",
        "scope": {
            "in_scope": [],
            "out_of_scope": []
        },
        "dfd_overview": "Provide a high-level description or reference to the DFD.",
        "assets": [],
        "entry_points_trust_boundaries": [],
        "components": []
    }

    for comp in components:
        threat_model_data["components"].append({
            "name": comp,
            "threats": {
                "spoofing": {"threat": "", "countermeasure": ""},
                "tampering": {"threat": "", "countermeasure": ""},
                "repudiation": {"threat": "", "countermeasure": ""},
                "information_disclosure": {"threat": "", "countermeasure": ""},
                "denial_of_service": {"threat": "", "countermeasure": ""},
                "elevation_of_privilege": {"threat": "", "countermeasure": ""},
            }
        })
    if not components:
         threat_model_data["components"].append({
            "name": "Core System",
            "threats": {
                "spoofing": {"threat": "", "countermeasure": ""},
                "tampering": {"threat": "", "countermeasure": ""},
                "repudiation": {"threat": "", "countermeasure": ""},
                "information_disclosure": {"threat": "", "countermeasure": ""},
                "denial_of_service": {"threat": "", "countermeasure": ""},
                "elevation_of_privilege": {"threat": "", "countermeasure": ""},
            }
        })


    threat_model_data["risk_assessment"] = "Prioritize identified threats based on likelihood and impact."
    threat_model_data["remediation_plan"] = "Outline actions to mitigate identified risks."
    threat_model_data["review_and_approval"] = {
        "reviewers": [],
        "approval_date": ""
    }

    with open(output_file, 'w') as f:
        yaml.dump(threat_model_data, f, sort_keys=False, indent=2)
    print(f"YAML threat model template generated at: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a basic threat model template (Markdown or YAML).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-n", "--project-name",
        default="MyProject",
        help="Name of the project for the threat model."
    )
    parser.add_argument(
        "-a", "--author",
        default=os.getenv("USER", "Anonymous"),
        help="Author of the threat model."
    )
    parser.add_argument(
        "-f", "--format",
        choices=["md", "yaml"],
        default="md",
        help="Output format for the threat model template (md or yaml)."
    )
    parser.add_argument(
        "-o", "--output",
        default="threat_model_template",
        help="Output file name (without extension). Default: threat_model_template"
    )
    parser.add_argument(
        "-c", "--components",
        nargs="*",
        help="List of key components in the system (e.g., 'Frontend API Database')."
    )

    args = parser.parse_args()

    today = datetime.date.today().strftime("%Y-%m-%d")
    output_filename = f"{args.output}.{args.format}"

    if args.format == "md":
        generate_markdown_template(args.project_name, args.author, today, args.components, output_filename)
    elif args.format == "yaml":
        generate_yaml_template(args.project_name, args.author, today, args.components, output_filename)

if __name__ == "__main__":
    main()
