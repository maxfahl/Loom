# CLAUDE.md Template for User Projects

**Purpose**: This is the source template for `CLAUDE.md` files deployed to user projects via the `scripts/deploy-claude-md.sh` script.

**DO NOT modify user project CLAUDE.md files directly—update this template and re-run the deployment script.**

---

## Marker System

The deployment script uses markers to identify which sections to update:

- `<!-- LOOM_FRAMEWORK_START -->` / `<!-- LOOM_FRAMEWORK_END -->` = Framework sections (auto-updated)
- Everything outside markers = User customizations (preserved)

---

## Template Content

```markdown
# [PROJECT_NAME] - Claude Code Instructions

**Framework**: Loom AI-Native Development Framework
**Version**: 1.0
**Last Updated**: [YYYY-MM-DD]

---

<!-- LOOM_FRAMEWORK_START -->

## 🧵 What is Loom?

Loom is an **AI-native meta-framework** that provides:

- **44 specialized AI agents** (coordinator, full-stack-developer, test-automator, code-reviewer, etc.)
- **15 slash commands** (/dev, /review, /commit, /yolo, /create-story, etc.)
- **Epic/Story organization** for feature tracking
- **YOLO mode** for autonomous development with configurable breakpoints
- **status.xml** for real-time project state tracking

**Your role**: Execute development tasks using Loom's agents, commands, and documentation structure.

---

## 🏗️ Loom Framework Components

### 1. Specialized Agents (`.claude/agents/`) - 44 Total

**Purpose**: Domain experts that perform specific tasks autonomously.

**Loom Framework Agents (6)**:
| Agent | Use For |
|-------|---------|
| **coordinator** | Orchestrate parallel sub-agents, manage autonomous workflows |
| **agent-creator** | Create new specialized agents with proper structure |
| **skill-creator** | Create reusable Claude Skills packages |
| **codebase-analyzer** | Analyze brownfield codebases to generate PROJECT_OVERVIEW.md |
| **project-scaffolder** | Create feature directory structures and initialize tracking files |
| **structure-validator** | Validate and migrate project structures non-destructively |

**Quality & Review Agents (3)**:
| Agent | Use For |
|-------|---------|
| **code-reviewer** | 7-phase code review with pragmatic quality framework (Opus) |
| **design-reviewer** | UI/UX review with Playwright + WCAG 2.1 AA validation |
| **security-reviewer** | OWASP/NIST/ISO 27001 security auditing |

**Development Agents (7)**:
| Agent | Use For |
|-------|---------|
| **full-stack-developer** | End-to-end web application development |
| **frontend-developer** | Frontend development (React, Angular, Vue) |
| **backend-architect** | Server-side logic and API development |
| **mobile-developer** | iOS/Android native app development |
| **test-automator** | Automated testing frameworks and coverage |
| **qa-expert** | Quality assurance strategy and test planning |
| **debugger** | Bug analysis and root cause investigation |

**Technology Specialists (7)**:
| Agent | Use For |
|-------|---------|
| **nextjs-pro** | Next.js expert (App Router, Server Components) |
| **react-pro** | React specialist (hooks, context, performance) |
| **typescript-pro** | TypeScript expert (strict mode, type safety) |
| **python-pro** | Python development (FastAPI, Django) |
| **golang-pro** | Go development (Gin, Echo, concurrency) |
| **postgres-pro** | PostgreSQL optimization and schema design |
| **electron-pro** | Electron desktop app development |

**Architecture & Operations (6)**:
| Agent | Use For |
|-------|---------|
| **cloud-architect** | AWS/GCP/Azure infrastructure design |
| **devops-incident-responder** | Incident response and reliability engineering |
| **deployment-engineer** | CI/CD pipelines and deployment automation |
| **performance-engineer** | Performance optimization and scalability |
| **database-optimizer** | Database performance tuning and indexing |
| **graphql-architect** | GraphQL API design and optimization |

**Additional Specialists (15)**:
| Agent | Use For |
|-------|---------|
| **ai-engineer** | AI/ML integration and model deployment |
| **api-documenter** | API documentation (OpenAPI, Swagger) |
| **data-engineer** | Data pipelines and ETL workflows |
| **data-scientist** | Data analysis and ML model development |
| **documentation-expert** | Technical writing and user guides |
| **dx-optimizer** | Developer experience optimization |
| **incident-responder** | Production incident management |
| **legacy-modernizer** | Legacy code modernization and refactoring |
| **ml-engineer** | Machine learning engineering and MLOps |
| **product-manager** | Product requirements and roadmapping |
| **prompt-engineer** | LLM prompt optimization and engineering |
| **ui-designer** | UI design and component systems |
| **ux-designer** | UX research and interaction design |
| **agent-organizer** | Agent workflow coordination and task decomposition |

**Guardrail**: Each agent has a **single responsibility**. Don't use `code-reviewer` for implementation or `test-automator` for refactoring.

---

### 2. Slash Commands (`.claude/commands/`)

**Purpose**: Streamlined workflows for common operations.

| Command            | What It Does                          | Guardrail                                                              |
| ------------------ | ------------------------------------- | ---------------------------------------------------------------------- |
| `/dev`             | Continue development on current story | ONLY works on current story tasks; reads status.xml first              |
| `/commit`          | Smart commit with tests + linting     | ONLY commits if tests pass and coverage ≥80%                           |
| `/review`          | Comprehensive code review             | ONLY reviews uncommitted changes; creates Review Tasks if issues found |
| `/test`            | Run tests with coverage report        | Reports coverage; fails if <80%                                        |
| `/loom-status`     | Show project status report            | Read-only; shows git, tasks, tests                                     |
| `/plan`            | Plan feature/task with TDD breakdown  | Creates plan docs; doesn't implement                                   |
| `/create-feature`  | Create new feature with epics         | Scaffolds structure; doesn't implement code                            |
| `/create-story`    | Generate next user story              | Creates story file; doesn't implement                                  |
| `/correct-course`  | Adjust feature direction              | Reorganizes epics; doesn't delete work                                 |
| `/yolo`            | Configure YOLO mode breakpoints       | Interactive config; doesn't start development                          |
| `/docs`            | Update documentation                  | ONLY updates docs; doesn't change code                                 |
| `/one-off`         | Delegate ad-hoc task to coordinator   | For tasks outside story workflow                                       |
| `/fix`             | Create high-priority bug fix story    | Creates story; doesn't fix immediately                                 |
| `/security-review` | OWASP security scan                   | Analysis only; creates findings report                                 |
| `/design-review`   | UI/UX + accessibility review          | Analysis only; creates findings report                                 |

**Guardrail**: Commands are **single-purpose workflows**. They do EXACTLY what their name says—no more, no less.

---

### 3. Epic/Story Organization

**Structure**:
```

Feature → Epic 1, Epic 2, Epic 3
Epic 1 → Story 1.1, 1.2, 1.3
Epic 2 → Story 2.1, 2.2

```

**Rules**:
- **Features** = Major capabilities (2-6 months)
- **Epics** = Logical groupings (2-4 weeks)
- **Stories** = Implementable units (2-5 days)

**Guardrail**: Work on ONE story at a time. Never jump ahead without completing current story.

---

### 4. YOLO Mode (Autonomous Development)

**What it does**: Coordinator agent autonomously completes stories/epics based on configured breakpoints.

**Stopping Granularities**:
- **STORY-LEVEL**: Stop at breakpoints within each story (default)
- **EPIC-LEVEL**: Only stop when full epics complete (maximum autonomy)
- **CUSTOM**: Select individual breakpoints (1-9)

**Guardrail**: ALWAYS respect configured breakpoints. Don't proceed past a breakpoint without user approval.

---

## 📁 Loom Project Structure

**CRITICAL FILES TO READ**:
1. **`.claude/AGENTS.md`** - Complete agent directory (read before delegating work)
2. **`docs/development/INDEX.md`** - Navigation hub for all documentation

```

project/
├── .claude/ # Loom framework files
│ ├── AGENTS.md # 🚨 CRITICAL: Directory of all 44 agents
│ ├── agents/ # 44 AI agents (*.md files)
│ │ ├── coordinator.md # Master orchestrator
│ │ ├── full-stack-developer.md # Full-stack implementation
│ │ ├── code-reviewer.md # 7-phase review (Opus)
│ │ └── ... # 41+ more agents
│ ├── commands/ # 15 slash commands (_.md files)
│ │ ├── dev.md # /dev command
│ │ ├── review.md # /review command
│ │ └── ... # 13+ more commands
│ └── skills/ # 100+ reusable Claude Skills
│ ├── react-js-development/
│ ├── tdd-red-green-refactor/
│ └── ...
│
├── docs/
│ └── development/ # LOOM DOCUMENTATION ROOT
│ ├── INDEX.md # 🚨 READ THIS FIRST - Master navigation
│ ├── status.xml # 🚨 GLOBAL: Current feature/epic/story state
│ │
│ ├── PROJECT_SUMMARY.md # Project overview
│ ├── START_HERE.md # Onboarding guide
│ ├── YOLO_MODE.md # YOLO configuration guide
│ ├── CODE_REVIEW_PRINCIPLES.md # 7-phase review workflow
│ ├── SECURITY_REVIEW_CHECKLIST.md # OWASP guidelines
│ ├── DESIGN_PRINCIPLES.md # UI/UX guidelines
│ │
│ └── features/ # Feature-specific documentation
│ └── [feature-name]/ # One directory per feature
│ ├── PRD.md # Product requirements
│ ├── FEATURE_SPEC.md # Detailed specifications
│ ├── TECHNICAL_DESIGN.md # Technical blueprint
│ ├── ARCHITECTURE.md # System design
│ ├── DESIGN_SYSTEM.md # UI/UX guidelines
│ ├── DEVELOPMENT_PLAN.md # TDD workflow
│ │
│ └── epics/ # Epic breakdown
│ └── [epic-name]/ # One directory per epic
│ ├── DESCRIPTION.md # Epic overview
│ ├── TASKS.md # Epic tasks
│ ├── NOTES.md # Epic notes
│ │
│ └── stories/ # Story files
│ ├── story-1.1-setup-auth.md
│ ├── story-1.2-login-endpoint.md
│ └── ...
│
│── [...SOURCE_DIRECTORIES] # [Project source code, depending on project type]
│
├── CLAUDE.md # 👈 This file (AI instructions)
└── README.md # Project README

````

### 📍 File Location Quick Reference

| What You Need | Where To Look |
|---------------|---------------|
| **Current feature/epic/story** | `docs/development/status.xml` (parse `<current-story>`) |
| **Story tasks & acceptance criteria** | `docs/development/features/[feature]/epics/[epic]/stories/[story].md` |
| **All documentation paths** | `docs/development/INDEX.md` |
| **Feature requirements** | `docs/development/features/[feature]/PRD.md` |
| **Technical design** | `docs/development/features/[feature]/TECHNICAL_DESIGN.md` |
| **YOLO breakpoint config** | `docs/development/status.xml` (`<yolo-mode>` tag) |
| **Available agents** | `.claude/agents/*.md` |
| **Available commands** | `.claude/commands/*.md` |
| **Review Tasks** | Current story file (added after `/review` if issues found) |

**Guardrail**: NEVER guess file paths. Read `INDEX.md` or `status.xml` to find exact locations.

---

## 🎯 How to Work in This Project

### Pre-Task Checklist (ALWAYS)

Before starting ANY task, perform these steps in order:

1. **[ ] Read `docs/development/status.xml`**
   - Find current feature: `<current-feature>`
   - Find current epic: `<current-epic>`
   - Find current story: `<current-story>`
   - Find current task: `<current-task>`
   - Check YOLO mode: `<yolo-mode enabled="true/false">`

2. **[ ] Read current story file**
   - Path format: `docs/development/features/[feature]/epics/[epic]/stories/[story].md`
   - Review acceptance criteria
   - Review task list
   - Check for "Review Tasks" section (if exists, prioritize FIRST)

3. **[ ] Read `docs/development/INDEX.md`**
   - Find relevant documentation for this task
   - Understand where to look for additional context

4. **[ ] Determine task complexity**
   - Simple task → Use appropriate agent directly
   - Complex task → Spawn coordinator agent

5. **[ ] Check TDD requirements**
   - **TDD Level**: [TDD_LEVEL]
   - Write tests BEFORE implementation if required

---

### Task Execution Rules

**Rule 1: Single Responsibility**
- Agents and commands do ONLY what they're designed for
- Don't use `/review` to implement code
- Don't use `/dev` to configure YOLO mode
- Don't use `test-automator` for refactoring

**Rule 2: Respect Boundaries**
- Work on current story ONLY (unless using `/one-off`)
- Don't modify other stories' files
- Don't skip ahead to next epic without completing current

**Rule 3: Update Tracking**
- After completing a task: Update `status.xml`
- After completing story tasks: Check off tasks in story file (`[ ]` → `[x]`)
- After all story tasks done: Update story status to "Waiting For Review"

**Rule 4: YOLO Breakpoints**
- ALWAYS check YOLO mode configuration in `status.xml`
- STOP at enabled breakpoints
- Request user approval before proceeding past breakpoint

**Rule 5: Test-First (TDD Level: [TDD_LEVEL])**
- [IF STRICT] **MANDATORY**: Write failing tests (RED) → Implement (GREEN) → Refactor (BLUE)
- [IF RECOMMENDED] **RECOMMENDED**: Write tests before or alongside implementation
- [IF OPTIONAL] **OPTIONAL**: Add tests for critical functionality
- Never refactor when tests are RED
- Never commit with failing tests

---

### Coordinator Agent Pattern

**When to spawn coordinator**:
- Multi-component features (back-end + front-end)
- Parallel workflows (review existing + implement new)
- Complex tasks requiring orchestration
- YOLO mode autonomous loops

**How to spawn**:
1. Gather ALL context (status.xml, story file, requirements)
2. Spawn coordinator with comprehensive prompt
3. Coordinator spawns parallel sub-agents
4. Coordinator synthesizes results

**Guardrail**: Coordinator MUST receive ALL context. NO information loss during delegation.

---

### Common Workflows

**Workflow 1: Continue Development**
```bash
1. Read status.xml
2. Read current story file
3. Run: /dev
4. Complete tasks (TDD: RED → GREEN → REFACTOR)
5. Tests pass + coverage ≥80%
6. Run: /review
7. If issues → Fix Review Tasks → Repeat from step 6
8. If no issues → Run: /commit
````

**Workflow 2: Start Autonomous Development**

```bash
1. Configure breakpoints: /yolo
2. Launch: /dev (with YOLO mode configured)
3. Coordinator autonomously completes stories
4. Stops at configured breakpoints
5. Review work, then resume: /dev
```

**Workflow 3: Create New Story**

```bash
1. Run: /create-story
2. Story file created with acceptance criteria
3. status.xml updated with new story
4. Run: /dev to start implementation
```

**Workflow 4: Fix Bug Outside Story**

```bash
1. Run: /fix "Description of bug"
2. High-priority fix story created
3. status.xml updated
4. Run: /dev to implement fix
```

---

## 🚫 Critical Guardrails

### NEVER Do

- ❌ Skip reading `status.xml` before starting work
- ❌ Work on multiple stories simultaneously
- ❌ Implement code before writing tests (if TDD STRICT)
- ❌ Commit with failing tests
- ❌ Commit with coverage <80% (if enforced)
- ❌ Proceed past YOLO breakpoints without approval
- ❌ Use agents for purposes outside their responsibility
- ❌ Modify files outside current feature directory (unless `/one-off`)
- ❌ Guess file paths—read `INDEX.md` or `status.xml`
- ❌ Delete Review Tasks—fix them first

### ALWAYS Do

- ✅ Read `docs/development/INDEX.md` when starting new task
- ✅ Read `docs/development/status.xml` BEFORE every task
- ✅ Read current story file for task details
- ✅ Check for "Review Tasks" section (prioritize FIRST if exists)
- ✅ Update `status.xml` after completing tasks
- ✅ Check off completed tasks in story file (`[ ]` → `[x]`)
- ✅ Run tests after every change
- ✅ Respect YOLO mode breakpoint configuration
- ✅ Use coordinator for complex multi-phase tasks
- ✅ Write conventional commit messages
- ✅ Update story status when work complete

---

## 🎯 Quick Reference

| Need To...            | Command/Action                                                             |
| --------------------- | -------------------------------------------------------------------------- |
| Continue development  | `/dev`                                                                     |
| Start autonomous mode | `/dev` (with YOLO mode configured)                                        |
| Review changes        | `/review`                                                                  |
| Commit work           | `/commit`                                                                  |
| Run tests             | `/test`                                                                    |
| Check project status  | `/loom-status`                                                             |
| Create new story      | `/create-story`                                                            |
| Fix a bug             | `/fix "description"`                                                       |
| Plan a feature        | `/plan`                                                                    |
| Update docs           | `/docs`                                                                    |
| Configure YOLO        | `/yolo`                                                                    |
| Find documentation    | Read `docs/development/INDEX.md`                                           |
| Find current task     | Read `docs/development/status.xml`                                         |
| Find story details    | Read `docs/development/features/[feature]/epics/[epic]/stories/[story].md` |

---

## 📝 status.xml Structure

**Location**: `docs/development/status.xml`
**Purpose**: Single source of truth for project state

**Key Tags**:

```xml
<project>
  <features>
    <feature name="[name]" is-active-feature="true">
      <current-epic>[epic-name]</current-epic>
      <current-story>[story-name]</current-story>
      <current-task>[task-description]</current-task>
      <completed-tasks>...</completed-tasks>
      <whats-next>...</whats-next>
      <yolo-mode enabled="true" granularity="story-level">
        <breakpoints>1,3,4,8</breakpoints>
      </yolo-mode>
    </feature>
  </features>
</project>
```

**Parse this file FIRST to understand where you are in the project.**

---

## 💡 Remember

**Loom is a framework that organizes AI agents to build software autonomously.**

- You have 44 specialized agents at your disposal
- You have 15+ streamlined commands for common workflows
- You have a clear epic/story structure for tracking
- You have YOLO mode for autonomous development
- You have guardrails to keep work focused and safe

**Your job**: Execute tasks efficiently using these tools while respecting boundaries.

**When in doubt**:

1. Read `docs/development/INDEX.md`
2. Read `docs/development/status.xml`
3. Read current story file
4. Ask the user

---

<!-- LOOM_FRAMEWORK_END -->

## 📊 Project-Specific Details

### Tech Stack

[TECH_STACK]

### TDD Enforcement

**Level**: [TDD_LEVEL]

[IF STRICT]

- **MANDATORY**: Red-Green-Refactor cycle enforced
- Write failing tests FIRST (RED)
- Implement minimal code to pass (GREEN)
- Refactor only when tests GREEN (BLUE)
- Coverage requirement: ≥80%
- Tests MUST pass before committing

[IF RECOMMENDED]

- **RECOMMENDED**: Tests should be written before or alongside implementation
- Write tests for all new features
- Coverage target: ≥80%
- Tests should pass before committing

[IF OPTIONAL]

- **OPTIONAL**: Add tests for critical functionality
- Coverage measured but not strictly enforced

### Preview Command

[PREVIEW_COMMAND]

### Test Command

[TEST_COMMAND]

### Build Command

[BUILD_COMMAND]

---

_Last Updated: [YYYY-MM-DD]_
_Loom Framework Version: 1.0_

```

```
