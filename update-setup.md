Your task is to update an existing Loom setup to the latest version. You will assume the Current Working Directory is the root of the target project. You will use intelligent scripts to synchronize framework files and migrate project structures.

---

### Step 1: Synchronize Core Framework Files

The primary update mechanism is to sync the core files from the Loom source repository. This ensures all agents, commands, and essential configurations are up-to-date.

1.  **Explain the action**: Inform the user that you are about to synchronize the core framework files into the current directory.

2.  **Execute the sync script**: Run the `sync-loom-files.sh` script. You must use the absolute path to the script (which you can determine from the path of this prompt) and provide `.` as the target directory path.

    ```bash
    # The agent must resolve the absolute path to the script
    bash /path/to/loom/scripts/sync-loom-files.sh .
    ```

3.  **Review the output**: Note which files were created or updated.

### Step 2: Validate Feature Documentation

Your next task is to ensure every feature directory in the project is complete. You will scan each feature, identify missing documentation, and ask the user for permission to create placeholder files.

1.  **Identify All Features**: Scan the `docs/development/features/` directory to get a list of all feature subdirectories.
2.  **Get Canonical Document List**: Read `prompts/setup/3-features-setup.md` to get the authoritative list of all documents that must exist within each feature folder (e.g., `PRD.md`, `ARCHITECTURE.md`, etc.).
3.  **Iterate and Verify Each Feature**:
    *   For each feature directory you found, check if all the required documents from the canonical list are present.
    *   If a feature is missing one or more documents, you **must** stop and ask the user:

        ```
        I have noticed that the feature '[feature-name]' is missing the following required document(s): `[list_of_missing_docs.md]`. 

To ensure the project conforms to the latest Loom standards, these files should be present. May I create placeholder files for you now? (yes/no)
        ```
    *   **If the user says yes**, spawn `documentation-writer` agents to create the missing files inside that specific feature's directory.
    *   **If the user says no**, acknowledge and move on to the next feature.
4.  **Validate Content of Existing Files**: After ensuring all files exist for all features, spawn the `structure-validator` agent (defined in `prompts/update-setup/1-structure-validator.md`). This agent will scan the content of all existing documents and non-destructively add any missing sections required by the latest specification.

3.  **Review the output**: The agent will produce a report of all the structural changes it made. Present this summary to the user.

### Step 4: Migrate Story Structure

Older versions of Loom used a different story structure. Run the migration script to move any old story files to their correct new location.

1.  **Explain the action**: Inform the user that you are going to check for and migrate any stories from old locations.

2.  **Execute the migration script**: First, attempt to detect the active feature by parsing `docs/development/status.xml` for the `<is-active-feature>true</is-active-feature>` tag. If you find the feature name, use it. If not, then ask the user for the feature name.

    ```bash
    # Replace [feature-name] with the auto-detected or user-provided name
    bash scripts/migrate-stories.sh [feature-name]
    ```

3.  **Confirm the output**: The script will report if any stories were migrated.

### Step 4: Final Verification

After the scripts have run, the project is up-to-date. Inform the user about the changes and suggest they commit the updates to their version control.

```
✅ Project update complete.

The core agent and command files have been synchronized with the latest version of the Loom framework. The story file structure has also been updated.

Please review and commit the changes to your project.
```
