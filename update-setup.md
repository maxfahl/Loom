Your task is to update an existing Loom setup in a user's project to the latest version. You will use an intelligent synchronization script to copy the latest framework files and a migration script to update the project's story structure.

---

### Step 1: Identify Target Project

First, confirm the absolute path to the user's project directory that needs to be updated.

### Step 2: Synchronize Core Framework Files

The primary update mechanism is to sync the core files from the Loom source repository. This ensures all agents, commands, and essential configurations are up-to-date.

1.  **Explain the action**: Inform the user that you are about to synchronize the core framework files to update their setup.

2.  **Execute the sync script**: Run the `sync-loom-files.sh` script, providing the target project directory path.

    ```bash
    bash scripts/sync-loom-files.sh /path/to/user/project
    ```

3.  **Review the output**: Note which files were created or updated.

### Step 3: Validate & Migrate Project-Specific Files

Next, you will run a validation agent to ensure the user's project-specific files (like `status.xml` and `PRD.md`) are structurally compliant with the latest Loom specification. This is a non-destructive operation that only adds missing sections or tags.

1.  **Explain the action**: Inform the user that you are about to scan their configuration and documentation to update their structure without altering their content.

2.  **Execute the Structure Validator Agent**: Run the agent defined in `prompts/update-setup/1-structure-validator.md`. This agent will read the user's files, compare them to the canonical templates, and insert any missing structural elements.

3.  **Review the output**: The agent will produce a report of all the structural changes it made. Present this summary to the user.

### Step 4: Migrate Story Structure

Older versions of Loom used a different story structure. Run the migration script to move any old story files to their correct new location within the `epics` directory structure.

1.  **Explain the action**: Inform the user that you are going to check for and migrate any stories from old locations.

2.  **Execute the migration script**: Run the `migrate-stories.sh` script. You will need to get the feature name from the user or detect it from their `status.xml` file.

    ```bash
    # You may need to ask the user for the feature name
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
