Your task is to set up or update the Loom agentic development framework in the user's project. You will assume the Current Working Directory is the root of the target project.

---

## Mode Detection

First, determine whether this is a new setup or an update to an existing Loom project.

**Check for existing Loom installation**:

```bash
# Check if status.xml exists (indicates existing Loom project)
if [ -f "docs/development/status.xml" ]; then
    echo "EXISTING_LOOM_PROJECT"
else
    echo "NEW_LOOM_PROJECT"
fi
```

**Based on the result**:

- If `EXISTING_LOOM_PROJECT`: Execute **Update Mode** (see below)
- If `NEW_LOOM_PROJECT`: Execute **Setup Mode** (see below)

---

# Setup Mode - New Loom Installation

Execute this workflow when `docs/development/status.xml` does NOT exist.

---

### Phase 1: Discovery & Analysis

First, you must understand the project in the Current Working Directory. Follow the instructions in `prompts/setup/1-discovery.md` to autonomously analyze the project.

**CRITICAL**: The Current Working Directory is the `TARGET_DIR` for the synchronization script.

### Phase 2: Documentation Creation

Next, based on the information gathered in Phase 1, create the project-specific documentation by following the instructions in `prompts/setup/2-documentation.md`.

### Phase 3: Synchronize Framework Files

Synchronize core framework files (agents, commands, skills) from the Loom repository.

1.  **Ask user for sync preference**: Before synchronizing files, ask the user:

    ```
    How would you like to sync framework files (agents, commands, skills)?

    1. FULL REPLACEMENT (Recommended for clean installs)
       - Completely replaces .claude/agents/, .claude/commands/, .claude/skills/
       - Fastest option (uses cp)
       - Removes any custom modifications you made to these folders

    2. INTELLIGENT SYNC (Recommended if you have custom agents/commands)
       - Uses rsync to merge changes
       - Preserves your custom files
       - Updates existing Loom files
       - Slower but safer for customized setups

    Choose: [1] Full Replacement or [2] Intelligent Sync
    ```

2.  **Resolve Loom repository path**: You know the full path to this prompt file because the user provided it when invoking this prompt (e.g., `/path/to/loom/loom.md`). Extract the directory portion to get LOOM_ROOT.

3.  **Execute sync based on user choice**:

    **Option 1 - Full Replacement (Fast)**:

    ```bash
    # LOOM_ROOT is the directory containing this prompt file (loom.md)
    LOOM_ROOT="[directory-of-this-prompt-file]"
    TARGET_DIR="."

    # Remove existing directories
    rm -rf "$TARGET_DIR/.claude/agents" "$TARGET_DIR/.claude/commands" "$TARGET_DIR/.claude/skills"

    # Copy fresh from Loom repository
    cp -r "$LOOM_ROOT/.claude/agents" "$TARGET_DIR/.claude/"
    cp -r "$LOOM_ROOT/.claude/commands" "$TARGET_DIR/.claude/"
    cp -r "$LOOM_ROOT/.claude/skills" "$TARGET_DIR/.claude/"

    # Copy AGENTS.md
    cp "$LOOM_ROOT/.claude/AGENTS.md" "$TARGET_DIR/.claude/"

    echo "✅ Full replacement complete - all framework files synchronized"
    ```

    **Option 2 - Intelligent Sync (Safe)**:

    ```bash
    # LOOM_ROOT is the directory containing this prompt file (loom.md)
    LOOM_ROOT="[directory-of-this-prompt-file]"

    # Execute sync script (uses rsync)
    bash "$LOOM_ROOT/scripts/sync-loom-files.sh" .
    ```

4.  **Confirm the output**: Review the output to ensure that files were created/updated as expected.

### Phase 4: Deploy CLAUDE.md

Deploy the `CLAUDE.md` file using the `scripts/deploy-claude-md.sh` script. This file serves as the operating manual for Claude Code in this project.

1. **Gather project information from Phase 1**:
   - Project name
   - Tech stack (full description)
   - TDD enforcement level (STRICT/RECOMMENDED/OPTIONAL)
   - Preview command (e.g., `npm run dev`)
   - Test command (e.g., `npm test`)
   - Build command (e.g., `npm run build`)

2. **Run the deployment script**:

   Execute the `scripts/deploy-claude-md.sh` script with all gathered parameters. The script will create the CLAUDE.md file with proper formatting and markers. Use the same `LOOM_ROOT` path you determined in Phase 3. The first argument must be the absolute path to the current working directory (the target project).

   ```bash
   # Get absolute path to current working directory (the target project)
   TARGET_PROJECT_DIR=$(pwd)

   # Use LOOM_ROOT from Phase 3 (absolute path to Loom repository)
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

   **Example**:

   ```bash
   bash /Users/dev/loom/scripts/deploy-claude-md.sh \
     "." \
     "E-Commerce Platform" \
     "Next.js 14, React 18, TypeScript, Prisma, PostgreSQL" \
     "STRICT" \
     "npm run dev" \
     "npm test" \
     "npm run build"
   ```

3. **Review script output**:

   The script will report the file creation and confirm successful deployment. Verify that `CLAUDE.md` was created in the project root.

### Phase 5: Final Setup & Verification

Follow the instructions in `prompts/setup/3-features-setup.md` and `prompts/setup/4-verification.md` to complete the setup, which includes creating the feature structure and the initial Git commit.

After these steps, the user's project will be fully set up with the latest version of the Loom framework.

---

# Update Mode - Existing Loom Installation

Execute this workflow when `docs/development/status.xml` EXISTS.

---

### Step 1: Synchronize Core Framework Files

Synchronize core framework files (agents, commands, skills) from the Loom repository. This ensures all agents, commands, and essential configurations are up-to-date.

1.  **Ask user for sync preference**: Before synchronizing files, ask the user:

    ```
    How would you like to sync framework files (agents, commands, skills)?

    1. FULL REPLACEMENT (Recommended for most updates)
       - Completely replaces .claude/agents/, .claude/commands/, .claude/skills/
       - Fastest option (uses cp)
       - Removes any custom modifications you made to these folders
       - Ensures you have the latest framework versions

    2. INTELLIGENT SYNC (Recommended if you have custom agents/commands)
       - Uses rsync to merge changes
       - Preserves your custom files
       - Updates existing Loom files
       - Slower but safer for customized setups

    Choose: [1] Full Replacement or [2] Intelligent Sync
    ```

2.  **Resolve Loom repository path**: You know the full path to this prompt file because the user provided it when invoking this prompt (e.g., `/path/to/loom/loom.md`). Extract the directory portion to get LOOM_ROOT.

3.  **Execute sync based on user choice**:

    **Option 1 - Full Replacement (Fast)**:

    ```bash
    # LOOM_ROOT is the directory containing this prompt file (loom.md)
    LOOM_ROOT="[directory-of-this-prompt-file]"
    TARGET_DIR="."

    # Remove existing directories
    rm -rf "$TARGET_DIR/.claude/agents" "$TARGET_DIR/.claude/commands" "$TARGET_DIR/.claude/skills"

    # Copy fresh from Loom repository
    cp -r "$LOOM_ROOT/.claude/agents" "$TARGET_DIR/.claude/"
    cp -r "$LOOM_ROOT/.claude/commands" "$TARGET_DIR/.claude/"
    cp -r "$LOOM_ROOT/.claude/skills" "$TARGET_DIR/.claude/"

    # Copy AGENTS.md
    cp "$LOOM_ROOT/.claude/AGENTS.md" "$TARGET_DIR/.claude/"

    echo "✅ Full replacement complete - all framework files synchronized"
    ```

    **Option 2 - Intelligent Sync (Safe)**:

    ```bash
    # LOOM_ROOT is the directory containing this prompt file (loom.md)
    LOOM_ROOT="[directory-of-this-prompt-file]"

    # Execute sync script (uses rsync)
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
