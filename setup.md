Your task is to set up the Loom agentic development framework in the user's project. You will assume the Current Working Directory is the root of the target project. You will orchestrate the setup process by first autonomously analyzing the project, then creating documentation, and finally copying the latest framework files into the directory.

---

### Phase 1: Discovery & Analysis

First, you must understand the project in the Current Working Directory. Follow the instructions in `prompts/setup/1-discovery.md` to autonomously analyze the project.

**CRITICAL**: The Current Working Directory is the `TARGET_DIR` for the synchronization script.

### Phase 2: Documentation Creation

Next, based on the information gathered in Phase 1, create the project-specific documentation. Follow the instructions in `prompts/setup/2-documentation.md`.

- For brownfield projects, this includes creating the `PROJECT_OVERVIEW.md` and handling legacy documentation.
- For all projects, this includes creating the `PRD.md`, `TECHNICAL_SPEC.md`, `ARCHITECTURE.md`, etc.

### Phase 3: Synchronize Framework Files

Instead of generating agents and commands from scratch, you will copy them from the Loom source repository using the `sync-loom-files.sh` script.

1.  **Explain the action**: Inform the user that you are about to copy the necessary agent, command, and configuration files into their project.

2.  **Execute the script**: Run the `sync-loom-files.sh` script. You must use the absolute path to the script (which you can determine from the path of this prompt) and provide `.` as the target directory path.

    ```bash
    # The agent must resolve the absolute path to the script
    bash /path/to/loom/scripts/sync-loom-files.sh .
    ```

3.  **Confirm the output**: Review the output of the script to ensure that files were created and updated as expected.

### Phase 4: Final Setup & Verification

Follow the instructions in `prompts/setup/3-features-setup.md` and `prompts/setup/4-verification.md` to complete the setup.

- This includes creating the `features/` directory structure and the `status.xml` file.
- It concludes with creating the initial Git commit for the user.

After these steps, the user's project will be fully set up with the latest version of the Loom framework.
