Your task is to set up the Loom agentic development framework in a user's new (greenfield) or existing (brownfield) project. You will orchestrate the setup process, focusing on creating project-specific documentation and copying the latest framework files (agents, commands) from the Loom source repository.

---

### Phase 1: Discovery & Analysis

First, you must understand the user's project. Follow the instructions in `prompts/setup/1-discovery.md` to ask the discovery questions and, if it's a brownfield project, to perform the codebase analysis.

**CRITICAL**: You must get the absolute path to the user's project directory. This will be the `TARGET_DIR` for the synchronization script.

### Phase 2: Documentation Creation

Next, based on the information gathered in Phase 1, create the project-specific documentation. Follow the instructions in `prompts/setup/2-documentation.md`.

- For brownfield projects, this includes creating the `PROJECT_OVERVIEW.md` and handling legacy documentation.
- For all projects, this includes creating the `PRD.md`, `TECHNICAL_SPEC.md`, `ARCHITECTURE.md`, etc.

### Phase 3: Synchronize Framework Files

Instead of generating agents and commands from scratch, you will copy them from the Loom source repository using the `sync-loom-files.sh` script.

1.  **Explain the action**: Inform the user that you are about to copy the necessary agent, command, and configuration files into their project.

2.  **Execute the script**: Run the `sync-loom-files.sh` script, providing the target project directory path you obtained in Phase 1.

    ```bash
    bash scripts/sync-loom-files.sh /path/to/user/project
    ```

3.  **Confirm the output**: Review the output of the script to ensure that files were created and updated as expected.

### Phase 4: Final Setup & Verification

Follow the instructions in `prompts/setup/3-features-setup.md` and `prompts/setup/4-verification.md` to complete the setup.

- This includes creating the `features/` directory structure and the `status.xml` file.
- It concludes with creating the initial Git commit for the user.

After these steps, the user's project will be fully set up with the latest version of the Loom framework.
