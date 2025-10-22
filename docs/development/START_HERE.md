# START_HERE: Getting Started with Loom

Welcome to **Loom** - an AI-native development framework that orchestrates autonomous agents to build features autonomously using test-driven development.

This guide helps you find the right resources based on your role and what you need to do.

---

## What is Loom?

Loom treats **AI agents as the spec executors** - they maintain context, follow TDD, and autonomously implement features based on living documentation (status.xml, epic docs, story files).

Key concepts:

- **AI-Only Development**: Specialized agents handle development, testing, review, security
- **Strict TDD**: Red-Green-Refactor cycle enforced by design
- **Epic/Story Organization**: Features broken into logical milestones
- **YOLO Mode**: Autonomous workflows with configurable breakpoints (story-level, epic-level)
- **Parallel Execution**: Multiple agents work simultaneously for 70-80% speed improvements

---

## Quick Start for Different Roles

### I'm Setting Up a New Project

**Read these in order**:

1. **[README.md](README.md)** - Project overview and philosophy
2. **[project-setup-meta-prompt.md](../prompts/project-setup-meta-prompt.md)** - Bootstrap your project (give this to Claude Code)
3. **[YOLO_MODE.md](YOLO_MODE.md)** - Configure autonomous development

**What happens**:
- Bootstrap prompt asks discovery questions
- Agent creates complete documentation, agents, and commands
- You get a ready-to-use development environment

---

### I'm Starting Development on an Existing Project

**Read these first**:

1. **[INDEX.md](INDEX.md)** - Master navigation for all docs
2. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview
3. Your feature's **FEATURE_SPEC.md** in `docs/development/features/[feature-name]/`

**Then choose your workflow**:

- **Autonomous Development**: Run `/yolo` to configure, then `/dev-yolo` to let agents work
- **Manual Development**: Run `/dev` to continue current task
- **Code Review**: Run `/review` to catch issues

---

### I'm Planning a New Feature

**Read these**:

1. **[PRD.md](PRD.md)** - Product requirements format
2. **[/create-feature command](../prompts/commands/create-feature.md)** - Create feature with epics

**Then execute**:

```bash
/create-feature [feature-name]
```

The agent will:
- Ask about your feature
- Create FEATURE_SPEC, TECHNICAL_DESIGN, TASKS
- Create 3 epics (Foundation, Core Features, Polish)
- Create first story
- Update status.xml

---

### I'm Writing Documentation

**Read these**:

1. **[INDEX.md](INDEX.md)** - Documentation structure overview
2. **[doc-templates.md](../prompts/templates/doc-templates.md)** - All documentation templates
3. The specific doc template for what you're writing

**Use the `/docs` command**:

```bash
/docs                # Auto-detect what needs updating
/docs code          # Update JSDoc/TSDoc comments
/docs api           # Update API reference
/docs user          # Update user guides
/docs all           # Update everything
```

---

### I'm Writing Tests (TDD)

**Philosophy**: Write tests FIRST, before implementation.

**Read these**:

1. **[DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md)** - TDD methodology and requirements
2. **[/test command](../prompts/commands/test.md)** - Running tests

**Workflow** (Red-Green-Refactor):

1. 🔴 **RED**: Write failing test
2. 🟢 **GREEN**: Implement minimal code to pass
3. 🔵 **REFACTOR**: Improve code quality
4. ♻️ **REPEAT**: Next test case

**Coverage Requirements**:
- Task level: 80% minimum
- Story level: 85% minimum
- Epic level: 90% minimum

---

### I'm Reviewing Code

**Read these**:

1. **[CODE_REVIEW_PRINCIPLES.md](CODE_REVIEW_PRINCIPLES.md)** - 7-phase review framework
2. **[/review command](../prompts/commands/review.md)** - Run code review

**Review Phases** (in priority order):

1. Architectural Design & Integrity
2. Functionality & Correctness
3. Security (non-negotiable)
4. Maintainability & Readability
5. Testing Strategy & Robustness
6. Performance & Scalability
7. Dependencies & Documentation

**Triage Matrix**:
- 🔴 **Blocker**: Must fix before merge
- 🟡 **Improvement**: Strong recommendation
- 🟢 **Nit**: Optional polish

---

### I'm Doing Security Review

**Read these**:

1. **[SECURITY_REVIEW_CHECKLIST.md](SECURITY_REVIEW_CHECKLIST.md)** - OWASP-based security methodology
2. **[/security-review command](../prompts/commands/security-review.md)** - Run security review

**Framework**:
- OWASP Top 10 vulnerabilities
- FALSE_POSITIVE filtering (17 hard exclusions + 12 precedents)
- Confidence scoring (only report ≥8/10)
- Opus model required for maximum accuracy

---

### I'm Doing Design Review

**Read these**:

1. **[DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md)** - 7-phase design review methodology
2. **[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)** - UI component library priority
3. **[/design-review command](../prompts/commands/design-review.md)** - Run design review

**Framework**:
- Phase 0: Preparation
- Phase 1: Interaction and User Flow
- Phase 2: Responsiveness (3 viewports: 1440px, 768px, 375px)
- Phase 3: Visual Polish
- Phase 4: Accessibility (WCAG 2.1 AA)
- Phase 5: Robustness Testing
- Phase 6: Code Health
- Phase 7: Content and Console

---

### I'm Fixing a Bug

**Quick steps**:

1. Read current story file: `docs/development/features/[feature]/epics/[epic-id]/stories/[story].md`
2. Check **Acceptance Criteria** - does the bug violate this?
3. Run `/dev` to fix (write test first!)
4. Run `/test` to verify
5. Run `/review` to check quality
6. Run `/commit` to save changes

---

### I'm Managing Development Progress

**Check status anytime**:

```bash
/status
```

**Output shows**:
- Current feature, epic, story
- YOLO mode configuration
- Test status and coverage
- Pending tasks
- Recently completed work

**Update progress**:

Each agent automatically updates:
- `docs/development/status.xml` - Feature tracking
- Story file - Task checkboxes and status
- Git commits - What work was completed

---

## Key Documentation Files

| Need | Document | Where |
| --- | --- | --- |
| **What to build** | PRD.md | docs/development/ |
| **How to build it** | TECHNICAL_SPEC.md | docs/development/ |
| **System design** | ARCHITECTURE.md | docs/development/ |
| **UI guidelines** | DESIGN_SYSTEM.md | docs/development/ |
| **Development workflow** | DEVELOPMENT_PLAN.md | docs/development/ |
| **TDD methodology** | DEVELOPMENT_PLAN.md | docs/development/ |
| **Feature details** | FEATURE_SPEC.md | docs/development/features/[feature]/ |
| **Feature tasks** | TASKS.md | docs/development/features/[feature]/ |
| **Current story** | [epic].[story].md | docs/development/features/[feature]/epics/[epic-id]/stories/ |
| **Review principles** | CODE_REVIEW_PRINCIPLES.md | docs/development/ |
| **Security review** | SECURITY_REVIEW_CHECKLIST.md | docs/development/ |
| **Design review** | DESIGN_PRINCIPLES.md | docs/development/ |
| **Doc templates** | doc-templates.md | docs/development/prompts/templates/ |
| **Command reference** | /[command].md | docs/development/prompts/commands/ |
| **Agent reference** | [agent].md | docs/development/prompts/reference/core-agents.md |

---

## Common Commands Quick Reference

| Command | Use Case | Model |
| --- | --- | --- |
| `/dev` | Continue development with TDD | Sonnet |
| `/dev-yolo` | Autonomous loop (story or epic level) | Sonnet |
| `/commit` | Smart commit with tests and linting | Sonnet |
| `/review` | 7-phase code review | Sonnet |
| `/security-review` | OWASP security scanning | Opus |
| `/design-review` | UI/UX design review with Playwright | Sonnet |
| `/test` | Run tests with coverage | Haiku |
| `/plan` | Plan feature with TDD breakdown | Sonnet |
| `/status` | Project status report | Haiku |
| `/docs` | Update documentation | Haiku |
| `/yolo` | Configure YOLO mode breakpoints | Haiku |
| `/create-feature` | Create new feature | Sonnet |
| `/correct-course` | Adjust feature direction | Sonnet |
| `/create-story` | Create next user story | Sonnet |

---

## YOLO Mode: Autonomous Development

**YOLO mode** controls when agents stop vs. proceed autonomously.

### Three Stopping Granularities

**A. STORY-LEVEL** (default):
- Stop at specific breakpoints within each story
- Balanced control, review each story

**B. EPIC-LEVEL** (maximum autonomy):
- Only stop when full epics complete
- Ideal for trusted workflows
- Agents complete ALL stories in epic automatically

**C. CUSTOM**:
- Select individual breakpoints manually
- Fine-grained control

### Configure YOLO Mode

```bash
# One-time setup
/yolo

# Choose:
# A - STORY-LEVEL
# B - EPIC-LEVEL
# C - CUSTOM
```

### Launch Autonomous Loop

```bash
# Start autonomous development
/dev-yolo

# Agents will:
# 1. Read current story
# 2. Write failing tests
# 3. Implement code
# 4. Refactor
# 5. Run tests
# 6. Check code quality
# 7. Stop or continue based on config
```

---

## Development Workflow Overview

### Setup Phase (One Time)

1. Run bootstrap prompt
2. Answer discovery questions
3. Agent creates all documentation and agents
4. Git commit complete setup

### Development Cycle (Repeatable)

1. `/create-feature` - Set up feature with epics
2. `/create-story` - Generate next user story
3. `/yolo` - Configure autonomous breakpoints
4. `/dev` (or `/dev-yolo`) - Implement with TDD
5. `/review` - Code review
6. Fix any issues found
7. `/review` (final) - Approve story
8. `/commit` - Smart commit

### Autonomous Loop (YOLO)

```
Read status.xml → Read story file → Check for Review Tasks →
Write failing tests → Implement code → Refactor →
Run tests → Spawn code-reviewer → Handle Review Tasks →
Update story status → Check YOLO breakpoint →
Stop or continue → Next story
```

---

## Key Concepts Explained

### Red-Green-Refactor (TDD)

```
🔴 RED     → Write failing test
🟢 GREEN   → Minimal code to pass
🔵 REFACTOR → Improve code quality
♻️ REPEAT   → Next test case
```

**Rules**:
1. Write tests BEFORE implementation (always)
2. Write the simplest test first
3. Watch tests fail before implementing
4. Write minimal code to pass
5. Refactor only when tests are GREEN

### Epic-Based Organization

Features are divided into **epics** (logical milestones) with multiple **stories**:

```
Feature: user-authentication
├── Epic 1: Foundation (1.1, 1.2, 1.3)
├── Epic 2: Core Features (2.1, 2.2)
└── Epic 3: Polish (3.1)
```

**Benefits**:
- Parallel development across epics
- Independent story validation
- Incremental feature delivery
- Clear progress tracking

### Living Specifications

Loom treats agents and documentation as **living specs**:
- Agents read status.xml, epic docs, story files
- Agents automatically maintain context
- Documentation drives implementation
- No specification drift

---

## Troubleshooting

### "I don't know what to do next"

1. Run `/status` to see current task
2. Read current story file: `docs/development/features/[feature]/epics/[epic-id]/stories/[story].md`
3. Check **Acceptance Criteria** and **Tasks** sections
4. Read **Technical Details** for implementation guidance

### "My story is stuck or blocked"

1. Check **Blockers** in status.xml
2. Read **Notes** in epic DESCRIPTION.md
3. Run `/correct-course` to adjust direction if needed
4. Ask coordinators to reassess approach

### "Tests are failing"

1. Run `/test` to see failures
2. Read error messages carefully
3. Use `/dev` to implement fix (tests already written, just need code)
4. Red → Green → Refactor cycle

### "Code review found issues"

1. Read review feedback carefully
2. Issues are categorized as Blocker, Improvement, Nit
3. Fix Blockers first
4. Run `/review` again when done

---

## Next Steps

**Choose your path**:

- **New Project**: Go to [README.md](README.md), then run bootstrap prompt
- **Existing Project**: Read [INDEX.md](INDEX.md), then run `/status`
- **New Feature**: Run `/create-feature [name]`
- **Continue Development**: Run `/dev` or `/dev-yolo`

---

## Additional Resources

- **[README.md](README.md)** - Project philosophy and overview
- **[INDEX.md](INDEX.md)** - Complete documentation index
- **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Technical architecture overview
- **[YOLO_MODE.md](YOLO_MODE.md)** - In-depth YOLO mode documentation
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Comprehensive project details

---

**Ready to get started?** Pick your workflow above and jump in!

_For updates to this file, use the `#` key during Claude Code sessions_
