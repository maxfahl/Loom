# 2: Generate Global Documentation

**Part of**: `setup.md`

## Overview

Your task is to create the **global** suite of standard Loom documentation for the user's project. These are the documents that apply to the entire project, not to a specific feature.

**CRITICAL**: Do NOT create feature-specific documents like `PRD.md` or `ARCHITECTURE.md` in this step. Those are handled in Phase 3.

## Source of Truth

All documentation structures and boilerplate content are defined in: `../templates/doc-templates.md`.

## Creation Workflow

1.  **Read the Templates**: Open and fully understand the contents of `../templates/doc-templates.md`.
2.  **Identify Global Documents**: From the templates, identify the global documents that belong in the `docs/development` directory. This includes:
    *   `INDEX.md`
    *   `START_HERE.md`
    *   `PROJECT_SUMMARY.md`
    *   `YOLO_MODE.md`
    *   `CODE_REVIEW_PRINCIPLES.md`
    *   `SECURITY_REVIEW_CHECKLIST.md`
    *   `DESIGN_PRINCIPLES.md`
3.  **Generate Each File**: For each of the **global** documents listed above, **spawn a dedicated `documentation-writer` agent** tasked with creating that specific file in the user's `docs/development` directory.
4.  **Use Parallel Execution**: To be efficient, spawn the `documentation-writer` agents in parallel batches.
5.  **Customize Content**: Where appropriate, use the information gathered during the Discovery phase (`1-discovery.md`) to customize the generated documents with the project's name, technology stack, and other specifics.

