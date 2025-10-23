#!/usr/bin/env python3

"""
generate_requirement_template.py

This script generates a new requirement file (e.g., User Story, Functional Requirement, Non-Functional Requirement)
based on a chosen template. It prompts the user for key details and outputs a Markdown file,
ensuring consistency and saving time in documentation.

Usage:
    python3 generate_requirement_template.py --type <type> --name <name> [--output-dir <dir>] [--dry-run]

Examples:
    # Generate a User Story
    python3 generate_requirement_template.py --type user-story --name "UserLogin"

    # Generate a Functional Requirement in a specific directory
    python3 generate_requirement_template.py --type functional-requirement --name "PaymentProcessing" --output-dir ./requirements/functional

    # Generate a Non-Functional Requirement with dry-run
    python3 generate_requirement_template.py --type nfr --name "SystemPerformance" --dry-run

    # Get help
    python3 generate_requirement_template.py --help
"""

import argparse
import os
import sys
from datetime import datetime

def get_user_input(prompt, default_value=None):
    """Helper function to get user input with a default value."""
    if default_value:
        return input(f"{prompt} (default: {default_value}): ") or default_value
    return input(f"{prompt}: ")

def generate_user_story(name):
    """Generates content for a User Story."""
    print("\n--- User Story Details ---")
    actor = get_user_input("As a (e.g., registered user)", "User")
    goal = get_user_input("I want to (e.g., log in securely)")
    reason = get_user_input("so that I can (e.g., access my dashboard)")
    priority = get_user_input("Priority (e.g., Must Have, Should Have, Could Have)", "Should Have")
    status = get_user_input("Status (e.g., Draft, Approved, In Progress)", "Draft")

    acceptance_criteria = []
    print("\n--- Acceptance Criteria (type 'done' to finish) ---")
    while True:
        ac = get_user_input(f"Acceptance Criterion {len(acceptance_criteria) + 1}")
        if ac.lower() == 'done':
            break
        acceptance_criteria.append(f"- {ac}")

    ac_str = "\n".join(acceptance_criteria) if acceptance_criteria else "- [ ] (No acceptance criteria defined yet)"

    content = f"""### User Story: {name}

**As a** {actor},
**I want to** {goal}
**so that I can** {reason}.

**Priority:** {priority}
**Status:** {status}
**Date Created:** {datetime.now().strftime("%Y-%m-%d")}

---

#### Acceptance Criteria:

{ac_str}

---

#### Notes:
-
"""
    return content

def generate_functional_requirement(name):
    """Generates content for a Functional Requirement."""
    print("\n--- Functional Requirement Details ---")
    description = get_user_input("Description (one-line summary)")
    input_data = get_user_input("Input (e.g., User credentials, API request body)", "N/A")
    output_data = get_user_input("Output (e.g., Success message, JSON response)", "N/A")
    pre_conditions = get_user_input("Pre-conditions (comma-separated)", "N/A")
    post_conditions = get_user_input("Post-conditions (comma-separated)", "N/A")
    priority = get_user_input("Priority (e.g., High, Medium, Low)", "Medium")
    status = get_user_input("Status (e.g., Draft, Approved, In Progress)", "Draft")

    content = f"""### Functional Requirement: {name}

**FR-ID:** FR-{name.replace(' ', '')[:5].upper()}-{datetime.now().strftime("%H%M%S")}

**Description:** {description}

**Priority:** {priority}
**Status:** {status}
**Date Created:** {datetime.now().strftime("%Y-%m-%d")}

---

**Input:** {input_data}
**Output:** {output_data}

**Pre-conditions:** {pre_conditions}
**Post-conditions:** {post_conditions}

---

#### Notes:
-
"""
    return content

def generate_nfr(name):
    """Generates content for a Non-Functional Requirement."""
    print("\n--- Non-Functional Requirement Details ---")
    category = get_user_input("Category (e.g., Performance, Security, Usability)", "Performance")
    description = get_user_input("Description (measurable statement)")
    metric = get_user_input("Measurement Metric (e.g., Response Time, Availability %)", "N/A")
    target = get_user_input("Target Value (e.g., < 2 seconds, 99.9%)", "N/A")
    conditions = get_user_input("Conditions (e.g., under 100 concurrent users)", "N/A")
    priority = get_user_input("Priority (e.g., Critical, High, Medium)", "High")
    status = get_user_input("Status (e.g., Draft, Approved, In Progress)", "Draft")

    content = f"""### Non-Functional Requirement: {name}

**NFR-ID:** NFR-{category.replace(' ', '')[:5].upper()}-{datetime.now().strftime("%H%M%S")}

**Category:** {category}
**Description:** {description}

**Priority:** {priority}
**Status:** {status}
**Date Created:** {datetime.now().strftime("%Y-%m-%d")}

---

**Measurement Metric:** {metric}
**Target Value:** {target}
**Conditions:** {conditions}

---

#### Notes:
-
"""
    return content

def main():
    parser = argparse.ArgumentParser(
        description="Generate a new requirement file based on a chosen template.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--type",
        choices=["user-story", "functional-requirement", "nfr"],
        required=True,
        help="Type of requirement to generate (user-story, functional-requirement, nfr)."
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Name of the requirement (e.g., UserLogin, PaymentProcessing)."
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to save the generated requirement file. Defaults to current directory."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, prints the content to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    file_name = f"{args.name.replace(' ', '-').lower()}.md"
    output_path = os.path.join(args.output_dir, file_name)

    content = ""
    if args.type == "user-story":
        content = generate_user_story(args.name)
    elif args.type == "functional-requirement":
        content = generate_functional_requirement(args.name)
    elif args.type == "nfr":
        content = generate_nfr(args.name)

    if args.dry_run:
        print("\n--- Generated Content (Dry Run) ---")
        print(content)
        print("-----------------------------------\n")
    else:
        os.makedirs(args.output_dir, exist_ok=True)
        try:
            with open(output_path, "w") as f:
                f.write(content)
            print(f"Successfully generated {args.type} '{args.name}' at: {output_path}")
        except IOError as e:
            print(f"Error writing file to {output_path}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
