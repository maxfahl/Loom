# 3: Scaffold Project Structure

**Part of**: `setup.md`

## Overview

Your task is to create the standard Loom directory structure for features, epics, and stories, and to initialize the `status.xml` tracking file. You will delegate this entire task to the `project-scaffolder` agent.

## Workflow

1.  **Gather Feature Information**: Based on the `PRD.md` created in the previous step, determine the name of the initial feature and a list of its initial epics (e.g., `epic-1-foundation`, `epic-2-core-features`).
2.  **Spawn the `project-scaffolder` Agent**: Launch the `project-scaffolder` agent with instructions to create the full directory tree for the initial feature and all its epics, and to create the main `status.xml` file.

    ```markdown
    Task: Scaffold the project structure for the feature `[feature-name]`.

    1.  Create the full Loom directory structure, including `docs/development/features/[feature-name]/epics/`.
    2.  For the epics `[epic-1-name]`, `[epic-2-name]`, create the respective subdirectories.
    3.  Inside each epic's directory, create the `stories` subdirectory and placeholder `DESCRIPTION.md`, `TASKS.md`, and `NOTES.md` files.
    4.  Create and initialize the main `docs/development/status.xml` file, setting `[feature-name]` as the active feature.
    ```
3.  **Verify Output**: After the agent completes, verify that the directory structure and the `status.xml` file have been created correctly.

## Related Files
- `../reference/status-xml.md` - Complete status.xml structure
- `1-discovery.md` - Brownfield analysis is used as input here
- `../templates/story-template.md` - Story file structure

## Next Steps

After this phase, the core project structure is in place, ready for the final verification and commit in the next step (`4-verification.md`).
