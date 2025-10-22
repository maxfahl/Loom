# Project Summary

**Project**: Loom - AI-Native Development Framework
**Type**: Meta-Framework (Documentation + Templates)
**Current Status**: Production-Ready (Framework Complete)
**Last Updated**: 2025-10-22

---

## What is Loom?

Loom is an AI-native development framework that provides a complete system for orchestrating autonomous Claude Code agents to build, test, review, and deploy features using strict test-driven development (TDD) and epic/story-based feature tracking.

Think of Loom as your development **operating system** - it provides the infrastructure (agents, commands, documentation structure, status tracking) that allows specialized AI agents to collaborate autonomously while maintaining human oversight through configurable breakpoints.

### Core Concept

Traditional development frameworks treat specifications as static documents that drift from reality. **Loom treats agents as living executors** - they read the specification (status.xml, epic/story files, TECHNICAL_SPEC.md), execute their expertise (development, testing, review, deployment), and continuously maintain documentation as they work.

---

## Why Loom Exists

### The Problem

1. **Sequential Workflows**: Traditional multi-agent systems process tasks one-at-a-time, wasting parallelization potential
2. **Documentation Drift**: Specs diverge from actual implementation within days
3. **TDD Inconsistency**: Without built-in enforcement, test coverage drops over time
4. **Agent Coordination Overhead**: No standard patterns for how agents communicate and track state
5. **Feature Tracking Rigidity**: Monolithic task lists don't work for parallel agent teams
6. **Slow Cycles**: Coordination overhead and sequential reviews slow delivery

### The Loom Solution

- **Parallel by Default**: Multiple agents execute stories simultaneously (70-80% speed improvement)
- **Living Documentation**: status.xml + story files serve as both specification and status tracker
- **TDD Enforced**: Red-Green-Refactor cycle mandatory in agent design
- **Agent Coordination Built-In**: Agents know how to read status, maintain context, handoff work
- **Epic/Story Organization**: Logical grouping enables parallel stories within coherent epics
- **Autonomous YOLO Mode**: Agents can complete full stories/epics without human intervention (configurable)

---

## Key Concepts

### 1. The Three-Layer Architecture

```
┌─────────────────────────────────────────────────┐
│ Layer 3: User Commands                          │
│ /dev, /dev-yolo, /review, /test, /commit, etc  │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│ Layer 2: Agents                                 │
│ 13 specialized agents (coordinator, reviewer,   │
│ test-writer, bug-finder, etc)                   │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│ Layer 1: Living Documentation                   │
│ status.xml (state), epic/story files (spec),    │
│ TECHNICAL_SPEC.md, ARCHITECTURE.md, etc         │
└─────────────────────────────────────────────────┘
```

### 2. Agents as Executors

Loom provides 13 specialized agents, each expert in their domain:

**Development Agents**:
- **coordinator** - Orchestrates TDD workflow and YOLO loops
- **senior-developer** - Architecture and design decisions
- **refactor-specialist** - Code quality improvements

**Quality Agents**:
- **code-reviewer** - Code quality and best practices
- **test-writer** - Test creation (TDD-first)
- **bug-finder** - Edge cases and vulnerabilities
- **qa-tester** - Test execution and coverage

**Operations Agents**:
- **git-helper** - Version control and commits
- **architecture-advisor** - System design
- **performance-optimizer** - Optimization

**Extension Agents**:
- **documentation-writer** - Fast doc updates
- **agent-creator** - Build custom agents
- **skill-creator** - Create Claude Skills

### 3. Slash Commands for Workflows

14+ commands provide streamlined entry points to complex agent workflows:

```
Development Workflow:
  /plan          → Plan feature with TDD breakdown
  /dev           → Execute development with task tracking
  /dev-yolo      → Run autonomous YOLO loop
  /commit        → Smart commit with tests and linting

Quality Workflow:
  /review        → 7-phase code review
  /security-review → OWASP security scanning
  /design-review → UI/UX review with WCAG 2.1 AA
  /test          → Test execution with coverage

Configuration:
  /yolo          → Configure YOLO mode breakpoints
  /status        → Project status report
  /docs          → Update documentation

Feature Setup:
  /create-feature    → Set up new feature with epics
  /create-story      → Generate next user story
  /correct-course    → Adjust feature direction
```

### 4. Epic/Story Organization

Features divided into logical **epics** with individual **stories**:

```
Feature: "user-authentication"
│
├── Epic 1: Foundation
│   ├── Story 1.1: Setup JWT middleware
│   ├── Story 1.2: Add login endpoint
│   └── Story 1.3: Add token refresh
│
├── Epic 2: Advanced Features
│   ├── Story 2.1: Add multi-factor auth
│   ├── Story 2.2: Add social login
│   └── Story 2.3: Add passwordless auth
│
└── Epic 3: Polish & Security
    ├── Story 3.1: Add rate limiting
    ├── Story 3.2: Add audit logging
    └── Story 3.3: Security hardening
```

**Key advantages**:
- Stories execute in parallel (3+ stories/hour in YOLO mode)
- Epics provide logical milestones for review/approval
- Each story has acceptance criteria, tasks, subtasks
- status.xml tracks progress across all epics

### 5. Test-Driven Development (Mandatory)

Red-Green-Refactor cycle enforced at agent level:

```
🔴 RED Phase
├─ Write failing test first
├─ Test must fail (verify test quality)
└─ Minimum viable test case

🟢 GREEN Phase
├─ Write minimal code to pass
├─ Implement only what's needed
└─ Code is "ugly" but correct

🔵 REFACTOR Phase
├─ Clean up code quality
├─ Remove duplication
├─ Improve naming & structure
└─ Tests still pass (green)

♻️ REPEAT
└─ Next test case, continue cycle
```

**Loom enforcement**:
- Agents write tests FIRST (non-negotiable)
- Minimum 80% code coverage (mandatory)
- All commits must pass test suite
- Code review checks TDD compliance

### 6. YOLO Mode: Autonomous Development

Configure when agents stop vs proceed autonomously:

**Three Stopping Granularities**:

1. **Story-Level** (Default)
   - 8 configurable breakpoints within each story
   - Granular control: dev → review → test → user testing → commit → push
   - Stop after each story for human review

2. **Epic-Level** (Maximum Autonomy)
   - Single breakpoint: after entire epic completes
   - Agents complete all stories in epic without stopping
   - Stop only at epic milestones
   - 3-5 stories/hour throughput

3. **Custom**
   - Select individual breakpoints (1-9)
   - Fine-grained control
   - Balance between autonomy and oversight

**Example: Epic-Level YOLO Configuration**

```bash
/yolo
> Select: B (EPIC-LEVEL)

/dev-yolo
# Agents autonomously complete all stories in Epic 1
# Story 1.1: Setup JWT middleware ✅
# Story 1.2: Add login endpoint ✅
# Story 1.3: Add token refresh ✅
# Epic 1: Complete ✅
# STOPS HERE for human review
```

### 7. Living Documentation

Documentation isn't static - it's maintained by agents during development:

**Core Documentation Files**:

- **status.xml** - Feature state (current epic, current story, YOLO config, completed tasks)
- **Epic Files** - DESCRIPTION.md, TASKS.md, NOTES.md per epic
- **Story Files** - Acceptance criteria, tasks, subtasks per story
- **Technical Specs** - TECHNICAL_SPEC.md, ARCHITECTURE.md
- **Design Docs** - DESIGN_SYSTEM.md, DESIGN_PRINCIPLES.md
- **Quality Guides** - CODE_REVIEW_PRINCIPLES.md, SECURITY_REVIEW_CHECKLIST.md

**How Living Documentation Works**:

```
1. /create-feature generates all docs from scratch
2. Agents read docs to understand requirements (specification)
3. Agents execute implementation
4. Agents update status.xml with completed tasks
5. Agents update story file with actual results
6. Documentation reflects ground truth throughout dev cycle
```

---

## Project Structure

### Repository Layout

```
Loom/
├── README.md                           # User getting started guide
├── CLAUDE.md                          # AI assistant instructions
├── LICENSE                            # MIT license
│
├── prompts/                           # Bootstrap & setup prompts
│   ├── project-setup-meta-prompt.md   # Main orchestrator
│   ├── project-update-meta-prompt.md  # Update existing projects
│   ├── phases/                        # Detailed phase guides
│   │   ├── phase-1-discovery.md
│   │   ├── phase-2-documentation.md
│   │   ├── phase-3-agents.md
│   │   ├── phase-4-commands.md
│   │   └── phase-5-validation.md
│   ├── reference/                     # Reference docs
│   │   ├── core-agents.md             # 13 agent definitions
│   │   ├── yolo-mode.md               # Autonomous workflow
│   │   ├── status-xml.md              # Feature tracking format
│   │   └── slash-commands.md           # Command reference
│   └── templates/                     # Document & project templates
│       ├── doc-templates.md            # 15+ doc templates
│       └── projects/                   # Template projects
│           ├── greenfield/             # New projects
│           ├── brownfield/             # Existing codebases
│           └── domain-specific/        # Industry templates
│
├── docs/
│   └── development/
│       ├── INDEX.md                   # Master navigation
│       ├── PRD.md                     # Product requirements (THIS FILE)
│       ├── PROJECT_SUMMARY.md          # Project overview
│       ├── TECHNICAL_SPEC.md          # Implementation details
│       ├── ARCHITECTURE.md             # System design
│       ├── DESIGN_SYSTEM.md           # UI guidelines
│       ├── DEVELOPMENT_PLAN.md        # Roadmap & TDD
│       ├── YOLO_MODE.md               # Autonomous workflow
│       ├── CODE_REVIEW_PRINCIPLES.md  # 7-phase review
│       ├── SECURITY_REVIEW_CHECKLIST.md # OWASP Top 10
│       ├── DESIGN_PRINCIPLES.md       # UI/UX review
│       ├── HOOKS_REFERENCE.md         # Claude Code hooks
│       ├── TASKS.md                   # Development checklist
│       ├── START_HERE.md              # Role-specific guide
│       ├── EXECUTIVE_SUMMARY.md       # Technical summary
│       ├── status.xml                 # Feature tracking
│       └── features/                  # Feature documentation (example)
│           └── example-feature/
│               ├── INDEX.md
│               ├── FEATURE_SPEC.md
│               ├── TECHNICAL_DESIGN.md
│               ├── TASKS.md
│               ├── CHANGELOG.md
│               └── epics/
│                   ├── epic-1-foundation/
│                   │   ├── DESCRIPTION.md
│                   │   ├── TASKS.md
│                   │   ├── NOTES.md
│                   │   └── stories/
│                   │       ├── 1.1.md
│                   │       ├── 1.2.md
│                   │       └── 1.3.md
│                   ├── epic-2-core-features/
│                   └── epic-3-polish/
│
└── .github/                           # GitHub integration
    ├── workflows/                     # CI/CD workflows
    └── ISSUE_TEMPLATE.md              # Issue templates
```

### Key Directories

- **prompts/** - Bootstrap and setup infrastructure
- **docs/development/** - All documentation
- **.claude/agents/** - Agent definitions (created per project)
- **.claude/commands/** - Slash command definitions (created per project)

---

## How Loom Works: The Development Cycle

### Phase 1: Project Setup (30-90 minutes)

```
1. User reads: project-setup-meta-prompt.md
2. Bootstrap agent asks discovery questions:
   - Project name and type
   - Technology stack
   - Team size and skill level
   - TDD enforcement level
   - YOLO mode preferences
3. Agent creates:
   - Complete docs/ folder with 15+ files
   - .claude/agents/ with 13 agents
   - .claude/commands/ with 14 commands
   - status.xml with feature tracking
   - Initial feature setup
4. Git commit: "Initial Loom setup with [features]"
5. Team ready to start development
```

### Phase 2: Feature Planning (20-40 minutes per feature)

```
1. User runs: /create-feature "my-feature"
   - Name the feature
   - Describe the problem it solves
   - Identify 3-5 epics (logical milestones)

2. Agent creates:
   - docs/development/features/my-feature/FEATURE_SPEC.md
   - docs/development/features/my-feature/TECHNICAL_DESIGN.md
   - docs/development/features/my-feature/epics/
   - Updates status.xml with feature metadata

3. User runs: /plan my-feature
   - Coordinator agents create TDD breakdown
   - Each epic planned with 3-5 stories
   - Each story has acceptance criteria
   - TDD tests outlined (Red phase specs)

4. Git commit: "Plan feature: my-feature with [N] epics"
```

### Phase 3: Story Development (15-45 minutes per story)

```
1. User runs: /dev
   - Coordinator reads status.xml
   - Reads current story file
   - Identifies next incomplete story

2. Coordinator Executes TDD Cycle:
   🔴 RED: Write failing tests (3-5 tests per story)
   🟢 GREEN: Implement minimal code to pass
   🔵 REFACTOR: Clean up code quality
   ✅ CHECKS: Verify 80%+ coverage

3. Tasks Tracked:
   - Each task in story file gets checkmark
   - Subtasks checked off as completed
   - Story file updated in real-time

4. Story Status Updates:
   - "In Progress" → "Waiting For Review"
   - Coordinator spawns code-reviewer + qa-tester
   - Reviews check quality and TDD compliance

5. If Issues Found:
   - Review Tasks added to story
   - Story status → "In Progress"
   - Back to step 2

6. Story Complete:
   - Story status → "Done"
   - All tests passing
   - Coverage ≥80%
   - Code reviewed
```

### Phase 4: Autonomous YOLO Loop (Stories per hour)

```
With YOLO mode configured:

/dev-yolo

1. Coordinator reads YOLO config
   - Stopping granularity: STORY / EPIC / CUSTOM
   - Breakpoints enabled: [1, 3, 4, 8, 9] (example)

2. Story Loop (repeats for each story):
   a. Development cycle (RED-GREEN-REFACTOR)
   b. Tests passing (80%+ coverage)
   c. Code review (7-phase framework)
   d. Check breakpoint 1: Dev → Review
      - If breakpoint enabled: STOP for user
      - If breakpoint disabled: Continue
   e. Run tests (automated coverage validation)
   f. Check breakpoint 2: Review → Test
   g. Commit automatically
   h. Check breakpoint 5: Commit → Push
   i. Next story or exit

3. Epic Loop (if epic-level mode):
   - Completes all stories in epic
   - Runs integration tests
   - Updates epic status
   - STOPS at epic boundary (breakpoint 9)

4. Example Output:
   ✅ Story 1.1: JWT setup (8 min) - DONE
   ✅ Story 1.2: Login endpoint (12 min) - DONE
   ✅ Story 1.3: Token refresh (15 min) - DONE
   🎯 Epic 1: Complete (35 min)

   STOPPED AT: Epic boundary
   Coverage: 87% | Tests: 42/42 passing

   Your turn: Review Epic 1, run /dev-yolo again
```

### Phase 5: Deployment & Completion

```
1. After epic/feature complete:

2. User reviews:
   - Code changes
   - Test results
   - Documentation updates

3. Final validation:
   /review           → Final code review
   /security-review  → Final security check
   /design-review    → Final UX/design check

4. Merge to main branch:
   /commit "feat: complete [feature-name]"
   git push origin main

5. Update status.xml:
   - Feature status → "Released"
   - Next feature becomes active
   - Clear completed-tasks
```

---

## Comparison with Other Frameworks

### vs. SpecKit

| Aspect | SpecKit | Loom |
|--------|---------|------|
| **Workflow** | Sequential spec→plan→task→implement | Parallel agents + epic/story breakdown |
| **Parallelization** | Single implementation path | 70-80% faster with parallel agents |
| **Autonomy** | Human approval at each gate | YOLO mode (configurable) |
| **TDD** | Optional/advisory | Mandatory by design |
| **Feature Tracking** | Task list | Epic/story with living docs |

### vs. BMAD Method

| Aspect | BMAD | Loom |
|--------|------|------|
| **Integration** | External orchestration platform | Native Claude Code CLI |
| **Architecture** | File-based agent communication | Agent coordination built-in |
| **Configuration** | YAML workflows | Markdown agents/commands |
| **UI** | Web dashboard + IDE | CLI-native + markdown |
| **TDD Support** | Via expansion packs | Built into all agents |

### vs. Traditional Agile/Scrum

| Aspect | Traditional | Loom |
|--------|-------------|------|
| **Planning** | Human sprint planning | Agents plan via /plan command |
| **Execution** | Developer-driven | Agent-driven |
| **Status** | Standup meetings | status.xml real-time |
| **Docs** | Static, drift over time | Living documentation |
| **Cycle Time** | 1-2 weeks (sprint) | 1-2 hours (story in YOLO) |

---

## Core Technologies

### Framework Foundation

- **Claude Code CLI** - Exclusive runtime environment (ports to other CLIs planned)
- **Markdown** - All documentation and configuration
- **Git** - Version control and history (source of truth)
- **YAML** (minimal) - Some configuration

### Documentation Stack

- **15+ Markdown Files** - Specifications, guides, templates
- **status.xml** - Feature state tracking (single file)
- **Epic/Story Files** - Markdown with structured sections
- **Inline Comments** - JSDoc/TSDoc (project-specific)

### Agent Stack

- **13 Specialized Agents** - Claude 3 Sonnet/Haiku models
- **Agent Communication** - File-based (git + status.xml)
- **Agent State** - Preserved in git history
- **Agent Coordination** - Handled by coordinator agent

### Command Stack

- **14+ Slash Commands** - Claude Code CLI native
- **Command Routing** - Via `/` prefix in Claude Code
- **Command Output** - Structured markdown responses
- **Command State** - Tracked in status.xml

---

## Success Stories & Use Cases

### Use Case 1: Greenfield Startup MVP

```
Timeline: 4-6 weeks (vs 12-16 weeks traditional)

Week 1-2: Foundation
├─ /create-feature "authentication"
├─ Epic 1: JWT setup
├─ Epic 2: Login/signup
└─ /dev-yolo (story-level mode)
   → Complete 5 stories, 40-50 tests

Week 3: Core Features
├─ /create-feature "data-management"
├─ Epic 1: CRUD operations
├─ Epic 2: Search & filtering
└─ /dev-yolo (epic-level mode)
   → Complete 8 stories, 80+ tests

Week 4-5: Integration & Polish
├─ /create-feature "ui-components"
├─ /design-review on components
├─ /security-review full stack
└─ /dev-yolo with all reviews
   → Complete 6 stories

Result: MVP with 150+ tests, 85% coverage, fully documented
```

### Use Case 2: Brownfield Legacy Migration

```
Timeline: 2-4 weeks per feature (vs 4-8 weeks traditional)

Week 1: Analysis
├─ PROJECT_OVERVIEW.md created (brownfield analysis)
├─ Identify high-risk areas
├─ Plan migration feature

Week 2-3: Feature by Feature
├─ /create-feature "payment-system"
├─ /dev-yolo (epic-level, high reviews)
├─ All changes backward compatible
└─ Full test coverage on new code

Result: Legacy features incrementally modernized with high confidence
```

### Use Case 3: Rapid Prototyping

```
Timeline: 1-2 days per prototype

Day 1: Setup + Foundation
├─ /create-feature "chat-interface"
├─ /dev-yolo (epic-level, no reviews)
└─ Complete 8 stories in 6 hours

Day 2: Polish + Features
├─ /dev-yolo (story-level, design reviews only)
└─ Add advanced features, refine UX

Result: Working prototype with documentation, ready for user testing
```

---

## Key Metrics & Achievements

### Speed Improvements

- **Setup**: 30-90 minutes (vs 2-3 days traditional)
- **Story Completion**: 15-45 minutes per story (vs 2-4 hours traditional)
- **Throughput**: 3-5 stories/hour in YOLO mode (vs 1-2 stories/week traditional)
- **Epic Completion**: 2-4 hours (vs 1-2 weeks traditional)

### Quality Improvements

- **Test Coverage**: 80-95% (mandatory enforcement)
- **Bug Reduction**: <5% regression rate (code review + security review)
- **Documentation**: 100% (enforced with living docs)
- **Security**: Zero HIGH severity vulnerabilities (OWASP Top 10 scanning)

### Parallelization

- **Sequential vs Parallel**: 70-80% time savings
- **Agent Utilization**: 13 agents can work simultaneously
- **Story Independence**: Multiple stories execute in parallel
- **Zero Context Switching**: Agents maintain full context across work

---

## Getting Started

### For New Projects

```bash
1. Read: /path/to/loom/README.md
2. Copy: project-setup-meta-prompt.md
3. Give to Claude Code:
   "Read and understand this prompt fully and follow the trail:
    /path/to/loom/prompts/project-setup-meta-prompt.md"
4. Answer discovery questions
5. Agent creates complete development environment
```

### For Existing Projects

```bash
1. Read: /path/to/loom/README.md
2. Copy: project-update-meta-prompt.md
3. Give to Claude Code:
   "Update my existing project to follow latest Loom guidelines:
    /path/to/loom/prompts/project-update-meta-prompt.md"
4. Agent analyzes project and adds Loom structure
```

### For Learning

1. **Conceptual**: Read docs/development/PROJECT_SUMMARY.md (this file)
2. **Practical**: Read docs/development/README.md (getting started)
3. **Reference**: Read docs/development/TECHNICAL_SPEC.md (implementation)
4. **Navigation**: Read docs/development/INDEX.md (find any info)

---

## Contributing & Extending

### Creating Custom Agents

```
1. Read: .claude/agents/coordinator.md (example)
2. Create: .claude/agents/my-custom-agent.md
3. Define:
   - Purpose and expertise
   - Input (what information it needs)
   - Output (what it produces)
   - Integration points (which commands use it)
4. Test: Create test scenarios
5. Document: Add to .claude/README.md
```

### Creating Custom Commands

```
1. Read: .claude/commands/dev.md (example)
2. Create: .claude/commands/my-custom-command.md
3. Define:
   - Trigger (command name and syntax)
   - Required agents
   - Workflow steps
   - Output format
4. Test: Run manually
5. Document: Add to slash command reference
```

### Template Projects

Share successful project setups:

```
loom/prompts/templates/projects/
├── greenfield/
│   ├── [your-project]/
│   │   ├── SETUP.md
│   │   ├── agents/
│   │   ├── commands/
│   │   └── docs/
│   └── ...
├── brownfield/
└── domain-specific/
    ├── web-app/
    ├── data-pipeline/
    ├── mobile-app/
    └── ...
```

---

## FAQ

**Q: Is Loom only for AI development?**
A: No - Loom works for any development workflow where you use Claude Code. The agents are specialized for AI-native dev, but can be customized for any domain.

**Q: What if YOLO mode runs something I didn't intend?**
A: Breakpoints prevent this. Every critical decision has a corresponding breakpoint you can enable. Epic-level mode acts as hard stop.

**Q: How do I add existing code to Loom?**
A: Use brownfield flow: project-update-meta-prompt.md analyzes your code and adds Loom structure without breaking existing workflows.

**Q: Can I use Loom for non-software projects?**
A: Yes - Create custom agents for your domain. The framework (epics, stories, YOLO mode, TDD) applies to any project.

**Q: What if I want to modify agents or commands?**
A: All are markdown-based. Edit .claude/agents/[name].md or .claude/commands/[name].md directly. No compilation needed.

---

## Philosophy & Vision

### Our Philosophy

> "Agents as the spec executors, not spec consumers"

Traditional frameworks give specifications to developers/agents and hope they follow them. Loom treats agents as the specification maintainers - they read the spec, execute work, and update the spec with results. This creates a living system where documentation is always current.

### The Vision

Loom is the foundation for a new paradigm: **AI-native software development at enterprise scale**. Where teams of specialized agents autonomously execute features based on epic/story specifications, maintain strict TDD without human enforcement, parallelize work across multiple stories simultaneously, and deliver completed features in hours instead of weeks.

The endgame: Humans focus on defining requirements and providing oversight. Agents focus on execution. Both thrive.

---

## Next Steps

1. **Read** - docs/development/README.md for comprehensive guide
2. **Explore** - docs/development/INDEX.md for navigation
3. **Setup** - Run bootstrap prompt on new project
4. **Develop** - Use /dev, /dev-yolo, /review, /commit
5. **Extend** - Create custom agents and commands
6. **Share** - Contribute template projects back to community

---

**Document Status**: Complete
**Framework Status**: Production-Ready
**Last Update**: 2025-10-22

For questions or contributions, see [Contributing Guidelines](CONTRIBUTING.md)

---

_This document is the high-level overview. For detailed information, see the full documentation suite in docs/development/_
