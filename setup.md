Your task is to set up the Loom agentic development framework in the user's project. You will assume the Current Working Directory is the root of the target project. You will orchestrate the setup process by first autonomously analyzing the project, then creating documentation, and finally copying the latest framework files into the directory.

---

### Phase 1: Discovery & Analysis

First, you must understand the project in the Current Working Directory. Follow the instructions in `prompts/setup/1-discovery.md` to autonomously analyze the project.

**CRITICAL**: The Current Working Directory is the `TARGET_DIR` for the synchronization script.

### Phase 2: Documentation Creation

Next, based on the information gathered in Phase 1, create the project-specific documentation by following the instructions in `prompts/setup/2-documentation.md`.

### Phase 3: Synchronize Framework Files

Synchronize core framework files (agents, commands, skills) from the Loom repository using the `sync-loom-files.sh` script.

1.  **Explain the action**: Inform the user that you are about to copy the necessary agent, command, and configuration files into their project.

2.  **Resolve Loom repository path**: You know the full path to this prompt file because the user provided it when invoking this prompt (e.g., `/path/to/loom/setup.md`). Extract the directory portion to get LOOM_ROOT.

3.  **Execute the sync script**: Run the `sync-loom-files.sh` script using the resolved LOOM_ROOT path.

    ```bash
    # LOOM_ROOT is the directory containing this prompt file (setup.md)
    # Example: if this prompt is at /Users/dev/loom/setup.md, then LOOM_ROOT=/Users/dev/loom
    LOOM_ROOT="[directory-of-this-prompt-file]"

    # Execute sync script
    bash "$LOOM_ROOT/scripts/sync-loom-files.sh" .
    ```

4.  **Confirm the output**: Review the output of the script to ensure that files were created and updated as expected.

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
