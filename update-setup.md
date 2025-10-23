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

### Step 2: Audit and Repair Documentation Structure

Your next task is to perform a comprehensive audit and repair of the project's documentation structure.

1.  **Audit File Placement and Completeness**: Follow the detailed instructions in `prompts/update-setup/2-audit-and-repair.md`. This sub-prompt will guide you through identifying and fixing misplaced, missing, and irrelevant documentation files for both the global and feature-specific scopes.

2.  **Validate File Content**: After the file structure has been repaired, follow the instructions in `prompts/update-setup/1-structure-validator.md`. This will guide you in using the `structure-validator` agent to non-destructively update the content of existing files to match the latest Loom specifications.

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
