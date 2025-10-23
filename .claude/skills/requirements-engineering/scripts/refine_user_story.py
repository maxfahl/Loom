#!/usr/bin/env python3

"""
refine_user_story.py

This script assists in refining a user story by prompting for more details,
breaking it down into smaller stories, or generating more specific acceptance criteria.
It reads an existing user story from a Markdown file and provides interactive options
for refinement.

Usage:
    python3 refine_user_story.py --file <user_story_file> [--dry-run]

Examples:
    # Refine an existing user story interactively
    python3 refine_user_story.py --file ./requirements/user-stories/LargeFeature.md

    # Dry-run refinement of a user story
    python3 refine_user_story.py --file ./requirements/user-stories/ComplexLogin.md --dry-run

    # Get help
    python3 refine_user_story.py --help
"""

import argparse
import os
import re
import sys

def get_user_input(prompt, default_value=None):
    """Helper function to get user input with a default value."""
    if default_value:
        return input(f"{prompt} (default: {default_value}): ") or default_value
    return input(f"{prompt}: ")

def parse_user_story(content):
    """Parses a user story Markdown content into its components."""
    story = {"actor": "", "goal": "", "reason": "", "acceptance_criteria": []}
    lines = content.splitlines()

    for line in lines:
        if line.startswith("**As a**"):
            story["actor"] = line.replace("**As a**", "").strip().strip(',')
        elif line.startswith("**I want to**"):
            story["goal"] = line.replace("**I want to**", "").strip()
        elif line.startswith("**so that I can**"):
            story["reason"] = line.replace("**so that I can**", "").strip().strip('.')
        elif line.startswith("- ") or line.startswith("1. ") or line.startswith("Scenario:"):
            story["acceptance_criteria"].append(line.strip())
    return story

def format_user_story(story_name, actor, goal, reason, acceptance_criteria):
    """Formats user story components back into Markdown."""
    ac_str = "\n".join(acceptance_criteria) if acceptance_criteria else "- [ ] (No acceptance criteria defined yet)"
    return f"""
### User Story: {story_name}

**As a** {actor},
**I want to** {goal}
**so that I can** {reason}.

---

#### Acceptance Criteria:

{ac_str}

---

#### Notes:
-
"""

def refine_story_interactively(file_path, story_name, parsed_story):
    """Interactively refines a user story."""
    print(f"\n--- Refining User Story: {story_name} ---")
    print(f"Current Story: As a {parsed_story["actor"]}, I want to {parsed_story["goal"]} so that I can {parsed_story["reason"]}.")

    new_actor = get_user_input(f"New Actor (current: {parsed_story["actor"]})", parsed_story["actor"])
    new_goal = get_user_input(f"New Goal (current: {parsed_story["goal"]})", parsed_story["goal"])
    new_reason = get_user_input(f"New Reason (current: {parsed_story["reason"]})", parsed_story["reason"])

    print("\n--- Current Acceptance Criteria ---")
    for i, ac in enumerate(parsed_story["acceptance_criteria"]):
        print(f"{i+1}. {ac}")

    new_acceptance_criteria = list(parsed_story["acceptance_criteria"])
    print("\n--- Add/Edit Acceptance Criteria (type 'done' to finish, 'skip' to keep current) ---")
    while True:
        action = get_user_input("Add new AC, Edit existing (e.g., 'edit 1'), or 'done'/'skip'?")
        if action.lower() == 'done':
            break
        if action.lower() == 'skip':
            new_acceptance_criteria = list(parsed_story["acceptance_criteria"])
            break
        if action.lower().startswith('edit '):
            try:
                idx = int(action.split(' ')[1]) - 1
                if 0 <= idx < len(new_acceptance_criteria):
                    new_ac_text = get_user_input(f"Edit AC {idx+1} (current: {new_acceptance_criteria[idx]})")
                    new_acceptance_criteria[idx] = new_ac_text
                else:
                    print("Invalid AC number.")
            except ValueError:
                print("Invalid edit command. Use 'edit <number>'.")
        else:
            new_acceptance_criteria.append(f"- {action}")

    refined_content = format_user_story(
        story_name,
        new_actor,
        new_goal,
        new_reason,
        new_acceptance_criteria
    )
    return refined_content

def main():
    parser = argparse.ArgumentParser(
        description="Refine a user story by prompting for more details or generating specific acceptance criteria.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the user story Markdown file to refine."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, prints the refined content to stdout instead of overwriting the file."
    )

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: User story file not found at {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"Error reading file {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    story_name_match = re.search(r'^### User Story: (.+)', original_content, re.MULTILINE)
    story_name = story_name_match.group(1).strip() if story_name_match else os.path.basename(args.file).replace(".md", "")

    parsed_story = parse_user_story(original_content)
    refined_content = refine_story_interactively(args.file, story_name, parsed_story)

    if args.dry_run:
        print("\n--- Refined User Story (Dry Run) ---")
        print(refined_content)
        print("------------------------------------\n")
    else:
        try:
            with open(args.file, "w", encoding='utf-8') as f:
                f.write(refined_content)
            print(f"Successfully refined user story: {args.file}")
        except IOError as e:
            print(f"Error writing refined story to {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
