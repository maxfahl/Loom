# 3: Scaffold Feature Structure

**Part of**: `setup.md`

## Overview

Your task is to create the standard Loom directory structure for a feature, including its epics, stories, and all required feature-specific documentation. You will also initialize the global `status.xml` tracking file. You will delegate this entire task to the `project-scaffolder` agent.

**Note**: Global documentation (`INDEX.md`, `PROJECT_SUMMARY.md`, etc.) was created in the previous phase.

## Workflow

1.  **Gather Feature Information**: Based on the project discovery, determine the name of the initial feature and a list of its initial epics (e.g., `epic-1-foundation`).

2.  **Define Canonical Feature Documents**: This is the authoritative list of documents that **MUST** exist inside every feature directory (`docs/development/features/[feature-name]/`).
    *   `PRD.md` (Product Requirements Document)
    *   `FEATURE_SPEC.md` (Detailed feature specifications)
    *   `TECHNICAL_DESIGN.md` (The technical blueprint for the feature)
    *   `ARCHITECTURE.md` (System design and patterns relevant to the feature)
    *   `DESIGN_SYSTEM.md` (UI/UX guidelines for the feature)
    *   `DEVELOPMENT_PLAN.md` (TDD workflow and timeline for the feature)

3.  **Spawn the `project-scaffolder` Agent**: Launch the agent with instructions to create the full directory tree and all required files.

    ```markdown
    Task: Scaffold the project structure for the feature `[feature-name]`.

    1.  Create the main feature directory: `docs/development/features/[feature-name]/`.
    2.  Inside it, create placeholder files for all required feature-specific documents as defined in `prompts/setup/3-features-setup.md`.
    3.  Create the `epics` subdirectory.
    4.  For each epic (`[epic-1-name]`, etc.), create the respective subdirectory inside `epics`.
    5.  Inside each epic's directory, create the `stories` subdirectory and placeholder `DESCRIPTION.md`, `TASKS.md`, and `NOTES.md` files.
    6.  Create and initialize the global `docs/development/status.xml` file, setting `[feature-name]` as the active feature.
    ```

4.  **Verify Output**: After the agent completes, verify that the directory structure and the `status.xml` file have been created correctly.

## Related Files
- `../reference/status-xml.md` - Complete status.xml structure
- `1-discovery.md` - Brownfield analysis is used as input here
- `../templates/story-template.md` - Story file structure

## Next Steps

After this phase, the core project structure is in place, ready for the final verification and commit in the next step (`4-verification.md`).
