# Project Setup Meta Prompt - Main Orchestrator

**Version**: 2.0 (Sharded)
**Last Updated**: 2025-10-22
**Total Agents**: 13 core + 2-4 tech-specific
**Total Commands**: 12+ slash commands

---

## 📖 What This Is

This is the **main orchestrator** for the complete agentic development workflow setup system. This meta prompt guides Claude Code through setting up a full development environment with:

- **13 core specialized agents** for parallel development
- **12+ custom slash commands** for streamlined workflows
- **Comprehensive documentation** (12+ files)
- **TDD methodology** with YOLO mode autonomous development
- **MCP server integration** (7 servers across 11 agents)
- **Feature tracking system** with epics, stories, and status.xml

**Important**: This framework is designed for **AI-only development** where all coding, testing, and implementation is performed by AI agents. Human involvement is limited to defining requirements, approving plans, and providing oversight.

**This file is the navigation hub** - it tells you which specific prompt files to read for each phase of setup.

---

## ⚡ CRITICAL: Maximum Parallelization Required

**TIME SAVINGS: 70-80% faster setup (30-40 minutes vs 2+ hours)**

### When to Parallelize

**ALWAYS use parallel execution for these phases**:

- **Phase 2 (Documentation)**: Create 6-10 docs in 3 batches (5 min vs 30 min)
- **Phase 3 (Agents)**: Create 13 agents in 4 batches (8 min vs 50 min)
- **Phase 4 (Commands)**: Create 11 commands in 3 batches (6 min vs 35 min)

### What NOT to Do (Sequential Execution)

❌ **WRONG** - Sequential:
```
Create PRD → wait → Create TECHNICAL_SPEC → wait → Create ARCHITECTURE → wait...
(30 minutes for 10 docs)
```

✅ **CORRECT** - Parallel batches:
```
Batch 1: Create PRD + TECHNICAL_SPEC + ARCHITECTURE + DEVELOPMENT_PLAN + DESIGN_SYSTEM + TASKS (6 docs in parallel)
Batch 2: Create INDEX + HOOKS_REFERENCE + PROJECT_SUMMARY + EXECUTIVE_SUMMARY (4 docs in parallel)
Batch 3: Create START_HERE + CLAUDE (2 docs in parallel)
(~5 minutes total)
```

### Batch Sizes Per Phase

**Phase 2 (Documentation)**: 3 batches
- Batch 1: 6 docs (PRD, TECHNICAL_SPEC, ARCHITECTURE, DEVELOPMENT_PLAN, DESIGN_SYSTEM, TASKS)
- Batch 2: 4 docs (INDEX, HOOKS_REFERENCE, PROJECT_SUMMARY, EXECUTIVE_SUMMARY)
- Batch 3: 2 docs (START_HERE, CLAUDE)

**Phase 3 (Agents)**: 4 batches
- Batch 1: 4 agents (coordinator, senior-developer, test-writer, code-reviewer)
- Batch 2: 4 agents (bug-finder, refactor-specialist, qa-tester, git-helper)
- Batch 3: 4 agents (architecture-advisor, performance-optimizer, documentation-writer, agent-creator)
- Batch 4: 1 agent (skill-creator)

**Phase 4 (Commands)**: 3 batches
- Batch 1: 4 commands (/dev, /commit, /review, /status)
- Batch 2: 4 commands (/test, /plan, /docs, /yolo)
- Batch 3: 3 commands (/create-feature, /correct-course, /create-story)

**See**: [`prompts/reference/parallelization-patterns.md`](prompts/reference/parallelization-patterns.md) for detailed patterns

---

## 🎯 Key Features

### 1. **Template Project Support**
- Copy agents/commands/docs from existing project instead of generating from scratch
- Options: "trust" (fast copy) or "validate" (verify before copy)
- See: [`prompts/reference/template-system.md`](prompts/reference/template-system.md)

### 2. **Three Operating Modes**
- **NEW SETUP**: Full setup from scratch (or from template)
- **UPDATE MODE**: Validate and update existing setup to match current spec
- **TEMPLATE MODE**: Copy from existing project with optional validation

### 3. **Parallel Execution Throughout**
- 4-6 parallel agents per phase for maximum efficiency
- Template validation: 3 parallel validators
- Doc creation: 4 parallel doc writers
- Agent creation: 4 parallel agent creators
- See: [`prompts/reference/parallelization-patterns.md`](prompts/reference/parallelization-patterns.md)

### 4. **MCP Server Integration**
- 11/13 agents have MCP server knowledge
- 7 MCP servers documented (playwright, github, jina, vibe-check, firecrawl, zai, web-search-prime)
- Smart tool selection guidance (when to use MCP vs standard tools)
- See: [`prompts/reference/mcp-integration.md`](prompts/reference/mcp-integration.md)

---

## 🔄 Operating Mode Detection

**FIRST STEP: Determine which mode this is**

Read: [`prompts/phases/phase-0-detection.md`](prompts/phases/phase-0-detection.md)

### Quick Detection

```bash
# Check if the single status.xml file exists
find docs/development/ -name "status.xml" -type f 2>/dev/null | head -1
```

**Decision Tree**:
- **If NO status.xml found** → This is **NEW SETUP** → Continue to New Setup Workflow
- **If status.xml found** → This is **UPDATE/VALIDATION** → Jump to Update Mode Workflow

---

## 🆕 New Setup Workflow (7 Phases)

**Use this workflow when status.xml does NOT exist (new project setup).**

### Phase 0: Setup Mode Detection
**File**: [`prompts/phases/phase-0-detection.md`](prompts/phases/phase-0-detection.md)
**What**: Detect operating mode, check for templates
**Output**: Mode determined (new/update/template)

### Phase 1: Discovery & Analysis
**File**: [`prompts/phases/phase-1-discovery.md`](prompts/phases/phase-1-discovery.md)
**What**: Ask discovery questions, analyze brownfield codebase, get approval
**Questions**: Project type, template project?, description, tech stack, TDD enforcement, team size
**Brownfield**: Launch Explore agent for comprehensive analysis
**Output**: User approval + PROJECT_OVERVIEW.md (brownfield only)

**Related**:
- [`prompts/reference/template-system.md`](prompts/reference/template-system.md) - Template processing

### Phase 2: Documentation Creation
**File**: [`prompts/phases/phase-2-documentation.md`](prompts/phases/phase-2-documentation.md)
**What**: Create 12+ documentation files (or ~4-6 if using template)
**Order**: Brownfield: PROJECT_OVERVIEW.md first → All: INDEX → PRD → TECHNICAL_SPEC → etc.
**Parallel**: Launch 4-6 parallel doc creation agents
**Output**: Complete documentation in `docs/development/`

**Related**:
- [`prompts/templates/doc-templates.md`](prompts/templates/doc-templates.md) - All documentation templates

### Phase 3: Agent Creation
**File**: [`prompts/phases/phase-3-agents.md`](prompts/phases/phase-3-agents.md)
**What**: Create 13 core agents + 2-4 tech-specific agents (or skip if template used)
**Parallel**: Launch 4 parallel agent creation agents
**Output**: All agents in `.claude/agents/`

**Related**:
- [`prompts/reference/core-agents.md`](prompts/reference/core-agents.md) - Complete agent definitions
- [`prompts/reference/mcp-integration.md`](prompts/reference/mcp-integration.md) - MCP assignments
- [`prompts/reference/coordinator-workflow.md`](prompts/reference/coordinator-workflow.md) - Coordinator details
- [`prompts/templates/agent-template.md`](prompts/templates/agent-template.md) - Generic template

### Phase 4: Command Creation
**File**: [`prompts/phases/phase-4-commands.md`](prompts/phases/phase-4-commands.md)
**What**: Create 11+ custom slash commands (or skip if template used)
**Commands**: /dev, /commit, /review, /status, /test, /plan, /docs, /yolo, /create-feature, /correct-course, /create-agent, /create-skill
**Parallel**: Launch 3 parallel command creation agents
**Output**: All commands in `.claude/commands/`

**Related**:
- [`prompts/templates/command-template.md`](prompts/templates/command-template.md) - Generic template

### Phase 5: CLAUDE.md Creation
**File**: [`prompts/phases/phase-5-claude-md.md`](prompts/phases/phase-5-claude-md.md)
**What**: Create comprehensive CLAUDE.md (project instructions for Claude Code)
**Sections**: Skills, parallel agents, coordinator pattern, agents, commands, model reference, docs, tech stack, structure, methodology, code style, do/don't, checklist
**Brownfield**: Merge with existing CLAUDE.md if present
**Output**: `CLAUDE.md` in project root

### Phase 6: Root Files & Features Setup
**File**: [`prompts/phases/phase-6-features-setup.md`](prompts/phases/phase-6-features-setup.md)
**What**: Create .gitignore, README.md, features/ directory structure
**Greenfield**: Create initial feature folders from PRD
**Brownfield**: Ask user if they want feature tracking, analyze existing features
**Output**: features/ directory with status.xml files, epic folders

**Related**:
- [`prompts/reference/status-xml.md`](prompts/reference/status-xml.md) - Complete status.xml structure

### Phase 7: Verification & Commit
**File**: [`prompts/phases/phase-7-verification.md`](prompts/phases/phase-7-verification.md)
**What**: Verify all deliverables, create git commit
**Checks**: Docs complete, agents complete, commands complete, INDEX.md accurate, CLAUDE.md comprehensive
**Output**: Git commit with conventional commit message

---

## 🔄 Update Mode Workflow (6 Phases)

**Use this workflow when status.xml EXISTS (existing setup to validate/update).**

**File**: [`prompts/update-mode/validation-workflow.md`](prompts/update-mode/validation-workflow.md)

### Quick Overview

1. **Phase 0**: Read existing setup (status.xml, INDEX.md, CLAUDE.md, agents, commands)
2. **Phase 1**: Spawn 6 parallel validation agents (docs, agents, commands, features, CLAUDE.md, cross-refs)
3. **Phase 2**: Synthesize validation reports into prioritized update plan
4. **Phase 3**: Spawn 4 parallel update agents (docs, agents, commands, structure)
5. **Phase 4**: Verification (re-run validators, confirm all issues fixed)
6. **Phase 5**: Git commit (optional)

**Output**: Updated setup matching current meta prompt specification

---

## 📚 Reference Documents

These files contain reusable knowledge that's referenced by multiple phases:

### Core References

| File | Contents | Used By |
|------|----------|---------|
| [`core-agents.md`](prompts/reference/core-agents.md) | All 13 core agent definitions with complete workflows | Phase 3, Update Mode |
| [`coordinator-workflow.md`](prompts/reference/coordinator-workflow.md) | Coordinator agent TDD workflow, autonomous loop, breakpoints | Phase 3, agents |
| [`mcp-integration.md`](prompts/reference/mcp-integration.md) | MCP server assignments for all agents | Phase 3, agents |
| [`status-xml.md`](prompts/reference/status-xml.md) | Complete status.xml structure and usage | Phase 6, agents, commands |
| [`yolo-mode.md`](prompts/reference/yolo-mode.md) | YOLO mode documentation for autonomous development | Phase 5, agents |
| [`template-system.md`](prompts/reference/template-system.md) | Template project workflow (trust vs validate) | Phase 1 |
| [`parallelization-patterns.md`](prompts/reference/parallelization-patterns.md) | Parallel execution patterns for all phases | All phases |
| [`troubleshooting.md`](prompts/reference/troubleshooting.md) | Common issues and fixes | All phases |

### Templates

| File | Contents | Used By |
|------|----------|---------|
| [`prompts/templates/doc-templates.md`](prompts/templates/doc-templates.md) | All 12+ documentation templates | Phase 2 |
| [`prompts/templates/agent-template.md`](prompts/templates/agent-template.md) | Generic agent structure | Phase 3 |
| [`prompts/templates/command-template.md`](prompts/templates/command-template.md) | Generic command structure | Phase 4 |
| [`prompts/templates/story-template.md`](prompts/templates/story-template.md) | Story file structure (epic.story format) | /create-story command |

---

## 🚀 Quick Start Guide

### For Claude Code Running This Prompt

1. **Read this file completely** to understand the structure
2. **Determine operating mode**: Read [`prompts/phases/phase-0-detection.md`](prompts/phases/phase-0-detection.md)
3. **Follow the appropriate workflow**:
   - NEW SETUP: Follow Phases 1-7 sequentially
   - UPDATE MODE: Read [`prompts/update-mode/validation-workflow.md`](prompts/update-mode/validation-workflow.md)
4. **Reference files as needed**: See Reference Documents table above
5. **Parallelize aggressively**: See [`prompts/reference/parallelization-patterns.md`](prompts/reference/parallelization-patterns.md)

### For Humans Reading This Prompt

This prompt is designed for Claude Code to execute, not for manual use. The sharded structure allows:
- **Targeted context loading**: Only load relevant files for current phase
- **Parallel agent work**: Each agent gets specific instructions
- **Easier maintenance**: Update one file without touching others
- **Better organization**: Single responsibility per file

---

## 📊 File Structure Overview

```
prompts/
├── project-setup-meta-prompt.md (THIS FILE - Main Orchestrator)
│
├── phases/ (Sequential workflow phases)
│   ├── phase-0-detection.md          # Operating mode detection
│   ├── phase-1-discovery.md          # Discovery questions, brownfield analysis
│   ├── phase-2-documentation.md      # Doc creation workflow
│   ├── phase-3-agents.md             # Agent creation workflow
│   ├── phase-4-commands.md           # Command creation workflow
│   ├── phase-5-claude-md.md          # CLAUDE.md structure
│   ├── phase-6-features-setup.md     # features/ directory setup
│   └── phase-7-verification.md       # Verification & commit
│
├── reference/ (Reusable knowledge)
│   ├── core-agents.md                # All 13 agent definitions
│   ├── coordinator-workflow.md       # Coordinator TDD workflow
│   ├── mcp-integration.md            # MCP server assignments
│   ├── status-xml.md                 # status.xml structure
│   ├── yolo-mode.md                  # YOLO mode documentation
│   ├── template-system.md            # Template project workflow
│   ├── parallelization-patterns.md   # Parallel execution patterns
│   └── troubleshooting.md            # Common issues & fixes
│
├── update-mode/ (Validation workflow)
│   └── validation-workflow.md        # Complete update mode workflow
│
└── templates/ (Content templates)
    ├── doc-templates.md              # All documentation templates
    ├── agent-template.md             # Generic agent structure
    ├── command-template.md           # Generic command structure
    └── story-template.md             # Story file structure
```

**Total files**: 21 focused prompt files instead of 1 monolithic 156KB file

**Context savings**: 40-75% depending on phase (load only what you need)

---

## ⚡ Critical Principles

### 1. **Parallelize Everything**
See: [`prompts/reference/parallelization-patterns.md`](prompts/reference/parallelization-patterns.md)

- Launch 4-6 agents per phase whenever possible
- Synthesize results before moving to next phase
- Maximum efficiency with parallel work

### 2. **Ask First, Then Set Up**
See: [`prompts/phases/phase-1-discovery.md`](prompts/phases/phase-1-discovery.md)

- NEVER start setup without user approval
- Ask ALL questions upfront (no follow-ups mid-setup)
- Confirm understanding before proceeding

### 3. **Template First**
See: [`prompts/reference/template-system.md`](prompts/reference/template-system.md)

- ALWAYS ask about template project (saves 50-80% time)
- Two modes: trust (fast) or validate (safe)
- Smart selective copying (agents/commands vs project-specific docs)

### 4. **Brownfield Analysis Required**
See: [`prompts/phases/phase-1-discovery.md`](prompts/phases/phase-1-discovery.md)

- For brownfield projects: Launch Explore agent BEFORE confirming setup
- Create PROJECT_OVERVIEW.md with comprehensive analysis
- Use analysis to inform ALL subsequent documentation

### 5. **Feature Tracking for Brownfield**
See: [`prompts/phases/phase-6-features-setup.md`](prompts/phases/phase-6-features-setup.md)

- **FIXED**: Ask brownfield projects if they want features/ + status.xml tracking
- Analyze existing codebase to propose feature directories
- Set up tracking for work in progress

---

## 🎓 Tips for Success

### Best Practices

1. **Read phase files completely** before starting that phase
2. **Reference core-agents.md** for all agent-related questions
3. **Use parallelization** - launch multiple agents simultaneously
4. **Validate brownfield first** - don't skip the Explore agent
5. **Follow TDD language** - adjust based on enforcement level (MUST/SHOULD/MAY)

### Common Pitfalls

1. ❌ Starting setup without user approval → Read phase-1-discovery.md first
2. ❌ Not asking about template projects → Always ask, saves massive time
3. ❌ Skipping brownfield analysis → Required for existing projects
4. ❌ Creating agents sequentially → Use parallelization-patterns.md
5. ❌ Not setting up features/ for brownfield → Fixed in phase-6

---

## 📈 Success Metrics

After completing this meta prompt, the project should have:

- ✅ **Documentation**: 12+ comprehensive docs in `docs/development/`
- ✅ **Agents**: 13 core + 2-4 tech-specific agents in `.claude/agents/`
- ✅ **Commands**: 11+ slash commands in `.claude/commands/`
- ✅ **CLAUDE.md**: Complete project instructions
- ✅ **Features**: features/ directory with status.xml tracking
- ✅ **Git**: Initial commit with all deliverables
- ✅ **Ready to Code**: Developer can run `/dev` and start working

**Time to complete**:
- With template: 15-30 minutes (mostly validation)
- From scratch (greenfield): 45-75 minutes (parallelized)
- From scratch (brownfield): 60-90 minutes (includes analysis)

---

## 🔗 Original File Reference

This sharded structure was created from:
- **Original**: `project-setup-meta-prompt-ORIGINAL.md` (5469 lines, 156KB)
- **Sharding date**: 2025-10-22
- **Reason**: Context efficiency, easier maintenance, parallel agent work

---

## 📝 Version History

### Version 2.0 (2025-10-22) - Sharded Structure
- Split monolithic 156KB file into 21 focused files
- Added brownfield status.xml gap fix (phase-6)
- Added senior-developer agent (agent #2)
- Improved parallel execution documentation

### Version 1.0 (2025-10-20) - Monolithic
- Original single-file meta prompt
- 12 core agents, 11+ commands, 12+ docs

---

## 🤝 Contributing

To update this meta prompt system:

1. **Identify which file(s) to modify** (use File Structure Overview above)
2. **Update the specific file(s)** (maintain headers and cross-references)
3. **Test changes** by running setup on a new project
4. **Update this orchestrator** if navigation or structure changes
5. **Commit with descriptive message** explaining what changed and why

---

**Ready to begin?**

1. Determine operating mode: [`prompts/phases/phase-0-detection.md`](prompts/phases/phase-0-detection.md)
2. NEW SETUP: Start with [`prompts/phases/phase-1-discovery.md`](prompts/phases/phase-1-discovery.md)
3. UPDATE MODE: Read [`prompts/update-mode/validation-workflow.md`](prompts/update-mode/validation-workflow.md)

**Questions?** Check [`prompts/reference/troubleshooting.md`](prompts/reference/troubleshooting.md)
