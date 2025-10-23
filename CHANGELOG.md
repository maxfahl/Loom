# Changelog

All notable changes to this project will be documented in this file.

---

## [0.4] - 2025-10-23

### Added
- **CLAUDE.md Template System**: Added `prompts/reference/claude-md-template.md` as the single source of truth for CLAUDE.md content, with marker-based section management (`<!-- LOOM_FRAMEWORK_START -->` / `<!-- LOOM_FRAMEWORK_END -->`).
- **Automated CLAUDE.md Deployment**: Created `scripts/deploy-claude-md.sh` to intelligently deploy or update CLAUDE.md in user projects with marker-based section replacement, preserving user customizations.
- **Reference Documentation**: Added `prompts/setup/5-claude-md.md` as reference documentation for the CLAUDE.md template architecture.

### Changed
- **Streamlined CLAUDE.md Content**: CLAUDE.md now focuses exclusively on:
  - What Loom is (concise overview)
  - Core components (agents, commands, epics/stories, YOLO mode)
  - How Claude Code should work in Loom projects
  - Folder structure with descriptions
  - Clear guardrails for commands/agents (single responsibility, no deviation)
- **Path Resolution**: Both `setup.md` and `update-setup.md` now explicitly resolve the Loom root path from the prompt file location provided by the user, eliminating ambiguity in script paths.
- **Absolute Path Handling**: Updated `scripts/deploy-claude-md.sh` invocations to use `$(pwd)` to pass the absolute path to the target project directory.
- **Marker-Based Updates**: Existing CLAUDE.md files with Loom markers are now updated non-destructively, preserving user customizations outside markers. Custom CLAUDE.md files without markers trigger creation of separate LOOM_FRAMEWORK.md file.

### Removed
- **Redundant Helper Script**: Removed `scripts/get-loom-root.sh` as path resolution is now handled directly by Claude Code deriving the directory from the prompt file path.

---

## [0.3] - 2025-10-23

### Added
- **Skill Synchronization**: The `setup` and `update` flows now also synchronize the contents of the `.claude/skills` directory, ensuring that the project has the latest framework-provided skills. This operation is non-destructive and will not remove user-created skills.

### Changed
- The `sync-loom-files.sh` script was updated to include the `.claude/skills` directory in its synchronization process.

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

