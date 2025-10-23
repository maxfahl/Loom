<div align="center">

<pre>
╔══════════════════════════════════════════════╗
║                                              ║
║     ██╗      ██████╗  ██████╗ ███╗   ███╗    ║
║     ██║     ██╔═══██╗██╔═══██╗████╗ ████║    ║
║     ██║     ██║   ██║██║   ██║██╔████╔██║    ║
║     ██║     ██║   ██║██║   ██║██║╚██╔╝██║    ║
║     ███████╗╚██████╔╝╚██████╔╝██║ ╚═╝ ██║    ║
║     ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝    ║
║                                              ║
║          Weave Features Autonomously         ║
║                                              ║
╚══════════════════════════════════════════════╝
</pre>

**AI-only development framework with autonomous agents, TDD workflows, and epic-based feature tracking.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Built for Claude Code](https://img.shields.io/badge/Built%20for-Claude%20Code-5A67D8)](https://claude.ai/code)

[Quick Start](#-quick-start) • [Features](#-what-you-get) • [YOLO Loop](#-yolo-loop-autonomous-development) • [Documentation](#-documentation)

> **⚠️ Claude Code Exclusive**: Loom is specifically designed for [Claude Code CLI](https://claude.ai/code). Ports for Gemini CLI and Codex are planned and will be developed when those CLIs reach feature parity with Claude Code.

</div>

---

## 🧵 What is Loom?

**Loom** is an AI-native development framework that weaves together autonomous agents, test-driven development, and epic-based feature tracking into a seamless workflow. Think of it as your development orchestrator - coordinating specialized AI agents to build, test, review, and deploy features autonomously.

### Why Loom?

- 🤖 **16+ Core Agents** - Each expert in their domain (dev, testing, review, security, design)
- 🔄 **Autonomous Workflows** - YOLO mode with configurable breakpoints (story-level, epic-level)
- 🧪 **Strict TDD** - Red-Green-Refactor cycle enforced by design
- 📊 **Epic/Story Organization** - Break features into logical milestones
- ⚡ **Parallel Execution** - Multiple agents work simultaneously (70-80% time savings)
- 🎯 **16+ Slash Commands** - Streamlined workflow (/dev, /review, /commit, /test, etc.)

### The Loom Philosophy

Traditional frameworks treat specs as static documents that drift from reality. **Loom treats agents as living executors** - they maintain context, follow TDD, and autonomously implement features based on living documentation.

The epic/story structure provides granularity without rigidity. YOLO mode provides autonomy without losing control. Parallel agent execution provides speed without sacrificing quality.

---

## 🚀 Quick Start

### 1. New Project Setup (Greenfield or Brownfield)

From the root directory of your new or existing project, give your AI coding agent this prompt (you will need to use the absolute path to the Loom framework repository):

```
# Run this from your project's directory
Read and fully understand the prompt in the `setup.md` file and execute the workflow.

/path/to/loom/setup.md
```

The agent will autonomously analyze your project, generate the necessary documentation, and copy the latest agents and commands into your project.

### 2. Update an Existing Loom Setup

From the root directory of your project that already uses Loom, run the `update-setup.md` prompt:

```
# Run this from your project's directory
Read and fully understand the prompt in the `update-setup.md` file and execute the workflow.

/path/to/loom/update-setup.md
```

This will intelligently synchronize all agents and commands, and then generate or update any necessary documentation to match the latest standard.

## 🎯 What You Get

### 16 Core Agents

- **coordinator** - Orchestrates parallel sub-agents to complete complex tasks.
- **senior-developer** - Implements features following project architecture and standards.
- **code-reviewer** - Performs detailed, 7-phase code reviews.
- **test-writer** - Writes comprehensive tests following TDD methodology.
- **bug-finder** - Analyzes code for bugs and edge cases.
- **refactor-specialist** - Improves code quality and structure.
- **qa-tester** - Runs tests and validates functionality.
- **git-helper** - Manages git operations like commits and branches.
- **architecture-advisor** - Reviews system design and architecture.
- **performance-optimizer** - Analyzes and improves application performance.
- **documentation-writer** - Creates and updates documentation.
- **agent-creator** - Creates new specialized agents.
- **skill-creator** - Creates reusable Claude Code Skills.
- **codebase-analyzer** - Autonomously analyzes brownfield projects.
- **project-scaffolder** - Creates standard Loom directory structures.
- **structure-validator** - Non-destructively updates the structure of existing files.


### 16+ Slash Commands

- **/dev** - Continue development on the current story.
- **/dev-yolo** - Launch the autonomous development loop.
- **/commit** - Smart commit with tests and linting.
- **/review** - Run a comprehensive 7-phase code review.
- **/loom-status** - Show a report of the current project status.
- **/test** - Run tests with coverage.
- **/plan** - Plan a new feature.
- **/docs** - Update documentation.
- **/yolo** - Configure the autonomous YOLO mode breakpoints.
- **/create-feature** - Set up a new feature with epics and stories.
- **/correct-course** - Adjust the direction of an in-progress feature.
- **/create-story** - Generate the next user story.
- **/one-off** - Delegate a one-off task to the coordinator agent.
- **/fix** - Address a bug by creating a new, high-priority story.
- **/security-review** - Run an OWASP-based security scan.
- **/design-review** - Run a UI/UX design and accessibility review.

### Complete Documentation

15+ files covering PRD, technical specs, architecture, design systems, development plans, code review principles (7-phase framework), security review checklist (OWASP Top 10 + FALSE_POSITIVE filtering), design principles (Playwright + WCAG 2.1 AA), and more.

## 🎮 YOLO Mode: Autonomous Development

Configure when agents stop vs. proceed autonomously with **three stopping granularities**:

### Stopping Granularities

**A. STORY-LEVEL** (default): Stop at specific breakpoints within each story
**B. EPIC-LEVEL**: Only stop when full epics are completed (highest autonomy)
**C. CUSTOM**: Select individual breakpoints manually

### Breakpoint Options

```yaml
Story-Level Breakpoints:
1. After development, before code review
2. After code review, before tests
3. After tests, before user testing
4. After user testing, before commit
5. After commit, before push
6. Before any file changes
7. Before running tests
8. Before major refactoring

Epic-Level Breakpoint:
9. After completing epic, before starting next epic
```

### Configuration Examples

**Story-Level Control:**

- `"none"` - Full autonomous mode (prototyping)
- `"1,3,4,8"` - Balanced control (recommended)
- `"all"` - Maximum control (production)

**Epic-Level Control:**

- `"epic"` - Autonomous per epic, stop only at epic boundaries
- Agents complete ALL stories in epic before stopping
- Ideal for high-trust autonomous development

The coordinator agent reads your YOLO configuration and automatically handles the complete TDD cycle: Red → Green → Refactor → Review → Test → Deploy.

**EPIC-LEVEL mode** enables maximum autonomy - agents handle dev → review → test → commit for all stories within an epic, only pausing when switching between major epic milestones.

---

## 🔁 YOLO Loop: Autonomous Development

**Start the autonomous development loop** where agents complete entire stories, epics, or features automatically.

### Quick Start

```bash
# 1. Configure YOLO mode (one-time setup)
/yolo

# Select stopping granularity:
# A. STORY-LEVEL - Stop at breakpoints within each story (balanced control)
# B. EPIC-LEVEL - Only stop when full epics complete (maximum autonomy)
# C. CUSTOM - Select individual breakpoints manually

# 2. Launch the YOLO loop
/dev-yolo
```

### How It Works

The `/dev-yolo` command spawns the **coordinator agent** which:

1. ✅ **Reads current state** - Checks `status.xml`, current epic, current story
2. 🔴 **Writes failing tests** (TDD Red phase)
3. 🟢 **Implements code** (TDD Green phase)
4. 🔵 **Refactors** (TDD Blue phase)
5. ✅ **Checks off tasks** in story file as completed
6. 🧪 **Runs tests** (ensures 80%+ coverage)
7. 👁️ **Spawns code-reviewer** for quality check
8. 🔧 **Handles Review Tasks** if issues found
9. 📝 **Updates story status** to "Waiting For Review" when complete
10. 🔄 **Checks breakpoints** - Stop or continue based on YOLO config
11. ➡️ **Moves to next story** (if allowed by YOLO config)
12. 🏁 **Stops at epic boundary** (if breakpoint 9 enabled) or continues to next epic

### Stopping Modes

| Mode            | Stops When                                      | Use Case                               |
| --------------- | ----------------------------------------------- | -------------------------------------- |
| **STORY-LEVEL** | At configured breakpoints within stories (1-8)  | Balanced control, review each story    |
| **EPIC-LEVEL**  | Only after completing full epics (breakpoint 9) | Maximum autonomy, review at milestones |
| **CUSTOM**      | At any configured breakpoints (1-9)             | Fine-grained control                   |

### Example Workflow

```bash
# Configure EPIC-LEVEL mode (stop only at epic boundaries)
/yolo
> Select: B (EPIC-LEVEL)

# Start autonomous loop
/dev-yolo

# Output:
# 🚀 Launching coordinator agent in YOLO mode...
# Feature: user-authentication
# YOLO Mode: ON
# Stopping Granularity: EPIC-LEVEL
# Breakpoints: 9 only
#
# Coordinator will autonomously complete all stories in Epic 1.
# Will stop after Epic 1 completes for your review.

# ... agents work autonomously ...
# ... complete Story 1.1, 1.2, 1.3 ...
# ... run tests, review, commit ...

# 🎯 YOLO Loop Status Report
#
# **Feature**: user-authentication
# **Stopped At**: Epic Complete (Breakpoint 9)
#
# **Completed**:
# - ✅ Story 1.1: Setup JWT middleware (commit: abc123)
# - ✅ Story 1.2: Add login endpoint (commit: def456)
# - ✅ Story 1.3: Add token refresh (commit: ghi789)
#
# **Current State**:
# - Epic: epic-1-foundation
# - Status: Done
# - Tests: 42/42 passing, 87% coverage
#
# **Next Steps**:
# - Review Epic 1 work
# - Run /dev-yolo again to start Epic 2

# Review the work, then continue
/dev-yolo  # Starts Epic 2
```

### Resume After Stop

```bash
# If stopped at breakpoint or epic boundary
/dev-yolo  # Resume from where it stopped

# If you want to change YOLO configuration
/yolo      # Reconfigure breakpoints
/dev-yolo  # Resume with new configuration
```

### When to Use YOLO Loop

✅ **Use `/dev-yolo` for:**

- New feature development (let agents work autonomously)
- Rapid prototyping (high-speed iteration)
- Overnight development (wake up to completed epics)
- Trusted workflows (stable, well-tested patterns)

❌ **Use manual `/dev` for:**

- First-time YOLO configuration testing
- Critical production changes requiring review
- Learning the codebase
- Debugging complex issues

---

## 📊 Feature Tracking with Epics & Stories

Features are organized into **epics** (logical groupings) and then broken down into individual **stories**. This structure is generated inside your project's `docs/development/features/` directory.

**status.xml** tracks:

- Current epic and story
- YOLO mode configuration
- Pending tasks
- Active feature status

## 🔄 Comparison with Other Frameworks

### vs. SpecKit (GitHub)

**SpecKit** focuses on sequential spec-to-code transformation:

- Fixed 4-phase workflow (specify → plan → tasks → implement)
- Human approval required at each gate
- Single implementation path
- Tightly coupled to software development

**Loom** offers flexible parallel workflows:

- Multiple specialized agents working simultaneously
- Epic-based feature breakdown with independent stories
- YOLO mode for autonomous development (story-level, epic-level)
- Works for any domain (via agent customization)

### vs. BMAD Method

**BMAD** provides orchestrated multi-agent collaboration:

- Agent teams communicate via file-based messages
- Web UI + IDE integration
- Expansion packs for different domains
- YAML-based workflow definitions

**Loom** emphasizes AI-native development:

- Agents as first-class Claude Code primitives
- Slash commands for streamlined workflows
- Git-integrated feature branches
- Built-in TDD methodology with YOLO mode
- Epic/story structure for granular tracking

### Key Differentiator

Loom treats **agents and workflows as code** within Claude Code, not as external orchestration. You get:

- Native slash command integration
- Direct git workflow support
- Built-in TDD with autonomous loops
- Flexible epic/story breakdown (not rigid task lists)
- Template project support for instant setup

## 🏗 How It Works

### Setup Phase (One Time)

1.  Run the `setup.md` prompt from within your project's directory.
2.  The AI autonomously analyzes your project to determine context (tech stack, brownfield vs. greenfield, etc.). It only asks questions if it cannot find the information.
3.  Specialized agents are spawned to generate all standard documentation and scaffold the required directory structures (`docs/development`, etc.).
4.  The latest versions of all agents and commands are copied into your project's `.claude` directory.
5.  A final verification is performed and the initial setup is committed to git.

### Development Cycle (Repeatable)

1. **/create-feature** - Set up a new feature with epics.
2. **/create-story** - Generate the next user story.
3. **/yolo** - Configure autonomous breakpoints.
4. **/dev** or **/dev-yolo** - Implement the story using the TDD cycle.
5. **/review** - Run a 7-phase code review.
6. **/fix** - If a bug is found outside of a story, use this to create a new fix-story.
7. **/commit** - Commit the completed work.

### Autonomous Loop (YOLO Mode)

```
Coordinator reads status.xml →
Reads current story file →
Checks for Review Tasks (prioritizes first) →
Writes failing tests (RED) →
Implements code (GREEN) →
Refactors (BLUE) →
Checks off completed tasks in story file →
Updates story status to "Waiting For Review" →
Spawns code-reviewer + qa-tester in parallel →
If issues → Adds Review Tasks, status to "In Progress" →
If no issues → Status to "Done" →
Checks YOLO breakpoint →
Continues or stops for approval →
Repeats for next story
```

## 🎓 Key Concepts

### AI-Only Development

All coding, testing, and implementation performed by AI agents. Human involvement limited to:

- Defining requirements
- Approving plans
- Providing oversight

### Test-Driven Development (TDD)

Strict Red-Green-Refactor cycle:

1. **RED** - Write failing test
2. **GREEN** - Minimal code to pass
3. **REFACTOR** - Improve code quality

### Epic-Based Organization

Features divided into logical epics, each with multiple stories. Allows:

- Parallel development across epics
- Independent story validation
- Incremental feature delivery

## 📁 Project Structure

This is the standard directory structure that Loom will generate inside your project:

```
project/
├── .claude/                     # Agents and commands live here
│   ├── agents/
│   └── commands/
├── docs/
│   └── development/
│       ├── status.xml         # GLOBAL: Tracks status across all features
│       ├── INDEX.md           # GLOBAL: Project-wide documentation index
│       └── features/
│           └── [feature-name]/  # All docs for a specific feature live here
│               ├── PRD.md
│               ├── FEATURE_SPEC.md
│               ├── TECHNICAL_DESIGN.md
│               ├── ARCHITECTURE.md
│               └── epics/
│                   └── [epic-name]/
│                       ├── DESCRIPTION.md
│                       ├── TASKS.md
│                       ├── NOTES.md
│                       └── stories/
│                           └── [story].md
├── src/                       # Your project's source code lives here
├── CLAUDE.md                  # High-level instructions for the AI
└── README.md                  # Your project's README
```

## 🔧 Requirements

- Claude Code CLI
- Git
- Node.js (project-specific)

## 📖 Documentation

- **[Project Setup](setup.md)** - The main entry point for setting up a new project.
- **[Update Setup](update-setup.md)** - The main entry point for updating an existing project.
- **[Agent Reference](prompts/reference/core-agents.md)** - Detailed definitions of all specialized agents.
- **[Command Reference](prompts/prepare-setup/2-create-commands.md)** - Detailed definitions of all slash commands.
- **[Status XML Guide](prompts/reference/status-xml.md)** - The specification for the feature tracking file.

## 🎯 Use Cases

- **Greenfield Projects** - Complete setup from requirements to deployment
- **Brownfield Projects** - Add feature tracking to existing codebases
- **Rapid Prototyping** - YOLO mode for fast iteration
- **Enterprise Development** - Strict TDD with review gates
- **Team Projects** - Multiple agents working in parallel

## 🚨 Why This Approach?

Traditional spec-driven frameworks treat specifications as static documents that quickly drift from implementation. Loom treats **agents as the spec executors** - they maintain context, follow TDD, and autonomously implement features based on living documentation (status.xml, epic docs, story files).

The epic/story structure provides granularity without rigidity. The YOLO mode provides autonomy without losing control. The parallel agent execution provides speed without sacrificing quality.

## 📝 License

MIT

## 🤝 Contributing

This framework is designed to be extended. Create custom agents, add new slash commands, or build domain-specific templates. All agents and commands are markdown-based for easy modification.

### Framework Development

If you are a developer modifying the Loom framework itself (for example, adding a new agent or changing a command's core prompt), you will need to regenerate the core files. The `prepare-setup.md` prompt is used for this purpose.

**⚠️ Warning:** Do NOT run this command unless you are developing the Loom framework itself. It is not for setting up a user project.

To regenerate the agents and commands from their source prompts, run:

```
# Run this from the root of the Loom framework repository
Read and fully understand the prompt in the `prepare-setup.md` file and execute the workflow.

/path/to/loom/prepare-setup.md
```

This will update the contents of the `.claude/agents/` and `.claude/commands/` directories based on the latest definitions in the `prompts/` directory.

---

**Ready to build?** Run the bootstrap prompt and let the agents set up your development environment.
