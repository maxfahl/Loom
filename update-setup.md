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

### Step 2: Validate and Generate Documentation

Your next task is to ensure the project's documentation suite is complete and up-to-date. You will compare the project's `docs/development` directory against the canonical templates and generate any missing documentation from scratch.

1.  **Read Canonical Templates**: Review `prompts/templates/doc-templates.md` to get the complete, authoritative list and content structure of all required documentation files.
2.  **Scan Current Project**: Run `find ./docs/development -maxdepth 2` to list the currently existing documentation files.
3.  **Compare and Generate**: Compare the actual file list with the canonical list. If any standard documentation files are missing, **spawn a `documentation-writer` agent** for each missing file to generate it from the templates.
4.  **Validate Content**: After ensuring all files exist, **spawn the `structure-validator` agent**. This agent will scan the content of the existing files and non-destructively add any missing sections required by the latest specification.

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
