Your task is to update an existing Loom setup to the latest version. You will assume the Current Working Directory is the root of the target project. You will use intelligent scripts to synchronize framework files and migrate project structures.

---

### Step 1: Synchronize Core Framework Files

Synchronize core framework files (agents, commands, skills) from the Loom repository. This ensures all agents, commands, and essential configurations are up-to-date.

1.  **Explain the action**: Inform the user that you are about to synchronize the core framework files into the current directory.

2.  **Resolve Loom repository path**: You know the full path to this prompt file because the user provided it when invoking this prompt (e.g., `/path/to/loom/update-setup.md`). Extract the directory portion to get LOOM_ROOT.

3.  **Execute the sync script**: Run the `sync-loom-files.sh` script using the resolved LOOM_ROOT path.

    ```bash
    # LOOM_ROOT is the directory containing this prompt file (update-setup.md)
    # Example: if this prompt is at /Users/dev/loom/update-setup.md, then LOOM_ROOT=/Users/dev/loom
    LOOM_ROOT="[directory-of-this-prompt-file]"

    # Execute sync script
    bash "$LOOM_ROOT/scripts/sync-loom-files.sh" .
    ```

4.  **Review the output**: Note which files were created or updated.

### Step 2: Audit and Repair Documentation Structure

Your next task is to perform a comprehensive audit and repair of the project's documentation structure.

1.  **Audit File Placement and Completeness**: Follow the detailed instructions in `prompts/update-setup/2-audit-and-repair.md`. This sub-prompt will guide you through identifying and fixing misplaced, missing, and irrelevant documentation files for both the global and feature-specific scopes.

2.  **Validate File Content**: After the file structure has been repaired, follow the instructions in `prompts/update-setup/1-structure-validator.md`. This will guide you in using the `structure-validator` agent to non-destructively update the content of existing files to match the latest Loom specifications.

### Step 3: Update or Deploy CLAUDE.md

Update (or create) the `CLAUDE.md` file using the `deploy-claude-md.sh` script. This script intelligently handles existing files with marker-based updates.

1. **Gather project information** (from existing docs if available):
   - Project name (from README.md or package.json)
   - Tech stack (from existing CLAUDE.md or PROJECT_SUMMARY.md)
   - TDD level (check existing CLAUDE.md or infer from tests: STRICT/RECOMMENDED/OPTIONAL)
   - Preview command (from package.json scripts or existing docs)
   - Test command (from package.json scripts or existing docs)
   - Build command (from package.json scripts or existing docs)

2. **Run the deployment script**:

   Execute the `scripts/deploy-claude-md.sh` script with all gathered parameters. The script will intelligently handle existing files, markers, and updates. Use the same `LOOM_ROOT` path you determined in Step 1. The first argument must be the absolute path to the current working directory (the target project).

   ```bash
   # Get absolute path to current working directory (the target project)
   TARGET_PROJECT_DIR=$(pwd)

   # Use LOOM_ROOT from Step 1 (absolute path to Loom repository)
   # Execute deployment script
   bash "$LOOM_ROOT/scripts/deploy-claude-md.sh" \
     "$TARGET_PROJECT_DIR" \
     "Project Name" \
     "Tech Stack Description" \
     "TDD_LEVEL" \
     "preview command" \
     "test command" \
     "build command"
   ```

3. **Review script output**:

   The script will report what action it took (created new file, updated existing file with markers, or created LOOM_FRAMEWORK.md). Inform the user of the outcome.

### Step 4: Migrate Story Structure

Older versions of Loom used a different story structure. Run the migration script to move any old story files to their correct new location.

1.  **Explain the action**: Inform the user that you are going to check for and migrate any stories from old locations.

2.  **Execute the migration script**: First, attempt to detect the active feature by parsing `docs/development/status.xml` (in the user project) for the `<is-active-feature>true</is-active-feature>` tag. If you find the feature name, use it. If not, then ask the user for the feature name. Use the same `LOOM_ROOT` path from Step 1.

    ```bash
    # Use LOOM_ROOT from Step 1 (absolute path to Loom repository)
    # Execute migration script (replace [feature-name] with actual feature)
    bash "$LOOM_ROOT/scripts/migrate-stories.sh" [feature-name]
    ```

3.  **Confirm the output**: The script will report if any stories were migrated.

### Step 5: Final Verification

After the scripts have run, the project is up-to-date. Inform the user about the changes and suggest they commit the updates to their version control.

```
✅ Project update complete.

The core agent and command files have been synchronized with the latest version of the Loom framework. The story file structure has also been updated.

Please review and commit the changes to your project.
```
