# Web Accessibility (WCAG) Skill

This skill provides comprehensive guidance and automation tools for implementing Web Content Accessibility Guidelines (WCAG) in web applications. It aims to help developers build inclusive digital experiences that are accessible to all users, including those with disabilities.

## Features

-   **Core WCAG Principles:** Detailed explanation of Perceivable, Operable, Understandable, and Robust (POUR) principles.
-   **Semantic HTML & ARIA:** Best practices for using HTML5 and WAI-ARIA to enhance accessibility.
-   **Keyboard Navigation & Focus Management:** Guidance on ensuring full keyboard operability and visible focus indicators.
-   **Color Contrast:** WCAG requirements and tools for checking color contrast ratios.
-   **Anti-Patterns & Solutions:** Identifies common accessibility mistakes and provides corrected code examples.
-   **Code Review Checklist:** A practical checklist for reviewing code from an accessibility perspective.
-   **Automation Scripts:** A suite of scripts to automate accessibility testing and validation tasks.

## Getting Started

To utilize this skill, refer to the `SKILL.md` file for detailed instructions, core knowledge, and best practices. Explore the `examples/` directory for practical code implementations and the `scripts/` directory for automation tools.

## Automation Scripts

The `scripts/` directory contains the following utilities:

-   **`audit-a11y.py`:** Automates running an accessibility audit using `axe-core` via Playwright, generating a detailed report.
-   **`check-alt-text.py`:** Scans HTML/TSX files for `<img>` tags with missing or generic `alt` attributes.
-   **`color-contrast-checker.py`:** Verifies color contrast ratios from CSS files or direct color inputs against WCAG standards.
-   **`aria-linter.py`:** Checks for common misuses or missing required ARIA attributes in HTML/TSX files.

Each script includes detailed usage instructions, error handling, and configuration options.
