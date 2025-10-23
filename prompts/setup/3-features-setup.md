# 3: Scaffold Project Structure

**Part of**: `setup.md`

## Overview

Your task is to create the standard Loom directory structure for features, epics, and stories, and to initialize the `status.xml` tracking file. You will delegate this entire task to the `project-scaffolder` agent.

## Workflow

1.  **Gather Feature Information**: Based on the project discovery, determine the name of the initial feature and a list of its initial epics (e.g., `epic-1-foundation`).
2.  **Define Feature-Specific Documents**: The complete set of documents required for every feature is:
    *   `PRD.md`
    *   `FEATURE_SPEC.md`
    *   `TECHNICAL_DESIGN.md`
    *   `ARCHITECTURE.md`
3.  **Spawn the `project-scaffolder` Agent**: Launch the agent with instructions to create the full directory tree and all required files.

    ```markdown
    Task: Scaffold the project structure for the feature `[feature-name]`.

    1.  Create the main feature directory: `docs/development/features/[feature-name]/`.
    2.  Inside it, create placeholder files for all required feature-specific documents: `PRD.md`, `FEATURE_SPEC.md`, `TECHNICAL_DESIGN.md`, and `ARCHITECTURE.md`.
    3.  Create the `epics` subdirectory.
    4.  For each epic (`[epic-1-name]`, etc.), create the respective subdirectory inside `epics`.
    5.  Inside each epic's directory, create the `stories` subdirectory and placeholder `DESCRIPTION.md`, `TASKS.md`, and `NOTES.md` files.
    6.  Create and initialize the global `docs/development/status.xml` file, setting `[feature-name]` as the active feature.
    ```
3.  **Verify Output**: After the agent completes, verify that the directory structure and the `status.xml` file have been created correctly.

## Related Files
- `../reference/status-xml.md` - Complete status.xml structure
- `1-discovery.md` - Brownfield analysis is used as input here
- `../templates/story-template.md` - Story file structure

## Next Steps

After this phase, the core project structure is in place, ready for the final verification and commit in the next step (`4-verification.md`).
