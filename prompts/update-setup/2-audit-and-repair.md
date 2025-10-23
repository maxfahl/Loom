# 2: Audit and Repair Documentation Structure

**Part of**: `update-setup.md`

## Overview

Your task is to perform a comprehensive audit of the project's documentation structure. You will identify misplaced, missing, and irrelevant files, and then guide the user through the process of repairing the structure.

**CRITICAL**: You must be crystal clear in your instructions and get the user's explicit permission before moving or deleting any files.

### Part A: Load Canonical Document Lists

First, you must know what the correct structure is. Read the following files to load the two canonical lists of documents:

1.  **Global Documents List**: Read `prompts/setup/2-documentation.md` to get the list of all documents that should exist directly inside `docs/development/`.
2.  **Feature-Specific Documents List**: Read `prompts/setup/3-features-setup.md` to get the list of all documents that **MUST** exist inside every `docs/development/features/[feature-name]/` directory.

### Part B: Audit the Global Directory (`docs/development/`)

Now, scan the `docs/development/` directory (but not its subdirectories) to find misplaced files, irrelevant files, and to ensure all required global documents are present.

1.  **Handle Misplaced and Irrelevant Files**: List all files in `docs/development/` and, for each file, apply the following logic:
    *   **If the file is a valid Global Document**: It is in the correct place. Mark it as 'found'.
    *   **If the file is a known Feature-Specific Document** (e.g., `PRD.md`): It is misplaced. Ask the user how to handle it.
        ```
        I found `[file-name]` in the global `docs/development/` directory. This document should be specific to a feature.

        Which feature does this file belong to? (You can also say 'delete' or 'skip').
        ```
        *   If the user provides a feature name, **move** the file to the correct `docs/development/features/[feature-name]/` directory.
        *   If the user says 'delete', ask for confirmation and delete if confirmed.
        *   If the user says 'skip', do nothing.
    *   **If the file is not in either canonical list**: It is an unknown file. Ask the user for permission before deleting it.
        ```
        I found a file, `[file-name]`, which is not part of the standard Loom framework.

        May I delete this file to keep the project structure clean? (yes/no)
        ```
        *   If the user says yes, delete the file. Otherwise, do nothing.

2.  **Check for Missing Global Documents**: Now, iterate through your canonical list of Global Documents. For any document that was not 'found' in the previous step, you must ask the user for permission to create it.
    *   For each missing global document:
        ```
        I have noticed that the global document `[missing-global-doc.md]` is missing. This file is for [Explain the purpose of the global document, e.g., 'providing a master navigation index for the entire project'].

        May I create a placeholder file for `[missing-global-doc.md]` now? (yes/no)
        ```
        *   **If the user says yes**, spawn a `documentation-writer` agent to create the missing file with boilerplate content in the `docs/development/` directory.
        *   **If the user says no**, acknowledge their choice and move on to the next missing global document.

### Part C: Audit and Repair Each Feature Directory

Now, iterate through each feature in the `docs/development/features/` directory to ensure it is complete.

1.  **For each feature directory**:
    *   **Check for Missing Documents**: Using the canonical list of Feature-Specific Documents, check if all required files are present. If any are missing, perform the detailed conversational flow to explain their purpose and ask for permission to create them.
    *   **Check for Misplaced Global Documents**: Check if any files from the Global Documents list exist inside the feature directory. If you find one (e.g., `PROJECT_SUMMARY.md`), it is misplaced. Ask the user for permission to move it:
        ```
        I found `[file-name]` inside the '[feature-name]' feature directory. This is a global document and should be in `docs/development/`.

        May I move it to the correct location? (yes/no)
        ```
        *   If the user says yes, move the file.
