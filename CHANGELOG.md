# Changelog

All notable changes to this project will be documented in this file.

---

## [1.2.1] - 2025-01-23

### Fixed

- **CRITICAL YOLO Mode Fix**: Resolved issue where agents didn't work fully autonomously in EPIC mode
  - **Root Cause**: Coordinator agent was stopping between stories and asking for user confirmation
  - **Solution**: Added explicit self-spawning logic in Phase 9 (Story Loop)
  - Coordinator now automatically spawns new coordinator for next story in EPIC mode
  - No more "Should I continue?" prompts between stories

- **Comprehensive YOLO Mode Support**: All 5 YOLO modes now properly handled
  - **MANUAL**: Stops at all breakpoints (A, B, C, D) - full user control
  - **BALANCED**: Stops at B (commit) and C (stories) - semi-autonomous
  - **STORY**: Completes single story autonomously, stops at C
  - **EPIC**: Completes entire epic autonomously with self-spawning between stories
  - **CUSTOM**: Respects user-defined breakpoint configuration

### Added

- **Self-Spawning Instructions**: Coordinator agent Phase 9 now includes:
  - Clear decision tree for all YOLO modes
  - Explicit self-spawning logic for EPIC and CUSTOM modes
  - Examples of correct vs wrong behavior
  - Critical instructions to never return control between stories

- **Test Cases Documentation**: Created comprehensive test scenarios in YOLO-MODE-TEST-CASES.md
  - 5 test scenarios covering all YOLO modes
  - Expected vs wrong behavior examples
  - Validation checklist
  - Success criteria

### Changed

- **Coordinator Agent** (`.claude/agents/coordinator.md`):
  - Phase 9 rewritten with comprehensive mode handling
  - Added "CRITICAL: Self-Spawning in EPIC Mode" section
  - Clear examples of correct EPIC mode flow
  - Explicit "NEVER/ALWAYS" instructions for EPIC mode

- **Dev Command** (`.claude/commands/dev.md`):
  - Added delegation instructions for all 5 YOLO modes
  - MANUAL/BALANCED modes: Direct execution (no coordinator spawn)
  - STORY mode: Single coordinator spawn with stop instruction
  - EPIC mode: Coordinator spawn with self-continuation instructions
  - CUSTOM mode: Configurable breakpoint handling

### Impact

- EPIC mode now truly autonomous - completes entire epics without user intervention
- Significant time savings: No manual restarts between stories
- Clear behavioral expectations for each YOLO mode
- Proper delegation strategy based on autonomy level

---

## [1.2] - 2025-01-24

### Added

- **Coordinator Delegation Thought Template**: Coordinator now outputs structured reasoning before every Task tool call
  - Template format includes: Agent, Reason, Context, Dependencies, Expected Output
  - Applied to all delegation points: Phase 1-5 (YOLO mode) and Step 4 (Non-YOLO mode)
  - Provides transparency into delegation strategy
  - Helps identify parallelization opportunities and dependencies
  - Makes agent selection reasoning explicit and auditable

- **Fast Sync Option**: Users can now choose between Full Replacement or Intelligent Sync
  - **Full Replacement (Fast)**: Uses `rm -rf` + `cp -r` for instant directory replacement (~90% faster)
  - **Intelligent Sync (Safe)**: Uses existing `rsync`-based script to preserve custom files
  - Applied to both Setup Mode (Phase 3) and Update Mode (Step 1)
  - Clear prompts guide users to appropriate choice based on customization status
  - Full Replacement recommended for clean installs and most updates
  - Intelligent Sync recommended when custom agents/commands/skills exist

### Changed

- **loomify.md**: Updated both Setup Mode and Update Mode workflows to include sync preference prompt
  - Users explicitly choose sync method before execution
  - Default recommendation adapts to mode (clean install vs update)
  - Inline bash examples for both sync methods
  - Clearer documentation of trade-offs (speed vs safety)

### Improved

- **Coordinator Transparency**: All delegation decisions now include explicit reasoning
  - Example delegation thoughts added to 6 different phases
  - Dependencies clearly marked (None vs "Depends on: agent-X")
  - Expected outputs explicitly stated
  - Helps with debugging and understanding coordinator behavior

- **Setup/Update Performance**: Full Replacement option reduces sync time by ~90%
  - Typical sync: 5-10 seconds → <1 second
  - Particularly beneficial for large frameworks (44 agents, 17 commands, skills)
  - No functional changes to rsync path for users who need it

---

## [1.1] - 2025-01-24

### Added

- **Story File Update Protocol**: All coding and review agents now automatically update story files
  - **Coding agents (6)**: full-stack-developer, frontend-developer, backend-architect, mobile-developer, test-automator, debugger
    - Check off completed tasks (`[ ]` → `[x]`)
    - Update status to "Waiting For Review" when all tasks complete
    - Update timestamp with ISO 8601 format
  - **Review agents (3)**: code-reviewer, design-reviewer, security-reviewer
    - Append "Review Tasks" section when issues found
    - Set status to "In Progress" if issues found
    - Set status to "Done" if no issues found
    - Prioritize tasks: Fix (blocking) > Improvement (high) > Nit (low)
  - Story file is now THE definitive source of truth for feature progress

- **9-Phase Autonomous Workflow**: Coordinator now executes comprehensive YOLO mode workflow
  - **Phase 0**: Initialization - Read project state, analyze story readiness
  - **Phase 1**: Pre-Development - Research, documentation, architecture (parallel)
  - **Phase 2**: TDD Red - Write failing tests (parallel by type: unit/integration/E2E)
  - **Phase 3**: TDD Green - Implement code (parallel by layer: frontend/backend/mobile)
  - **Phase 4**: TDD Refactor - Clean up code while tests stay green
  - **Phase 5**: Review - All reviews run in parallel (code/security/design)
  - **Phase 6**: Review Loop - Fix issues until all reviewers approve (max 3 iterations)
  - **Phase 7**: Final Verification - Tests, coverage, documentation
  - **Phase 8**: Commit - Conventional commits (respects breakpoint B)
  - **Phase 9**: Story Loop - Continue to next story/epic (respects breakpoints C/D)

### Changed

- **Maximum Parallelization**: Coordinator now runs agents simultaneously at optimal points
  - Phase 1: All prep work runs in parallel
  - Phase 2: All test types run in parallel (unit/integration/E2E)
  - Phase 3: All development layers run in parallel (frontend/backend/mobile)
  - Phase 5: All review types run in parallel (code/security/design)
  - **Result**: 60-80% time savings over sequential execution

- **Intelligent Sequencing**: Workflow respects dependencies while maximizing parallelization
  - Research/prep → Tests → Implementation → Refactor → Reviews → Commit → Next Story
  - Review loop automatically fixes issues until approval
  - Smart abort after 3 review iterations to prevent infinite loops

- **Enhanced /dev Command**: Updated to reflect 9-phase workflow
  - MANUAL mode: Fully interactive, stops at all breakpoints
  - BALANCED mode: Semi-autonomous, stops at commit and between stories
  - STORY/EPIC/CUSTOM modes: Spawns coordinator with full 9-phase workflow
  - Clear documentation of each phase and parallelization strategy

### Improved

- **Story File Tracking**: Complete audit trail of all work
  - Development agents track task completion in real-time
  - Review agents document all findings with file:line references
  - Status field reflects current workflow state (In Progress/Waiting For Review/Done)
  - Timestamp tracking for all updates

- **Review Loop Safety**: Prevents infinite review/fix cycles
  - Automatically loops until story status is "Done"
  - Aborts after 3 iterations with clear error message
  - Prioritizes review tasks: Fix > Improvement > Nit

- **YOLO Mode Intelligence**: Coordinator now checks story readiness before coding
  - Validates alignment with PRD and TECHNICAL_SPEC
  - Identifies missing information or unclear requirements
  - Spawns research/documentation agents when needed
  - Prioritizes "Review Tasks" section if it exists

---

## [1.0] - 2025-01-24

### Added

- **MCP Server Documentation**: `MCP_SERVERS.md` - comprehensive guide for MCP server requirements and setup
- **Update Summary**: `MCP_UPDATE_SUMMARY.md` - detailed summary of all v1.0 changes

### Changed

- **MCP Server Consolidation**: Reduced from 5+ required to only 2 required MCP servers
  - **Required**: context7 (documentation), playwright (testing)
  - **Optional**: vibe-check, github, jina, firecrawl, zai-mcp-server, web-search-prime
  - Removed sequential-thinking from 28 agents (not available)
  - Removed magic tools from 5 agents (not available)
  - 60% reduction in required dependencies

### Fixed

- **Agent Count Consistency**: Updated all references from 41 → 44 agents
  - Fixed in CLAUDE.md (3 locations)
  - Fixed in coordinator.md (2 locations)
  - Fixed in prompts/templates/agent-template.md
  - All documentation now consistent

- **Removed Obsolete References**:
  - Removed all `prepare-setup.md` references from create-agent.md (4 locations)
  - Removed `/dev-yolo` command references from claude-md-template.md (3 locations)
  - Fixed template file references in agent-template.md and command-template.md

- **Framework Consistency**:
  - All agents now have accurate tool lists
  - Commands properly reference existing workflows
  - Documentation reflects current architecture

### Improved

- **Onboarding Experience**: Users now only need 2 MCP servers instead of 5+
- **Documentation Clarity**: Clear separation between required and optional dependencies
- **Agent Functionality**: All agents remain fully functional with graceful degradation

---

## [0.9] - 2025-01-23

### Added

- **44 Specialized Agents** (up from 14): Complete agent ecosystem with 6 categories
  - **Loom Framework (6)**: coordinator, agent-creator, skill-creator, codebase-analyzer, project-scaffolder, structure-validator
  - **Quality & Review (3)**: code-reviewer (7-phase, Opus 4.5), design-reviewer (8-phase + WCAG 2.1 AA), security-reviewer (OWASP/NIST/ISO)
  - **Development (7)**: full-stack-developer, frontend-developer, backend-architect, mobile-developer, test-automator, qa-expert, debugger
  - **Technology Specialists (7)**: nextjs-pro, react-pro, typescript-pro, python-pro, golang-pro, postgres-pro, electron-pro
  - **Architecture & Operations (6)**: cloud-architect, devops-incident-responder, deployment-engineer, performance-engineer, database-optimizer, graphql-architect
  - **Additional Specialists (15)**: ai-engineer, api-documenter, data-engineer, data-scientist, documentation-expert, dx-optimizer, incident-responder, legacy-modernizer, ml-engineer, product-manager, prompt-engineer, ui-designer, ux-designer, agent-organizer, and more

- **Setup Workflow Agents**: Three new agents for automated project setup and updates
  - **codebase-analyzer**: Deep brownfield codebase analysis with 7-phase methodology, generates comprehensive PROJECT_OVERVIEW.md (5KB+ minimum)
  - **project-scaffolder**: Automated Loom structure scaffolding, creates complete feature directory trees with all documentation files
  - **structure-validator**: Non-destructive validation and migration of project structures, preserves 100% of user data

- **MCP Server Integration**: Initial implementation with multiple servers
  - **context7**: Library documentation & resolution
  - **sequential-thinking**: Advanced multi-step reasoning (later removed in v1.0)
  - **playwright**: Browser automation & testing
  - **magic**: React component generation (later removed in v1.0)
  - **jina**: Web search & content extraction
  - **web-search-prime**: Enhanced web search
  - **firecrawl**: Advanced web crawling
  - **vibe-check**: Delegation strategy reflection (coordinator only)

- **Unified Entry Point**: `loomify.md` - single master prompt that auto-detects setup vs update mode
  - Automatically detects existing Loom installation via status.xml presence
  - Routes to Setup Mode (new projects) or Update Mode (existing projects)
  - Eliminates confusion about which prompt to use

- **Agent Directory**: `.claude/AGENTS.md` as single source of truth for all 44 agents
  - Complete directory with expertise, use cases, and delegation patterns
  - Organized by category with quick reference guide
  - Required reading for coordinator and all planning/delegation commands

- **MCP Server Reference**: `MCP_SERVERS_REFERENCE.md` - complete inventory of all MCP capabilities
  - Agent-by-agent usage matrix showing which servers each agent can access
  - Tool documentation and adoption statistics
  - Server categorization (ubiquitous, specialized, research, orchestration)

- **Template-Based Command System**: 17 pre-made command templates (99% cost savings)
  - 15 core commands: /dev, /commit, /review, /test, /plan, /docs, /create-feature, /correct-course, /create-story, /yolo, /one-off, /fix, /loom-status, /create-agent, /create-skill
  - 2 optional commands: /security-review, /design-review
  - Instant setup (<1 second vs ~40 minutes)
  - Commands can be edited directly before or after copying

- **YOLO Mode Simplification**: 4 intuitive autonomy presets
  - **MANUAL**: Full control (stop at: development, commit, stories, epics)
  - **BALANCED**: Recommended (stop at: commit, stories)
  - **STORY**: Autonomous per story (stop at: stories)
  - **EPIC**: Maximum speed (stop at: epics)
  - **CUSTOM**: Advanced with conversational design and epic-specific rules

- **CLAUDE.md Template System**: Marker-based deployment with intelligent updates
  - `<!-- LOOM_FRAMEWORK_START/END -->` markers preserve user customizations
  - `scripts/deploy-claude-md.sh` for automated deployment
  - Backward compatible with existing CLAUDE.md files

- **Comprehensive Documentation**:
  - `SYSTEMATIC_REVIEW_REPORT.md`: Complete workflow analysis
  - `AGENT_CREATION_SUMMARY.md`: Summary of new framework agents
  - `docs/command-creation-guidelines.md`: Official command creation guide
  - Official Claude Code skill creation guidelines integrated

### Changed

- **Simplified Architecture**: Templates now live directly in `.claude/` (no copying/generation needed for framework)
  - Agent templates: `.claude/agents/*.md` (edit directly)
  - Command templates: `.claude/commands/*.md` (edit directly)
  - Agent directory: `.claude/AGENTS.md` (edit directly)
  - 99% cost savings on setup time

- **Agent Consolidation**: Merged and renamed agents for clarity
  - senior-developer → full-stack-developer
  - test-writer + qa-tester → test-automator
  - documentation-writer → documentation-expert
  - architecture-advisor → cloud-architect
  - bug-finder → debugger
  - Removed git-helper (operations simple enough for any agent)

- **Command Consolidation**: Merged `/dev-yolo` into `/dev`
  - `/dev` now automatically respects YOLO configuration
  - Adaptive behavior: interactive for MANUAL/BALANCED, spawns coordinator for STORY/EPIC
  - Reduced from 16 to 15 core commands

- **YOLO Mode Improvements**:
  - Changed from `<yolo-mode enabled="true/false">` to intuitive `<autonomy-level>manual|balanced|story|epic|custom</autonomy-level>`
  - Simplified from 9 numbered breakpoints to 4 lettered breakpoints (A, B, C, D)
  - Added conversational CUSTOM mode design
  - BALANCED preset now recommended default

- **Agent Count Updates**: All references updated from 41 → 44 agents
  - README.md, CLAUDE.md, AGENTS.md, commands, documentation
  - Agent count in one-off.md fixed (line 30)

- **Path Resolution**: Both setup.md and update-setup.md explicitly resolve Loom root path
  - Eliminates ambiguity in script paths
  - Uses absolute path handling with `$(pwd)`

- **Agent Collaboration**: Complete cross-agent awareness system
  - All agents know about specialized agents and when to delegate
  - Clear rules for delegation vs. doing work yourself
  - Parallel execution patterns documented

### Removed

- **Obsolete Workflow System**: Entire prepare-setup generation system
  - `prepare-setup.md` (templates already in `.claude/`)
  - `prompts/prepare-setup/1-create-agents.md`
  - `prompts/prepare-setup/2-create-commands.md`

- **Legacy Reference Files**: Replaced by AGENTS.md and agent templates
  - `prompts/reference/core-agents.md` (3095 lines)
  - `prompts/reference/mcp-integration.md`
  - `prompts/reference/coordinator-workflow.md`
  - `prompts/reference/template-system.md`
  - `new-agents/` directory (moved to `.claude/agents/`)

- **Unused Scripts**: 7 extraction/generation scripts
  - extract-\*.sh files (from old generation workflow)
  - Framework now uses simple `cp` commands

- **Redundant Command**: `/dev-yolo` (functionality merged into `/dev`)

- **Helper Script**: `scripts/get-loom-root.sh` (path resolution handled directly)

- **Duplicate Files**: Removed duplicate and misnamed agents
  - `electorn-pro.md` → `electron-pro.md` (fixed typo)
  - `security-auditor.md` (kept `security-reviewer.md`)

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
