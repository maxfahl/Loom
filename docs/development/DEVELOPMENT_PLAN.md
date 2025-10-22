# Development Plan

**Project**: Loom Meta-Framework
**Status**: Complete (Framework Built)
**Last Updated**: 2025-10-22
**Version**: 1.0

---

## Overview

Loom is an AI-native development framework that automates the setup and operation of autonomous AI agent teams for AI coding platforms like Claude Code. This document describes how Loom was constructed and serves as a reference for understanding its architecture and methodology.

---

## How Loom Was Built: 7-Phase Setup Process

The Loom framework itself was built using a systematic 7-phase approach that creates complete development environments for new projects. This is the same process you use to set up a NEW project with Loom.

### Phase 0: Mode Detection

**Purpose**: Determine project type and context

**Activities**:
- Detect if project is greenfield (new) or brownfield (existing)
- Identify project root directory and structure
- Check for existing git repository
- Analyze existing documentation and code

**Output**: Project mode classification (greenfield/brownfield)

### Phase 1: Discovery & Template Processing

**Purpose**: Gather project context and process templates

**Activities**:
- Answer discovery questions (project name, description, tech stack, TDD enforcement)
- Process Loom templates for the specific project type
- Analyze brownfield codebases if applicable
- Create PROJECT_OVERVIEW.md for brownfield projects

**Key Questions Asked**:
1. What's your project name and description?
2. What's your primary tech stack (frontend/backend/full-stack)?
3. Is TDD enforced strictly or recommended?
4. What's your project phase (new/existing)?
5. What's your target YOLO mode configuration?

**Output**:
- Comprehensive project context
- Template selections
- Brownfield analysis (if applicable)

### Phase 2: Documentation Creation (Parallel)

**Purpose**: Create 15+ documentation files that define the project

**Activities** (all parallel):
- Create INDEX.md (master navigation hub)
- Create README.md (quick start guide)
- Create PRD.md (product requirements)
- Create TECHNICAL_SPEC.md (implementation details)
- Create ARCHITECTURE.md (system design)
- Create DESIGN_SYSTEM.md (UI/UX guidelines)
- Create TASKS.md (development checklist)
- Create DEVELOPMENT_PLAN.md (methodology)
- Create PROJECT_SUMMARY.md (comprehensive overview)
- Create EXECUTIVE_SUMMARY.md (technical summary)
- Create START_HERE.md (navigation guide)
- Create YOLO_MODE.md (autonomous workflow)
- Create CODE_REVIEW_PRINCIPLES.md (review framework)
- Create SECURITY_REVIEW_CHECKLIST.md (OWASP methodology)
- Create DESIGN_PRINCIPLES.md (design review methodology)

**Critical**: All documents use templates from `prompts/templates/doc-templates.md`

**Output**: Complete documentation suite

### Phase 3: Agent Creation (Parallel)

**Purpose**: Create 13-15 specialized AI agents

**Agents Created**:
- **coordinator** - Orchestrates TDD workflow and YOLO mode
- **code-reviewer** - 7-phase code review methodology
- **test-writer** - TDD-focused test creation
- **bug-finder** - Edge case and issue detection
- **refactor-specialist** - Code quality improvements (only when tests green)
- **qa-tester** - Fast test execution and validation
- **git-helper** - Version control operations
- **senior-developer** - Architecture and code review expert
- **architecture-advisor** - System design guidance
- **performance-optimizer** - Bottleneck identification
- **documentation-writer** - Fast doc updates
- **agent-creator** - Build custom agents
- **skill-creator** - Create Claude Skills
- **security-reviewer** - OWASP security scanning (Opus model)
- **design-reviewer** - UI/UX review with Playwright and WCAG 2.1 AA

**Each Agent**:
- Markdown file in `.claude/agents/`
- Clear purpose and expertise
- Integration with slash commands
- Project-specific customizations

**Output**: Complete agent team

### Phase 4: Command Creation (Parallel)

**Purpose**: Create 14+ slash commands for project workflow

**Commands Created**:
- **/dev** - Continue development with TDD
- **/dev-yolo** - Autonomous YOLO loop
- **/commit** - Smart commit with tests
- **/review** - 7-phase code review
- **/security-review** - OWASP security scanning
- **/design-review** - UI/UX design review
- **/test** - Run tests with coverage
- **/plan** - Plan feature implementation
- **/status** - Project status report
- **/docs** - Update documentation
- **/yolo** - Configure autonomous mode
- **/create-feature** - Set up feature with epics
- **/correct-course** - Adjust feature direction
- **/create-story** - Generate next user story

**Each Command**:
- Markdown file in `.claude/commands/`
- Clear usage examples
- Integration with agents
- Workflow context

**Output**: Complete command set

### Phase 5: CLAUDE.md Creation

**Purpose**: Create comprehensive AI assistant instructions

**Contents**:
- Project overview and goals
- Tech stack and architecture
- Specialized agents reference
- Custom slash commands reference
- Coding standards and conventions
- YOLO mode configuration
- Development workflow
- Epic/story organization
- TDD requirements and enforcement
- Code review principles
- Security review methodology
- Component library priority order
- Do's and don'ts

**Output**: Complete CLAUDE.md file

### Phase 6: Features Setup

**Purpose**: Create feature tracking infrastructure

**Activities**:
- Create status.xml for feature tracking
- Set up initial feature folder structure
- Create feature-specific documentation templates
- Prepare for epic/story creation

**Output**: Ready-to-develop feature tracking system

### Phase 7: Verification and Commit

**Purpose**: Verify complete setup and commit to git

**Activities**:
- Verify all documentation files exist
- Verify all agents are properly formatted
- Verify all commands are properly formatted
- Verify CLAUDE.md is complete
- Verify directory structure is correct
- Create initial git commit with all setup
- Tag initial commit for reference

**Output**: Complete, verified Loom setup

---

## Development Methodology: Test-Driven Development (TDD)

Loom enforces **strict TDD** - treating specifications as "tests" and agent execution as "implementation":

### The Red-Green-Refactor Cycle

```
1. 🔴 RED: Write failing test first
   - In Loom context: Write failing tests for feature
   - Tests define exact expected behavior
   - Tests MUST fail before implementation

2. 🟢 GREEN: Write minimal code to pass
   - Agents implement just enough code
   - Goal: turn tests from red to green
   - Don't over-engineer or add extra features

3. 🔵 REFACTOR: Clean up the code
   - Only refactor when tests are GREEN
   - Improve quality, naming, structure
   - Tests must still pass after refactor

4. ♻️ REPEAT: Iterate for next feature
```

### TDD Rules (Mandatory)

1. **Write tests BEFORE implementation** - Always, no exceptions
2. **Write the simplest test first** - Start with happy path
3. **Watch tests fail** - Confirm red state before implementing
4. **Write minimal code** - Only enough to turn tests green
5. **Refactor only when green** - Never refactor on red
6. **One test at a time** - Focus on one test case
7. **Run tests frequently** - After every small change

### Test Coverage Requirements

- **Minimum**: 80% code coverage (MANDATORY)
- **Target**: 90% code coverage
- **Critical paths**: 100% coverage

### Testing Tools

- **Vitest**: Unit and integration tests
- **Playwright**: E2E browser testing
- **@testing-library/react**: React component testing

---

## Code Style & Conventions

### TypeScript

- **Strict mode**: `"strict": true` required
- **No `any`**: Use proper types or `unknown`
- **Interfaces over types**: Prefer `interface` for object shapes
- **Explicit return types**: Always specify function return types

### React

- **Functional components**: No class components
- **Hooks**: Use hooks for state management
- **Memoization**: Use `memo`, `useMemo`, `useCallback` where needed
- **TypeScript props**: Always type component props

### Naming Conventions

- **Components**: PascalCase (`EventCard.tsx`)
- **Files**: kebab-case (`event-broadcaster.ts`)
- **Functions**: camelCase (`processHook()`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- **Types/Interfaces**: PascalCase (`HookPayload`, `IEventBroadcaster`)

### File Structure

- **Services**: `src/services/[ServiceName].ts`
- **Components**: `src/components/[ComponentName]/[ComponentName].tsx`
- **API Routes**: `src/app/api/[route]/route.ts`
- **Types**: `src/types/[domain].ts`
- **Utils**: `src/lib/[utility].ts`

---

## CI/CD Pipeline Strategy

Loom enables autonomous CI/CD through the `/dev-yolo` command:

### Autonomous Workflow

1. **Development Phase** - `/dev-yolo` writes tests and implements code
2. **Review Phase** - Spawns code-reviewer for 7-phase review
3. **Test Phase** - Runs full test suite (80%+ coverage required)
4. **Security Phase** - Runs OWASP security review (if enabled)
5. **Design Phase** - Runs UI/UX review with Playwright (if applicable)
6. **Commit Phase** - Creates conventional commit
7. **Loop Control** - Checks YOLO breakpoints (story-level or epic-level)

### YOLO Mode Breakpoints

**Story-Level (Default)**:
1. After development, before code review
2. After code review, before tests
3. After tests, before user testing
4. After user testing, before commit
5. After commit, before push
6. Before any file changes
7. Before running tests
8. Before major refactoring

**Epic-Level**:
9. After completing epic, before starting next epic

### YOLO Configuration

- `"none"` - Full autonomous mode
- `"1,3,4,8"` - Balanced control (recommended)
- `"all"` - Maximum control
- `"epic"` - Epic-level autonomy (stop only at epic boundaries)

---

## Release Process

### Git Workflow

1. **Create Feature Branch**: `/create-feature [name]`
2. **Create Story**: `/create-story` (for current epic)
3. **Develop**: `/dev` or `/dev-yolo`
4. **Review**: `/review` (code review, creates Review Tasks if needed)
5. **Fix Issues**: `/dev` (if review found issues)
6. **Commit**: `/commit` (conventional format, tests passing)
7. **Push**: `git push origin [branch]`

### Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore
**Scopes**: hooks, api, database, websocket, ui, skills, tests, docs, etc.

### Testing Gate

- All tests MUST pass
- Coverage MUST be ≥80%
- Linting MUST pass
- Type checking MUST pass

---

## Epic/Story Organization

### Feature Structure

```
docs/development/
└── status.xml                      # Feature tracking (single file)
└── features/
    └── my-feature/
        ├── FEATURE_SPEC.md         # Feature overview
        ├── TECHNICAL_DESIGN.md     # Implementation design
        ├── TASKS.md                # Epic-level tasks
        ├── CHANGELOG.md            # Change history
        └── epics/
            ├── epic-1-foundation/
            │   ├── DESCRIPTION.md   # Epic overview
            │   ├── TASKS.md         # Epic tasks
            │   ├── NOTES.md         # Implementation notes
            │   └── stories/
            │       ├── 1.1.md       # Story: Epic 1, Story 1
            │       ├── 1.2.md       # Story: Epic 1, Story 2
            │       └── 1.3.md       # Story: Epic 1, Story 3
            ├── epic-2-core/
            │   ├── DESCRIPTION.md
            │   ├── TASKS.md
            │   ├── NOTES.md
            │   └── stories/
            │       ├── 2.1.md
            │       └── 2.2.md
            └── epic-3-polish/
                ├── DESCRIPTION.md
                ├── TASKS.md
                ├── NOTES.md
                └── stories/
                    └── 3.1.md
```

### Story Format

**Filename**: `[epic].[story].md` (e.g., `1.1.md`, `2.3.md`)

**Contents**:
- Story description and acceptance criteria
- Task checklist with TDD requirements
- Technical details and dependencies
- Test requirements and coverage targets

### Status Tracking

**status.xml** tracks:
- Current feature (only ONE active)
- Current epic
- Current story
- Completed tasks with commit hashes
- YOLO mode configuration
- Blockers and notes

---

## 7-Phase Code Review Framework

All code reviews follow a hierarchical 7-phase framework:

1. **Architectural Design & Integrity** (Critical)
2. **Functionality & Correctness** (Critical)
3. **Security** (Non-Negotiable)
4. **Maintainability & Readability** (High Priority)
5. **Testing Strategy & Robustness** (High Priority)
6. **Performance & Scalability** (Important)
7. **Dependencies & Documentation** (Important)

**Triage Matrix**:
- **Blocker**: Must fix before merge
- **Improvement**: Strong recommendation
- **Nit**: Minor polish (optional)

---

## Component Library Priority

For UI components, check in this EXACT order:

1. **Kibo UI** (dev tools, specialized components) - CHECK FIRST
2. **Blocks.so** (layouts, dashboard patterns) - CHECK SECOND
3. **ReUI** (animations, motion) - CHECK THIRD
4. **shadcn/ui** (base primitives) - CHECK FOURTH
5. **Custom** (last resort only) - ONLY IF NOTHING EXISTS

---

## Loom Architecture

### Core Components

**Agents** (`.claude/agents/`)
- Markdown-based definitions
- 13-15 specialized agents
- Integrated with slash commands

**Commands** (`.claude/commands/`)
- Markdown-based workflow triggers
- 14+ streamlined commands
- Context-aware execution

**Documentation** (`.docs/development/`)
- 15+ comprehensive files
- Single source of truth
- Template-based creation

**Status Tracking** (`docs/development/status.xml`)
- Feature state management
- YOLO configuration
- Task tracking

**Features** (`docs/development/features/`)
- Feature specifications
- Epic organization
- Story breakdowns

---

## Future Roadmap

### Completed (Current Phase)

- Framework design and validation
- 13-15 core agents
- 14+ slash commands
- Complete documentation
- TDD enforcement
- YOLO mode implementation
- 7-phase code review framework
- OWASP security review
- UI/UX design review with Playwright

### Planned Enhancements

**Phase 1: Port to Gemini CLI** (when feature parity achieved)
- Adapt agents for Gemini CLI syntax
- Update command structure
- Maintain TDD and YOLO workflows

**Phase 2: Port to Codex** (when feature parity achieved)
- Adapt agents for Codex syntax
- Update MCP integrations
- Maintain autonomous workflows

**Phase 3: Enhanced Skills**
- Create reusable Claude Skills for domain-specific agents
- Optimize skill execution and context
- Build skill marketplace

**Phase 4: Advanced Analytics**
- Track agent performance metrics
- Analyze YOLO mode effectiveness
- Generate development reports

**Phase 5: Template Expansion**
- More project type templates
- Domain-specific agent packs
- Industry-specific frameworks

---

## Key Metrics & Success Criteria

### Development Velocity

- **Average story completion**: 2-4 hours (with `/dev-yolo`)
- **Test coverage**: 80%+ (mandatory)
- **Code review time**: 1-2 hours

### Quality Metrics

- **Bug escape rate**: <5% (should catch issues in review)
- **Test coverage**: 80%+ minimum, 90%+ target
- **Security findings**: 0 high-severity issues

### Autonomy Metrics (YOLO Mode)

- **Story-level autonomy**: 70-80% (with review gates)
- **Epic-level autonomy**: 85-95% (with epic boundaries)
- **Human intervention**: Minimal (at configured breakpoints)

---

## Design Principles

### Philosophy: "Living Documentation"

Loom treats **documentation as executable specifications**:

- **Documentation defines behavior** - PRD, TECHNICAL_SPEC, ARCHITECTURE are "tests"
- **Agents implement specifications** - /dev command executes the specs
- **Documentation evolves with code** - Update docs when requirements change
- **Living status.xml** - Real-time feature tracking, not static plans

### Philosophy: "Agents as Specialists"

Each agent has:
- **Clear expertise** - Senior-level knowledge in their domain
- **Defined responsibilities** - Specific tasks they own
- **Integration points** - Where they hand off to other agents
- **Quality standards** - Enforced by design (TDD, code review, testing)

### Philosophy: "Autonomy with Control"

YOLO mode provides:
- **Flexible stopping points** - Story-level or epic-level control
- **Configurable breakpoints** - Customize what requires approval
- **Override capability** - Always able to intervene
- **Gradual adoption** - Start with maximum control, increase autonomy over time

---

## How to Extend Loom

### Create Custom Agents

1. Read `agent-creator` agent documentation
2. Define agent purpose and expertise
3. Create markdown file in `.claude/agents/`
4. Integrate with existing commands or create new slash command
5. Test with sample project

### Create Custom Commands

1. Read command structure in `.claude/commands/`
2. Define command purpose and workflow
3. Create markdown file in `.claude/commands/`
4. Integrate with coordinator or specialized agents
5. Document in CLAUDE.md

### Add Project Templates

1. Create template project structure
2. Document setup process
3. Create phase guides for template-specific setup
4. Add to project-setup-meta-prompt.md

---

## Troubleshooting Guide

### Common Issues

**Issue**: Agents not finding documentation
- **Solution**: Check INDEX.md exists and all referenced docs are present
- **Prevention**: Run Phase 2 verification

**Issue**: YOLO mode stopping unexpectedly
- **Solution**: Check YOLO configuration in status.xml
- **Prevention**: Use `/yolo` command to reconfigure breakpoints

**Issue**: Tests failing in /dev-yolo
- **Solution**: Check test-writer created valid tests before implementation
- **Prevention**: Review test file before continuing with /dev

**Issue**: Code review finding major issues
- **Solution**: Prioritize blockers, create Review Tasks for improvements
- **Prevention**: More thorough testing before /review

---

## Version History

- **1.0 (2025-10-22)**: Initial Loom framework release
  - 7-phase setup process
  - 13-15 core agents
  - 14+ slash commands
  - Complete TDD enforcement
  - YOLO mode with story/epic control
  - 7-phase code review framework
  - OWASP security review
  - UI/UX design review

---

## Related Documentation

- **TASKS.md** - Development task checklist
- **YOLO_MODE.md** - Autonomous workflow details
- **CODE_REVIEW_PRINCIPLES.md** - 7-phase review framework
- **SECURITY_REVIEW_CHECKLIST.md** - OWASP methodology
- **DESIGN_PRINCIPLES.md** - UI/UX review methodology
- **CLAUDE.md** - AI assistant instructions
- **project-setup-meta-prompt.md** - Bootstrap prompt for new projects

---

_Last updated: 2025-10-22_
_Loom Framework Version: 1.0_
