# Changelog

All notable changes to this project will be documented in this file.

---

## [0.2] - 2025-10-23

### Added
- **Autonomous Discovery**: The `setup` flow no longer asks the user questions upfront. It now autonomously analyzes the target project's file system to determine its state (greenfield/brownfield), tech stack, and testing conventions, only asking for clarification if it finds no information.
- **`CHANGELOG.md`**: This file was created to track versions.

### Changed
- **Major Prompt Refactoring**: The entire prompt structure was reorganized. The single `project-setup-meta-prompt.md` was replaced by three distinct entry points (`setup.md`, `update-setup.md`, `prepare-setup.md`).
- **Script-Based File Sync**: The setup and update flows now use a `sync-loom-files.sh` script to copy/update framework files, replacing the previous prompt-based generation and validation for user projects.
- **Simplified User Interaction**: Both `setup` and `update` flows now assume they are run from within the target project's directory, removing the need to ask the user for the path.
- **Prompt Reorganization**: All workflow prompts were moved from `prompts/phases` into new, role-specific directories: `prompts/setup`, `prompts/update-setup`, and `prompts/prepare-setup`.
- **Robust Update Flow**: The `update-setup` flow was enhanced with a `structure-validator` agent that non-destructively updates the structure of user-owned files like `status.xml`.

---

## [0.1] - 2025-10-22

### Added
- **Initial Loom Framework**: The first version of the Loom agentic coding framework was created.
- **Monolithic Meta-Prompt**: All setup and update logic was orchestrated by a single, comprehensive `project-setup-meta-prompt.md`.
- **Prompt-Based Generation**: The framework used a 7-phase, prompt-based workflow to generate all agents, commands, and documentation from scratch for every new project.
- **Complex Validation**: The update workflow relied on a suite of 6 parallel validation agents to check for discrepancies.

