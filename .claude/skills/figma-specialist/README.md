# Figma Specialist Skill Package

This package provides Claude with the knowledge and tools to effectively interact with Figma programmatically. It focuses on automating design workflows, extracting design data, synchronizing design tokens, and understanding Figma plugin development.

## Overview

The `figma-specialist` skill enables Claude to:

-   **Automate Design Tasks**: Leverage the Figma API to streamline repetitive design-related operations.
-   **Extract Design Data**: Fetch and parse design information, such as file structures, components, and styles.
-   **Synchronize Design Tokens**: Keep design decisions in Figma in sync with development codebases using automated scripts.
-   **Understand Figma Plugins**: Grasp the fundamentals of Figma plugin architecture and development.
-   **Maintain Design System Hygiene**: Utilize linting tools to ensure Figma files adhere to best practices.

## Contents

-   `SKILL.md`: The main instruction file detailing Claude's core knowledge, guidance, and activation triggers for Figma-related tasks.
-   `examples/`: Contains practical code examples demonstrating how to interact with the Figma API and build basic plugins.
-   `patterns/`: Documents common patterns and best practices for structuring Figma files and using the API effectively.
-   `scripts/`: A collection of automation scripts (Python) designed to solve real-world pain points in Figma workflows.
-   `README.md`: This human-readable documentation providing an overview of the skill package.

## Getting Started

To utilize the scripts within this package, you will need:

1.  **Figma Personal Access Token**: Obtain a token from your Figma account settings (Developer settings).
2.  **Figma File Key**: The unique identifier for your Figma file, found in the URL (e.g., `https://www.figma.com/file/FILE_KEY/Your-Design-File`).
3.  **Python 3**: Ensure Python 3 is installed on your system.
4.  **Required Python Libraries**: Install dependencies as specified in each script (e.g., `requests`).

Refer to the `SKILL.md` for detailed guidance on when and how Claude should activate and apply this skill.

## Custom Scripts

The `scripts/` directory contains the following valuable automation tools:

-   `figma-token-sync.py`: Extracts design variables from Figma and converts them into a structured JSON format.
-   `figma-asset-extractor.py`: Exports specific assets (icons, images) from a Figma file in various formats.
-   `figma-linter.py`: Analyzes Figma file structure against best practices and generates a report.

Each script includes detailed comments, usage examples, and command-line arguments for easy execution and configuration.
