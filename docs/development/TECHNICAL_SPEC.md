# Technical Specifications - Loom Meta-Framework

**Version**: 2.0 (Sharded)
**Last Updated**: 2025-10-22
**Framework**: AI-native development orchestrator with autonomous agents and TDD workflows
**Total Prompts**: 21 files (sharded from monolithic 156KB)
**Total Agents**: 13 core + 2-4 tech-specific
**Total Commands**: 14+ slash commands

---

## Overview

Loom is a **documentation-only meta-framework** designed for Claude Code CLI that orchestrates autonomous AI agents through markdown-based prompts and XML-based feature tracking. It enforces Test-Driven Development (TDD), supports parallel agent execution, and enables autonomous development loops through YOLO mode.

### Key Design Principles

1. **Markdown as Code**: Agents and commands are defined in markdown files
2. **Sharded Architecture**: 21 focused files instead of 1 monolithic file (40-75% context savings)
3. **Phase-Based Setup**: 7 sequential phases for new projects, 6 phases for updates
4. **Maximum Parallelization**: 4-6 agents work simultaneously per phase (70-80% time savings)
5. **TDD by Design**: Red-Green-Refactor cycle enforced at every level
6. **Living Documentation**: Features tracked in status.xml and story files, not static specs

---

## System Architecture

### Core Layers

```
┌─────────────────────────────────────────────────────────────┐
│ Claude Code CLI Interface                                   │
│ (User entry point - /dev, /review, /commit, /test, etc.)   │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ Meta-Prompt Orchestrator                                    │
│ (project-setup-meta-prompt.md - Main navigation hub)       │
│ Determines: NEW SETUP | UPDATE MODE | TEMPLATE MODE       │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐   ┌──────▼───────────┐
│ Phase Files  │   │ Reference Files  │
│ (7 total)    │   │ (8 total)        │
│ Sequential   │   │ Reusable         │
│ workflow     │   │ knowledge        │
└──────┬───────┘   └──────┬───────────┘
       │                  │
       └──────────┬───────┘
                  │
        ┌─────────▼──────────┐
        │ Template System    │
        │ (trust/validate)   │
        │ Parallel copying   │
        └──────────┬─────────┘
                   │
        ┌──────────▼────────────┐
        │ Generated Artifacts   │
        ├──────────────────────┤
        │ .claude/agents/      │ 13+ agents
        │ .claude/commands/    │ 14+ commands
        │ docs/development/    │ 12+ docs
        │ features/            │ status.xml files
        │ CLAUDE.md            │ Project config
        └──────────────────────┘
```

### Meta-Prompt File Organization

```
prompts/
├── project-setup-meta-prompt.md (Main Orchestrator - THIS FILE)
│
├── phases/ (Sequential workflow)
│   ├── phase-0-detection.md          # Operating mode detection
│   ├── phase-1-discovery.md          # Questions + brownfield analysis
│   ├── phase-2-documentation.md      # Create 12+ docs
│   ├── phase-3-agents.md             # Create 13+ agents
│   ├── phase-4-commands.md           # Create 14+ commands
│   ├── phase-5-claude-md.md          # Create CLAUDE.md
│   ├── phase-6-features-setup.md     # Create features/ + status.xml
│   └── phase-7-verification.md       # Verify + commit
│
├── reference/ (Reusable knowledge)
│   ├── core-agents.md                # Complete agent definitions
│   ├── coordinator-workflow.md       # Coordinator TDD loop
│   ├── mcp-integration.md            # MCP server assignments
│   ├── status-xml.md                 # status.xml structure
│   ├── yolo-mode.md                  # YOLO mode documentation
│   ├── template-system.md            # Template workflow
│   ├── parallelization-patterns.md   # Parallel execution
│   └── troubleshooting.md            # Common issues & fixes
│
├── update-mode/
│   └── validation-workflow.md        # Update/validate workflow
│
└── templates/ (Content templates)
    ├── doc-templates.md              # All doc templates
    ├── agent-template.md             # Generic agent structure
    ├── command-template.md           # Generic command structure
    └── story-template.md             # Story file template
```

---

## Agent System

### Agent Architecture

Each agent is a **markdown file with YAML frontmatter** that defines:

```yaml
---
# Agent Definition Structure
name: [Agent Name]
model: [claude-opus-4-1 | claude-sonnet-4-5 | claude-haiku-4-5]
speed: [slow | medium | fast]
use_for: [Domain/specialization]
mcp_servers: [List of MCP servers this agent uses]
---

[Agent instructions - detailed prompt explaining role and workflow]
```

### 13 Core Agents

| # | Name | Model | Speed | Purpose | MCP Servers |
|---|------|-------|-------|---------|------------|
| 1 | **coordinator** | Sonnet | Medium | TDD workflow orchestrator, YOLO mode control | None |
| 2 | **senior-developer** | Sonnet | Medium | Architecture review, design decisions | None |
| 3 | **code-reviewer** | Sonnet | Medium | 7-phase code review with triage | None |
| 4 | **test-writer** | Sonnet | Medium | TDD test generation (80%+ coverage) | None |
| 5 | **bug-finder** | Sonnet | Medium | Edge case detection, error handling | None |
| 6 | **refactor-specialist** | Sonnet | Medium | Code quality improvements (GREEN tests only) | None |
| 7 | **qa-tester** | Haiku | Fast | Test execution, coverage validation | None |
| 8 | **git-helper** | Haiku | Fast | Git operations, conventional commits | None |
| 9 | **architecture-advisor** | Sonnet | Medium | System design, scalability | None |
| 10 | **performance-optimizer** | Sonnet | Medium | Performance analysis, bottleneck identification | None |
| 11 | **documentation-writer** | Haiku | Fast | Docs, JSDoc, API reference | github, jina, firecrawl |
| 12 | **agent-creator** | Sonnet | Medium | Build custom agents | None |
| 13 | **skill-creator** | Sonnet | Medium | Create Claude Skills packages | None |

### Optional Tech-Specific Agents

**Security Domain**:
- **security-reviewer** - OWASP Top 10 scanning (Opus model required)

**Design Domain**:
- **design-reviewer** - UI/UX with Playwright, WCAG 2.1 AA (Haiku/Sonnet)

**DevOps Domain**:
- **devops-specialist** - Infrastructure, deployment, CI/CD

**Data Engineering Domain**:
- **data-engineer** - Data pipeline, ETL, analytics

### Agent YAML Frontmatter Format

```yaml
---
name: [Agent Name]
model: claude-opus-4-1 | claude-sonnet-4-5 | claude-haiku-4-5
speed: slow | medium | fast
use_for: [Single-line purpose]
mcp_servers: [array or comma-list]
specialization: [Domain focus]
---
```

---

## Command System

### Command Architecture

Each command is a **slash command defined in markdown** with YAML frontmatter:

```yaml
---
# Command Definition Structure
name: /[command-name]
description: [One-line description]
model: [claude-opus-4-1 | claude-sonnet-4-5 | claude-haiku-4-5]
agents: [List of agents this command spawns]
---

[Command instructions - detailed workflow for this command]
```

### 14+ Core Commands

| Command | Model | Primary Agent | Purpose |
|---------|-------|---------------|---------|
| **/dev** | Sonnet | coordinator | Continue TDD development with automatic task tracking |
| **/dev-yolo** | Sonnet | coordinator | Launch autonomous YOLO loop (complete stories/epics) |
| **/commit** | Haiku | git-helper | Smart commit with tests, linting, conventional format |
| **/review** | Sonnet | code-reviewer | 7-phase code review with triage matrix (Blocker/Improvement/Nit) |
| **/security-review** | Opus | security-reviewer | OWASP Top 10 security scanning with FALSE_POSITIVE filtering |
| **/design-review** | Sonnet | design-reviewer | UI/UX review with Playwright, WCAG 2.1 AA, responsive testing |
| **/test** | Haiku | qa-tester | Run tests with coverage validation (80%+ mandatory) |
| **/plan** | Sonnet | senior-developer | Plan feature with TDD breakdown and parallel opportunities |
| **/status** | Haiku | git-helper | Project status report (git, tasks, tests, metrics) |
| **/docs** | Haiku | documentation-writer | Update documentation (code, API, user, all) |
| **/yolo** | Haiku | coordinator | Configure YOLO mode breakpoints (story/epic/custom) |
| **/create-feature** | Sonnet | coordinator | Create new feature with epics and documentation |
| **/correct-course** | Sonnet | senior-developer | Adjust feature direction, reorganize epics |
| **/create-story** | Sonnet | coordinator | Generate next user story for current epic |

### Model Routing Strategy

**Opus** (claude-opus-4-1):
- Security reviews (maximum accuracy for vulnerabilities)
- Complex architectural decisions
- When maximum reasoning power needed

**Sonnet** (claude-sonnet-4-5):
- Code implementation and reviews
- Testing and TDD workflows
- Coordination and orchestration
- Planning and architecture

**Haiku** (claude-haiku-4-5):
- Fast operations (tests, git, docs, status)
- Simple templating and generation
- When speed prioritized over depth

---

## Feature Tracking System

### Status.xml Structure

**Location**: `docs/development/status.xml` (single file for all features)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<loom>
  <metadata>
    <version>2.0</version>
    <last-updated>2025-10-22T15:30:00Z</last-updated>
  </metadata>

  <!-- Active Feature Configuration -->
  <active-feature>user-authentication</active-feature>

  <features>
    <!-- Feature Entry -->
    <feature name="user-authentication">
      <is-active-feature>true</is-active-feature>
      <description>JWT-based user authentication and authorization</description>
      <status>in-progress</status>

      <!-- Epic Tracking -->
      <current-epic>epic-1-foundation</current-epic>
      <current-story>1.2</current-story>

      <!-- Story Status -->
      <current-task>Implement login endpoint</current-task>
      <completed-tasks>
        <task story="1.1" commit="abc123">Setup JWT middleware</task>
      </completed-tasks>

      <whats-next>
        <task story="1.2">Add token refresh mechanism</task>
        <task story="1.3">Implement logout with token revocation</task>
      </whats-next>

      <!-- YOLO Mode Configuration -->
      <yolo-mode enabled="true">
        <granularity>epic-level</granularity>
        <breakpoints>9</breakpoints>
        <notes>Stopping only at epic boundaries</notes>
      </yolo-mode>

      <!-- Epic Organization -->
      <epics>
        <epic id="1" status="in-progress">epic-1-foundation</epic>
        <epic id="2" status="pending">epic-2-core-features</epic>
        <epic id="3" status="pending">epic-3-polish</epic>
      </epics>

      <!-- Blockers -->
      <blockers>
        <blocker story="1.2">Need database connection pool setup</blocker>
      </blockers>

      <!-- Notes -->
      <notes>
        <note timestamp="2025-10-22T15:30:00Z">
          Updated story 1.1 - JWT middleware working correctly
        </note>
      </notes>
    </feature>
  </features>
</loom>
```

### Story File Structure

**Location**: `docs/development/features/[feature]/epics/[epic-id]/stories/[epic.story].md`

**Naming**: `[epic-number].[story-number].md` (e.g., `1.1.md`, `1.2.md`, `2.1.md`)

```markdown
# Story [Epic.Story]: [User Story Title]

**Epic**: [Epic name]
**Status**: [Not Started | In Progress | Waiting For Review | Done]
**Acceptance Criteria Met**: [0/3] or similar

## User Story

As a [user type], I want to [action], so that [benefit].

## Acceptance Criteria

1. [ ] Criterion 1
2. [ ] Criterion 2
3. [ ] Criterion 3

## Implementation Tasks

### Task 1: Setup/Infrastructure
- [ ] Subtask 1.1
- [ ] Subtask 1.2

### Task 2: Feature Implementation
- [ ] Subtask 2.1
- [ ] Subtask 2.2

### Task 3: Testing (🔴🟢🔵 TDD Cycle)
- [ ] Write failing tests (RED)
- [ ] Implement code (GREEN)
- [ ] Refactor (BLUE)
- [ ] Verify coverage ≥80%

### Task 4: Review & Polish
- [ ] Code review (7-phase)
- [ ] Update documentation
- [ ] Final verification

## Technical Details

[Implementation approach, API changes, database changes, etc.]

## Testing Requirements

- Unit test coverage: ≥80%
- Integration tests: [Specific scenarios]
- E2E tests: [Specific flows]

## Dependencies

- [Other stories this depends on]
- [External systems]

## Completion Checklist

- [ ] All acceptance criteria met
- [ ] Tests passing with ≥80% coverage
- [ ] Code review approved
- [ ] Documentation updated
- [ ] Status updated in status.xml
```

### Epic Directory Structure

```
features/[feature-name]/
├── FEATURE_SPEC.md
├── TECHNICAL_DESIGN.md
├── TASKS.md
└── epics/
    ├── epic-1-foundation/
    │   ├── DESCRIPTION.md      # Epic overview
    │   ├── TASKS.md            # Epic-level tasks
    │   ├── NOTES.md            # Implementation notes
    │   └── stories/
    │       ├── 1.1.md          # Epic 1, Story 1
    │       ├── 1.2.md          # Epic 1, Story 2
    │       └── 1.3.md          # Epic 1, Story 3
    ├── epic-2-core/
    │   ├── DESCRIPTION.md
    │   ├── TASKS.md
    │   ├── NOTES.md
    │   └── stories/
    │       └── 2.1.md
    └── epic-3-polish/
        ├── DESCRIPTION.md
        ├── TASKS.md
        ├── NOTES.md
        └── stories/
            └── 3.1.md
```

---

## Template System

### Trust vs. Validate Modes

#### Trust Mode (Fast)
- **Time**: 2-3 minutes per batch
- **Validation**: None
- **Use Case**: Confident in template quality, speed priority
- **Process**: Copy files directly without verification

#### Validate Mode (Safe)
- **Time**: 8-12 minutes per batch
- **Validation**: Full verification before copy
- **Use Case**: First-time template use, production projects
- **Process**:
  1. Extract template content
  2. Compare with current project requirements
  3. Ask for approval per file
  4. Copy only approved files

### Template Parallelization

**Batch Size**: Process multiple components simultaneously

```
Batch 1 (Parallel): Validate/copy agents 1-4
Batch 2 (Parallel): Validate/copy agents 5-8
Batch 3 (Parallel): Validate/copy agents 9-12
Batch 4 (Sequential): Validate/copy agent 13
↓
Batch 1 (Parallel): Validate/copy commands 1-4
Batch 2 (Parallel): Validate/copy commands 5-8
Batch 3 (Parallel): Validate/copy commands 9-11
↓
Batch 1 (Parallel): Validate/copy docs 1-6
Batch 2 (Parallel): Validate/copy docs 7-10
Batch 3 (Parallel): Validate/copy docs 11-12
```

---

## YOLO Mode Implementation

### Stopping Granularities

#### A. STORY-LEVEL (Default)
- **Stops at**: Any of 8 story-level breakpoints
- **Control**: Fine-grained, maximum oversight
- **Use Case**: First implementations, critical features

**Breakpoints**:
1. After development, before code review
2. After code review, before tests
3. After tests, before user testing
4. After user testing, before commit
5. After commit, before push
6. Before any file changes
7. Before running tests
8. Before major refactoring

#### B. EPIC-LEVEL (Maximum Autonomy)
- **Stops at**: Breakpoint 9 only (epic boundary)
- **Control**: Minimal, high autonomy
- **Use Case**: Trusted patterns, rapid development

**Configuration**: `<yolo-mode><granularity>epic-level</granularity></yolo-mode>`

#### C. CUSTOM
- **Stops at**: User-selected breakpoints (1-9)
- **Control**: Balanced
- **Use Case**: Specific oversight requirements

**Configuration**: `<yolo-mode><breakpoints>1,3,4,8</breakpoints></yolo-mode>`

### Coordinator Workflow in YOLO Mode

```
1. Read status.xml (current epic, story, YOLO config)
2. Check for Review Tasks (prioritize first)
3. If Review Tasks:
   - Implement fixes (Red-Green-Refactor)
   - Run tests
   - Spawn code-reviewer again
4. If no Review Tasks:
   - Write failing tests (RED)
   - Implement code (GREEN)
   - Refactor (BLUE)
   - Check off story tasks
5. Run full test suite
6. Spawn code-reviewer + qa-tester (parallel)
7. If issues found:
   - Create Review Tasks in story
   - Update status to "In Progress"
   - Loop back to step 2
8. If no issues:
   - Update story status to "Done"
   - Increment to next story
9. Check YOLO breakpoint (1-9)
10. If breakpoint hit: Stop and wait for user
    Else: Continue to step 1
11. If epic complete and breakpoint 9 enabled: Stop
    Else: Continue with next epic
```

---

## Parallelization Patterns

### Phase 2: Documentation Creation (5 minutes)

```
Batch 1 (Parallel):
  - Create PRD.md
  - Create TECHNICAL_SPEC.md
  - Create ARCHITECTURE.md
  - Create DEVELOPMENT_PLAN.md
  - Create DESIGN_SYSTEM.md
  - Create TASKS.md

Batch 2 (Parallel):
  - Create INDEX.md
  - Create HOOKS_REFERENCE.md
  - Create PROJECT_SUMMARY.md
  - Create EXECUTIVE_SUMMARY.md

Batch 3 (Parallel):
  - Create START_HERE.md
  - Create CLAUDE.md (or prep for phase 5)
```

### Phase 3: Agent Creation (8 minutes)

```
Batch 1 (Parallel):
  - Create coordinator
  - Create senior-developer
  - Create test-writer
  - Create code-reviewer

Batch 2 (Parallel):
  - Create bug-finder
  - Create refactor-specialist
  - Create qa-tester
  - Create git-helper

Batch 3 (Parallel):
  - Create architecture-advisor
  - Create performance-optimizer
  - Create documentation-writer
  - Create agent-creator

Batch 4 (Sequential):
  - Create skill-creator
  - (Tech-specific agents if needed)
```

### Phase 4: Command Creation (6 minutes)

```
Batch 1 (Parallel):
  - Create /dev
  - Create /commit
  - Create /review
  - Create /status

Batch 2 (Parallel):
  - Create /test
  - Create /plan
  - Create /docs
  - Create /yolo

Batch 3 (Parallel):
  - Create /create-feature
  - Create /correct-course
  - Create /create-story
```

---

## MCP Server Integration

### MCP Server Assignments

| Server | Agents | Use Case |
|--------|--------|----------|
| **playwright** | design-reviewer | Live UI testing, WCAG validation, responsive checks |
| **github** | documentation-writer | Create/update GitHub files, search code patterns |
| **jina** | documentation-writer | Extract web content, research documentation |
| **firecrawl** | documentation-writer | Deep web research, crawl documentation sites |
| **zai** | senior-developer | Image analysis for architecture diagrams |
| **vibe-check** | security-reviewer | Code quality signals |
| **web-search-prime** | architecture-advisor | Research technical patterns, best practices |

### Smart Tool Selection

**Documentation Agent Decision Tree**:
```
Need to research external API?
  ├─ YES: Use jina_reader or firecrawl_scrape
  ├─ NO: Use Read/Write tools for local files
Need GitHub operations?
  ├─ YES: Use github tools
  ├─ NO: Use Read/Write for local repos
Need to extract web content at scale?
  ├─ YES: Use firecrawl_crawl
  ├─ NO: Use jina for single pages
```

---

## Operating Modes

### Mode 1: NEW SETUP (Greenfield)

**Detection**: No `status.xml` found

**Workflow**: 7 phases sequentially

```
Phase 0: Detection
  ↓
Phase 1: Discovery (Questions + approval)
  ↓
Phase 2: Documentation (Parallel batches)
  ↓
Phase 3: Agents (Parallel batches)
  ↓
Phase 4: Commands (Parallel batches)
  ↓
Phase 5: CLAUDE.md
  ↓
Phase 6: Features Setup
  ↓
Phase 7: Verification & Commit
```

**Time**: 45-75 minutes

### Mode 2: UPDATE (Existing Setup)

**Detection**: `status.xml` found

**Workflow**: 6 phases for validation and updates

```
Phase 0: Read existing state
  ↓
Phase 1: Spawn 6 parallel validators
  ├─ Validate docs
  ├─ Validate agents
  ├─ Validate commands
  ├─ Validate features
  ├─ Validate CLAUDE.md
  ├─ Validate cross-references
  ↓
Phase 2: Synthesize validation reports
  ↓
Phase 3: Spawn 4 parallel updaters
  ├─ Update docs
  ├─ Update agents
  ├─ Update commands
  ├─ Update structure
  ↓
Phase 4: Re-validate (confirm fixes)
  ↓
Phase 5: Commit (optional)
```

**Time**: 30-45 minutes

### Mode 3: TEMPLATE (From Existing Project)

**Detection**: User selects template project

**Options**:
- **Trust**: Copy directly (2-3 min)
- **Validate**: Verify before copy (8-12 min)

**Parallelization**: 3-4 parallel validators/agents during validation phase

---

## Development Cycle

### Standard Development Workflow

```
1. /create-feature
   └─> Creates feature folder, epics, FEATURE_SPEC, TECHNICAL_DESIGN

2. /create-story (repeat for each story)
   └─> Creates story file with acceptance criteria, tasks

3. /yolo
   └─> Configure stopping granularity (story/epic/custom)

4. /dev or /dev-yolo
   ├─> Coordinator reads story
   ├─> Implements Red-Green-Refactor cycle
   ├─> Checks off tasks
   ├─> Updates story status
   ├─> Spawns reviewers
   └─> Continues or stops based on YOLO config

5. /review (if needed)
   └─> 7-phase code review, creates Review Tasks if issues

6. /test
   └─> Run tests, validate ≥80% coverage

7. /commit
   └─> Git commit with conventional format

8. Repeat steps 4-7 until feature complete
```

### Code Review Phases

```
Phase 1: Architectural Design & Integrity (Critical)
Phase 2: Functionality & Correctness (Critical)
Phase 3: Security (Non-Negotiable)
Phase 4: Maintainability & Readability (High)
Phase 5: Testing Strategy & Robustness (High)
Phase 6: Performance & Scalability (Important)
Phase 7: Dependencies & Documentation (Important)

Triage: [Blocker] [Improvement] [Nit]
```

---

## Documentation Requirements

### 12+ Core Documentation Files

1. **INDEX.md** - Master navigation hub (quick reference tables)
2. **README.md** - Getting started (minimal, 3KB)
3. **PRD.md** - Product requirements (what to build)
4. **TECHNICAL_SPEC.md** - Implementation details (how to build)
5. **ARCHITECTURE.md** - System design and diagrams
6. **DESIGN_SYSTEM.md** - UI/UX guidelines, component priorities
7. **TASKS.md** - Development checklist with phases
8. **DEVELOPMENT_PLAN.md** - TDD methodology, roadmap
9. **PROJECT_SUMMARY.md** - Comprehensive overview
10. **EXECUTIVE_SUMMARY.md** - High-level technical summary
11. **START_HERE.md** - Role-based navigation guide
12. **YOLO_MODE.md** - Autonomous development configuration

### Optional Documentation

- **PROJECT_OVERVIEW.md** (brownfield only) - Existing codebase analysis
- **CODE_REVIEW_PRINCIPLES.md** - 7-phase review framework
- **SECURITY_REVIEW_CHECKLIST.md** - OWASP scanning methodology
- **DESIGN_PRINCIPLES.md** - UI/UX design review with Playwright
- Domain-specific docs (API_REFERENCE, DEPLOYMENT, etc.)

---

## Project Configuration File (CLAUDE.md)

**Location**: `CLAUDE.md` in project root

**Purpose**: Comprehensive project instructions for Claude Code

**Sections**:
1. Skills usage guide (if applicable)
2. Parallel agent execution strategy
3. Coordinator agent pattern
4. 13+ agent reference with MCP assignments
5. 14+ command reference with model routing
6. Code style and conventions
7. Testing framework and TDD requirements
8. Tech stack and versions
9. Project structure overview
10. Do/Don't checklist
11. Pre-task checklist

**Size**: 3-5KB typically

---

## File Format Specifications

### Markdown Agent Definition

```markdown
---
name: [Agent Name]
model: claude-opus-4-1 | claude-sonnet-4-5 | claude-haiku-4-5
speed: slow | medium | fast
use_for: [Single-line purpose]
mcp_servers: [Array of MCP servers]
---

# [Agent Name] Agent

**Specialization**: [Domain focus]
**Model Rationale**: [Why this model chosen]

## Responsibilities

[Detailed list of what this agent does]

## Workflow

[Step-by-step workflow this agent follows]

## Key Principles

[Operating principles and constraints]

## Related Agents

[Which agents this one coordinates with]
```

### Markdown Command Definition

```markdown
---
name: /[command-name]
description: [One-line description]
model: claude-opus-4-1 | claude-sonnet-4-5 | claude-haiku-4-5
agents: [List of agents spawned]
---

# /[command-name] Command

**Description**: [What this command does]
**Model Choice**: [Why this model]

## Workflow

[Step-by-step execution]

## Example Usage

```bash
/[command-name] [args]
```

## Related Commands

[Other related commands]
```

---

## Performance Targets

### Setup Performance

| Mode | Time | Notes |
|------|------|-------|
| NEW SETUP (greenfield) | 45-75 min | 7 phases, parallel batches |
| NEW SETUP (brownfield) | 60-90 min | Includes codebase analysis |
| UPDATE MODE | 30-45 min | Validation + updates |
| TEMPLATE (trust) | 15-30 min | Direct copy, minimal validation |
| TEMPLATE (validate) | 30-45 min | Full verification before copy |

### Agent Performance

| Agent | Task | Target Time | Notes |
|-------|------|------------|-------|
| coordinator | Plan story | <5 min | Read story, plan RED-GREEN-BLUE |
| test-writer | Write tests | 5-15 min | Depends on story complexity |
| code-reviewer | Review code | 10-20 min | 7-phase review |
| qa-tester | Run tests | <2 min | Fast execution |
| documentation-writer | Write docs | 3-10 min | Depends on doc type |

### YOLO Loop Targets

| Granularity | Typical Speed | Notes |
|-------------|---------------|-------|
| Story-Level | 30-60 min/story | Full TDD cycle + review |
| Epic-Level | 2-4 hours/epic | Complete all stories without stops |
| Custom | Variable | Depends on breakpoint selection |

---

## Scalability Considerations

### Agent Count Scaling

- **13 core agents**: Works well for projects
- **2-4 tech-specific agents**: Domain-specific add-ons
- **Parallel cap**: 6 agents per batch (diminishing returns beyond)

### Documentation Scaling

- **12+ core docs**: Covers standard projects
- **Additional docs**: Add domain-specific as needed
- **File size**: Keep individual files <5KB average for fast loading

### Feature Tracking Scaling

- **Single status.xml**: All features tracked in one file
- **Multiple epics per feature**: No limit on depth
- **Story files**: One per story, indexed in status.xml
- **Performance**: Tested up to 50+ stories per feature

### Prompt Context

- **Monolithic approach**: 1 file × 156KB = high context (75-100% of budget)
- **Sharded approach**: 21 files × avg 7KB = lower context (15-30% per phase)
- **Context savings**: 40-75% depending on phase and file selection

---

## Error Handling & Validation

### Setup Validation

**Phase 7 Checks**:
- [ ] All 12+ docs created
- [ ] All 13+ agents created
- [ ] All 14+ commands created
- [ ] INDEX.md accurate and linked
- [ ] CLAUDE.md comprehensive
- [ ] features/ directory initialized
- [ ] status.xml valid XML syntax
- [ ] Git commit successful

### Update Mode Validation

**Phase 1 Checks**:
- [ ] Docs complete and current
- [ ] Agents follow specification
- [ ] Commands have correct model routing
- [ ] status.xml valid
- [ ] CLAUDE.md matches agents/commands
- [ ] Story files follow template
- [ ] Cross-references correct

### Brownfield Validation

**Phase 1 (Brownfield) Extra Checks**:
- [ ] Codebase analyzed successfully
- [ ] PROJECT_OVERVIEW.md comprehensive
- [ ] Tech stack documented
- [ ] Existing workflows understood
- [ ] Pain points identified
- [ ] Recommendations actionable

---

## Security Considerations

### Setup Security

- No secrets in docs, agents, commands
- Template copying validates against existing secrets
- CLAUDE.md doesn't include API keys
- status.xml never contains credentials

### Agent Security

- Agents don't have access to system files
- MCP server integration vetted
- Code review agents check for secrets

### Template Security

- Validate mode recommended for first-time use
- Template content scanned for hardcoded secrets
- Cross-project template copying allowed only with approval

---

## Extensibility

### Adding Custom Agents

1. Create new agent markdown file in `.claude/agents/`
2. Follow YAML frontmatter + markdown format
3. Reference in CLAUDE.md
4. Add to coordinator workflow if needed

### Adding Custom Commands

1. Create command markdown file in `.claude/commands/`
2. Define which agents it spawns
3. Specify model routing (Opus/Sonnet/Haiku)
4. Document workflow steps

### Adding Domain-Specific Documentation

1. Create in `docs/development/`
2. Link from INDEX.md quick reference table
3. Reference from START_HERE.md
4. Update CLAUDE.md section if workflow relevant

### Adding Tech-Specific Agents

- Security: Use security-reviewer agent (requires Opus)
- Design: Use design-reviewer agent (requires Playwright MCP)
- DevOps: Create devops-specialist agent
- Data: Create data-engineer agent

---

## Related Documentation

- **README.md** - User getting started guide
- **project-setup-meta-prompt.md** - Main orchestrator (navigation hub)
- **ARCHITECTURE.md** - System design and file organization
- **YOLO_MODE.md** - Autonomous development detailed guide
- **CODE_REVIEW_PRINCIPLES.md** - 7-phase review framework
- **SECURITY_REVIEW_CHECKLIST.md** - OWASP scanning guide

---

**Last Updated**: 2025-10-22
**Version**: 2.0 (Sharded)
**Status**: Stable
