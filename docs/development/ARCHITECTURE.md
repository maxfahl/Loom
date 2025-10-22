# Architecture Documentation - Loom Meta-Framework

**Version**: 2.0 (Sharded)
**Last Updated**: 2025-10-22
**Framework Type**: AI-native development orchestrator
**Architecture Style**: Sharded prompt system with phase-based orchestration
**Context Efficiency**: 40-75% savings vs. monolithic approach

---

## System Design Overview

### Design Principles

1. **Prompt as Infrastructure**: Markdown files serve as executable infrastructure
2. **Sharded Architecture**: 21 focused files enable parallel loading and agent specialization
3. **Phase-Based Workflow**: Sequential phases ensure proper setup order
4. **Maximum Parallelization**: 4-6 agents work simultaneously per phase
5. **Living Documentation**: Features tracked in XML, not static specs
6. **Autonomous at Scale**: YOLO mode enables hands-off development

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                  Claude Code CLI Interface                  │
│              (/dev, /review, /commit, /test, etc.)          │
└─────────────────────┬─────────────────────────────────────┘
                      │
        ┌─────────────▼─────────────┐
        │   Meta-Prompt Orchestrator │
        │  (project-setup-meta-...)  │
        │   Determines operating     │
        │   mode (NEW/UPDATE/TEMPLATE)
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼────────────────────────────────┐
        │         Phase Files (Seq. Workflow)          │
        │  phase-0: Detect mode                        │
        │  phase-1: Discovery + questions              │
        │  phase-2: Generate 12+ docs (parallel)       │
        │  phase-3: Generate 13+ agents (parallel)     │
        │  phase-4: Generate 14+ commands (parallel)   │
        │  phase-5: Generate CLAUDE.md                 │
        │  phase-6: Setup features/ + status.xml       │
        │  phase-7: Verify + commit                    │
        └─────────────┬────────────────────────────────┘
                      │
        ┌─────────────▼────────────────────────┐
        │     Reference Files (Reusable)       │
        │  core-agents.md                      │
        │  coordinator-workflow.md             │
        │  mcp-integration.md                  │
        │  status-xml.md                       │
        │  yolo-mode.md                        │
        │  template-system.md                  │
        │  parallelization-patterns.md         │
        │  troubleshooting.md                  │
        └─────────────┬────────────────────────┘
                      │
        ┌─────────────▼──────────────────────┐
        │      Template System (Optional)     │
        │  Trust mode (fast copy)             │
        │  Validate mode (verify before copy) │
        └─────────────┬──────────────────────┘
                      │
        ┌─────────────▼──────────────────────────────┐
        │        Generated Artifacts                 │
        │  .claude/agents/ (13+ agents)              │
        │  .claude/commands/ (14+ commands)          │
        │  docs/development/ (12+ docs)              │
        │  features/ (epic/story hierarchy)          │
        │  CLAUDE.md (project instructions)          │
        │  status.xml (feature tracking)              │
        └────────────────────────────────────────────┘
```

---

## File Organization Structure

### Project Root

```
project-root/
├── .claude/
│   ├── agents/           # 13 core agents + tech-specific
│   │   ├── coordinator.md
│   │   ├── senior-developer.md
│   │   ├── code-reviewer.md
│   │   ├── test-writer.md
│   │   ├── [+9 more core agents]
│   │   ├── [+2-4 tech-specific agents]
│   │
│   └── commands/         # 14+ slash commands
│       ├── dev.md
│       ├── dev-yolo.md
│       ├── review.md
│       ├── [+11 more commands]
│
├── docs/
│   └── development/      # All documentation
│       ├── INDEX.md      # Navigation hub (READ FIRST)
│       ├── README.md     # User getting started
│       ├── PRD.md        # Product requirements
│       ├── TECHNICAL_SPEC.md
│       ├── ARCHITECTURE.md (this file)
│       ├── DESIGN_SYSTEM.md
│       ├── TASKS.md
│       ├── DEVELOPMENT_PLAN.md
│       ├── PROJECT_SUMMARY.md
│       ├── EXECUTIVE_SUMMARY.md
│       ├── START_HERE.md
│       ├── YOLO_MODE.md
│       ├── status.xml    # Feature tracking (SINGLE FILE)
│       ├── features/     # Feature documentation (not code)
│       │   └── [feature-name]/
│       │       ├── FEATURE_SPEC.md
│       │       ├── TECHNICAL_DESIGN.md
│       │       ├── TASKS.md
│       │       └── epics/
│       │           ├── epic-1-foundation/
│       │           │   ├── DESCRIPTION.md
│       │           │   ├── TASKS.md
│       │           │   ├── NOTES.md
│       │           │   └── stories/
│       │           │       ├── 1.1.md
│       │           │       ├── 1.2.md
│       │           │       └── [1.N.md]
│       │           ├── epic-2-core/
│       │           │   └── ...
│       │           └── epic-3-polish/
│       │               └── ...
│
├── features/            # Feature source code (runtime only)
│   └── [feature-name]/
│       ├── src/
│       └── tests/
│
├── CLAUDE.md            # Project instructions
├── README.md            # Root README
└── .gitignore
```

### Meta-Prompt File Structure (Loom Framework)

```
loom/
├── prompts/
│   ├── project-setup-meta-prompt.md (Main Orchestrator)
│   │   └── Total: 21 files instead of monolithic 156KB
│   │   └── Context savings: 40-75%
│   │
│   ├── phases/ (Sequential workflow - 7 phases for NEW SETUP)
│   │   ├── phase-0-detection.md          # Determine operating mode
│   │   ├── phase-1-discovery.md          # Ask questions, brownfield analysis
│   │   ├── phase-2-documentation.md      # Create 12+ docs (parallel)
│   │   ├── phase-3-agents.md             # Create 13+ agents (parallel)
│   │   ├── phase-4-commands.md           # Create 14+ commands (parallel)
│   │   ├── phase-5-claude-md.md          # Create CLAUDE.md
│   │   ├── phase-6-features-setup.md     # Create features/ structure
│   │   └── phase-7-verification.md       # Verify + commit
│   │
│   ├── reference/ (Reusable knowledge - used by multiple phases)
│   │   ├── core-agents.md                # All 13 agent definitions
│   │   ├── coordinator-workflow.md       # Coordinator TDD loop, YOLO logic
│   │   ├── mcp-integration.md            # MCP server assignments
│   │   ├── status-xml.md                 # Complete status.xml structure
│   │   ├── yolo-mode.md                  # YOLO mode detailed guide
│   │   ├── template-system.md            # Template workflow (trust/validate)
│   │   ├── parallelization-patterns.md   # Parallel execution patterns
│   │   └── troubleshooting.md            # Common issues & solutions
│   │
│   ├── update-mode/ (Validation & update workflow for existing projects)
│   │   └── validation-workflow.md        # 6-phase update process
│   │
│   └── templates/ (Content templates for generation)
│       ├── doc-templates.md              # All 12+ doc templates
│       ├── agent-template.md             # Generic agent structure
│       ├── command-template.md           # Generic command structure
│       └── story-template.md             # Story file template
│
├── README.md (Framework overview)
├── project-setup-meta-prompt.md (Same as main orchestrator in root)
└── project-update-meta-prompt.md (Entry point for UPDATE MODE)
```

---

## Component Architecture

### 1. Meta-Prompt Orchestrator Layer

**File**: `project-setup-meta-prompt.md`

**Purpose**: Main navigation hub that:
- Explains the framework
- Routes to appropriate workflow (NEW/UPDATE/TEMPLATE)
- Documents file structure
- Lists all parallelization opportunities

**Responsibilities**:
- Detect operating mode
- Route to correct phase files
- Explain parallelization strategy
- Provide troubleshooting links

**Context Needs**: Low (navigation hub)
**Runs Once**: Per project setup

### 2. Phase Files (Sequential Workflow)

**Location**: `prompts/phases/`

**Architecture**: 7 phases executed sequentially

| Phase | File | Purpose | Parallelization |
|-------|------|---------|-----------------|
| 0 | phase-0-detection.md | Detect mode (NEW/UPDATE/TEMPLATE) | N/A |
| 1 | phase-1-discovery.md | Ask questions, approve setup, analyze brownfield | N/A (user input) |
| 2 | phase-2-documentation.md | Create 12+ docs | 3 batches parallel |
| 3 | phase-3-agents.md | Create 13+ agents | 4 batches parallel |
| 4 | phase-4-commands.md | Create 14+ commands | 3 batches parallel |
| 5 | phase-5-claude-md.md | Create comprehensive CLAUDE.md | N/A (single file) |
| 6 | phase-6-features-setup.md | Create features/ + status.xml | N/A (dependencies) |
| 7 | phase-7-verification.md | Verify all + git commit | N/A (final check) |

**Context Loading**: Load ONLY current phase file + referenced reference files

**Dependencies**: Previous phases must complete before next starts

### 3. Reference Files (Reusable Knowledge)

**Location**: `prompts/reference/`

**Purpose**: Encyclopedic knowledge referenced by multiple phases

**Load Strategy**: Only load when referenced by current phase

| File | Used By | Content |
|------|---------|---------|
| core-agents.md | Phase 3, agents | All 13 agent definitions |
| coordinator-workflow.md | Phase 3, agents, /dev-yolo | Coordinator YOLO loop |
| mcp-integration.md | Phase 3, agents | MCP server assignments |
| status-xml.md | Phase 6, agents, commands | XML structure + examples |
| yolo-mode.md | Phase 5, agents, commands | YOLO modes, breakpoints |
| template-system.md | Phase 1, agents, docs | Template workflow |
| parallelization-patterns.md | All phases | Batch parallelization |
| troubleshooting.md | All phases | Common issues + fixes |

**Context Savings**: 60-80% reduction vs loading all files

### 4. Template System (Optional Path)

**Location**: `prompts/reference/template-system.md`

**Purpose**: Enable copying agents/commands/docs from existing projects

**Two Operating Modes**:

```
TEMPLATE WORKFLOW (Optional)
│
├─ Ask: "Want to use template project?"
│
├─ NO → Continue NEW SETUP normally
│
└─ YES → Ask: Trust or Validate?
   │
   ├─ TRUST (Fast, 2-3 min)
   │  └─> Copy directly without verification
   │
   └─ VALIDATE (Safe, 8-12 min)
      ├─> Phase 1: Extract template content
      ├─> Phase 2: Compare with requirements
      ├─> Phase 3: Ask for approval per file
      └─> Phase 4: Copy approved files only
```

**Parallelization**: 3-4 validators work simultaneously on agents/commands/docs

**Context Savings**: 50-80% if template fully utilized

### 5. Update Mode Workflow (Existing Projects)

**Location**: `prompts/update-mode/validation-workflow.md`

**Purpose**: Validate and update existing projects to match latest spec

**6-Phase Process**:

```
Phase 0: Read existing state
  └─> Load status.xml, INDEX.md, CLAUDE.md, sample agents/commands

Phase 1: Spawn 6 parallel validators
  ├─> Docs validator
  ├─> Agents validator
  ├─> Commands validator
  ├─> Features validator
  ├─> CLAUDE.md validator
  └─> Cross-references validator

Phase 2: Synthesize reports
  └─> Prioritize issues, create update plan

Phase 3: Spawn 4 parallel updaters
  ├─> Docs updater
  ├─> Agents updater
  ├─> Commands updater
  └─> Structure updater

Phase 4: Re-validate
  └─> Confirm all issues fixed

Phase 5: Commit
  └─> Optional git commit
```

**Time**: 30-45 minutes typically

**Parallelization**: 6 validators, then 4 updaters

---

## Agent Architecture

### Agent Design Pattern

Each agent is a **markdown file with YAML frontmatter**:

```
.claude/agents/[agent-name].md
```

**Structure**:

```yaml
---
name: [Agent Name]
model: claude-opus-4-1 | claude-sonnet-4-5 | claude-haiku-4-5
speed: slow | medium | fast
use_for: [Single-line domain]
mcp_servers: [jina, github, playwright, etc.]
---

# [Agent Name]

[Detailed instructions, workflow, principles]
```

### Agent Specialization Layers

```
Layer 1: Core Agents (13)
  ├─ Orchestration: coordinator, senior-developer
  ├─ Development: code-reviewer, test-writer, bug-finder, refactor-specialist
  ├─ Execution: qa-tester, git-helper
  ├─ Design: architecture-advisor, performance-optimizer
  ├─ Documentation: documentation-writer
  └─ Extensibility: agent-creator, skill-creator

Layer 2: Tech-Specific Agents (2-4 optional)
  ├─ Security: security-reviewer (OWASP, Opus model)
  ├─ Design: design-reviewer (Playwright, WCAG 2.1 AA)
  ├─ DevOps: devops-specialist (infrastructure, CI/CD)
  └─ Data: data-engineer (pipelines, ETL)
```

### Coordinator Agent Deep Dive

**Specialization**: TDD workflow orchestration + YOLO mode control

**Workflow** (Recursive loop for each story):

```
1. Read status.xml
   └─> Current epic, current story, YOLO config

2. Load story file
   └─> Read acceptance criteria, tasks, dependencies

3. Check for Review Tasks
   ├─ YES: Implement fixes (RED-GREEN-BLUE)
   ├─ Run tests
   └─ Re-spawn code-reviewer

4. If no Review Tasks:
   ├─ Write failing tests (RED)
   ├─ Implement minimal code (GREEN)
   ├─ Refactor (BLUE)
   └─ Check off story tasks

5. Run full test suite
   └─> Validate ≥80% coverage

6. Spawn reviewers (parallel)
   ├─ code-reviewer (7-phase)
   └─ qa-tester (coverage check)

7. Process review results
   ├─ If issues: Create Review Tasks, loop to step 3
   └─ If approved: Update status to "Done"

8. Check YOLO breakpoint
   ├─ Story-level: Stop if breakpoint 1-8 hit
   ├─ Epic-level: Continue unless epic complete + breakpoint 9
   └─ Custom: Stop if configured breakpoint hit

9. Move to next story
   └─> Increment story counter, loop to step 1

10. If epic complete
    └─> Check breakpoint 9 (epic boundary)
        ├─ If enabled: Stop
        └─ If disabled: Continue to next epic
```

**MCP Servers**: None (orchestration only)

**Model**: Sonnet (good reasoning, speed)

---

## Command Architecture

### Command Design Pattern

Each command is a **markdown file with YAML frontmatter**:

```
.claude/commands/[command-name].md
```

**Structure**:

```yaml
---
name: /[command-name]
description: [One-line description]
model: claude-opus-4-1 | claude-sonnet-4-5 | claude-haiku-4-5
agents: [coordinator, code-reviewer, etc.]
---

# /[command-name]

[Detailed workflow, examples, related commands]
```

### Command Execution Pipeline

```
User Input: /[command]
     │
     ▼
Command Handler
     │
     ├─> Read YAML frontmatter
     │   └─> Extract model, agents
     │
     ├─> Load agent prompts
     │   └─> Get each agent definition
     │
     ├─> Spawn agents
     │   ├─ Sequential if dependencies
     │   └─ Parallel if independent
     │
     ├─> Synthesize outputs
     │   └─> Combine results, resolve conflicts
     │
     └─> Present to user
         └─> Summary + recommendations
```

### Command Model Routing Strategy

**Decision Tree**:

```
Complexity & Context Needed?
├─ Needs maximum reasoning → Opus
│  └─> /security-review (OWASP, 8/10+ confidence)
│
├─ High complexity + speed balance → Sonnet
│  └─> /dev, /review, /plan, /correct-course
│
└─ Simple execution + speed → Haiku
   └─> /test, /commit, /docs, /status, /yolo
```

**Time Impact**:
- Opus: Slower (10-15 min) but more accurate
- Sonnet: Medium (5-10 min) good quality
- Haiku: Fast (1-3 min) sufficient for simple tasks

---

## Status Tracking Architecture

### XML Structure (status.xml)

**Single File**: `docs/development/status.xml` (all features)

**Design Rationale**:
- Easier to read multiple features at once
- Single source of truth for project state
- Simpler git diffs (one file vs. many)
- Faster update operations

**Root Structure**:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<loom>
  <metadata>
    <version>2.0</version>
    <last-updated>2025-10-22T15:30:00Z</last-updated>
  </metadata>

  <active-feature>feature-name</active-feature>

  <features>
    <feature name="feature-name">
      <is-active-feature>true/false</is-active-feature>
      <current-epic>epic-1-foundation</current-epic>
      <current-story>1.2</current-story>
      <current-task>Task description</current-task>
      <!-- [Additional tracking data] -->
    </feature>
  </features>
</loom>
```

### Story File Hierarchy

**Naming Convention**: `[epic-number].[story-number].md`

```
features/[feature]/
└── epics/
    ├── epic-1-foundation/
    │   └── stories/
    │       ├── 1.1.md     # Epic 1, Story 1
    │       ├── 1.2.md     # Epic 1, Story 2
    │       └── 1.N.md     # Epic 1, Story N
    │
    ├── epic-2-core/
    │   └── stories/
    │       └── 2.1.md     # Epic 2, Story 1
    │
    └── epic-3-polish/
        └── stories/
            └── 3.1.md     # Epic 3, Story 1
```

**Story File Content**:

```markdown
# Story [Epic.Story]: [Title]

**Status**: Not Started | In Progress | Waiting For Review | Done
**Acceptance Criteria Met**: [X/N]

## User Story
As a [user], I want to [action], so that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Implementation Tasks
### Task 1: Infrastructure
- [ ] Subtask 1.1
- [ ] Subtask 1.2

### Task 2: Implementation
- [ ] Subtask 2.1

### Task 3: Testing (🔴🟢🔵 TDD)
- [ ] RED phase
- [ ] GREEN phase
- [ ] BLUE phase
- [ ] Coverage ≥80%

### Task 4: Review & Polish
- [ ] Code review
- [ ] Documentation
- [ ] Final verification

## Dependencies
- [Other stories]
- [External systems]
```

### State Machine

```
Story Status Transitions:
┌──────────────────────────────────────────────────────┐
│ NOT_STARTED (initial)                                │
└─────────┬──────────────────────────────────────────┘
          │ /dev: Write tests (RED)
          ▼
┌──────────────────────────────────────────────────────┐
│ IN_PROGRESS                                          │
│ - Implement code (GREEN)                             │
│ - Refactor (BLUE)                                    │
│ - Check off tasks                                    │
└─────────┬──────────────────────────────────────────┘
          │ All tasks done + tests passing
          ▼
┌──────────────────────────────────────────────────────┐
│ WAITING_FOR_REVIEW                                   │
│ - code-reviewer + qa-tester working                  │
└─────────┬──────────────────────────────────────────┘
          │
    ┌─────┴──────────┐
    │                │
    │ Issues found   │ No issues
    ▼                ▼
IN_PROGRESS   ┌──────────────────────────────────────┐
(with         │ DONE (story complete)                │
Review        │ - Update status.xml                  │
Tasks)        │ - Move to next story                 │
              └──────────────────────────────────────┘
```

---

## Workflow Patterns

### NEW SETUP Workflow (Greenfield)

```
ENTRY POINT: project-setup-meta-prompt.md

Phase 0: Detection
├─ Check for status.xml
├─ Determine mode: NEW vs UPDATE vs TEMPLATE
└─ Route to appropriate workflow

Phase 1: Discovery & Questions
├─ Ask 6 questions (project type, template, description, tech stack, TDD, team size)
├─ Get user approval
├─ If brownfield: Spawn Explore agent for PROJECT_OVERVIEW.md
└─ Route to Phase 2

Phase 2: Documentation Creation
├─ Spawn 3 batches of doc writers (parallel)
│  ├─ Batch 1: PRD, TECHNICAL_SPEC, ARCHITECTURE, DEVELOPMENT_PLAN, DESIGN_SYSTEM, TASKS
│  ├─ Batch 2: INDEX, HOOKS_REFERENCE, PROJECT_SUMMARY, EXECUTIVE_SUMMARY
│  └─ Batch 3: START_HERE, CLAUDE
│
├─ Each doc writer loads templates from doc-templates.md
├─ Wait for all batches to complete
└─ Route to Phase 3

Phase 3: Agent Creation
├─ Spawn 4 batches of agent creators (parallel)
│  ├─ Batch 1: coordinator, senior-developer, test-writer, code-reviewer
│  ├─ Batch 2: bug-finder, refactor-specialist, qa-tester, git-helper
│  ├─ Batch 3: architecture-advisor, performance-optimizer, documentation-writer, agent-creator
│  └─ Batch 4: skill-creator, (tech-specific agents)
│
├─ Each loads core-agents.md for reference
├─ Each loads mcp-integration.md for MCP assignments
├─ Wait for all batches to complete
└─ Route to Phase 4

Phase 4: Command Creation
├─ Spawn 3 batches of command creators (parallel)
│  ├─ Batch 1: /dev, /commit, /review, /status
│  ├─ Batch 2: /test, /plan, /docs, /yolo
│  └─ Batch 3: /create-feature, /correct-course, /create-story
│
├─ Each loads command-template.md
├─ Each determines model routing (Opus/Sonnet/Haiku)
├─ Wait for all batches to complete
└─ Route to Phase 5

Phase 5: CLAUDE.md Creation
├─ Create comprehensive project instructions
├─ Include: skills, agents, commands, tech stack, methodology, do/dont, checklist
├─ Load reference-docs for context
└─ Route to Phase 6

Phase 6: Features Setup
├─ Create features/ directory structure
├─ For each feature from PRD:
│  ├─ Create feature folder
│  ├─ Create epic folders (1-foundation, 2-core, 3-polish)
│  └─ Create status.xml entry
│
├─ Initialize status.xml with first feature
└─ Route to Phase 7

Phase 7: Verification & Commit
├─ Verify all deliverables:
│  ├─ All 12+ docs created
│  ├─ All 13+ agents created
│  ├─ All 14+ commands created
│  ├─ CLAUDE.md comprehensive
│  ├─ INDEX.md accurate
│  └─ features/ structure correct
│
├─ Create git commit
└─ SUCCESS: Project ready for /dev
```

**Total Time**: 45-75 minutes (parallelized)

### UPDATE MODE Workflow (Existing Projects)

```
ENTRY POINT: validation-workflow.md (when status.xml exists)

Phase 0: Read Existing State
├─ Load status.xml
├─ Read INDEX.md, CLAUDE.md
├─ Sample agents, commands, docs
└─ Understand current setup

Phase 1: Spawn 6 Parallel Validators
├─ Docs Validator → Check all 12+ docs exist and current
├─ Agents Validator → Verify all 13 agents match specification
├─ Commands Validator → Verify all 14+ commands exist
├─ Features Validator → Check epic/story structure
├─ CLAUDE.md Validator → Verify sections match agents/commands
└─ Cross-refs Validator → Check all links valid

Phase 2: Synthesize Reports
├─ Collect validation reports from all 6 validators
├─ Prioritize issues (blockers first)
├─ Create update plan with specific actions
└─ Estimate time for updates

Phase 3: Spawn 4 Parallel Updaters
├─ Docs Updater → Update/create missing docs
├─ Agents Updater → Update/create agents
├─ Commands Updater → Update/create commands
├─ Structure Updater → Fix features/ organization

Phase 4: Re-validate
├─ Re-run validators from Phase 1
├─ Confirm all issues fixed
└─ Identify any new issues

Phase 5: Optional Commit
├─ Create conventional commit summarizing changes
└─ Show git diff to user
```

**Total Time**: 30-45 minutes

### TEMPLATE MODE Workflow

```
Entry Question: "Want to use existing project as template?"

Trust Path (Fast, 2-3 min):
├─ Ask for template project path
├─ Direct copy agents/ → .claude/agents/
├─ Direct copy commands/ → .claude/commands/
├─ Skip docs (project-specific)
└─ Continue to Phase 5

Validate Path (Safe, 8-12 min):
├─ Ask for template project path
├─ Phase 1: Extract template content
│   ├─ Read all template agents
│   ├─ Read all template commands
│   └─ Compare with specification
│
├─ Phase 2: Spawn 3 parallel validators
│   ├─ Agents validator
│   ├─ Commands validator
│   └─ Docs validator
│
├─ Phase 3: Ask for approval per file
│   ├─ "Use agent [X] from template? (Y/n)"
│   ├─ Collect decisions
│   └─ Copy only approved files
│
└─ Continue to Phase 5
```

---

## Data Flow Architecture

### Feature Development Data Flow

```
User: /create-feature "user-authentication"
         │
         ▼
coordinator agent
         │
         ├─ Create docs/development/features/user-authentication/
         │  ├─ FEATURE_SPEC.md
         │  ├─ TECHNICAL_DESIGN.md
         │  └── epics/
         │      ├── epic-1-foundation/
         │      ├── epic-2-core/
         │      └── epic-3-polish/
         │
         ├─ Create status.xml entry
         │
         └─ Update INDEX.md → Add feature link

User: /create-story
         │
         ▼
coordinator agent
         │
         ├─ Read status.xml → Find current epic
         │
         ├─ Read epic TASKS.md → Understand context
         │
         ├─ Create story file
         │  └─ docs/development/features/.../epics/.../stories/1.1.md
         │
         ├─ Populate story template
         │  ├─ User story
         │  ├─ Acceptance criteria
         │  ├─ Tasks (4 categories)
         │  └─ Dependencies
         │
         ├─ Update status.xml
         │  └─ <current-story>1.1</current-story>
         │
         └─ Display story to user

User: /dev
         │
         ▼
coordinator agent
         │
         ├─ Read status.xml → Get current story
         │
         ├─ Read story file → Get acceptance criteria
         │
         ├─ Spawn test-writer
         │  └─ Write failing tests (RED)
         │
         ├─ Implement code (GREEN)
         │
         ├─ Refactor (BLUE)
         │
         ├─ Run tests → Validate ≥80% coverage
         │
         ├─ Spawn parallel reviewers
         │  ├─ code-reviewer (7-phase)
         │  └─ qa-tester (coverage)
         │
         ├─ Update story file
         │  ├─ Check off completed tasks
         │  └─ Update status → "Waiting For Review"
         │
         ├─ Update status.xml
         │  └─ <current-task>Review complete</current-task>
         │
         └─ Check YOLO breakpoint
            ├─ If breakpoint hit: Stop
            └─ If continue: Loop to next story

User: /review (if code-reviewer found issues)
         │
         ▼
code-reviewer agent
         │
         ├─ Run 7-phase review
         │
         ├─ Create Review Tasks in story if issues
         │
         └─ Update story status
            ├─ If issues: "In Progress" (back to fixing)
            └─ If approved: "Done"
```

---

## Design Patterns & Principles

### Pattern 1: Sharded Prompts

**Problem**: Monolithic 156KB file exceeds context budgets

**Solution**: Split into 21 focused files
- Main orchestrator (navigation)
- 7 phase files (sequential workflow)
- 8 reference files (encyclopedic knowledge)
- 1 update workflow
- 4 template files

**Benefit**: Load only needed files per phase (40-75% context savings)

### Pattern 2: Parallel Batching

**Problem**: Sequential document/agent/command creation takes 2+ hours

**Solution**: Batch into 3-4 parallel executions per phase

```
Sequential: Create doc 1 → wait → Create doc 2 → wait → Create doc 3 (30 min)
Parallel:   Create docs 1-6 in parallel (5 min)
Savings:    80% faster
```

### Pattern 3: Markdown as Executable Code

**Problem**: Traditional specs drift from implementation

**Solution**: Agents and commands are markdown files with YAML frontmatter

```yaml
---
name: [name]
model: [model]
---

[Executable instructions]
```

**Benefit**: Single source of truth, easy to modify, versioned in git

### Pattern 4: Living Documentation

**Problem**: Feature specs become outdated quickly

**Solution**: Store features in status.xml + story files

- **status.xml**: Current state (what's in progress)
- **Story files**: Task checklists that agents check off
- **Epic docs**: Overview, but story details in story files

**Benefit**: Agents maintain docs as they complete tasks

### Pattern 5: Recursive Coordinator Loop

**Problem**: How to autonomously complete multiple stories?

**Solution**: Coordinator loops through stories

```
For each story in epic:
  Read story file
  Implement RED-GREEN-BLUE
  Check off tasks
  Run reviewers
  If issues: Handle as Review Tasks
  Update status
  Check YOLO breakpoint
  Continue or stop
```

---

## Integration Points

### MCP Server Integration

**Integration Pattern**:

```
Agent needs external data?
  │
  ├─ YES: Use MCP server from mcp_servers list
  │  └─> documentation-writer has github, jina, firecrawl
  │
  └─ NO: Use local tools (Read, Write, Bash)
```

**Assignment Logic** (from mcp-integration.md):

- **github**: documentation-writer (creating/updating docs in repos)
- **jina**: documentation-writer (reading web pages, extracting content)
- **firecrawl**: documentation-writer (scraping, crawling documentation)
- **playwright**: design-reviewer (live UI testing, screenshots)
- **zai**: senior-developer (analyze architecture diagrams)
- **vibe-check**: security-reviewer (code quality signals)
- **web-search-prime**: architecture-advisor (research best practices)

### Git Integration

**Operations Flow**:

```
Agent completes task
  │
  ├─ git status → Check what changed
  ├─ git add . → Stage changes
  ├─ git commit -m "conventional format" → Commit
  └─ Optionally: git push (if auto-push enabled)
```

**Commit Format** (conventional):
```
type(scope): subject

Body with details

Closes #123
```

---

## Extensibility Architecture

### Adding Custom Agents

1. Create `.claude/agents/[name].md`
2. Add YAML frontmatter with model, speed, MCP servers
3. Write detailed instructions
4. Reference in CLAUDE.md
5. Link from coordinator if needed

### Adding Custom Commands

1. Create `.claude/commands/[name].md`
2. Add YAML frontmatter with model, agents list
3. Document workflow
4. Reference in CLAUDE.md

### Adding Domain-Specific Documentation

1. Create in `docs/development/`
2. Link from INDEX.md quick reference table
3. Update START_HERE.md if role-specific
4. Update CLAUDE.md if methodology related

---

## Performance Characteristics

### Startup Performance

| Mode | Phase Loading | Time | Context Used |
|------|---------------|------|--------------|
| NEW SETUP Phase 1 | Meta + Phase 1 | <1 sec | ~10KB |
| NEW SETUP Phase 2 | Phase 2 + doc-templates | 1-2 sec | ~20KB |
| NEW SETUP Phase 3 | Phase 3 + core-agents | 1-2 sec | ~50KB |
| UPDATE MODE | validation-workflow + validators | 2-3 sec | ~30KB |
| /dev | coordinator + story file | <1 sec | ~15KB |

### Parallel Execution Speedup

| Task | Sequential | Parallel | Speedup |
|------|-----------|----------|---------|
| Phase 2 (12 docs) | 30 min | 5 min | **6x** |
| Phase 3 (13 agents) | 50 min | 8 min | **6x** |
| Phase 4 (14 commands) | 35 min | 6 min | **6x** |
| Full NEW SETUP | 120+ min | 30 min | **4x** |

---

## Security Architecture

### Prompt Injection Prevention

- Agents don't accept user code as input (only existing files)
- Story files are templated, not user-generated
- YAML frontmatter validated before execution

### Secret Management

- No secrets in docs, agents, commands
- Template copying scans for hardcoded secrets
- CLAUDE.md never includes credentials

### Agent Isolation

- Agents have no access to system files outside project
- MCP servers are explicitly declared
- Code review agents check for secrets in code

---

## Related Documentation

- **TECHNICAL_SPEC.md** - Implementation details, agent system, commands
- **README.md** - Framework overview for users
- **project-setup-meta-prompt.md** - Main orchestrator (navigation hub)
- **YOLO_MODE.md** - Detailed autonomous mode guide

---

**Last Updated**: 2025-10-22
**Version**: 2.0 (Sharded)
**Status**: Stable
