#!/usr/bin/env python3

import argparse
import os
from datetime import datetime

def collect_feedback(retro_name: str, output_file: str, verbose: bool = False):
    """
    Collects anonymous feedback for a retrospective and saves it to a markdown file.

    Args:
        retro_name (str): The name of the retrospective.
        output_file (str): Path to the output markdown file.
        verbose (bool): If True, print detailed processing messages.
    """
    if verbose:
        print(f"Collecting feedback for retrospective: '{retro_name}'")

    feedback = {
        "went_well": [],
        "could_improve": [],
        "action_items": []
    }

    print(f"\n--- Retrospective Feedback for '{retro_name}' ---")
    print("Enter your feedback. Type 'done' or leave empty and press Enter to finish each section.")

    # What went well?
    print("\nWhat went well? (Type 'done' to finish)")
    while True:
        item = input("> ").strip()
        if item.lower() == 'done' or not item:
            break
        feedback["went_well"].append(item)

    # What could be improved?
    print("\nWhat could be improved? (Type 'done' to finish)")
    while True:
        item = input("> ").strip()
        if item.lower() == 'done' or not item:
            break
        feedback["could_improve"].append(item)

    # Action items?
    print("\nAny action items? (Type 'done' to finish)")
    while True:
        item = input("> ").strip()
        if item.lower() == 'done' or not item:
            break
        feedback["action_items"].append(item)

    report_content = f"# Retrospective Feedback: {retro_name}\n\n"
    report_content += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    report_content += "## What Went Well?\n\n"
    if feedback["went_well"]:
        for item in feedback["went_well"]:
            report_content += f"- {item}\n"
    else:
        report_content += "_No feedback provided for this section._\n"
    report_content += "\n"

    report_content += "## What Could Be Improved?\n\n"
    if feedback["could_improve"]:
        for item in feedback["could_improve"]:
            report_content += f"- {item}\n"
    else:
        report_content += "_No feedback provided for this section._\n"
    report_content += "\n"

    report_content += "## Action Items\n\n"
    if feedback["action_items"]:
        for item in feedback["action_items"]:
            report_content += f"- [ ] {item}\n"
    else:
        report_content += "_No feedback provided for this section._\n"
    report_content += "\n"

    try:
        with open(output_file, 'w') as f:
            f.write(report_content)
        print(f"\nRetrospective feedback successfully saved to '{output_file}'")
    except Exception as e:
        print(f"Error writing feedback to file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Collects anonymous feedback for a retrospective and saves it to a markdown file.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('retro_name', help='The name of the retrospective (e.g., "Sprint 5 Retro").')
    parser.add_argument('-o', '--output-file', default=None,
                        help='Path to the output markdown file. Defaults to 'retro_feedback_<retro_name_slug>.md'.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output.')

    args = parser.parse_args()

    if not args.output_file:
        # Sanitize retro_name for filename
        safe_retro_name = "_".join(args.retro_name.lower().split())
        args.output_file = f"retro_feedback_{safe_retro_name}.md"

    collect_feedback(
        retro_name=args.retro_name,
        output_file=args.output_file,
        verbose=args.verbose
    )

if __name__ == '__main__':
    main()
