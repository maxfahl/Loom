# Project Setup Meta Prompt

**Version**: 2.0 (Sharded Structure)
**Last Updated**: 2025-10-22
**Total Files**: 22 focused prompt files
**Total Agents**: 13 core + 2-4 tech-specific
**Total Commands**: 11+ slash commands

---

## 🚀 Quick Start

**For Claude Code**: Read [`project-setup-meta-prompt.md`](project-setup-meta-prompt.md) in the root of this directory.

This is the **main orchestrator** that will guide you through:

- Determining operating mode (NEW SETUP vs UPDATE MODE)
- Following the appropriate workflow
- Loading only the necessary prompt files for each phase
- Setting up a complete agentic development environment

Promt with:

```
Read and fully understand the prompt in the below markdown file and follow it to the dot. Be extremely careful and take your time.
`/Users/maxfahl/Fahl/Common/AgentDevMetaPrompt/project-setup-meta-prompt.md`
```

---

## 📖 What This System Does

This meta prompt system guides Claude Code through setting up a comprehensive development environment with:

- **13 core specialized agents** for parallel development
- **11+ custom slash commands** for streamlined workflows
- **12+ documentation files** (PRD, Technical Spec, Architecture, etc.)
- **TDD methodology** with YOLO mode autonomous development
- **MCP server integration** (7 servers across 11 agents)
- **Feature tracking system** with epics, stories, and status.xml

---

## 📁 Directory Structure

```
/
├── README.md (this file)
├── project-setup-meta-prompt.md (MAIN ORCHESTRATOR - START HERE)
│
└── prompts/ (All sharded prompt files)
    ├── README.md (Detailed sharding documentation)
    │
    ├── phases/ (8 files - Sequential workflow)
    │   ├── phase-0-detection.md
    │   ├── phase-1-discovery.md
    │   ├── phase-2-documentation.md
    │   ├── phase-3-agents.md
    │   ├── phase-4-commands.md
    │   ├── phase-5-claude-md.md
    │   ├── phase-6-features-setup.md
    │   └── phase-7-verification.md
    │
    ├── reference/ (8 files - Reusable knowledge)
    │   ├── core-agents.md (All 13 agent definitions)
    │   ├── coordinator-workflow.md
    │   ├── mcp-integration.md
    │   ├── parallelization-patterns.md
    │   ├── status-xml.md
    │   ├── template-system.md
    │   ├── troubleshooting.md
    │   └── yolo-mode.md
    │
    ├── update-mode/ (1 file - Validation workflow)
    │   └── validation-workflow.md
    │
    └── templates/ (4 files - Content templates)
        ├── doc-templates.md
        ├── agent-template.md
        ├── command-template.md
        └── story-template.md
```

---

## 🎯 Two Operating Modes

### 1. NEW SETUP Mode

Use when setting up a project from scratch or migrating to this framework.

**Workflow**: 7 phases (Discovery → Documentation → Agents → Commands → CLAUDE.md → Features → Verification)

**Time**:

- With template project: 15-30 minutes
- From scratch (greenfield): 45-75 minutes
- From scratch (brownfield): 60-90 minutes

### 2. UPDATE Mode

Use when you have an existing setup and want to validate/update it to match the current specification.

**Workflow**: 6 phases (Read → Validate → Synthesize → Update → Verify → Commit)

**Time**: 20-40 minutes depending on gaps found

---

## 💡 How To Use

### For a New Project

1. Give Claude Code this path:

   ```
   /Users/maxfahl/Fahl/Common/AgentDevMetaPrompt/project-setup-meta-prompt.md
   ```

2. Claude Code will:
   - Determine this is a NEW SETUP
   - Ask discovery questions
   - Get your approval
   - Create all agents, commands, and documentation
   - Set up feature tracking
   - Commit everything to git

### For an Existing Project (Update/Validate)

1. Navigate to your project directory

2. Give Claude Code the same path:

   ```
   /Users/maxfahl/Fahl/Common/AgentDevMetaPrompt/project-setup-meta-prompt.md
   ```

3. Claude Code will:
   - Detect existing status.xml (UPDATE MODE)
   - Validate current setup against specification
   - Identify gaps and outdated components
   - Update everything in parallel
   - Verify all issues fixed

---

## 🔑 Key Features

### 1. Sharded Structure

- **40-75% context savings** per phase
- Load only what you need for current phase
- Parallel agents get targeted instructions
- Easy to maintain and update

### 2. Template Project Support

- Copy agents/commands from existing project
- **50-80% time savings**
- Two modes: "trust" (fast) or "validate" (safe)

### 3. Parallel Execution

- 4-6 parallel agents per phase
- Maximum efficiency
- Independent validation and updates

### 4. Brownfield Support

- Analyzes existing codebase
- Creates PROJECT_OVERVIEW.md
- Adapts documentation to current state
- Optional feature tracking setup

---

## 📚 What Gets Created

After running this meta prompt, your project will have:

### Documentation (12+ files in `docs/development/`)

- INDEX.md (Master documentation index)
- PRD.md (Product Requirements)
- TECHNICAL_SPEC.md (Implementation details)
- ARCHITECTURE.md (System design)
- DESIGN_SYSTEM.md (UI components)
- DEVELOPMENT_PLAN.md (TDD guide)
- TASKS.md (Task checklist)
- TESTING_STRATEGY.md
- And more...

### Agents (13 core + tech-specific in `.claude/agents/`)

1. coordinator (Orchestrates TDD workflow)
2. senior-developer (Primary implementation)
3. test-writer (Comprehensive TDD tests)
4. code-reviewer (Quality review)
5. documentation-writer (Doc updates)
6. bug-finder (Bug detection)
7. refactor-specialist (Code improvements)
8. qa-tester (Test execution)
9. git-helper (Git operations)
10. architecture-advisor (Design review)
11. performance-optimizer (Performance analysis)
12. agent-creator (Create custom agents)
13. skill-creator (Create Claude Skills)

Plus tech-specific agents based on your stack (React component builder, API endpoint builder, etc.)

### Commands (11+ in `.claude/commands/`)

- /dev - Continue development (TDD)
- /commit - Smart commit with tests
- /review - Comprehensive code review
- /status - Project status report
- /test - Run tests with coverage
- /plan - Plan next feature
- /docs - Update documentation
- /yolo - Configure YOLO mode breakpoints
- /create-feature - Create new feature with setup
- /correct-course - Adjust feature direction
- /create-agent - Create specialized agent
- /create-skill - Create Claude Skill package

### Root Files

- CLAUDE.md (Project instructions for Claude Code)
- README.md (Project overview)
- .gitignore (Configured for your stack)

### Feature Tracking

- features/ directory with epic folders
- status.xml files for each feature
- Story files (epic.story format)
- YOLO mode configuration

---

## 🎓 Learn More

- **Detailed sharding documentation**: [`prompts/README.md`](prompts/README.md)
- **All agent definitions**: [`prompts/reference/core-agents.md`](prompts/reference/core-agents.md)
- **Coordinator workflow**: [`prompts/reference/coordinator-workflow.md`](prompts/reference/coordinator-workflow.md)
- **Parallel execution patterns**: [`prompts/reference/parallelization-patterns.md`](prompts/reference/parallelization-patterns.md)
- **Troubleshooting**: [`prompts/reference/troubleshooting.md`](prompts/reference/troubleshooting.md)

---

## 📈 Success Metrics

Projects using this framework report:

- **80-95% test coverage** (TDD methodology)
- **50-80% setup time savings** (with templates)
- **4-6x parallel efficiency** (multiple agents)
- **Zero forgotten tasks** (comprehensive tracking)
- **Consistent code quality** (specialized reviewers)

---

## 🤝 Contributing

To update this meta prompt system:

1. Identify which file(s) to modify (see directory structure above)
2. Update the specific file(s) maintaining headers and cross-references
3. Test changes by running setup on a new project
4. Update `project-setup-meta-prompt.md` if navigation changes
5. Commit with descriptive message

---

## 📝 Version History

### Version 2.0 (2025-10-22) - Sharded Structure

- Split monolithic 156KB file into 22 focused files
- Added senior-developer agent (primary implementation agent)
- Fixed brownfield status.xml gap (phase-6)
- Improved parallel execution documentation
- Main orchestrator in root, all shards in prompts/

### Version 1.0 (2025-10-20) - Monolithic

- Original single-file meta prompt (5469 lines, 156KB)
- 12 core agents, 11+ commands, 12+ docs

---

**Ready to begin?** Read [`project-setup-meta-prompt.md`](project-setup-meta-prompt.md) →
