# EXECUTIVE_SUMMARY: Loom Meta-Framework

**Loom** is an AI-native development framework that orchestrates autonomous agents to build features using strict test-driven development, epic-based organization, and configurable autonomy (YOLO mode).

---

## The Problem: Specification Drift

Traditional spec-driven frameworks treat specifications as **static documents** that quickly drift from implementation:

- Product requirements written at project start
- Implementation diverges from spec over time
- No feedback loop to keep spec current
- Specs become outdated guides that nobody trusts
- Developers ignore specs and rely on code as source of truth

**Result**: Miscommunication, rework, delayed releases, unclear requirements.

---

## The Loom Solution: Agents as Spec Executors

Loom treats **AI agents as the specification executors** - they maintain context, follow TDD, and autonomously implement features based on **living documentation**:

- **Living Specs**: status.xml, epic descriptions, story files actively guide agents
- **Agents Maintain Context**: Read specs before every task, understand the "why"
- **Spec Feedback Loop**: Implementation drives spec updates, specs drive implementation
- **No Drift**: Agents are spec compliance enforcers (TDD = spec validator)

**Result**: Specification and implementation stay in sync by design.

---

## Key Features

### 1. 13 Core Specialized Agents

Each agent is an expert in their domain:

- **coordinator** - TDD workflow orchestrator with YOLO mode autonomy
- **senior-developer** - Architecture and code review expert
- **code-reviewer** - Quality assurance and best practices
- **test-writer** - Comprehensive test coverage (TDD-focused)
- **bug-finder** - Edge case detection and analysis
- **refactor-specialist** - Code quality improvements
- **qa-tester** - Fast test execution and validation
- **git-helper** - Version control operations
- **architecture-advisor** - System design guidance
- **performance-optimizer** - Bottleneck identification
- **documentation-writer** - Fast doc updates
- **agent-creator** - Build custom agents
- **skill-creator** - Create reusable Claude Skills
- **security-reviewer** - OWASP security scanning (Opus model, 8/10+ confidence)
- **design-reviewer** - UI/UX review (Playwright + WCAG 2.1 AA)

### 2. 14+ Slash Commands

Streamlined workflow commands:

| Command | Purpose | Model |
| --- | --- | --- |
| `/dev` | Continue development with TDD | Sonnet |
| `/dev-yolo` | Launch autonomous YOLO loop | Sonnet |
| `/commit` | Smart commit with validation | Sonnet |
| `/review` | 7-phase code review | Sonnet |
| `/security-review` | OWASP security scanning | Opus |
| `/design-review` | UI/UX design review with Playwright | Sonnet |
| `/test` | Run tests with coverage | Haiku |
| `/plan` | Plan feature implementation | Sonnet |
| `/status` | Project status report | Haiku |
| `/docs` | Update documentation | Haiku |
| `/yolo` | Configure autonomy breakpoints | Haiku |
| `/create-feature` | Create feature with epics | Sonnet |
| `/correct-course` | Adjust feature direction | Sonnet |
| `/create-story` | Create next user story | Sonnet |

### 3. Strict Test-Driven Development (TDD)

Red-Green-Refactor cycle enforced by design:

1. 🔴 **RED** - Write failing test first
2. 🟢 **GREEN** - Implement minimal code to pass
3. 🔵 **REFACTOR** - Improve code quality
4. ♻️ **REPEAT** - Next test case

**Coverage Requirements**:
- Task level: 80% minimum
- Story level: 85% minimum
- Epic level: 90% minimum

**Why TDD matters**: Tests ARE the specification. Agents verify implementation against tests, ensuring spec compliance.

### 4. Epic/Story Organization

Break features into **epics** (logical milestones) with individual **stories**:

```
Feature: user-authentication
├── Epic 1: Foundation
│   ├── Story 1.1: Setup JWT middleware
│   ├── Story 1.2: Add login endpoint
│   └── Story 1.3: Add token refresh
├── Epic 2: Core Features
│   ├── Story 2.1: Multi-factor authentication
│   └── Story 2.2: Session management
└── Epic 3: Polish
    └── Story 3.1: Security hardening
```

**Granularity Without Rigidity**:
- Epics provide high-level structure
- Stories maintain independence
- Agents can work on multiple stories in parallel
- Progress tracked story-by-story

### 5. YOLO Mode: Configurable Autonomy

**Three stopping granularities**:

**A. STORY-LEVEL** (default):
- Stop at specific breakpoints within each story
- Balanced control, review each story
- Breakpoints: dev→review, review→tests, tests→commit, etc.

**B. EPIC-LEVEL** (maximum autonomy):
- Only stop when full epics complete
- Agents autonomously complete ALL stories in epic
- Ideal for trusted workflows, overnight development

**C. CUSTOM**:
- Select individual breakpoints manually
- Fine-grained control over workflow

**Coordinator reads YOLO configuration** and automatically handles complete TDD cycle:

```
Read status.xml →
Reads current story →
Checks for Review Tasks (prioritizes first) →
Writes failing tests (RED) →
Implements code (GREEN) →
Refactors (BLUE) →
Checks off completed tasks →
Updates story status →
Spawns code-reviewer + qa-tester in parallel →
If issues → Adds Review Tasks, status to "In Progress" →
If no issues → Status to "Done" →
Checks YOLO breakpoint →
Continues to next story or stops
```

### 6. Parallel Agent Execution

**Multiple agents work simultaneously** for 70-80% time savings:

```
Coordinator spawns in parallel:
├── Backend agent (implement API)
├── Frontend agent (build UI)
├── Test writer (write tests)
├── Security reviewer (scan code)
└── Documentation writer (update docs)

All work at same time, coordinator synthesizes results
```

### 7. Comprehensive Documentation (15+ Files)

Living specifications that drive implementation:

| Document | Purpose |
| --- | --- |
| INDEX.md | Master navigation hub |
| README.md | Project introduction |
| START_HERE.md | Getting started guide |
| PRD.md | Product requirements |
| TECHNICAL_SPEC.md | Implementation details |
| ARCHITECTURE.md | System design and components |
| DESIGN_SYSTEM.md | UI component library priority |
| DEVELOPMENT_PLAN.md | Development methodology and roadmap |
| EXECUTIVE_SUMMARY.md | High-level technical overview |
| YOLO_MODE.md | Autonomy configuration and workflows |
| CODE_REVIEW_PRINCIPLES.md | 7-phase hierarchical review framework |
| SECURITY_REVIEW_CHECKLIST.md | OWASP-based security methodology |
| DESIGN_PRINCIPLES.md | UI/UX design review (Playwright + WCAG 2.1 AA) |
| FEATURE_SPEC.md | Per-feature specification |
| TASKS.md | Development task checklist |
| status.xml | Feature tracking (single file for all features) |

Plus domain-specific docs (API_REFERENCE, DATA_PIPELINE, etc.)

---

## Architecture: Sharded Prompts for Maximum Efficiency

Loom uses **21 sharded prompt files** organized in a tree structure for optimal context management:

### Prompt Structure

```
prompts/
├── project-setup-meta-prompt.md        # Main orchestrator
├── project-update-meta-prompt.md       # Update flow
├── phases/
│   ├── phase-1-discovery.md
│   ├── phase-2-documentation.md
│   ├── phase-3-agents.md
│   └── phase-4-commands.md
├── reference/
│   ├── core-agents.md                  # 15 agent definitions
│   ├── slash-commands.md               # 14+ command specs
│   └── yolo-mode.md                    # YOLO configuration
├── templates/
│   └── doc-templates.md                # All 17 doc templates
└── troubleshooting/
    └── recovery-guide.md
```

**Why Sharded Prompts?**
- Claude Code excels at following prompt chains ("follow the trail of prompts to the dot")
- Each prompt is focused, digestible, and actionable
- Reduces token usage through modular context
- Easier to update individual components
- Agents can specialize to specific prompt subsets

---

## Two Core Workflows

### 1. NEW SETUP (Greenfield Projects)

**Bootstrap prompt** (`project-setup-meta-prompt.md`):

```
Read and fully understand the prompt in the below markdown file
and follow the trail of prompts to the dot. Be extremely careful
and take your time.

/path/to/loom/project-setup-meta-prompt.md
```

**What happens**:
1. Agent asks discovery questions (project type, tech stack, TDD enforcement)
2. Agent creates complete documentation (15+ files)
3. Agent creates specialized agents (13 core + customizations)
4. Agent creates slash commands (14+)
5. Agent creates status.xml for feature tracking
6. Agent commits everything to git

**Result**: Ready-to-use development environment in ~30 minutes

### 2. UPDATE EXISTING PROJECT (Brownfield)

**Update prompt** (`project-update-meta-prompt.md`):

```
Read and fully understand the prompt in the below markdown file
and follow the trail of prompts to the dot. I want you to run the
"update flow" without asking any unnecessary questions.

/path/to/loom/project-update-meta-prompt.md
```

**What happens**:
1. Agent analyzes existing codebase
2. Agent creates PROJECT_OVERVIEW.md (comprehensive analysis)
3. Agent migrates existing code to Loom structure
4. Agent creates comprehensive documentation based on existing code
5. Agent sets up agents and commands
6. Agent initializes status.xml with realistic feature estimates
7. Agent commits everything to git

**Result**: Existing project gains Loom benefits without rewriting

---

## Autonomous Development Loop Example

**Configuration** (one-time):
```bash
/yolo
# Choose: B (EPIC-LEVEL)
```

**Launch loop**:
```bash
/dev-yolo
```

**Output** (agents work autonomously):
```
🚀 Launching coordinator agent in YOLO mode...
Feature: user-authentication
YOLO Mode: ON
Stopping Granularity: EPIC-LEVEL
Breakpoints: 9 only

Coordinator will autonomously complete all stories in Epic 1.
Will stop after Epic 1 completes for your review.

... agents work autonomously ...
... complete Story 1.1, 1.2, 1.3 ...
... run tests (87% coverage), review, commit ...

🎯 YOLO Loop Status Report

Feature: user-authentication
Stopped At: Epic Complete (Breakpoint 9)

Completed:
- ✅ Story 1.1: Setup JWT middleware (commit: abc123)
- ✅ Story 1.2: Add login endpoint (commit: def456)
- ✅ Story 1.3: Add token refresh (commit: ghi789)

Current State:
- Epic: epic-1-foundation
- Status: Done
- Tests: 42/42 passing, 87% coverage

Next Steps:
- Review Epic 1 work
- Run /dev-yolo again to start Epic 2
```

**Resume** (after review):
```bash
/dev-yolo  # Starts Epic 2
```

---

## Time Savings: 70-80% Development Acceleration

### Traditional Workflow (100% baseline)

1. Manual planning and task breakdown (8h)
2. Manual test writing (16h)
3. Implementation (32h)
4. Manual testing (16h)
5. Code review (8h)
6. Fixes and rework (16h)

**Total: 96 hours**

### Loom Workflow (20-30% of baseline)

1. Automated documentation and epic generation (30 min)
2. TDD automated: agents write tests + code (5h autonomously, batched reviews)
3. Parallel agent execution: backend + frontend + tests + review simultaneously (2h clock time)
4. Automated test running with coverage validation (automated)
5. Automated code review with 7-phase framework (automated)
6. Automated fixes and rework (agents handle Review Tasks)

**Total: 16-24 hours (75% reduction)**

**Key multipliers**:
- Parallel execution (backend, frontend, tests, review simultaneous)
- Automated testing and review
- TDD preventing bugs before they happen
- Living specs prevent rework
- Agents maintain context (no context-switching overhead)

---

## Differentiation from Other Frameworks

### vs. SpecKit (GitHub: mCodingLLC/SpecKit)

**SpecKit** (sequential spec-to-code transformation):
- Fixed 4-phase workflow: specify → plan → tasks → implement
- Human approval required at each gate
- Single implementation path
- Tightly coupled to software development
- Good for: Waterfall-style projects, strict gates

**Loom** (flexible parallel autonomous workflows):
- Multiple specialized agents working simultaneously
- Epic-based feature breakdown with independent stories
- YOLO mode for story-level or epic-level autonomy
- Works for any domain (agents customizable)
- Good for: Rapid development, high-trust teams, continuous delivery

**Why Loom is better**:
- Parallel execution (2-3x faster)
- Agents can work on multiple stories simultaneously
- YOLO mode provides flexibility in autonomy granularity
- Built on TDD for specification compliance

### vs. BMAD Method

**BMAD** (orchestrated multi-agent collaboration):
- Agent teams communicate via file-based messages
- Web UI + IDE integration
- Expansion packs for different domains
- YAML-based workflow definitions
- Good for: Complex team coordination, visual workflows

**Loom** (AI-native development with Claude Code):
- Agents as first-class Claude Code primitives
- Slash commands for streamlined workflows
- Git-integrated feature branches
- Built-in TDD methodology with YOLO mode
- Epic/story structure for granular tracking
- Good for: AI-native development, fast iteration, clear structure

**Why Loom is different**:
- Native Claude Code integration (uses native capabilities)
- Simpler setup (no web UI required)
- Stronger TDD enforcement
- Living documentation that drives implementation
- Sharded prompts for optimal token efficiency

---

## Core Benefits

1. **Autonomous Development**: Agents handle dev, test, review, security autonomously (70-80% faster)

2. **Specification Compliance**: TDD ensures implementation matches spec; agents enforce compliance

3. **Parallel Execution**: Backend + frontend + tests + review work simultaneously

4. **Configurable Autonomy**: YOLO mode from story-level to epic-level control

5. **Living Documentation**: Specs actively drive implementation; no drift

6. **Strict TDD**: Red-Green-Refactor enforced; 80%+ coverage mandatory

7. **Comprehensive Code Review**: 7-phase hierarchical framework with triage matrix

8. **Security by Default**: OWASP scanning with FALSE_POSITIVE filtering (Opus model)

9. **Design Review**: WCAG 2.1 AA compliance, responsive testing, Playwright live testing

10. **Easy Setup**: Bootstrap prompt creates complete environment in 30 minutes

---

## Tech Stack Integration

Loom is framework-agnostic and works with:

- **Frontend**: React, Vue, Angular, Svelte, Next.js
- **Backend**: Node.js, Python, Go, Rust
- **Database**: PostgreSQL, MySQL, MongoDB, SQLite
- **Testing**: Jest, Vitest, Pytest, Go testing, Playwright
- **Deployment**: Docker, Kubernetes, AWS, GCP, Azure
- **VCS**: Git (GitHub, GitLab, Bitbucket)

All documentation templates are customizable for any stack.

---

## Quick Start

### For New Projects

```bash
# Read the bootstrap prompt
cat /path/to/loom/prompts/project-setup-meta-prompt.md

# Give this to Claude Code:
Read and fully understand the prompt in the below markdown file
and follow the trail of prompts to the dot. Be extremely careful
and take your time.

/path/to/loom/project-setup-meta-prompt.md
```

**Result**: Complete development environment in 30 minutes

### For Existing Projects

```bash
# Update prompt for brownfield projects
cat /path/to/loom/prompts/project-update-meta-prompt.md

# Give this to Claude Code:
Read and fully understand the prompt in the below markdown file
and follow the trail of prompts to the dot. I want you to run the
"update flow" without asking any unnecessary questions.

/path/to/loom/project-update-meta-prompt.md
```

**Result**: Existing project gains Loom benefits

---

## Current Status

- **Version**: 1.0 (stable)
- **Phase**: Production Ready
- **Framework**: Claude Code (Claude Sonnet + Haiku + Opus models)
- **Focus**: AI-native development with autonomous agents

---

## Next Steps

1. **Read [START_HERE.md](START_HERE.md)** - Getting started guide for different roles
2. **Run bootstrap prompt** for new projects or update prompt for existing
3. **Configure YOLO mode** with `/yolo` command
4. **Launch autonomous loop** with `/dev-yolo`
5. **Monitor progress** with `/status`

---

## Key Metrics

- **Setup Time**: 30 minutes (complete environment)
- **Development Speed**: 70-80% faster (parallel execution)
- **Test Coverage**: 80%+ mandatory (TDD enforced)
- **Code Review**: 7-phase framework (comprehensive)
- **Autonomous Loop**: Story-level or epic-level control
- **Model Efficiency**: Sharded prompts, 21 files (optimal context management)

---

**Loom turns specification drift into specification synchronization.**

_For detailed information, see [INDEX.md](INDEX.md)_

_Last updated: 2025-10-22_
